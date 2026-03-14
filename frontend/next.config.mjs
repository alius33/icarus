import withPWAInit from "next-pwa";

const withPWA = withPWAInit({
  dest: "public",
  disable: process.env.NODE_ENV === "development",
  fallbacks: {
    document: "/offline.html",
  },
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
};

export default withPWA(nextConfig);
