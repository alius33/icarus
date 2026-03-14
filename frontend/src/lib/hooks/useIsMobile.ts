"use client";

import { useState, useEffect } from "react";

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(query);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

export function useIsMobile() {
  const isFoldCover = useMediaQuery("(max-width: 499px)");
  const isMobile = useMediaQuery("(max-width: 767px)");
  const isTablet = useMediaQuery("(max-width: 1023px)");
  return { isFoldCover, isMobile, isTablet };
}
