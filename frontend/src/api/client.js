export async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(opts.headers||{}) },
    ...opts
  });
  if (!res.ok) {
    const txt = await res.text().catch(()=> '');
    throw new Error(`API ${res.status}: ${txt}`);
  }
  const ct = res.headers.get('content-type') || '';
  return ct.includes('application/json') ? res.json() : res.text();
}

// Convenience helpers
export const getSeries = (search = '', monitored = null) => {
  const qs = new URLSearchParams();
  if (search) qs.set('search', search);
  if (monitored !== null) qs.set('monitored', monitored);
  return api(`/api/series${qs.toString() ? `?${qs}` : ''}`);
};

export const createSeries = (payload) =>
  api('/api/series', { method: 'POST', body: JSON.stringify(payload) });

export const getSeriesDetail = (id) => api(`/api/series/${id}`);
export const getEpisodes = (seriesId) => api(`/api/series/${seriesId}/episodes`);

export const createEpisode = (payload) =>
  api('/api/episodes', { method: 'POST', body: JSON.stringify(payload) });

export const startDownload = (episodeId) =>
  api(`/api/episodes/${episodeId}/download`, { method: 'POST' });
