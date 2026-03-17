"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  FileBarChart,
  CalendarDays,
  Users,

  Gavel,
  KanbanSquare,
  AlertCircle,
  BookOpen,
  Search,
  Upload,
  Handshake,
  Trophy,
  Globe,
  User,
  AudioLines,
  Rocket,
  MessageSquarePlus,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useSidebarState } from "@/lib/hooks/useSidebarState";

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  children?: NavItem[];
}

interface NavSection {
  title: string;
  items: NavItem[];
}

const navSections: NavSection[] = [
  {
    title: "Overview",
    items: [
      {
        label: "Dashboard",
        href: "/",
        icon: <LayoutDashboard className="h-4 w-4" />,
      },
      {
        label: "Weekly Plan",
        href: "/weekly-plan",
        icon: <Rocket className="h-4 w-4" />,
      },
      {
        label: "Weekly Reports",
        href: "/analysis/weekly",
        icon: <CalendarDays className="h-4 w-4" />,
      },
      {
        label: "Updates",
        href: "/updates",
        icon: <MessageSquarePlus className="h-4 w-4" />,
      },
    ],
  },
  {
    title: "Content",
    items: [
      {
        label: "Transcripts",
        href: "/transcripts",
        icon: <FileText className="h-4 w-4" />,
      },
      {
        label: "Upload",
        href: "/upload",
        icon: <Upload className="h-4 w-4" />,
      },
      {
        label: "Speaker Review",
        href: "/speaker-review",
        icon: <AudioLines className="h-4 w-4" />,
      },
      {
        label: "Analysis",
        href: "/analysis",
        icon: <FileBarChart className="h-4 w-4" />,
        children: [
          {
            label: "Summaries",
            href: "/analysis/summaries",
            icon: <FileBarChart className="h-4 w-4" />,
          },
          {
            label: "Weekly Reports",
            href: "/analysis/weekly",
            icon: <CalendarDays className="h-4 w-4" />,
          },
        ],
      },
    ],
  },
  {
    title: "Tracking",
    items: [
      {
        label: "Decisions",
        href: "/decisions",
        icon: <Gavel className="h-4 w-4" />,
      },
      {
        label: "Tasks",
        href: "/tasks",
        icon: <KanbanSquare className="h-4 w-4" />,
      },
      {
        label: "Open Threads",
        href: "/open-threads",
        icon: <AlertCircle className="h-4 w-4" />,
      },
      {
        label: "Commitments",
        href: "/commitments",
        icon: <Handshake className="h-4 w-4" />,
      },
      {
        label: "My Items",
        href: "/my-items",
        icon: <User className="h-4 w-4" />,
      },
      {
        label: "Stakeholders",
        href: "/stakeholders",
        icon: <Users className="h-4 w-4" />,
      },
    ],
  },
  {
    title: "Strategy",
    items: [
      {
        label: "Programme Wins",
        href: "/wins",
        icon: <Trophy className="h-4 w-4" />,
      },
      {
        label: "Outreach Tracker",
        href: "/outreach",
        icon: <Globe className="h-4 w-4" />,
      },
    ],
  },
  {
    title: "Reference",
    items: [
      {
        label: "Glossary",
        href: "/glossary",
        icon: <BookOpen className="h-4 w-4" />,
      },
    ],
  },
  {
    title: "Search",
    items: [
      {
        label: "Search",
        href: "/search",
        icon: <Search className="h-4 w-4" />,
      },
    ],
  },
];

function NavLink({
  item,
  pathname,
  indent = false,
}: {
  item: NavItem;
  pathname: string;
  indent?: boolean;
}) {
  const isActive =
    pathname === item.href ||
    (item.href !== "/" && pathname.startsWith(item.href));

  return (
    <Link
      href={item.href}
      aria-current={isActive ? "page" : undefined}
      className={cn(
        "flex items-center gap-3 rounded-md px-3 py-3 md:py-2 text-base font-medium transition-colors",
        indent && "ml-4",
        isActive
          ? "bg-forest-500 text-white"
          : "text-forest-100 hover:bg-forest-700 hover:text-white",
      )}
    >
      {item.icon}
      {item.label}
    </Link>
  );
}

export default function Sidebar() {
  const pathname = usePathname();
  const { isOpen, close } = useSidebarState();

  return (
    <>
      {/* Backdrop overlay — mobile only */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 transition-opacity duration-200 md:hidden"
          onClick={close}
          aria-hidden="true"
        />
      )}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-64 flex-col bg-gradient-to-b from-forest-900 to-forest-950",
          "transition-transform duration-200 ease-in-out",
          "md:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        )}
        role="navigation"
        aria-label="Main navigation"
        aria-hidden={!isOpen ? true : undefined}
      >
        {/* Logo / Title */}
        <div className="flex h-16 items-center border-b border-forest-700 px-6">
          <span className="text-lg font-bold tracking-widest text-white">
            ICARUS
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
          {navSections.map((section) => (
            <div key={section.title} className="mb-4">
              <p className="mb-1 px-3 text-sm font-semibold uppercase tracking-wider text-forest-300">
                {section.title}
              </p>
              {section.items.map((item) => (
                <div key={item.href}>
                  {item.children ? (
                    <>
                      <div className="flex items-center gap-3 px-3 py-3 md:py-2 text-base font-medium text-forest-300">
                        {item.icon}
                        {item.label}
                      </div>
                      {item.children.map((child) => (
                        <NavLink
                          key={child.href}
                          item={child}
                          pathname={pathname}
                          indent
                        />
                      ))}
                    </>
                  ) : (
                    <NavLink item={item} pathname={pathname} />
                  )}
                </div>
              ))}
            </div>
          ))}
        </nav>

        {/* Footer */}
        <div className="border-t border-forest-700 px-6 py-4">
          <p className="text-sm text-forest-300">Icarus v1.0</p>
        </div>
      </aside>
    </>
  );
}
