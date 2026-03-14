"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  FileBarChart,
  CalendarDays,
  Network,
  Users,
  Clock,
  Gavel,
  KanbanSquare,
  AlertCircle,
  BookOpen,
  Search,
  Upload,
  FolderKanban,
  ShieldAlert,
  Link2,
  UserCog,
  Target,
  Handshake,
  Trophy,
  Globe,
  User,
  AudioLines,
  TrendingUp,
  GitBranch,
  AlertTriangle,
  BarChart3,
} from "lucide-react";
import { cn } from "@/lib/utils";
import ThemeToggle from "@/components/ThemeToggle";

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
        label: "Timeline",
        href: "/timeline",
        icon: <Clock className="h-4 w-4" />,
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
    title: "Programme",
    items: [
      {
        label: "Project Hub",
        href: "/projects",
        icon: <FolderKanban className="h-4 w-4" />,
      },
      {
        label: "Workstreams",
        href: "/workstreams",
        icon: <Network className="h-4 w-4" />,
      },
      {
        label: "Stakeholders",
        href: "/stakeholders",
        icon: <Users className="h-4 w-4" />,
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
    ],
  },
  {
    title: "Intelligence",
    items: [
      {
        label: "Risk Register",
        href: "/risks",
        icon: <ShieldAlert className="h-4 w-4" />,
      },
      {
        label: "Dependencies",
        href: "/dependencies",
        icon: <Link2 className="h-4 w-4" />,
      },
      {
        label: "Resources",
        href: "/resources",
        icon: <UserCog className="h-4 w-4" />,
      },
      {
        label: "Scope",
        href: "/scope",
        icon: <Target className="h-4 w-4" />,
      },
      {
        label: "Topic Evolution",
        href: "/topic-evolution",
        icon: <TrendingUp className="h-4 w-4" />,
      },
      {
        label: "Influence Map",
        href: "/influence-graph",
        icon: <GitBranch className="h-4 w-4" />,
      },
      {
        label: "Contradictions",
        href: "/contradictions",
        icon: <AlertTriangle className="h-4 w-4" />,
      },
      {
        label: "Meeting Scores",
        href: "/meeting-scores",
        icon: <BarChart3 className="h-4 w-4" />,
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
        "flex items-center gap-3 rounded-md px-3 py-2 text-base font-medium transition-colors",
        indent && "ml-4",
        isActive
          ? "bg-blue-600 text-white"
          : "text-gray-300 hover:bg-gray-800 hover:text-white",
      )}
    >
      {item.icon}
      {item.label}
    </Link>
  );
}

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-50 flex w-64 flex-col bg-gray-900 dark:bg-gray-950" role="navigation" aria-label="Main navigation">
      {/* Logo / Title */}
      <div className="flex h-16 items-center border-b border-gray-800 px-6">
        <span className="text-lg font-bold tracking-widest text-white">
          ICARUS
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {navSections.map((section) => (
          <div key={section.title} className="mb-4">
            <p className="mb-1 px-3 text-sm font-semibold uppercase tracking-wider text-gray-500">
              {section.title}
            </p>
            {section.items.map((item) => (
              <div key={item.href}>
                {item.children ? (
                  <>
                    <div className="flex items-center gap-3 px-3 py-2 text-base font-medium text-gray-400">
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
      <div className="border-t border-gray-800 px-6 py-4 flex items-center justify-between">
        <p className="text-sm text-gray-500">Icarus v1.0</p>
        <ThemeToggle />
      </div>
    </aside>
  );
}
