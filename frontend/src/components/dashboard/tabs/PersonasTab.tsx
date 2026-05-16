'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';

type Persona = {
  id: string;
  name: string;
  age: number;
  job: string;
  location: string;
  photo: string;
  goals: string[];
  painPoints: string[];
  channels: string[];
  buyingTriggers: string[];
  soncas: { [key: string]: string };
  aida: { attention: string; interest: string; desire: string; action: string };
  spin: { situation: string; problem: string; implication: string; need: string };
  nudges: string[];
  quote: string;
};

const sonCasColors: Record<string, string> = {
  Sécurité: 'bg-blue-50 text-blue-700',
  Orgueil: 'bg-purple-50 text-purple-700',
  Nouveauté: 'bg-cyan-50 text-cyan-700',
  Confort: 'bg-green-50 text-green-700',
  Argent: 'bg-amber-50 text-amber-700',
  Sympathie: 'bg-pink-50 text-pink-700',
};

export default function PersonasTab({ data }: { data?: Persona[] }) {
  const [selected, setSelected] = useState(0);
  const [activeSection, setActiveSection] = useState<'soncas' | 'aida' | 'spin' | 'nudges'>('soncas');

  if (!data?.length) return <div className="card text-gray-400 text-center py-12">Personas non disponibles</div>;

  const p = data[selected];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Personas & Psychologie Consommateur</h2>
        <p className="section-subtitle">5 profils détaillés avec frameworks SONCAS, AIDA et SPIN pour cibler précisément vos clients.</p>
      </div>

      {/* Persona selector */}
      <div className="flex gap-3 overflow-x-auto pb-2">
        {data.map((persona, i) => (
          <button
            key={persona.id}
            onClick={() => setSelected(i)}
            className={`flex items-center gap-3 px-4 py-3 rounded-2xl border-2 whitespace-nowrap transition-all ${
              selected === i ? 'border-primary-500 bg-primary-50' : 'border-gray-200 bg-white hover:border-gray-300'
            }`}
          >
            {persona.photo && (
              <Image
                src={persona.photo}
                alt={persona.name}
                width={36}
                height={36}
                className="rounded-full object-cover"
              />
            )}
            <div className="text-left">
              <div className="font-semibold text-sm text-gray-900">{persona.name}</div>
              <div className="text-xs text-gray-500">{persona.age} ans · {persona.job}</div>
            </div>
          </button>
        ))}
      </div>

      {/* Main persona card */}
      <motion.div
        key={selected}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="grid grid-cols-1 lg:grid-cols-3 gap-6"
      >
        {/* Profile */}
        <div className="card">
          <div className="flex items-start gap-4 mb-6">
            {p.photo && (
              <Image
                src={p.photo}
                alt={p.name}
                width={72}
                height={72}
                className="rounded-2xl object-cover shadow-sm"
              />
            )}
            <div>
              <h3 className="text-xl font-bold text-gray-900">{p.name}</h3>
              <p className="text-gray-500 text-sm">{p.job}</p>
              <p className="text-gray-400 text-xs mt-1">{p.age} ans · {p.location}</p>
            </div>
          </div>
          {p.quote && (
            <blockquote className="text-sm text-gray-600 italic border-l-3 border-primary-500 pl-3 mb-4">
              "{p.quote}"
            </blockquote>
          )}
          <div className="space-y-4">
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Objectifs</h4>
              <ul className="space-y-1">
                {p.goals.map((g, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-emerald-500 mt-0.5">✓</span>{g}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Points de douleur</h4>
              <ul className="space-y-1">
                {p.painPoints.map((pp, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-rose-400 mt-0.5">✗</span>{pp}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Canaux préférés</h4>
              <div className="flex flex-wrap gap-2">
                {p.channels.map((c, i) => (
                  <span key={i} className="badge-primary text-xs">{c}</span>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Déclencheurs d'achat</h4>
              <div className="flex flex-wrap gap-2">
                {p.buyingTriggers.map((t, i) => (
                  <span key={i} className="badge-magenta text-xs">{t}</span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Frameworks */}
        <div className="lg:col-span-2 card">
          <div className="flex gap-2 mb-6 border-b border-gray-100 pb-4">
            {(['soncas', 'aida', 'spin', 'nudges'] as const).map((s) => (
              <button
                key={s}
                onClick={() => setActiveSection(s)}
                className={`px-3 py-1.5 rounded-xl text-sm font-medium transition-all ${
                  activeSection === s ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {s.toUpperCase()}
              </button>
            ))}
          </div>

          {activeSection === 'soncas' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
              <p className="text-sm text-gray-500 mb-4">Motivations d'achat selon le modèle SONCAS (Sécurité, Orgueil, Nouveauté, Confort, Argent, Sympathie)</p>
              {Object.entries(p.soncas).map(([k, v]) => (
                <div key={k} className="p-3 rounded-xl border border-gray-100">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`badge text-xs font-semibold ${sonCasColors[k] || 'bg-gray-100 text-gray-600'}`}>{k}</span>
                  </div>
                  <p className="text-sm text-gray-700">{v}</p>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === 'aida' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <p className="text-sm text-gray-500 mb-4">Parcours client selon le modèle AIDA</p>
              {[
                { k: 'attention', label: 'Attention', color: 'bg-blue-50 border-blue-200', icon: '👁️' },
                { k: 'interest', label: 'Intérêt', color: 'bg-purple-50 border-purple-200', icon: '🎯' },
                { k: 'desire', label: 'Désir', color: 'bg-rose-50 border-rose-200', icon: '❤️' },
                { k: 'action', label: 'Action', color: 'bg-green-50 border-green-200', icon: '⚡' },
              ].map(({ k, label, color, icon }) => (
                <div key={k} className={`p-4 rounded-xl border ${color}`}>
                  <div className="flex items-center gap-2 mb-1">
                    <span>{icon}</span>
                    <span className="font-semibold text-sm text-gray-800">{label}</span>
                  </div>
                  <p className="text-sm text-gray-700">{p.aida[k as keyof typeof p.aida]}</p>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === 'spin' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
              <p className="text-sm text-gray-500 mb-4">Questions de vente selon le modèle SPIN</p>
              {[
                { k: 'situation', label: 'Situation', icon: '📍' },
                { k: 'problem', label: 'Problème', icon: '⚠️' },
                { k: 'implication', label: 'Implication', icon: '🔗' },
                { k: 'need', label: 'Besoin de solution', icon: '💡' },
              ].map(({ k, label, icon }) => (
                <div key={k} className="p-4 rounded-xl bg-gray-50">
                  <div className="flex items-center gap-2 mb-1">
                    <span>{icon}</span>
                    <span className="font-semibold text-sm text-gray-800">{label}</span>
                  </div>
                  <p className="text-sm text-gray-600 italic">"{p.spin[k as keyof typeof p.spin]}"</p>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === 'nudges' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <p className="text-sm text-gray-500 mb-4">Leviers psychologiques et biais cognitifs à exploiter</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {p.nudges.map((nudge, i) => (
                  <div key={i} className="p-3 rounded-xl bg-gradient-to-br from-primary-50 to-magenta-50 border border-gray-100">
                    <span className="text-sm text-gray-700">🧠 {nudge}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
