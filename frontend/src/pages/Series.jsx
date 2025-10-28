import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getSeries, createSeries } from '../api/client';

export default function Series() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');
  const [form, setForm] = useState({
    title: '',
    source: 'manual',     // 'manual' oder 'rss'
    source_url: '',
    monitored: false
  });

  async function load() {
    try {
      setLoading(true);
      setItems(await getSeries());
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function onCreate(e) {
    e.preventDefault();
    setErr('');
    try {
      await createSeries(form);
      setForm({ title:'', source:'manual', source_url:'', monitored:false });
      await load();
    } catch (e) {
      setErr(String(e));
    }
  }

  return (
    <div>
      <h2>Series</h2>
      {err && <div style={{color:'crimson'}}>{err}</div>}
      {loading ? <div>Loading…</div> : (
        <>
          <ul style={{display:'grid', gap:8, padding:0, listStyle:'none'}}>
            {items.map(s => (
              <li key={s.id} style={{border:'1px solid #333', padding:12, borderRadius:8}}>
                <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                  <div>
                    <strong>{s.title}</strong> {s.title_original ? `(${s.title_original})` : ''}<br/>
                    <small>Source: {s.source || 'manual'}</small>{' '}
                    {s.monitored ? <span>• monitored</span> : null}
                  </div>
                  <Link to={`/series/${s.id}`}>Details →</Link>
                </div>
              </li>
            ))}
          </ul>

          <hr style={{margin:'16px 0'}}/>

          <h3>Neue Serie anlegen</h3>
          <form onSubmit={onCreate} style={{display:'grid', gap:8, maxWidth:520}}>
            <label>
              Titel<br/>
              <input
                value={form.title}
                onChange={e=>setForm(f=>({...f, title:e.target.value}))}
                required
              />
            </label>
            <label>
              Quelle (manual | rss)<br/>
              <input
                value={form.source}
                onChange={e=>setForm(f=>({...f, source:e.target.value}))}
                placeholder="manual oder rss"
              />
            </label>
            <label>
              Source URL (optional; bei RSS: Feed-URL)<br/>
              <input
                value={form.source_url}
                onChange={e=>setForm(f=>({...f, source_url:e.target.value}))}
                placeholder="https://…"
              />
            </label>
            <label>
              <input
                type="checkbox"
                checked={form.monitored}
                onChange={e=>setForm(f=>({...f, monitored:e.target.checked}))}
              /> Monitored
            </label>
            <button type="submit">Anlegen</button>
          </form>
        </>
      )}
    </div>
  );
}
