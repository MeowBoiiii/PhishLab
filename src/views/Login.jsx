import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // Jeśli w main.py kolega ustawił inny prefiks niż /api/v1/auth, podmień go tutaj
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || 'Nieprawidłowy adres email lub hasło');
        return;
      }

      // Zapis tokena JWT w przeglądarce
      localStorage.setItem('access_token', data.access_token);

      // Przekierowanie na Dashboard
      navigate('/dashboard');
    } catch (err) {
      setError('Brak połączenia z serwerem. Upewnij się, że backend (FastAPI) działa na porcie 8000.');
    }
  };

  return (
    <div className="flex h-[80vh] items-center justify-center">
      <div className="w-full max-w-sm mx-auto overflow-hidden bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div className="px-6 py-4">
          <h3 className="mt-3 text-xl font-medium text-center text-gray-600 dark:text-gray-200">PhishLab</h3>
          <p className="mt-1 text-center text-gray-500 dark:text-gray-400">Logowanie Administratora</p>

          {error && (
            <div className="mt-4 p-3 text-sm text-red-700 bg-red-100 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div className="w-full mt-4">
              <input
                className="block w-full px-4 py-2 mt-2 text-gray-700 placeholder-gray-500 bg-white border rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Adres Email"
                aria-label="Email Address"
              />
            </div>

            <div className="w-full mt-4">
              <input
                className="block w-full px-4 py-2 mt-2 text-gray-700 placeholder-gray-500 bg-white border rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 focus:border-blue-400 focus:outline-none focus:ring focus:ring-blue-300"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Hasło"
                aria-label="Password"
              />
            </div>

            <div className="flex items-center justify-between mt-4">
              <a href="#" className="text-sm text-gray-600 dark:text-gray-200 hover:text-gray-500">Zapomniałeś hasła?</a>
              <button
                type="submit"
                className="px-6 py-2 text-sm font-medium tracking-wide text-white capitalize transition-colors duration-300 transform bg-blue-500 rounded-lg hover:bg-blue-400 focus:outline-none focus:ring focus:ring-blue-300"
              >
                Zaloguj się
              </button>
            </div>
          </form>
        </div>

        <div className="flex items-center justify-center py-4 text-center bg-gray-50 dark:bg-gray-700">
          <span className="text-sm text-gray-600 dark:text-gray-200">Nie masz konta? </span>
          <a href="#" className="mx-2 text-sm font-bold text-blue-500 dark:text-blue-400 hover:underline">Zgłoś się do IT</a>
        </div>
      </div>
import React from 'react';

export default function Login() {
  return (
    <div className="flex h-[80vh] items-center justify-center">
        <div className="w-full max-w-sm mx-auto overflow-hidden bg-white rounded-lg shadow-md dark:bg-gray-800">
            <div className="px-6 py-4">
                <div className="flex justify-center mx-auto">
                    <img className="w-auto h-7 sm:h-8" src="https://cdn.vectorstock.com/i/500p/70/39/linked-font-logo-pl-initial-vector-32497039.jpg" alt="PhishLab Logo" />
                </div>

                <h3 className="mt-3 text-xl font-medium text-center text-gray-600 dark:text-gray-200">PhishLab</h3>

                <p className="mt-1 text-center text-gray-500 dark:text-gray-400">Logowanie Administratora</p>

                <form>
                    <div className="w-full mt-4">
                        <input className="block w-full px-4 py-2 mt-2 text-gray-700 placeholder-gray-500 bg-white border rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 focus:border-blue-400 dark:focus:border-blue-300 focus:ring-opacity-40 focus:outline-none focus:ring focus:ring-blue-300" type="email" placeholder="Adres Email" aria-label="Email Address" />
                    </div>

                    <div className="w-full mt-4">
                        <input className="block w-full px-4 py-2 mt-2 text-gray-700 placeholder-gray-500 bg-white border rounded-lg dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 focus:border-blue-400 dark:focus:border-blue-300 focus:ring-opacity-40 focus:outline-none focus:ring focus:ring-blue-300" type="password" placeholder="Hasło" aria-label="Password" />
                    </div>

                    <div className="flex items-center justify-between mt-4">
                        <a href="#" className="text-sm text-gray-600 dark:text-gray-200 hover:text-gray-500">Zapomniałeś hasła?</a>

                        <button className="px-6 py-2 text-sm font-medium tracking-wide text-white capitalize transition-colors duration-300 transform bg-blue-500 rounded-lg hover:bg-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-50">
                            Zaloguj się
                        </button>
                    </div>
                </form>
            </div>

            <div className="flex items-center justify-center py-4 text-center bg-gray-50 dark:bg-gray-700">
                <span className="text-sm text-gray-600 dark:text-gray-200">Nie masz konta? </span>
                <a href="#" className="mx-2 text-sm font-bold text-blue-500 dark:text-blue-400 hover:underline">Zarejestruj się</a>
            </div>
        </div>
    </div>
  );
}