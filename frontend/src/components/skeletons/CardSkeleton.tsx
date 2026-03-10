export default function CardSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 animate-pulse">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5 space-y-3">
          <div className="h-5 w-3/4 bg-gray-200 dark:bg-gray-700 rounded" />
          <div className="h-3 w-full bg-gray-100 dark:bg-gray-700/50 rounded" />
          <div className="h-3 w-2/3 bg-gray-100 dark:bg-gray-700/50 rounded" />
          <div className="flex gap-2 pt-2">
            <div className="h-6 w-16 bg-gray-100 dark:bg-gray-700/50 rounded-full" />
            <div className="h-6 w-12 bg-gray-100 dark:bg-gray-700/50 rounded-full" />
          </div>
        </div>
      ))}
    </div>
  );
}
