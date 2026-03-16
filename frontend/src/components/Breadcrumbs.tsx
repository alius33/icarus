import Link from "next/link";
import { ChevronRight } from "lucide-react";

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

export default function Breadcrumbs({ items }: BreadcrumbsProps) {
  if (items.length === 0) return null;

  return (
    <nav aria-label="Breadcrumb" className="flex items-center text-base text-forest-400 dark:text-forest-300">
      {items.map((item, index) => {
        const isLast = index === items.length - 1;

        return (
          <span key={`${item.label}-${index}`} className="flex items-center">
            {index > 0 && (
              <ChevronRight className="mx-1.5 h-3.5 w-3.5 flex-shrink-0 text-forest-300 dark:text-forest-400" />
            )}
            {isLast || !item.href ? (
              <span
                className="font-medium text-forest-950 dark:text-forest-50"
                aria-current={isLast ? "page" : undefined}
              >
                {item.label}
              </span>
            ) : (
              <Link
                href={item.href}
                className="hover:text-forest-600 dark:hover:text-forest-200 transition-colors"
              >
                {item.label}
              </Link>
            )}
          </span>
        );
      })}
    </nav>
  );
}
