import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Login from './views/Login';
import DashboardMockup from './views/DashboardMockup';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <nav className="bg-blue-800 text-white p-4 shadow flex gap-4">
          <Link to="/" className="font-bold">PhishLab</Link>
          <Link to="/login" className="hover:underline">Logowanie</Link>
          <Link to="/dashboard" className="hover:underline">Dashboard (Makieta)</Link>
        </nav>
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<div className="p-8">Witaj w PhishLab - wybierz widok z menu.</div>} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<DashboardMockup />} />
          </Routes>
        </div>
      </div>
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    </BrowserRouter>
  );
}
