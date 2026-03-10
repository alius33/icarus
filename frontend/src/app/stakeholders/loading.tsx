import TableSkeleton from "@/components/skeletons/TableSkeleton";

export default function StakeholdersLoading() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-48 bg-gray-200 rounded animate-pulse" />
      <TableSkeleton rows={10} />
    </div>
  );
}
