import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Layout from './components/Layout';

function App() {
  // Try to get user from localStorage first for offline persistence
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('userData')));
  const [pin, setPin] = useState(() => localStorage.getItem('userPin'));

  const handleLogin = (userPin, userData) => {
    // Save to state
    setPin(userPin);
    setUser(userData);
    
    // Save to localStorage
    localStorage.setItem('userPin', userPin);
    localStorage.setItem('userData', JSON.stringify(userData));
  };

  const handleLogout = () => {
    // Clear state
    setUser(null);
    setPin(null);

    // Clear localStorage
    localStorage.removeItem('userPin');
    localStorage.removeItem('userData');
  };

  // If there is no user, show the Login component.
  // Otherwise, show the main Layout of the app.
  return (
    user 
      ? <Layout user={user} pin={pin} onLogout={handleLogout} /> 
      : <Login onLogin={handleLogin} />
  );
}

export default App;