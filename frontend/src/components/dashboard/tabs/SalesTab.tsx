'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Copy, CheckCheck } from 'lucide-react';
import toast from 'react-hot-toast';

type Objection = { objection: string; response: string };
type SalesScript = {
  framework: string;
  intro: string;
  qualification: string;
  pitch: string;
  objections: Objection[];
  closing: string;
  followUp: string;
};
type ClosingTechnique = { name: string; description: string; example: string };
type MessageTemplate = { channel: string; subject: string; body: string };

type SalesData = {
  scripts: SalesScript[];
  closingTechniques: ClosingTechnique[];
  messageTemplates: MessageTemplate[];
};

const SCRIPT_FIELDS: { label: string; field: keyof Omit<SalesScript, 'framework' | 'objections'>; icon: string }[] = [
  { label: "Accroche d'ouverture", field: 'intro', icon: '👋' },
  { label: 'Qualification', field: 'qualification', icon: '🔍' },
  { label: 'Pitch de valeur', field: 'pitch', icon: '⚡' },
  { label: 'Closing', field: 'closing', icon: '🎯' },
  { label: 'Relance', field: 'followUp', icon: '📨' },
];

export default function SalesTab({ data }: { data?: SalesData }) {
  const [activeScript, setActiveScript] = useState(0);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  if (!data) return <div className="card text-gray-400 text-center py-12">Données indisponibles</div>;

  const scripts = data.scripts ?? [];
  const script = scripts[activeScript];

  const copy = (text: string, key: string) => {
    navigator.clipboard.writeText(text).catch(() => {});
    setCopiedKey(key);
    toast.success('Copié dans le presse-papiers !');
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const CopyBtn = ({ text, id }: { text: string; id: string }) => (
    <button
      onClick={() => copy(text, id)}
      className="text-gray-400 hover:text-primary-500 transition-colors flex-shrink-0"
      aria-label="Copier"
    >
      {copiedKey === id
        ? <CheckCheck className="w-4 h-4 text-emerald-500" />
        : <Copy className="w-4 h-4" />}
    </button>
  );

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Stratégie de Vente</h2>
        <p className="section-subtitle">Scripts personnalisés, techniques de closing et messages par canal.</p>
      </div>

      {/* Script selector */}
      {scripts.length > 0 && (
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
          {scripts.map((s, i) => (
            <button
              key={s.framework}
              onClick={() => setActiveScript(i)}
              className={`px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all flex-shrink-0 ${
                activeScript === i
                  ? 'bg-primary-500 text-white shadow-sm'
                  : 'bg-white border border-gray-200 text-gray-600 hover:border-gray-300'
              }`}
            >
              {s.framework}
            </button>
          ))}
        </div>
      )}

      {script && (
        <motion.div key={activeScript} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Script fields */}
          <div className="space-y-4">
            {SCRIPT_FIELDS.map(({ label, field, icon }) => {
              const value = script[field] as string;
              return (
                <div key={field} className="card">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-sm text-gray-800">{icon} {label}</h4>
                    <CopyBtn text={value} id={`script-${field}`} />
                  </div>
                  <p className="text-sm text-gray-600 leading-relaxed">{value}</p>
                </div>
              );
            })}
          </div>

          {/* Objections */}
          <div className="card">
            <h4 className="font-semibold text-gray-800 mb-4">💬 Gestion des objections</h4>
            <div className="space-y-4">
              {(script.objections ?? []).map((obj, i) => (
                <div key={`obj-${i}`} className="border-l-2 border-amber-400 pl-3 py-1">
                  <p className="text-sm font-medium text-gray-700 mb-1">❓ {obj.objection}</p>
                  <p className="text-sm text-gray-600">✅ {obj.response}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Closing techniques */}
      {(data.closingTechniques?.length ?? 0) > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">🏁 Techniques de closing</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.closingTechniques.map((t, i) => (
              <motion.div
                key={t.name}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.08 }}
                className="card"
              >
                <div className="badge-primary mb-3">{t.name}</div>
                <p className="text-sm text-gray-600 mb-3">{t.description}</p>
                <div className="p-3 bg-gray-50 rounded-xl">
                  <p className="text-xs text-gray-400 font-medium mb-1">Exemple :</p>
                  <p className="text-sm italic text-gray-700">&ldquo;{t.example}&rdquo;</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Message templates */}
      {(data.messageTemplates?.length ?? 0) > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">📤 Templates de messages</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {data.messageTemplates.map((msg, i) => {
              const copyText = `${msg.subject ? msg.subject + '\n\n' : ''}${msg.body}`;
              return (
                <div key={`msg-${i}`} className="card">
                  <div className="flex items-center justify-between mb-3">
                    <span className="badge-magenta">{msg.channel}</span>
                    <CopyBtn text={copyText} id={`msg-${i}`} />
                  </div>
                  {msg.subject && (
                    <p className="font-medium text-sm text-gray-900 mb-2">Objet : {msg.subject}</p>
                  )}
                  <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-line">{msg.body}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
