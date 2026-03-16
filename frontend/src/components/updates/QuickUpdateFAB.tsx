"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import QuickUpdateModal from "./QuickUpdateModal";

export default function QuickUpdateFAB() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        aria-label="Add project update"
        className="fixed bottom-20 right-4 md:bottom-6 md:right-6 z-40 flex items-center justify-center w-14 h-14 rounded-full bg-forest-600 hover:bg-forest-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 active:scale-95"
      >
        <Plus className="h-6 w-6" />
      </button>
      <QuickUpdateModal open={open} onClose={() => setOpen(false)} />
    </>
  );
}
