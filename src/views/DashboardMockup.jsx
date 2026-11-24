import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

// Dane tymczasowe (mocki) - później do podmiany na fetch z API
const campaignStats = [
  { name: 'Faktura VAT', otwarcia: 45, klikniecia: 12 },
  { name: 'Reset hasła HR', otwarcia: 62, klikniecia: 28 },
  { name: 'Paczka kurierska', otwarcia: 38, klikniecia: 9 },
  { name: 'Aktualizacja VPN', otwarcia: 51, klikniecia: 19 },
];

const recentEvents = [
  { id: 'usr_9f82a1', dzial: 'Sprzedaż', kampania: 'Reset hasła HR', akcja: 'Kliknięcie linku', czas: '2 min temu', status: 'wysokie' },
  { id: 'usr_3c41b8', dzial: 'Finanse', kampania: 'Faktura VAT', akcja: 'Otwarcie maila', czas: '14 min temu', status: 'srednie' },
  { id: 'usr_7d10e4', dzial: 'IT', kampania: 'Aktualizacja VPN', akcja: 'Zgłoszono phishing', czas: '1 godz. temu', status: 'bezpieczne' },
  { id: 'usr_2a55c9', dzial: 'Marketing', kampania: 'Paczka kurierska', akcja: 'Kliknięcie linku', czas: '3 godz. temu', status: 'wysokie' },
];

export default function DashboardMockup() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Dashboard Administratora</h1>

      {/* Kafelki KPI */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <h3 className="text-gray-500 text-sm font-bold uppercase">Risk Score</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">Niski (24%)</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
          <h3 className="text-gray-500 text-sm font-bold uppercase">Aktywne kampanie</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">4</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-red-500">
          <h3 className="text-gray-500 text-sm font-bold uppercase">Kliknięcia (7 dni)</h3>
          <p className="text-3xl font-bold text-gray-800 mt-2">68</p>
        </div>
      </div>

      {/* Sekcja wykresu */}
      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Skuteczność kampanii (Otwarcia vs Kliknięcia)</h2>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={campaignStats} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="otwarcia" name="Otwarte maile" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="klikniecia" name="Kliknięte linki" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Sekcja tabeli */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-800">Ostatnie zdarzenia (Tracking)</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 text-gray-600 text-sm uppercase">
                <th className="py-3 px-6">ID Użytkownika (Hash)</th>
                <th className="py-3 px-6">Dział</th>
                <th className="py-3 px-6">Kampania</th>
                <th className="py-3 px-6">Akcja</th>
                <th className="py-3 px-6">Czas</th>
              </tr>
            </thead>
            <tbody className="text-gray-700 text-sm divide-y divide-gray-200">
              {recentEvents.map((event, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="py-3 px-6 font-mono text-gray-500">{event.id}</td>
                  <td className="py-3 px-6 font-medium">{event.dzial}</td>
                  <td className="py-3 px-6">{event.kampania}</td>
                  <td className="py-3 px-6">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        event.status === 'wysokie'
                          ? 'bg-red-100 text-red-700'
                          : event.status === 'srednie'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-green-100 text-green-700'
                      }`}
                    >
                      {event.akcja}
                    </span>
                  </td>
                  <td className="py-3 px-6 text-gray-500">{event.czas}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
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
