'use client';

import { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Calendar, Target, Layers, TrendingUp, Zap } from 'lucide-react';

interface MarketingTabProps {
  data?: {
    platforms?: Array<{
      name: string;
      priority: string;
      frequency: string;
      contentTypes?: string[];
    }>;
    budgetAllocation?: Array<{
      category: string;
      percentage: number;
      amount: number;
    }>;
    contentCalendar?: Array<{
      week: number | string;
      platform: string;
      topic: string;
      format?: string;
    }>;
    rule8020?: string[];
    hooks?: string[];
    weeklySchedule?: Array<{
      day: string;
      tasks?: string[];
    }>;
  };
  copywriting?: {
    aida?: Record<string, { principe: string; exemple: string; formules: string[]; conseil: string }>;
    copywriting_principles?: string[];
  };
  input?: {
    monthlyBudget?: number;
  };
}

const AIDA_META: Record<string, { emoji: string; color: string; bg: string; border: string }> = {
  attention: { emoji: '🎯', color: 'text-red-600',     bg: 'bg-red-50',     border: 'border-red-200' },
  interest:  { emoji: '💡', color: 'text-amber-600',   bg: 'bg-amber-50',   border: 'border-amber-200' },
  desire:    { emoji: '💜', color: 'text-purple-600',  bg: 'bg-purple-50',  border: 'border-purple-200' },
  action:    { emoji: '🚀', color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200' },
};

const PRIORITY_BADGE: Record<string, string> = {
  haute:   'badge-danger',
  high:    'badge-danger',
  moyenne: 'badge-warning',
  medium:  'badge-warning',
  faible:  'badge-gray',
  low:     'badge-gray',
};

const CHART_COLORS = ['#38B6FF', '#E20074', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444'];

export default function MarketingTab({ data, copywriting, input }: MarketingTabProps) {
  const [activeDay, setActiveDay] = useState<string | null>(null);

  if (!data) {
    return (
      <div className="flex items-center justify-center py-20 text-gray-400">
        <div className="text-center">
          <TrendingUp className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p>Données marketing non disponibles</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Budget allocation */}
      {data.budgetAllocation?.length ? (
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Target className="w-5 h-5 text-primary-500" />
            Répartition budgétaire
            {input?.monthlyBudget ? (
              <span className="text-sm font-normal text-gray-500 ml-1">
                ({input.monthlyBudget} €/mois)
              </span>
            ) : null}
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 items-center">
            {/* Pie chart */}
            <div style={{ height: 220 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.budgetAllocation}
                    dataKey="percentage"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={88}
                    paddingAngle={3}
                  >
                    {data.budgetAllocation.map((_, i) => (
                      <Cell key={`cell-${i}`} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ fontSize: 12, borderRadius: 8, border: '1px solid #f3f4f6' }}
                    formatter={(v: number) => [`${v}%`, '']}
                  />
                  <Legend
                    iconType="circle"
                    iconSize={8}
                    formatter={(v) => <span style={{ fontSize: 12, color: '#6b7280' }}>{v}</span>}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            {/* Budget rows */}
            <div className="space-y-3">
              {data.budgetAllocation.map((item, i) => (
                <div key={`budget-${item.category}`} className="flex items-center gap-3">
                  <div
                    className="w-3 h-3 rounded-full flex-shrink-0"
                    style={{ backgroundColor: CHART_COLORS[i % CHART_COLORS.length] }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700 truncate">{item.category}</span>
                      <span className="text-sm font-bold text-gray-900 ml-2">{item.amount} €</span>
                    </div>
                    <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className="h-1.5 rounded-full transition-all duration-500"
                        style={{
                          width: `${item.percentage}%`,
                          backgroundColor: CHART_COLORS[i % CHART_COLORS.length],
                        }}
                      />
                    </div>
                  </div>
                  <span className="text-xs text-gray-400 w-8 text-right flex-shrink-0">
                    {item.percentage}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : null}

      {/* Platforms */}
      {data.platforms?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Layers className="w-5 h-5 text-primary-500" />
            Plateformes recommandées
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.platforms.map((p) => (
              <div key={`platform-${p.name}`} className="card-sm">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-gray-900">{p.name}</span>
                  {p.priority && (
                    <span className={`badge ${PRIORITY_BADGE[p.priority?.toLowerCase()] ?? 'badge-gray'}`}>
                      {p.priority}
                    </span>
                  )}
                </div>
                <p className="text-xs text-gray-500 mb-3">{p.frequency}</p>
                {p.contentTypes?.length ? (
                  <div className="flex flex-wrap gap-1.5">
                    {p.contentTypes.map(ct => (
                      <span key={ct} className="badge badge-primary text-xs">{ct}</span>
                    ))}
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Content calendar */}
      {data.contentCalendar?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-magenta-500" />
            Calendrier éditorial
          </h2>
          <div className="overflow-x-auto rounded-2xl border border-gray-100">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  {['Semaine', 'Plateforme', 'Sujet', 'Format'].map(h => (
                    <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {data.contentCalendar.map((row, i) => (
                  <tr key={`cal-${row.week}-${row.platform}-${i}`} className="bg-white hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 font-medium text-gray-900 whitespace-nowrap">
                      S{row.week}
                    </td>
                    <td className="px-4 py-3">
                      <span className="badge badge-primary">{row.platform}</span>
                    </td>
                    <td className="px-4 py-3 text-gray-600 max-w-[220px]">
                      <span className="line-clamp-2">{row.topic}</span>
                    </td>
                    <td className="px-4 py-3 text-gray-500">{row.format ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : null}

      {/* Weekly schedule */}
      {data.weeklySchedule?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-500" />
            Planning hebdomadaire
          </h2>
          <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-2">
            {data.weeklySchedule.map(day => (
              <button
                key={`day-${day.day}`}
                onClick={() => setActiveDay(activeDay === day.day ? null : day.day)}
                className={`flex-shrink-0 px-4 py-2 rounded-xl text-sm font-medium transition-all border-2
                  ${activeDay === day.day
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'}`}
              >
                {day.day}
              </button>
            ))}
          </div>
          {activeDay && (() => {
            const day = data.weeklySchedule?.find(d => d.day === activeDay);
            return day?.tasks?.length ? (
              <div className="mt-3 card-sm animate-fade-in">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">{day.day}</p>
                <ul className="space-y-1.5">
                  {day.tasks.map((t, i) => (
                    <li key={`task-${i}`} className="flex items-start gap-2 text-sm text-gray-600">
                      <span className="text-primary-500 font-bold flex-shrink-0">·</span>
                      {t}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null;
          })()}
        </div>
      ) : null}

      {/* Rule 80/20 */}
      {data.rule8020?.length ? (
        <div className="card" style={{ background: 'linear-gradient(135deg, #F0F9FF, #FFF0F7)' }}>
          <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary-500" />
            Règle des 80/20 — Priorités d'action
          </h2>
          <div className="space-y-2">
            {data.rule8020.map((item, i) => (
              <div key={`rule-${i}`} className="flex items-start gap-3 text-sm">
                <span className="w-5 h-5 rounded-full bg-gradient-primary text-white text-xs
                  flex items-center justify-center flex-shrink-0 font-bold mt-0.5">
                  {i + 1}
                </span>
                <span className="text-gray-700">{item}</span>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Hooks */}
      {data.hooks?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">✍️ Hooks & accroches</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {data.hooks.map((hook, i) => (
              <div key={`hook-${i}`} className="card-sm flex items-start gap-3">
                <span className="text-xl flex-shrink-0">💡</span>
                <p className="text-sm text-gray-700 italic">"{hook}"</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* ── AIDA Copywriting (complement from copywriting service) ─────────── */}
      {copywriting?.aida && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" /> Copywriting AIDA — Appliquer à vos contenus
          </h2>
          <p className="text-sm text-gray-500 mb-5">
            Structurez chaque contenu marketing selon la séquence AIDA pour maximiser l'engagement et la conversion.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(copywriting.aida).map(([step, content]) => {
              const meta = AIDA_META[step] ?? { emoji: '📌', color: 'text-gray-600', bg: 'bg-gray-50', border: 'border-gray-200' };
              return (
                <div key={`mkt-aida-${step}`} className={`rounded-2xl border-2 p-5 ${meta.bg} ${meta.border}`}>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-2xl">{meta.emoji}</span>
                    <h3 className={`font-bold text-lg ${meta.color} uppercase`}>{step}</h3>
                  </div>
                  <p className="text-sm font-semibold text-gray-900 mb-2">{content.principe}</p>
                  <div className="bg-white/70 rounded-xl p-3 mb-3">
                    <p className="text-xs font-semibold text-gray-500 mb-1">Exemple pour ce contenu :</p>
                    <p className="text-sm text-gray-700 italic">"{content.exemple}"</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs font-semibold text-gray-500">Formules à tester :</p>
                    {content.formules.map((f, i) => (
                      <p key={`mf-${i}`} className="text-xs text-gray-600 flex gap-1.5">
                        <span className={`font-bold ${meta.color} flex-shrink-0`}>→</span>{f}
                      </p>
                    ))}
                  </div>
                  <div className="mt-3 bg-white/50 rounded-lg px-3 py-2">
                    <p className="text-xs text-gray-500">
                      <span className="font-semibold">💡 Conseil : </span>{content.conseil}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
          {copywriting.copywriting_principles?.length ? (
            <div className="mt-5 card-sm bg-gradient-to-r from-blue-50 to-purple-50">
              <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
                📐 Principes de copywriting à appliquer à vos campagnes
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {copywriting.copywriting_principles.map((p, i) => (
                  <div key={`mcp-${i}`} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-primary-500 font-bold flex-shrink-0">{i + 1}.</span>{p}
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </section>
      )}
    </div>
  );
}
