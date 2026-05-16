'use client';

import { Users, Target, AlertTriangle, MessageSquare, ShoppingBag } from 'lucide-react';

interface Persona {
  name: string;
  age: number;
  job: string;
  income?: string;
  location?: string;
  goals?: string[];
  painPoints?: string[];
  channels?: string[];
  buyingTriggers?: string[];
  objections?: string[];
  quote?: string;
}

interface PersonasTabProps {
  data?: Persona[];
}

const AVATAR_COLORS = [
  { bg: 'bg-primary-100', text: 'text-primary-600' },
  { bg: 'bg-magenta-100', text: 'text-magenta-600' },
  { bg: 'bg-purple-100',  text: 'text-purple-600' },
];

export default function PersonasTab({ data }: PersonasTabProps) {
  if (!data?.length) {
    return (
      <div className="flex items-center justify-center py-20 text-gray-400">
        <div className="text-center">
          <Users className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p>Personas non disponibles</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {data.map((persona, i) => {
        const colors = AVATAR_COLORS[i % AVATAR_COLORS.length];
        const initials = persona.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

        return (
          <div key={`persona-${i}-${persona.name}`} className="card animate-fade-in" style={{ animationDelay: `${i * 80}ms` }}>
            {/* Header */}
            <div className="flex items-start gap-4 mb-6">
              <div className={`w-14 h-14 rounded-2xl ${colors.bg} flex items-center justify-center flex-shrink-0`}>
                <span className={`font-bold text-lg ${colors.text}`}>{initials}</span>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-gray-900 text-lg">{persona.name}</h3>
                <p className="text-gray-500 text-sm">
                  {persona.age} ans · {persona.job}
                  {persona.location ? ` · ${persona.location}` : ''}
                  {persona.income ? ` · ${persona.income}` : ''}
                </p>
              </div>
              <span className="badge badge-primary flex-shrink-0">Persona {i + 1}</span>
            </div>

            {/* Quote */}
            {persona.quote && (
              <blockquote className="bg-gray-50 rounded-xl px-4 py-3 mb-6 border-l-4 border-primary-300">
                <p className="text-sm text-gray-600 italic">"{persona.quote}"</p>
              </blockquote>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Goals */}
              {persona.goals?.length ? (
                <div>
                  <p className="text-xs font-semibold text-emerald-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <Target className="w-3.5 h-3.5" /> Objectifs
                  </p>
                  <ul className="space-y-1.5">
                    {persona.goals.map((g, j) => (
                      <li key={`goal-${i}-${j}`} className="flex items-start gap-2 text-sm text-gray-600">
                        <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                        {g}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {/* Pain points */}
              {persona.painPoints?.length ? (
                <div>
                  <p className="text-xs font-semibold text-amber-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5" /> Points de douleur
                  </p>
                  <ul className="space-y-1.5">
                    {persona.painPoints.map((pp, j) => (
                      <li key={`pp-${i}-${j}`} className="flex items-start gap-2 text-sm text-gray-600">
                        <span className="text-amber-500 mt-0.5 flex-shrink-0">⚠</span>
                        {pp}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {/* Channels */}
              {persona.channels?.length ? (
                <div>
                  <p className="text-xs font-semibold text-primary-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <MessageSquare className="w-3.5 h-3.5" /> Canaux
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {persona.channels.map(c => (
                      <span key={`ch-${i}-${c}`} className="badge badge-primary">{c}</span>
                    ))}
                  </div>
                </div>
              ) : null}

              {/* Buying triggers */}
              {persona.buyingTriggers?.length ? (
                <div>
                  <p className="text-xs font-semibold text-purple-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <ShoppingBag className="w-3.5 h-3.5" /> Déclencheurs d'achat
                  </p>
                  <ul className="space-y-1.5">
                    {persona.buyingTriggers.map((bt, j) => (
                      <li key={`bt-${i}-${j}`} className="flex items-start gap-2 text-sm text-gray-600">
                        <span className="text-purple-400 flex-shrink-0">→</span>
                        {bt}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>

            {/* Objections */}
            {persona.objections?.length ? (
              <div className="mt-4 pt-4 border-t border-gray-100">
                <p className="text-xs font-semibold text-red-500 uppercase tracking-wider mb-2">Objections fréquentes</p>
                <div className="flex flex-wrap gap-2">
                  {persona.objections.map((obj, j) => (
                    <span key={`obj-${i}-${j}`} className="badge badge-danger">{obj}</span>
                  ))}
                </div>
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
