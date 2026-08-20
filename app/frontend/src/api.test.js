import { beforeEach, describe, expect, it, vi } from 'vitest';
import { api } from './api.js';

describe('api', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.stubGlobal('localStorage', { getItem: vi.fn(() => null) });
  });

  it('returns JSON from a successful request', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 200, json: vi.fn().mockResolvedValue({ status: 'healthy' }) });
    vi.stubGlobal('fetch', fetchMock);
    await expect(api('/health')).resolves.toEqual({ status: 'healthy' });
    expect(fetchMock).toHaveBeenCalledWith('http://localhost:8000/health', expect.objectContaining({ headers: { 'Content-Type': 'application/json' } }));
  });

  it('adds the stored bearer token and handles an empty response', async () => {
    localStorage.getItem.mockReturnValue('test-token');
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 204 });
    vi.stubGlobal('fetch', fetchMock);
    await expect(api('/api/bookings/1', { method: 'DELETE' })).resolves.toBeNull();
    expect(fetchMock.mock.calls[0][1].headers.Authorization).toBe('Bearer test-token');
  });

  it('surfaces API validation errors', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 422, json: vi.fn().mockResolvedValue({ detail: [{ msg: 'Invalid booking time' }] }) }));
    await expect(api('/api/bookings')).rejects.toThrow('Invalid booking time');
  });
});