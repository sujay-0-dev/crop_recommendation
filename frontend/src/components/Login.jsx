import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const Login = ({ onLogin }) => {
  const { t } = useTranslation();
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!pin) return;
    try {
      const response = await axios.post('http://localhost:5000/api/login', { pin });
      if (response.data.success) {
        onLogin(pin, response.data.user);
      }
    } catch (err) {
      setError('Login failed. Please check your PIN and try again.');
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-green-50 p-4">
      <h1 className="text-4xl font-bold text-green-700 mb-4">🌿 KisanAI</h1>
      <p className="text-gray-600 mb-6">{t('loginPrompt')}</p>
      <input
        type="password"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
        placeholder={t('pinPlaceholder')}
        className="w-full max-w-sm p-3 mb-4 text-center rounded-lg border-2 border-green-300 focus:outline-none focus:ring-2 focus:ring-green-500"
      />
      <button
        onClick={handleLogin}
        className="w-full max-w-sm bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg transition duration-300"
      >
        {t('loginButton')}
      </button>
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
};

export default Login;