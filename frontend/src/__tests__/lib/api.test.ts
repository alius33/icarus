import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// We test the API client by mocking global fetch.
// The `api` module uses `getApiBase()` which checks `typeof window` and env vars.
// In jsdom, `window` is defined, so it uses NEXT_PUBLIC_API_URL or defaults to localhost:8000.

describe('api module', () => {
  beforeEach(() => {
    vi.resetModules();
    delete process.env.NEXT_PUBLIC_API_URL;
    delete process.env.INTERNAL_API_URL;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // Helper to mock fetch via vi.spyOn and reimport the module
  async function setupWithMockedFetch(mockImpl: (...args: unknown[]) => unknown) {
    // Use spyOn to override the existing global fetch (including jsdom's)
    vi.spyOn(globalThis, 'fetch').mockImplementation(mockImpl as typeof fetch);
    const mod = await import('@/lib/api');
    return mod.api;
  }

  // -------------------------------------------------------------------------
  // Successful JSON response
  // -------------------------------------------------------------------------
  describe('fetchApi — successful response', () => {
    it('returns parsed JSON on successful fetch', async () => {
      const mockData = { items: [{ id: 1, name: 'Test' }], total: 1 };
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        }),
      );

      const result = await api.getDashboard();
      expect(result).toEqual(mockData);
      expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    });

    it('calls fetch with no-store cache option for GET requests', async () => {
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({}),
        }),
      );

      await api.getDashboard();

      expect(globalThis.fetch).toHaveBeenCalledTimes(1);
      const callArgs = vi.mocked(globalThis.fetch).mock.calls[0];
      const url = String(callArgs[0]);
      const options = callArgs[1];
      expect(url).toContain('/api/dashboard');
      expect(options).toEqual({ cache: 'no-store' });
    });
  });

  // -------------------------------------------------------------------------
  // Error response (non-ok status)
  // -------------------------------------------------------------------------
  describe('fetchApi — error response', () => {
    it('throws an error when response is not ok (404)', async () => {
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: false,
          status: 404,
          json: () => Promise.resolve({ detail: 'Not found' }),
        }),
      );

      await expect(api.getDashboard()).rejects.toThrow('Not found');
    });

    it('throws an error for 500 status', async () => {
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: false,
          status: 500,
          json: () => Promise.resolve({ detail: 'Internal server error' }),
        }),
      );

      await expect(api.getWorkstreams()).rejects.toThrow('Internal server error');
    });
  });

  // -------------------------------------------------------------------------
  // URL construction
  // -------------------------------------------------------------------------
  describe('URL construction', () => {
    it('uses localhost:8000 as default base on client side', async () => {
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve([]),
        }),
      );

      await api.getWorkstreams();

      const calledUrl = String(vi.mocked(globalThis.fetch).mock.calls[0][0]);
      expect(calledUrl).toContain('http://localhost:8000/api/workstreams');
    });

    it('appends query parameters correctly', async () => {
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ items: [], total: 0, page: 1, pages: 1 }),
        }),
      );

      await api.getTranscripts(2, 10);

      const calledUrl = String(vi.mocked(globalThis.fetch).mock.calls[0][0]);
      expect(calledUrl).toContain('page=2');
      expect(calledUrl).toContain('limit=10');
    });

    it('uses NEXT_PUBLIC_API_URL when set', async () => {
      process.env.NEXT_PUBLIC_API_URL = 'http://custom-api:9000';

      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve([]),
        }),
      );

      await api.getWorkstreams();

      const calledUrl = String(vi.mocked(globalThis.fetch).mock.calls[0][0]);
      expect(calledUrl).toContain('http://custom-api:9000/api/workstreams');
    });
  });

  // -------------------------------------------------------------------------
  // mutateApi — POST/PATCH/DELETE operations
  // -------------------------------------------------------------------------
  describe('mutateApi — mutation operations', () => {
    it('sends POST with JSON body for create operations', async () => {
      const mockResponse = { id: 1, description: 'Test decision' };
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockResponse),
        }),
      );

      const result = await api.createDecision({
        description: 'Test decision',
        rationale: 'Test rationale',
        made_by: 'Tester',
        date: '2026-03-10',
      });

      expect(result).toEqual(mockResponse);
      const callArgs = vi.mocked(globalThis.fetch).mock.calls[0];
      const options = callArgs[1] as RequestInit;
      expect(options.method).toBe('POST');
      expect(options.headers).toEqual({ 'Content-Type': 'application/json' });
    });

    it('throws on failed mutation', async () => {
      const api = await setupWithMockedFetch(() =>
        Promise.resolve({
          ok: false,
          status: 422,
          json: () => Promise.resolve({ detail: 'Validation error' }),
        }),
      );

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
