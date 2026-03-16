export default function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="animate-pulse space-y-3">
      {/* Header */}
      <div className="flex gap-4 border-b border-forest-200 dark:border-forest-700 pb-3">
        <div className="h-4 w-24 bg-forest-200 dark:bg-forest-700 rounded" />
        <div className="h-4 w-32 bg-forest-200 dark:bg-forest-700 rounded" />
        <div className="h-4 w-20 bg-forest-200 dark:bg-forest-700 rounded" />
        <div className="h-4 w-16 bg-forest-200 dark:bg-forest-700 rounded" />
      </div>
      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 py-2">
          <div className="h-4 w-24 bg-forest-100 dark:bg-forest-800 rounded" />
          <div className="h-4 w-48 bg-forest-100 dark:bg-forest-800 rounded" />
          <div className="h-4 w-20 bg-forest-100 dark:bg-forest-800 rounded" />
          <div className="h-4 w-16 bg-forest-100 dark:bg-forest-800 rounded" />
        </div>
      ))}
    </div>
  );
}
