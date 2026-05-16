'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Copy, CheckCheck } from 'lucide-react';
import toast from 'react-hot-toast';

type SalesScript = {
  framework: string;
  intro: string;
  qualification: string;
  pitch: string;
  objections: { objection: string; response: string }[];
  closing: string;
  followUp: string;
};

type SalesData = {
  scripts: SalesScript[];
  closingTechniques: { name: string; description: string; example: string }[];
  messageTemplates: { channel: string; subject: string; body: string }[];
};

export default function SalesTab({ data, personas }: { data?: SalesData; personas?: any[] }) {
  const [activeScript, setActiveScript] = useState(0);
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);

  if (!data) return <div className="card text-gray-400 text-center py-12">Données indisponibles</div>;

  const copyToClipboard = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    toast.success('Copié dans le presse-papiers !');
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  const script = data.scripts?.[activeScript];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Stratégie de Vente</h2>
        <p className="section-subtitle">Scripts personnalisés, techniques de closing et messages par canal.</p>
      </div>

      {/* Script selector */}
      {data.scripts?.length > 0 && (
        <div className="flex gap-2 overflow-x-auto pb-1">
          {data.scripts.map((s, i) => (
            <button
              key={i}
              onClick={() => setActiveScript(i)}
              className={`px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
                activeScript === i ? 'bg-primary-500 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:border-gray-300'
              }`}
            >
              {s.framework}
            </button>
          ))}
        </div>
      )}

      {script && (
        <motion.div key={activeScript} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            {[
              { label: 'Accroche d\'ouverture', value: script.intro, icon: '👋' },
              { label: 'Qualification', value: script.qualification, icon: '🔍' },
              { label: 'Pitch de valeur', value: script.pitch, icon: '⚡' },
              { label: 'Closing', value: script.closing, icon: '🎯' },
              { label: 'Relance', value: script.followUp, icon: '📨' },
            ].map(({ label, value, icon }, i) => (
              <div key={label} className="card">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-sm text-gray-800">{icon} {label}</h4>
                  <button
                    onClick={() => copyToClipboard(value, i)}
                    className="text-gray-400 hover:text-primary-500 transition-colors"
                  >
                    {copiedIdx === i ? <CheckCheck className="w-4 h-4 text-emerald-500" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">{value}</p>
              </div>
            ))}
          </div>
          <div className="space-y-4">
            <div className="card">
              <h4 className="font-semibold text-gray-800 mb-4">💬 Gestion des objections</h4>
              <div className="space-y-3">
                {script.objections?.map((obj, i) => (
                  <div key={i} className="border-l-2 border-amber-400 pl-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">❓ {obj.objection}</p>
                    <p className="text-sm text-gray-600">✅ {obj.response}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Closing techniques */}
      {data.closingTechniques?.length > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">🏁 Techniques de closing</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.closingTechniques.map((t, i) => (
              <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.1 }} className="card">
                <div className="badge-primary mb-3">{t.name}</div>
                <p className="text-sm text-gray-600 mb-3">{t.description}</p>
                <div className="p-3 bg-gray-50 rounded-xl">
                  <p className="text-xs text-gray-500 font-medium mb-1">Exemple :</p>
                  <p className="text-sm italic text-gray-700">"{t.example}"</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Message templates */}
      {data.messageTemplates?.length > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">📤 Templates de messages</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {data.messageTemplates.map((msg, i) => (
              <div key={i} className="card">
                <div className="flex items-center justify-between mb-3">
                  <span className="badge-magenta">{msg.channel}</span>
                  <button
                    onClick={() => copyToClipboard(`${msg.subject}\n\n${msg.body}`, 100 + i)}
                    className="text-gray-400 hover:text-primary-500 transition-colors"
                  >
                    {copiedIdx === 100 + i ? <CheckCheck className="w-4 h-4 text-emerald-500" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
                {msg.subject && <p className="font-medium text-sm text-gray-900 mb-2">Objet : {msg.subject}</p>}
                <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-line">{msg.body}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
