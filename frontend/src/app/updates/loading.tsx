import CardSkeleton from "@/components/skeletons/CardSkeleton";

export default function Loading() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-48 bg-forest-200 dark:bg-forest-700 rounded animate-pulse" />
      <div className="grid gap-4 md:grid-cols-2">
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
      </div>
    </div>
  );
}
