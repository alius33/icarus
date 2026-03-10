import { describe, it, expect } from 'vitest';
import {
  cn,
  formatDate,
  statusColor,
  getStatusColor,
  ragDotColor,
  severityColor,
  capacityColor,
  trendArrow,
  healthRagColor,
  healthRagTextColor,
  tierLabels,
} from '@/lib/utils';

// ---------------------------------------------------------------------------
// cn — class name merging via clsx
// ---------------------------------------------------------------------------
describe('cn', () => {
  it('merges multiple class strings', () => {
    expect(cn('foo', 'bar')).toBe('foo bar');
  });

  it('handles conditional classes', () => {
    expect(cn('base', false && 'hidden', 'visible')).toBe('base visible');
  });

  it('returns empty string for no inputs', () => {
    expect(cn()).toBe('');
  });

  it('handles undefined and null inputs', () => {
    expect(cn('a', undefined, null, 'b')).toBe('a b');
  });

  it('handles arrays of class names', () => {
    expect(cn(['foo', 'bar'])).toBe('foo bar');
  });
});

// ---------------------------------------------------------------------------
// formatDate — locale date formatting
// ---------------------------------------------------------------------------
describe('formatDate', () => {
  it('formats an ISO date string to en-GB short format', () => {
    const result = formatDate('2026-03-10');
    // en-GB with day:numeric, month:short, year:numeric → "10 Mar 2026"
    expect(result).toBe('10 Mar 2026');
  });

  it('formats a datetime string (ignores time part)', () => {
    const result = formatDate('2026-01-15T14:30:00Z');
    expect(result).toBe('15 Jan 2026');
  });

  it('formats another date correctly', () => {
    const result = formatDate('2025-12-25');
    expect(result).toBe('25 Dec 2025');
  });
});

// ---------------------------------------------------------------------------
// statusColor — static map
// ---------------------------------------------------------------------------
describe('statusColor', () => {
  it('has a mapping for LIVE', () => {
    expect(statusColor['LIVE']).toBe('bg-green-100 text-green-800 border-green-200');
  });

  it('has a mapping for STALLED', () => {
    expect(statusColor['STALLED']).toBe('bg-red-100 text-red-800 border-red-200');
  });

  it('has a mapping for planning', () => {
    expect(statusColor['planning']).toBe('bg-blue-100 text-blue-800 border-blue-200');
  });

  it('returns undefined for unknown keys', () => {
    expect(statusColor['NONEXISTENT']).toBeUndefined();
  });
});

// ---------------------------------------------------------------------------
// getStatusColor — with fallback
// ---------------------------------------------------------------------------
describe('getStatusColor', () => {
  it('returns the correct color for a known status', () => {
    expect(getStatusColor('ACTIVE')).toBe('bg-green-100 text-green-800 border-green-200');
  });

  it('returns fallback for an unknown status', () => {
    expect(getStatusColor('UNKNOWN_STATUS')).toBe('bg-gray-100 text-gray-600 border-gray-200');
  });

  it('returns the correct color for OPEN', () => {
    expect(getStatusColor('OPEN')).toBe('bg-red-100 text-red-800 border-red-200');
  });
});

// ---------------------------------------------------------------------------
// ragDotColor — RAG dot colour for project / workstream status
// ---------------------------------------------------------------------------
describe('ragDotColor', () => {
  it('returns green for LIVE', () => {
    expect(ragDotColor('LIVE')).toBe('bg-green-500');
  });

  it('returns green for ACTIVE', () => {
    expect(ragDotColor('ACTIVE')).toBe('bg-green-500');
  });

  it('returns green for COMPLETED', () => {
    expect(ragDotColor('COMPLETED')).toBe('bg-green-500');
  });

  it('returns green for statuses containing ACTIVE (case insensitive)', () => {
    expect(ragDotColor('ACTIVE — Demo targeting March 21')).toBe('bg-green-500');
  });

  it('returns amber for EARLY STAGE', () => {
    expect(ragDotColor('EARLY STAGE')).toBe('bg-amber-500');
  });

  it('returns amber for WATCHING', () => {
    expect(ragDotColor('WATCHING')).toBe('bg-amber-500');
  });

  it('returns amber for planning (case insensitive)', () => {
    expect(ragDotColor('planning')).toBe('bg-amber-500');
  });

  it('returns red for STALLED', () => {
    expect(ragDotColor('STALLED')).toBe('bg-red-500');
  });

  it('returns red for MINIMAL PROGRESS', () => {
    expect(ragDotColor('MINIMAL PROGRESS')).toBe('bg-red-500');
  });

  it('returns gray for unknown status', () => {
    expect(ragDotColor('SOMETHING ELSE')).toBe('bg-gray-400');
  });
});

// ---------------------------------------------------------------------------
// severityColor — severity level mapping
// ---------------------------------------------------------------------------
describe('severityColor', () => {
  it('returns red for CRITICAL', () => {
    expect(severityColor('CRITICAL')).toBe('bg-red-100 text-red-800 border-red-200');
  });

  it('returns orange for HIGH', () => {
    expect(severityColor('HIGH')).toBe('bg-orange-100 text-orange-800 border-orange-200');
  });

  it('returns yellow for MEDIUM', () => {
    expect(severityColor('MEDIUM')).toBe('bg-yellow-100 text-yellow-800 border-yellow-200');
  });

  it('returns green for LOW', () => {
    expect(severityColor('LOW')).toBe('bg-green-100 text-green-800 border-green-200');
  });

  it('is case insensitive', () => {
    expect(severityColor('critical')).toBe('bg-red-100 text-red-800 border-red-200');
    expect(severityColor('high')).toBe('bg-orange-100 text-orange-800 border-orange-200');
  });

  it('returns gray fallback for unknown severity', () => {
    expect(severityColor('UNKNOWN')).toBe('bg-gray-100 text-gray-600 border-gray-200');
  });
});

// ---------------------------------------------------------------------------
// capacityColor — capacity status mapping
// ---------------------------------------------------------------------------
describe('capacityColor', () => {
  it('returns green for available', () => {
    expect(capacityColor('available')).toBe('text-green-600');
  });

  it('returns amber for stretched', () => {
    expect(capacityColor('stretched')).toBe('text-amber-600');
  });

  it('returns red for overloaded', () => {
    expect(capacityColor('overloaded')).toBe('text-red-600');
  });

  it('is case insensitive', () => {
    expect(capacityColor('AVAILABLE')).toBe('text-green-600');
    expect(capacityColor('Stretched')).toBe('text-amber-600');
    expect(capacityColor('OVERLOADED')).toBe('text-red-600');
  });

  it('returns gray fallback for unknown capacity', () => {
    expect(capacityColor('unknown')).toBe('text-gray-500');
  });
});

// ---------------------------------------------------------------------------
// trendArrow — trend direction indicators
// ---------------------------------------------------------------------------
describe('trendArrow', () => {
  it('returns up arrow when current > previous', () => {
    const result = trendArrow(10, 5);
    expect(result.icon).toBe('↑');
    expect(result.color).toBe('text-green-600');
    expect(result.label).toBe('up');
  });

  it('returns down arrow when current < previous', () => {
    const result = trendArrow(3, 8);
    expect(result.icon).toBe('↓');
    expect(result.color).toBe('text-red-600');
    expect(result.label).toBe('down');
  });

  it('returns flat arrow when current === previous', () => {
    const result = trendArrow(5, 5);
    expect(result.icon).toBe('→');
    expect(result.color).toBe('text-gray-400');
    expect(result.label).toBe('flat');
  });
});

// ---------------------------------------------------------------------------
// healthRagColor — health score to RAG dot color
// ---------------------------------------------------------------------------
describe('healthRagColor', () => {
  it('returns green for "green"', () => {
    expect(healthRagColor('green')).toBe('bg-green-500');
  });

  it('returns amber for "amber"', () => {
    expect(healthRagColor('amber')).toBe('bg-amber-500');
  });

  it('returns red for "red"', () => {
    expect(healthRagColor('red')).toBe('bg-red-500');
  });

  it('returns gray fallback for unknown rag', () => {
    expect(healthRagColor('unknown')).toBe('bg-gray-400');
  });
});

// ---------------------------------------------------------------------------
// healthRagTextColor — health score to text color
// ---------------------------------------------------------------------------
describe('healthRagTextColor', () => {
  it('returns green text for "green"', () => {
    expect(healthRagTextColor('green')).toBe('text-green-700');
  });

  it('returns amber text for "amber"', () => {
    expect(healthRagTextColor('amber')).toBe('text-amber-700');
  });

  it('returns red text for "red"', () => {
    expect(healthRagTextColor('red')).toBe('text-red-700');
  });

  it('returns gray fallback for unknown rag', () => {
    expect(healthRagTextColor('unknown')).toBe('text-gray-500');
  });
});

// ---------------------------------------------------------------------------
// tierLabels — static record
// ---------------------------------------------------------------------------
describe('tierLabels', () => {
  it('maps tier 1 correctly', () => {
    expect(tierLabels[1]).toBe('Decision Makers & Sponsors');
  });

  it('maps tier 2 correctly', () => {
    expect(tierLabels[2]).toBe('Influential Gatekeepers');
  });

  it('maps tier 3 correctly', () => {
    expect(tierLabels[3]).toBe('Technical & Delivery');
  });

  it('maps tier 4 correctly', () => {
    expect(tierLabels[4]).toBe('Adjacent / Emerging');
  });

  it('returns undefined for unknown tier', () => {
    expect(tierLabels[99]).toBeUndefined();
  });
});
