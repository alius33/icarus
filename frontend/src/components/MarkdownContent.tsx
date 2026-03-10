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
      className={`prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-strong:text-gray-900 prose-li:text-gray-700 prose-table:text-sm prose-th:bg-gray-50 prose-th:px-3 prose-th:py-2 prose-th:text-left prose-th:font-semibold prose-th:text-gray-700 prose-td:px-3 prose-td:py-2 prose-td:text-gray-600 prose-tr:border-b prose-tr:border-gray-200 prose-blockquote:border-l-blue-500 prose-blockquote:text-gray-600 ${className || ""}`}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
