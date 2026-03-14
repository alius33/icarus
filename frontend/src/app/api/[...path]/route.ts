import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

const getBackendUrl = () =>
  process.env.INTERNAL_API_URL || "http://localhost:8000";

async function proxy(
  request: NextRequest,
  { params }: { params: { path: string[] } },
) {
  const targetPath = `/api/${params.path.join("/")}`;
  const url = new URL(targetPath, getBackendUrl());

  // Forward query params
  request.nextUrl.searchParams.forEach((value, key) => {
    url.searchParams.set(key, value);
  });

  // Forward relevant headers
  const headers = new Headers();
  for (const key of ["content-type", "authorization", "accept"]) {
    const value = request.headers.get(key);
    if (value) headers.set(key, value);
  }

  const init: RequestInit = { method: request.method, headers };

  // Forward body for non-GET/HEAD
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = Buffer.from(await request.arrayBuffer());
  }

  try {
    const res = await fetch(url.toString(), init);

    // Forward response headers (skip hop-by-hop)
    const responseHeaders = new Headers();
    const skip = new Set([
      "transfer-encoding",
      "connection",
      "keep-alive",
      "upgrade",
    ]);
    res.headers.forEach((value, key) => {
      if (!skip.has(key.toLowerCase())) {
        responseHeaders.set(key, value);
      }
    });

    return new Response(res.body, {
      status: res.status,
      statusText: res.statusText,
      headers: responseHeaders,
    });
  } catch {
    return NextResponse.json(
      { detail: "Backend service unavailable" },
      { status: 502 },
    );
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
