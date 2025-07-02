import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [sentiment, setSentiment] = useState(null);

  const games = [
    'Call of Duty', 
    'Grand Theft Auto',
    'The Witcher 3',
    'Portal 2',
    'Overwatch',
    'Fortnite'
  ];

  useEffect(() => {
    fetch('http://localhost:5000/api/youtube/sentiment')
      .then(res => res.json())
      .then(data => setSentiment(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="App">
      <h1>Today's Top Game</h1>
      <div className="search-banner">
        <input type="text" placeholder='Search games...' className="search-bar" />
      </div>
      <h2>Game Sentiment Hub</h2>
      <div className="tab-container">
        {games.map((game, index) => (
          <div key={index} className="tab">
            {game}
          </div>
        ))}
      </div>
      <h2>YouTube Sentiment Data</h2>
      <pre>{sentiment ? JSON.stringify(sentiment, null, 2) : "Loading..."}</pre>
    </div>
  );
}

export default App;