import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import BreadcrumbBar from "@/components/layout/BreadcrumbBar";
import MobileBottomNav from "@/components/layout/MobileBottomNav";
import QuickUpdateFAB from "@/components/updates/QuickUpdateFAB";
import { SidebarProvider } from "@/lib/hooks/useSidebarState";
import { ToastProvider } from "@/lib/hooks/useToast";

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
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "Icarus",
  },
  icons: {
    apple: "/icon-192.png",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#F1F2ED",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} font-[family-name:var(--font-geist-sans)] antialiased`}
      >
        <ToastProvider>
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
            <QuickUpdateFAB />
          </SidebarProvider>
        </ToastProvider>
      </body>
    </html>
  );
}
