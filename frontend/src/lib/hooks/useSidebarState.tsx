"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { usePathname } from "next/navigation";
import { useMediaQuery } from "./useIsMobile";

interface SidebarContextValue {
  isOpen: boolean;
  toggle: () => void;
  close: () => void;
  open: () => void;
}

const SidebarContext = createContext<SidebarContextValue>({
  isOpen: false,
  toggle: () => {},
  close: () => {},
  open: () => {},
});

export function SidebarProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const isDesktop = useMediaQuery("(min-width: 768px)");
  const pathname = usePathname();

  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);
  const close = useCallback(() => setIsOpen(false), []);
  const open = useCallback(() => setIsOpen(true), []);

  // Close sidebar on route change (mobile only)
  useEffect(() => {
    if (!isDesktop) {
      setIsOpen(false);
    }
  }, [pathname, isDesktop]);

  // Close on Escape key (mobile only)
  useEffect(() => {
    if (isDesktop || !isOpen) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setIsOpen(false);
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [isDesktop, isOpen]);

  // Prevent body scroll when sidebar is open on mobile
  useEffect(() => {
    if (!isDesktop && isOpen) {
      document.body.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = "";
      };
    }
  }, [isDesktop, isOpen]);

  return (
    <SidebarContext.Provider value={{ isOpen, toggle, close, open }}>
      {children}
    </SidebarContext.Provider>
  );
}

export function useSidebarState() {
  return useContext(SidebarContext);
}
