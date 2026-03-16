import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownContentProps {
  children: string;
  className?: string;
}

export default function MarkdownContent({
  children,
  className,
}: MarkdownContentProps) {
  return (
    <div
      className={`prose prose-sm max-w-none prose-headings:text-forest-950 dark:prose-headings:text-forest-50 prose-p:text-forest-600 dark:prose-p:text-forest-200 prose-strong:text-forest-950 dark:prose-strong:text-forest-50 prose-li:text-forest-600 dark:prose-li:text-forest-200 prose-table:text-base prose-th:bg-forest-50 dark:prose-th:bg-forest-700 prose-th:px-3 prose-th:py-2 prose-th:text-left prose-th:font-semibold prose-th:text-forest-600 dark:prose-th:text-forest-200 prose-td:px-3 prose-td:py-2 prose-td:text-forest-500 dark:prose-td:text-forest-200 prose-tr:border-b prose-tr:border-forest-200 dark:prose-tr:border-forest-700 prose-blockquote:border-l-forest-500 prose-blockquote:text-forest-500 dark:prose-blockquote:text-forest-300 ${className || ""}`}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
