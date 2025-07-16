import React, { useEffect, useState } from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate
} from 'react-router-dom';

const games = [
  { name: 'Call of Duty', path: '/call-of-duty', aliases: ['cod'] },
  { name: 'Grand Theft Auto', path: '/grand-theft-auto', aliases: ['gta'] },
  { name: 'The Witcher 3', path: '/the-witcher-3', aliases: ['witcher'] },
  { name: 'Portal 2', path: '/portal-2', aliases: [] },
  { name: 'Overwatch', path: '/overwatch', aliases: [] },
  { name: 'Fortnite', path: '/fortnite', aliases: [] }
];

function getClosestGame(search) {
  if (!search) return null;
  const s = search.trim().toLowerCase();
  // Check aliases first
  let found = games.find(g => g.aliases && g.aliases.some(a => a === s));
  if (found) return found;
  // Try includes in name
  found = games.find(g => g.name.toLowerCase().includes(s));
  if (found) return found;
  // Fallback: find closest search
  function levenshtein(a, b) {
    const matrix = Array(a.length + 1).fill(null).map(() => Array(b.length + 1).fill(null));
    for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
    for (let j = 0; j <= b.length; j++) matrix[0][j] = j;
    for (let i = 1; i <= a.length; i++) {
      for (let j = 1; j <= b.length; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j - 1] + cost
        );
      }
    }
    return matrix[a.length][b.length];
  }
  let minDist = Infinity, closest = null;
  for (const g of games) {
    const dist = levenshtein(s, g.name.toLowerCase());
    if (dist < minDist) {
      minDist = dist;
      closest = g;
    }
  }
  // Dynamic threshold: more forgiving for short words
  const threshold = s.length <= 4 ? 2 : 6;
  return minDist <= threshold ? closest : null;
}

function GamePage({ name }) {
  const [igdb, setIgdb] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`http://localhost:5000/api/igdb/game?name=${encodeURIComponent(name)}`)
      .then(res => {
        if (!res.ok) throw new Error('No IGDB info found');
        return res.json();
      })
      .then(data => {
        setIgdb(Array.isArray(data) ? data[0] : data);
        setLoading(false);
      })
      .catch(e => {
        setError(e.message);
        setLoading(false);
      });
  }, [name]);

  return (
    <div className="App" style={{ position: 'relative' }}>
      <Link to="/" className="back-link">
        <span className="back-arrow">&#8592;</span> Back to Home
      </Link>
      <h1>{name}</h1>
      {loading && <p>Loading game info...</p>}
      {error && <p style={{color:'#ff8a80'}}>Error: {error}</p>}
      {igdb && (
        <div className="igdb-info" style={{marginTop:'18px', maxWidth:600, marginLeft:'auto', marginRight:'auto', background:'rgba(30,30,40,0.7)', borderRadius:10, padding:24}}>
          {igdb.cover && igdb.cover.url && (
            <img src={igdb.cover.url.replace('t_thumb','t_cover_big')} alt="cover" style={{maxWidth:120, float:'left', marginRight:24, borderRadius:8}} />
          )}
          <div style={{textAlign:'left'}}>
            <div style={{fontSize:'1.5em', fontWeight:700, color:'#ffe082'}}>{igdb.name}</div>
            {igdb.summary && <div style={{margin:'10px 0', color:'#eee'}}>{igdb.summary}</div>}
            {igdb.first_release_date && (
              <div><b>Release:</b> {new Date(igdb.first_release_date*1000).toLocaleDateString()}</div>
            )}
            {igdb.genres && igdb.genres.length > 0 && (
              <div><b>Genres:</b> {igdb.genres.map(g=>g.name).join(', ')}</div>
            )}
            {igdb.platforms && igdb.platforms.length > 0 && (
              <div><b>Platforms:</b> {igdb.platforms.map(p=>p.name).join(', ')}</div>
            )}
            {igdb.involved_companies && igdb.involved_companies.length > 0 && (
              <div><b>Companies:</b> {igdb.involved_companies.map(c=>c.company && c.company.name).filter(Boolean).join(', ')}</div>
            )}
            {igdb.websites && igdb.websites.length > 0 && (
              <div><b>Websites:</b> {igdb.websites.map(w=>(<a key={w.url} href={w.url} target="_blank" rel="noopener noreferrer" style={{color:'#7c4dff', marginRight:8}}>{w.url}</a>))}</div>
            )}
            {igdb.updated_at && (
              <div style={{fontSize:'0.9em', color:'#aaa', marginTop:8}}>IGDB updated: {new Date(igdb.updated_at*1000).toLocaleString()}</div>
            )}
          </div>
          <div style={{clear:'both'}}></div>
        </div>
      )}
    </div>
  );
}

function Home({ sentiment }) {
  const [search, setSearch] = useState("");
  const [didYouMean, setDidYouMean] = useState(undefined);
  const [searchAttempted, setSearchAttempted] = useState(false);
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchAttempted(true);
    const s = search.trim().toLowerCase();
    let found = games.find(g => g.name.toLowerCase() === s || (g.aliases && g.aliases.includes(s)));
    if (found) {
      setDidYouMean(undefined);
      navigate(found.path);
    } else {
      const closest = getClosestGame(search);
      setDidYouMean(closest === null ? null : closest);
    }
  };

  return (
    <div className="App">
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
        <h2>Game Sentiment Hub</h2>
        <div className="tab-container">
          {games.map((game, index) => (
            <Link key={index} to={game.path} className="tab">
              {game.name}
            </Link>
          ))}
        </div>
      </div>
      <form className="search-banner" onSubmit={handleSearch} autoComplete="off" style={{ marginTop: '40px' }}>
        <input
          type="text"
          placeholder='Search games...'
          className="search-bar"
          value={search}
          onChange={e => { setSearch(e.target.value); setDidYouMean(undefined); setSearchAttempted(false); }}
        />
      </form>
      {searchAttempted && didYouMean === null && (
        <div className="did-you-mean" style={{color:'#ff8a80'}}>No results found.</div>
      )}
      {searchAttempted && didYouMean && didYouMean !== null && (
        <div className="did-you-mean">
          Did you mean <Link to={didYouMean.path}>{didYouMean.name}</Link>?
        </div>
      )}
    </div>
  );
}

function App() {
  const [sentiment, setSentiment] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/youtube/sentiment')
      .then(res => res.json())
      .then(data => setSentiment(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home sentiment={sentiment} />} />
        {games.map((game, idx) => (
          <Route
            key={game.path}
            path={game.path}
            element={<GamePage name={game.name} />}
          />
        ))}
      </Routes>
    </Router>
  );
}

export default App;