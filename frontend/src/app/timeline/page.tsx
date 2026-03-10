import Link from "next/link";
import { FileText, Gavel, Flag } from "lucide-react";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";

const eventTypeConfig: Record<
  string,
  { color: string; dotColor: string; icon: React.ReactNode }
> = {
  transcript: {
    color: "bg-blue-100 text-blue-800 border-blue-200",
    dotColor: "bg-blue-500",
    icon: <FileText className="h-3.5 w-3.5" />,
  },
  decision: {
    color: "bg-purple-100 text-purple-800 border-purple-200",
    dotColor: "bg-purple-500",
    icon: <Gavel className="h-3.5 w-3.5" />,
  },
  milestone: {
    color: "bg-green-100 text-green-800 border-green-200",
    dotColor: "bg-green-500",
    icon: <Flag className="h-3.5 w-3.5" />,
  },
};

function getEventConfig(type: string) {
  return (
    eventTypeConfig[type] || {
      color: "bg-gray-100 text-gray-800 border-gray-200",
      dotColor: "bg-gray-500",
      icon: <FileText className="h-3.5 w-3.5" />,
    }
  );
}

export default async function TimelinePage() {
  const timeline = await api.getTimeline();

  const events = [...timeline.events].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Timeline</h2>
        <p className="mt-1 text-sm text-gray-500">
          {timeline.total} events from{" "}
          {formatDate(timeline.from_date)} to {formatDate(timeline.to_date)}
        </p>
      </div>

      {events.length > 0 ? (
        <div className="relative ml-4">
          {/* Vertical line */}
          <div className="absolute left-0 top-0 bottom-0 border-l-2 border-gray-300" />

          <div className="space-y-6">
            {events.map((event, i) => {
              const config = getEventConfig(event.type);
              const eventContent = (
                <div className="relative flex gap-4 pl-8">
                  {/* Dot */}
                  <div
                    className={`absolute left-[-5px] top-2 h-3 w-3 rounded-full border-2 border-white ${config.dotColor}`}
                  />

                  {/* Date */}
                  <div className="w-28 flex-shrink-0 pt-0.5 text-sm text-gray-500">
                    {formatDate(event.date)}
                  </div>

                  {/* Card */}
                  <div className="flex-1 rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
                    <div className="flex items-center gap-2">
                      <span
                        className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium ${config.color}`}
                      >
                        {config.icon}
                        {event.type}
                      </span>
                    </div>
                    <p className="mt-2 text-sm font-medium text-gray-900">
                      {event.title}
                    </p>
                    {event.description && (
                      <p className="mt-1 text-sm text-gray-600">
                        {event.description}
                      </p>
                    )}
                  </div>
                </div>
              );

              if (event.reference_url) {
                return (
                  <Link
                    key={i}
                    href={event.reference_url}
                    className="block transition-opacity hover:opacity-80"
                  >
                    {eventContent}
                  </Link>
                );
              }

              return <div key={i}>{eventContent}</div>;
            })}
          </div>
        </div>
      ) : (
        <div className="rounded-lg border border-gray-200 bg-white p-12 text-center shadow-sm">
          <p className="text-gray-500">No timeline events.</p>
        </div>
      )}
    </div>
  );
}
