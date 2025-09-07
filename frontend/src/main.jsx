import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './i18n'; // Initializes internationalization
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// Register the Service Worker for offline mode
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('✅ Service Worker registered!');
      })
      .catch(error => {
        console.error('❌ Service Worker registration failed:', error);
      });
  });
}