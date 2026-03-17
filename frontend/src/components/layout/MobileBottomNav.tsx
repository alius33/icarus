"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  CheckSquare,
  Menu,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useSidebarState } from "@/lib/hooks/useSidebarState";

const tabs = [
  { label: "Dashboard", href: "/", icon: LayoutDashboard },
  { label: "Tasks", href: "/tasks", icon: CheckSquare },
] as const;

export default function MobileBottomNav() {
  const pathname = usePathname();
  const { open } = useSidebarState();

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-40 flex items-stretch border-t border-forest-200 dark:border-forest-700 bg-white/90 dark:bg-forest-900/90 backdrop-blur-sm md:hidden"
      style={{ paddingBottom: "env(safe-area-inset-bottom, 0px)" }}
      role="navigation"
      aria-label="Mobile navigation"
    >
      {tabs.map(({ label, href, icon: Icon }) => {
        const isActive =
          href === "/"
            ? pathname === "/"
            : pathname.startsWith(href);

        return (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex flex-1 flex-col items-center justify-center gap-1 py-2 text-[11px] font-medium transition-colors min-h-[56px]",
              isActive
                ? "text-forest-500 dark:text-forest-300"
                : "text-forest-400 dark:text-forest-400"
            )}
          >
            <Icon className="h-5 w-5" />
            {label}
          </Link>
        );
      })}
      <button
        onClick={open}
        className="flex flex-1 flex-col items-center justify-center gap-1 py-2 text-[11px] font-medium text-forest-400 dark:text-forest-400 transition-colors min-h-[56px]"
      >
        <Menu className="h-5 w-5" />
        More
      </button>
    </nav>
  );
}
