import TableSkeleton from "@/components/skeletons/TableSkeleton";

export default function TranscriptsLoading() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-48 bg-gray-200 rounded animate-pulse" />
      <TableSkeleton rows={8} />
    </div>
  );
}
