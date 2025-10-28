import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getSeriesDetail, getEpisodes, createEpisode, startDownload } from '../api/client';

export default function SeriesDetail() {
  const { id } = useParams();
  const [series, setSeries] = useState(null);
  const [episodes, setEpisodes] = useState([]);
  const [err, setErr] = useState('');
  const [form, setForm] = useState({
    season: 1, episode: 1, title: '', source_url: ''
  });

  async function load() {
    setErr('');
    try {
      const [s, eps] = await Promise.all([getSeriesDetail(id), getEpisodes(id)]);
      setSeries(s);
      setEpisodes(eps);
    } catch (e) {
      setErr(String(e));
    }
  }

  useEffect(()=>{ load(); }, [id]);

  async function addEpisode(e) {
    e.preventDefault();
    try {
      await createEpisode({ ...form, series_id: Number(id) });
      setForm({ season:1, episode:1, title:'', source_url:'' });
      await load();
    } catch (e) {
      setErr(String(e));
    }
  }

  async function dl(epId) {
    try {
      await startDownload(epId);
      alert('Download gestartet (Stub). Siehe Backend-Logs.');
    } catch (e) {
      alert(String(e));
    }
  }

  if (!series) return <div>Loading…</div>;
  return (
    <div>
      <p><Link to="/series">← Zurück</Link></p>
      <h2>{series.title}</h2>
      {series.title_original && <div><em>{series.title_original}</em></div>}
      <div>Source: {series.source || 'manual'} {series.source_url ? <>| <a href={series.source_url} target="_blank">Link</a></> : null}</div>
      <hr/>

      <h3>Episoden</h3>
      {err && <div style={{color:'crimson'}}>{String(err)}</div>}
      <table border="1" cellPadding="6">
        <thead>
          <tr><th>S</th><th>E</th><th>Title</th><th>Source URL</th><th>Status</th><th>Aktion</th></tr>
        </thead>
        <tbody>
          {episodes.map(ep => (
            <tr key={ep.id}>
              <td>{ep.season}</td>
              <td>{ep.episode}</td>
              <td>{ep.title || '-'}</td>
              <td style={{maxWidth:280, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>
                <a href={ep.source_url} target="_blank" rel="noreferrer">{ep.source_url}</a>
              </td>
              <td>{ep.status}</td>
              <td><button onClick={()=>dl(ep.id)}>Download</button></td>
            </tr>
          ))}
        </tbody>
      </table>

      <h4 style={{marginTop:16}}>Episode anlegen</h4>
      <form onSubmit={addEpisode} style={{display:'grid', gap:8, maxWidth:520}}>
        <label>Season <input type="number" value={form.season} onChange={e=>setForm(f=>({...f, season: Number(e.target.value)}))} /></label>
        <label>Episode <input type="number" value={form.episode} onChange={e=>setForm(f=>({...f, episode: Number(e.target.value)}))} /></label>
        <label>Title <input value={form.title} onChange={e=>setForm(f=>({...f, title:e.target.value}))} /></label>
        <label>Source URL <input required value={form.source_url} onChange={e=>setForm(f=>({...f, source_url:e.target.value}))} placeholder="https://…"/></label>
        <button type="submit">Speichern</button>
      </form>
    </div>
  );
}
