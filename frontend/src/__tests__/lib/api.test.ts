import { describe, it, expect, vi, beforeEach } from 'vitest';

// We test the API client by mocking global fetch.
// We must replace fetch before the api module loads and captures a reference.
// Using vi.stubGlobal at the top level ensures our mock replaces jsdom's fetch.
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

// Now import the api module — it will see our mocked fetch
import { api } from '@/lib/api';

describe('api module', () => {
  beforeEach(() => {
    mockFetch.mockReset();
    delete process.env.NEXT_PUBLIC_API_URL;
    delete process.env.INTERNAL_API_URL;
  });

  // -------------------------------------------------------------------------
  // Successful JSON response
  // -------------------------------------------------------------------------
  describe('fetchApi — successful response', () => {
    it('returns parsed JSON on successful fetch', async () => {
      const mockData = { items: [{ id: 1, name: 'Test' }], total: 1 };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockData),
      });

      const result = await api.getDashboard();
      expect(result).toEqual(mockData);
      expect(mockFetch).toHaveBeenCalledTimes(1);
    });

    it('calls fetch with no-store cache option for GET requests', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({}),
      });

      await api.getDashboard();

      expect(mockFetch).toHaveBeenCalledTimes(1);
      const [url, options] = mockFetch.mock.calls[0];
      expect(String(url)).toContain('/api/dashboard');
      expect(options).toEqual({ cache: 'no-store' });
    });
  });

  // -------------------------------------------------------------------------
  // Error response (non-ok status)
  // -------------------------------------------------------------------------
  describe('fetchApi — error response', () => {
    it('throws with detail from response body when available', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: () => Promise.resolve({ detail: 'Resource not found' }),
      });

      await expect(api.getDashboard()).rejects.toThrow('Resource not found');
    });

    it('falls back to status code when response body has no detail', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: () => Promise.reject(new Error('invalid json')),
      });

      await expect(api.getProjects()).rejects.toThrow('API error: 500');
    });

    it('throws for non-ok status (error propagates)', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 403,
        json: () => Promise.resolve({ detail: 'Forbidden' }),
      });

      await expect(api.getDashboard()).rejects.toThrow('Forbidden');
    });
  });

  // -------------------------------------------------------------------------
  // URL construction
  // -------------------------------------------------------------------------
  describe('URL construction', () => {
    it('uses localhost:8000 as default base on client side', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve([]),
      });

      await api.getProjects();

      const calledUrl = String(mockFetch.mock.calls[0][0]);
      expect(calledUrl).toContain('http://localhost:8000/api/projects');
    });

    it('appends query parameters correctly', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ items: [], total: 0, page: 1, pages: 1 }),
      });

      await api.getTranscripts(2, 10);

      const calledUrl = String(mockFetch.mock.calls[0][0]);
      expect(calledUrl).toContain('page=2');
      expect(calledUrl).toContain('limit=10');
    });
  });

  // -------------------------------------------------------------------------
  // mutateApi — POST/PATCH/DELETE operations
  // -------------------------------------------------------------------------
  describe('mutateApi — mutation operations', () => {
    it('sends POST with JSON body for create operations', async () => {
      const mockResponse = { id: 1, description: 'Test decision' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await api.createDecision({
        description: 'Test decision',
        rationale: 'Test rationale',
        made_by: 'Tester',
        date: '2026-03-10',
      });

      expect(result).toEqual(mockResponse);
      const [, options] = mockFetch.mock.calls[0];
      expect(options.method).toBe('POST');
      expect(options.headers).toEqual({ 'Content-Type': 'application/json' });
    });

    it('throws on failed mutation', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 422,
        json: () => Promise.resolve({ detail: 'Validation error' }),
      });

      await expect(
        api.createDecision({
          description: '',
          rationale: '',
          made_by: '',
          date: '',
        }),
      ).rejects.toThrow('API error: 422');
    });
  });
});
