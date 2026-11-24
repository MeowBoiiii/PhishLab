import React from 'react';

export default function DashboardMockup() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Dashboard Administratora</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded shadow border-l-4 border-green-500">
          <h3 className="text-gray-500 text-sm font-bold uppercase">Risk Score</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">Niski (24%)</p>
        </div>
        <div className="bg-white p-6 rounded shadow border-l-4 border-blue-500">
          <h3 className="text-gray-500 text-sm font-bold uppercase">Aktywne kampanie</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">2</p>
        </div>
        <div className="bg-white p-6 rounded shadow border-l-4 border-red-500">
          <h3 className="text-gray-500 text-sm font-bold uppercase">Kliknięcia (7 dni)</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">12</p>
        </div>
      </div>
      
      <div className="bg-white p-8 rounded shadow flex items-center justify-center border-dashed border-2 border-gray-300 h-64">
        <p className="text-gray-400 text-center">
          Miejsce na statystyki / wykresy analityczne<br/>
          (Zostaną dodane w Tygodniu 3 po spięciu z API)
        </p>
      </div>
    </div>
  );
}
