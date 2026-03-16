import CardSkeleton from "@/components/skeletons/CardSkeleton";

export default function Loading() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-48 bg-gray-200 dark:bg-forest-800 rounded animate-pulse" />
      <CardSkeleton count={6} />
    </div>
  );
}
