import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import Series from './pages/Series.jsx'
import SeriesDetail from './pages/SeriesDetail.jsx'
import Queue from './pages/Queue.jsx'
import Activity from './pages/Activity.jsx'
import Settings from './pages/Settings.jsx'

function App() {
  return (
    <BrowserRouter>
      <div style={{padding:16, fontFamily:'Inter, system-ui, sans-serif'}}>
        <h1>AniMonarr-Core</h1>
        <nav style={{display:'flex', gap:12, marginBottom:16}}>
          <Link to="/">Dashboard</Link>
          <Link to="/series">Series</Link>
          <Link to="/queue">Queue</Link>
          <Link to="/activity">Activity</Link>
          <Link to="/settings">Settings</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/series" element={<Series/>} />
          <Route path="/series/:id" element={<SeriesDetail/>} />
          <Route path="/queue" element={<Queue/>} />
          <Route path="/activity" element={<Activity/>} />
          <Route path="/settings" element={<Settings/>} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App/>)
