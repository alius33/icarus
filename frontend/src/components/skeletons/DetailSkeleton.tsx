export default function DetailSkeleton() {
  return (
    <div className="animate-pulse space-y-6">
      {/* Title */}
      <div className="h-7 w-2/3 bg-gray-200 rounded" />
      {/* Meta line */}
      <div className="flex gap-3">
        <div className="h-4 w-24 bg-gray-100 rounded" />
        <div className="h-4 w-32 bg-gray-100 rounded" />
        <div className="h-4 w-20 bg-gray-100 rounded" />
      </div>
      {/* Content blocks */}
      <div className="space-y-3">
        <div className="h-4 w-full bg-gray-100 rounded" />
        <div className="h-4 w-5/6 bg-gray-100 rounded" />
        <div className="h-4 w-4/6 bg-gray-100 rounded" />
        <div className="h-4 w-full bg-gray-100 rounded" />
        <div className="h-4 w-3/4 bg-gray-100 rounded" />
      </div>
      {/* Section */}
      <div className="pt-4 space-y-3">
        <div className="h-5 w-40 bg-gray-200 rounded" />
        <div className="h-4 w-full bg-gray-100 rounded" />
        <div className="h-4 w-2/3 bg-gray-100 rounded" />
      </div>
    </div>
  );
}
