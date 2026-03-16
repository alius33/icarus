export default function DetailSkeleton() {
  return (
    <div className="animate-pulse space-y-6">
      {/* Title */}
      <div className="h-7 w-2/3 bg-forest-200 dark:bg-forest-700 rounded" />
      {/* Meta line */}
      <div className="flex gap-3">
        <div className="h-4 w-24 bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-32 bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-20 bg-forest-100 dark:bg-forest-700/50 rounded" />
      </div>
      {/* Content blocks */}
      <div className="space-y-3">
        <div className="h-4 w-full bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-5/6 bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-4/6 bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-full bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-3/4 bg-forest-100 dark:bg-forest-700/50 rounded" />
      </div>
      {/* Section */}
      <div className="pt-4 space-y-3">
        <div className="h-5 w-40 bg-forest-200 dark:bg-forest-700 rounded" />
        <div className="h-4 w-full bg-forest-100 dark:bg-forest-700/50 rounded" />
        <div className="h-4 w-2/3 bg-forest-100 dark:bg-forest-700/50 rounded" />
      </div>
    </div>
  );
}
