import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import BreadcrumbBar from "@/components/layout/BreadcrumbBar";
import MobileBottomNav from "@/components/layout/MobileBottomNav";
import { ThemeProvider } from "@/components/ThemeProvider";
import { SidebarProvider } from "@/lib/hooks/useSidebarState";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Icarus Dashboard",
  description: "Programme intelligence dashboard for the Icarus project",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#111827" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} font-[family-name:var(--font-geist-sans)] antialiased`}
      >
        <ThemeProvider>
          <SidebarProvider>
            <Sidebar />
            <div className="min-h-screen md:ml-64">
              <Header />
              <BreadcrumbBar />
              <main className="p-4 md:p-6 lg:p-8 pb-20 md:pb-8">
                {children}
              </main>
            </div>
            <MobileBottomNav />
          </SidebarProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
