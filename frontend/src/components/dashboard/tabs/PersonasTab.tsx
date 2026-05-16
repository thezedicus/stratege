'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';

type Soncas = { [key: string]: string };
type Aida = { attention: string; interest: string; desire: string; action: string };
type Spin = { situation: string; problem: string; implication: string; need: string };

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
  soncas: Soncas;
  aida: Aida;
  spin: Spin;
  nudges: string[];
  quote: string;
};

const SONCAS_COLORS: Record<string, string> = {
  Sécurité: 'bg-blue-50 text-blue-700',
  Orgueil: 'bg-purple-50 text-purple-700',
  Nouveauté: 'bg-cyan-50 text-cyan-700',
  Confort: 'bg-green-50 text-green-700',
  Argent: 'bg-amber-50 text-amber-700',
  Sympathie: 'bg-pink-50 text-pink-700',
};

const AIDA_STEPS = [
  { k: 'attention' as const, label: 'Attention', cls: 'bg-blue-50 border border-blue-100', icon: '👁️' },
  { k: 'interest' as const, label: 'Intérêt', cls: 'bg-purple-50 border border-purple-100', icon: '🎯' },
  { k: 'desire' as const, label: 'Désir', cls: 'bg-rose-50 border border-rose-100', icon: '❤️' },
  { k: 'action' as const, label: 'Action', cls: 'bg-green-50 border border-green-100', icon: '⚡' },
];

const SPIN_STEPS = [
  { k: 'situation' as const, label: 'Situation', icon: '📍' },
  { k: 'problem' as const, label: 'Problème', icon: '⚠️' },
  { k: 'implication' as const, label: 'Implication', icon: '🔗' },
  { k: 'need' as const, label: 'Besoin de solution', icon: '💡' },
];

type Section = 'soncas' | 'aida' | 'spin' | 'nudges';

export default function PersonasTab({ data }: { data?: Persona[] }) {
  const [selected, setSelected] = useState(0);
  const [activeSection, setActiveSection] = useState<Section>('soncas');
  const [imgErrors, setImgErrors] = useState<Record<string, boolean>>({});

  if (!data?.length) return (
    <div className="card text-gray-400 text-center py-12">
      <p className="text-4xl mb-3">👥</p>
      <p>Personas non disponibles</p>
    </div>
  );

  const p = data[Math.min(selected, data.length - 1)];
  if (!p) return null;

  const photoSrc = imgErrors[p.id]
    ? `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(p.name)}`
    : p.photo;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Personas & Psychologie Consommateur</h2>
        <p className="section-subtitle">Profils détaillés avec frameworks SONCAS, AIDA et SPIN pour cibler précisément vos clients.</p>
      </div>

      {/* Persona selector */}
      <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
        {data.map((persona, i) => {
          const pPhotoSrc = imgErrors[persona.id]
            ? `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(persona.name)}`
            : persona.photo;
          return (
            <button
              key={persona.id}
              onClick={() => setSelected(i)}
              className={`flex items-center gap-3 px-4 py-3 rounded-2xl border-2 whitespace-nowrap transition-all flex-shrink-0 ${
                selected === i
                  ? 'border-primary-500 bg-primary-50 shadow-card-hover'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <div className="relative w-9 h-9 flex-shrink-0">
                {pPhotoSrc && (
                  <Image
                    src={pPhotoSrc}
                    alt={persona.name}
                    width={36}
                    height={36}
                    className="rounded-full object-cover"
                    onError={() => setImgErrors(prev => ({ ...prev, [persona.id]: true }))}
                  />
                )}
              </div>
              <div className="text-left">
                <div className="font-semibold text-sm text-gray-900">{persona.name}</div>
                <div className="text-xs text-gray-500">{persona.age} ans · {persona.job}</div>
              </div>
            </button>
          );
        })}
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
          <div className="flex items-start gap-4 mb-5">
            <div className="relative w-[72px] h-[72px] flex-shrink-0">
              {photoSrc && (
                <Image
                  src={photoSrc}
                  alt={p.name}
                  width={72}
                  height={72}
                  className="rounded-2xl object-cover shadow-sm"
                  onError={() => setImgErrors(prev => ({ ...prev, [p.id]: true }))}
                />
              )}
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">{p.name}</h3>
              <p className="text-gray-500 text-sm">{p.job}</p>
              <p className="text-gray-400 text-xs mt-1">{p.age} ans · {p.location}</p>
            </div>
          </div>

          {p.quote && (
            <blockquote className="text-sm text-gray-600 italic border-l-[3px] border-primary-500 pl-3 mb-5">
              &ldquo;{p.quote}&rdquo;
            </blockquote>
          )}

          <div className="space-y-4">
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Objectifs</h4>
              <ul className="space-y-1.5">
                {(p.goals ?? []).map((g, i) => (
                  <li key={`goal-${i}`} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>{g}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Points de douleur</h4>
              <ul className="space-y-1.5">
                {(p.painPoints ?? []).map((pp, i) => (
                  <li key={`pain-${i}`} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="text-rose-400 mt-0.5 flex-shrink-0">✗</span>{pp}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Canaux préférés</h4>
              <div className="flex flex-wrap gap-1.5">
                {(p.channels ?? []).map((c, i) => (
                  <span key={`ch-${i}`} className="badge-primary">{c}</span>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Déclencheurs d&apos;achat</h4>
              <div className="flex flex-wrap gap-1.5">
                {(p.buyingTriggers ?? []).map((t, i) => (
                  <span key={`bt-${i}`} className="badge-magenta">{t}</span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Frameworks */}
        <div className="lg:col-span-2 card">
          {/* Section tabs */}
          <div className="flex gap-2 mb-6 flex-wrap">
            {(['soncas', 'aida', 'spin', 'nudges'] as Section[]).map((s) => (
              <button
                key={s}
                onClick={() => setActiveSection(s)}
                className={`px-3 py-1.5 rounded-xl text-sm font-medium transition-all ${
                  activeSection === s
                    ? 'bg-primary-500 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {s.toUpperCase()}
              </button>
            ))}
          </div>

          {activeSection === 'soncas' && (
            <motion.div key="soncas" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
              <p className="text-sm text-gray-500 mb-4">
                Motivations d&apos;achat selon le modèle SONCAS — <em>Sécurité, Orgueil, Nouveauté, Confort, Argent, Sympathie</em>
              </p>
              {Object.entries(p.soncas ?? {}).map(([k, v]) => (
                <div key={k} className="p-3 rounded-xl border border-gray-100 hover:bg-gray-50 transition-colors">
                  <span className={`badge text-xs font-semibold mb-1.5 ${SONCAS_COLORS[k] ?? 'bg-gray-100 text-gray-600'}`}>{k}</span>
                  <p className="text-sm text-gray-700 mt-1">{v}</p>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === 'aida' && (
            <motion.div key="aida" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
              <p className="text-sm text-gray-500 mb-4">Parcours client selon le modèle AIDA</p>
              {AIDA_STEPS.map(({ k, label, cls, icon }) => (
                <div key={k} className={`p-4 rounded-xl ${cls}`}>
                  <div className="flex items-center gap-2 mb-1">
                    <span>{icon}</span>
                    <span className="font-semibold text-sm text-gray-800">{label}</span>
                  </div>
                  <p className="text-sm text-gray-700 ml-6">{p.aida?.[k] ?? '—'}</p>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === 'spin' && (
            <motion.div key="spin" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-3">
              <p className="text-sm text-gray-500 mb-4">Questions de vente selon le modèle SPIN</p>
              {SPIN_STEPS.map(({ k, label, icon }) => (
                <div key={k} className="p-4 rounded-xl bg-gray-50">
                  <div className="flex items-center gap-2 mb-1">
                    <span>{icon}</span>
                    <span className="font-semibold text-sm text-gray-800">{label}</span>
                  </div>
                  <p className="text-sm text-gray-600 italic ml-6">&ldquo;{p.spin?.[k] ?? '—'}&rdquo;</p>
                </div>
              ))}
            </motion.div>
          )}

          {activeSection === 'nudges' && (
            <motion.div key="nudges" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              <p className="text-sm text-gray-500 mb-4">Leviers psychologiques et biais cognitifs à exploiter</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {(p.nudges ?? []).map((nudge, i) => (
                  <div
                    key={`nudge-${i}`}
                    className="p-3 rounded-xl border border-gray-100"
                    style={{ background: 'linear-gradient(135deg, #EBF8FF 0%, #FFF0F7 100%)' }}
                  >
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
