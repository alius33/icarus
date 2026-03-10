/**
 * Sanitizes an HTML string by stripping all tags except safe highlight tags.
 * Allows only: <mark>, <b>, <em>, <strong> (and their closing variants).
 * This prevents XSS when rendering search result snippets.
 */
export function sanitizeHtml(html: string): string {
  // Remove all HTML tags except allowed highlight-related tags
  return html.replace(/<(?!\/?(?:mark|b|em|strong)\b)[^>]*>/gi, "");
}
