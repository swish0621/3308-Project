import React from 'react';
import './App.css';

function App() {
  const games = [
    'Call of Duty', 
    'Grand Theft Auto',
    'The Witcher 3',
    'Portal 2',
    'Overwatch',
    'Fortnite'
  ];

  return (
    <div className="App">
      <h1>Today's Top Game </h1>
      <div className="search-banner">
        <input type="text" placeholder='Search games...' className="search-bar" />
      </div>
      <h2> Game Sentiment Hub</h2>
      <div className="tab-container">
        {games.map((game, index) => (
          <div key={index} className="tab">
            {game}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
