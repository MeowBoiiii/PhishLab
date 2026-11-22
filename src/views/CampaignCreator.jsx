import React, { useState } from 'react';

export default function CampaignCreator() {
  const [name, setName] = useState('');
  const [template, setTemplate] = useState('faktura');
  const [targetGroup, setTargetGroup] = useState('wszyscy');
  const [scheduleDate, setScheduleDate] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    // Tutaj w przyszłości pójdzie zapytanie POST do API z danymi:
    // { name, template, targetGroup, scheduleDate }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Kreator Kampanii Phishingowej</h1>

      {submitted && (
        <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-800 rounded-lg">
          Kampania <strong>"{name || 'Bez nazwy'}"</strong> została przygotowana (tryb makiety — oczekuje na podpięcie API).
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md space-y-6">
        {/* Nazwa kampanii */}
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">
            Nazwa kampanii
          </label>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="np. Test Q4 - Reset hasła HR"
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Szablon wiadomości */}
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">
            Szablon wiadomości e-mail
          </label>
          <select
            value={template}
            onChange={(e) => setTemplate(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="faktura">Nieopłacona faktura VAT (Pilne)</option>
            <option value="hr">Wymagany reset hasła firmowego (Dział HR)</option>
            <option value="kurier">Niedoręczona paczka kurierska</option>
            <option value="vpn">Obowiązkowa aktualizacja klienta VPN</option>
          </select>
        </div>

        {/* Grupa docelowa */}
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">
            Grupa docelowa
          </label>
          <select
            value={targetGroup}
            onChange={(e) => setTargetGroup(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="wszyscy">Wszyscy pracownicy</option>
            <option value="sprzedaz">Dział Sprzedaży</option>
            <option value="finanse">Dział Finansów</option>
            <option value="it">Dział IT</option>
            <option value="marketing">Marketing</option>
          </select>
        </div>

        {/* Harmonogram */}
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">
            Harmonogram wysyłki (data i godzina)
          </label>
          <input
            type="datetime-local"
            required
            value={scheduleDate}
            onChange={(e) => setScheduleDate(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Przyciski */}
        <div className="flex justify-end gap-4 pt-4 border-t">
          <button
            type="button"
            onClick={() => {
              setName('');
              setScheduleDate('');
              setSubmitted(false);
            }}
            className="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            Wyczyść
          </button>
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700"
          >
            Utwórz kampanię
          </button>
        </div>
      </form>
    </div>
  );
}