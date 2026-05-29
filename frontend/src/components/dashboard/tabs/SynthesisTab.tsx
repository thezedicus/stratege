'use client';

import {
  LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip, Legend,
} from 'recharts';
import { Star, Target, TrendingUp, CheckCircle2, BarChart2 } from 'lucide-react';

interface RoiPoint { month: number; pessimistic: number; realistic: number; optimistic: number; }

interface SynthesisTabProps {
  data?: {
    synthesis?: {
      score?: number;
      summary?: string;
      priorities?: string[];
      keyMetrics?: Record<string, string | number>;
      actionPlan?: Array<{
        action: string;
        priority: 'haute' | 'moyenne' | 'faible' | string;
        timeline: string;
        expectedResult?: string;
      }>;
      monthlyMilestones?: Array<{
        month: string | number;
        objective: string;
        kpi?: string;
      }>;
      roi?: RoiPoint[];
      nextSteps?: string[];
    };
  };
}

const PRIORITY_BADGE: Record<string, string> = {
  haute:   'badge-danger',
  moyenne: 'badge-warning',
  faible:  'badge-gray',
  high:    'badge-danger',
  medium:  'badge-warning',
  low:     'badge-gray',
};

const SCORE_COLOR = (s: number) =>
  s >= 70 ? '#22c55e' : s >= 50 ? '#f59e0b' : '#ef4444';

export default function SynthesisTab({ data }: SynthesisTabProps) {
  const synthesis = data?.synthesis;

  if (!synthesis) {
    return (
      <div className="flex items-center justify-center py-20 text-gray-400">
        <div className="text-center">
          <BarChart2 className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p>Synthèse non disponible</p>
        </div>
      </div>
    );
  }

  const score = synthesis.score ?? 0;
  const metricsArr = synthesis.keyMetrics
    ? Object.entries(synthesis.keyMetrics).map(([k, v]) => ({ name: k, raw: v }))
    : [];

  return (
    <div className="space-y-8">
      {/* Score + summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="card text-center">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Score stratégique</p>
          <div className="relative w-28 h-28 mx-auto mb-3">
            <svg viewBox="0 0 112 112" className="w-28 h-28 -rotate-90">
              <circle cx="56" cy="56" r="46" fill="none" stroke="#f3f4f6" strokeWidth="8" />
              <circle
                cx="56" cy="56" r="46"
                fill="none"
                stroke={SCORE_COLOR(score)}
                strokeWidth="8"
                strokeDasharray={`${(score / 100) * 289} 289`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold text-gray-900">{score}</span>
              <span className="text-xs text-gray-400">/100</span>
            </div>
          </div>
          <p className="text-sm font-medium text-gray-700">
            {score >= 70 ? '🚀 Excellent potentiel' : score >= 50 ? '✅ Bon potentiel' : '⚠️ À optimiser'}
          </p>
        </div>

        {synthesis.summary && (
          <div className="card sm:col-span-2">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Résumé stratégique</p>
            <p className="text-gray-700 leading-relaxed text-sm">{synthesis.summary}</p>
            {synthesis.priorities?.length ? (
              <div className="mt-4 space-y-1.5">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Priorités</p>
                {synthesis.priorities.map((p, i) => (
                  <div key={`priority-${i}`} className="flex items-center gap-2 text-sm text-gray-600">
                    <CheckCircle2 className="w-3.5 h-3.5 text-primary-500 flex-shrink-0" />
                    {p}
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        )}
      </div>

      {/* Key Metrics */}
      {metricsArr.length > 0 && (
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary-500" />
            Métriques clés (mois 1)
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {metricsArr.slice(0, 4).map(({ name, raw }) => (
              <div key={`metric-${name}`} className="text-center p-4 bg-gray-50 rounded-xl">
                <p className="text-xl font-bold text-gray-900">{raw}</p>
                <p className="text-xs text-gray-500 mt-1 leading-tight">{name}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ROI projection */}
      {synthesis.roi?.length ? (
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-500" />
            Projection ROI cumulatif sur 12 mois (€)
          </h2>
          <div style={{ height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={synthesis.roi} margin={{ top: 4, right: 8, bottom: 0, left: 0 }}>
                <XAxis
                  dataKey="month"
                  tick={{ fontSize: 11, fill: '#9ca3af' }}
                  axisLine={false} tickLine={false}
                  tickFormatter={(v) => `M${v}`}
                />
                <YAxis
                  tick={{ fontSize: 10, fill: '#9ca3af' }}
                  axisLine={false} tickLine={false}
                  tickFormatter={(v) => v >= 1000 ? `${(v/1000).toFixed(0)}k€` : `${v}€`}
                  width={44}
                />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8, border: '1px solid #f3f4f6' }}
                  formatter={(v: number) => [`${v.toLocaleString('fr-FR')} €`]}
                  labelFormatter={(l) => `Mois ${l}`}
                />
                <Legend iconSize={10} wrapperStyle={{ fontSize: 11 }} />
                <Line type="monotone" dataKey="pessimistic" name="Pessimiste" stroke="#ef4444" strokeWidth={1.5} dot={false} strokeDasharray="4 2" />
                <Line type="monotone" dataKey="realistic"   name="Réaliste"   stroke="#38B6FF" strokeWidth={2}   dot={false} />
                <Line type="monotone" dataKey="optimistic"  name="Optimiste"  stroke="#22c55e" strokeWidth={1.5} dot={false} strokeDasharray="4 2" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      ) : null}

      {/* Action plan */}
      {synthesis.actionPlan?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-primary-500" />
            Plan d&apos;action 90 jours
          </h2>
          <div className="space-y-3">
            {synthesis.actionPlan.map((action, i) => (
              <div
                key={`action-${i}`}
                className="card-sm flex items-start gap-4 animate-fade-in"
                style={{ animationDelay: `${i * 40}ms` }}
              >
                <div className="w-8 h-8 rounded-xl bg-gradient-primary flex items-center justify-center flex-shrink-0 text-white font-bold text-xs">
                  {i + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-3 mb-1 flex-wrap">
                    <p className="font-semibold text-gray-900 text-sm flex-1">{action.action}</p>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className={`badge ${PRIORITY_BADGE[action.priority] ?? 'badge-gray'}`}>
                        {action.priority}
                      </span>
                      <span className="badge badge-gray">{action.timeline}</span>
                    </div>
                  </div>
                  {action.expectedResult && (
                    <p className="text-xs text-gray-500">{action.expectedResult}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Monthly milestones */}
      {synthesis.monthlyMilestones?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-amber-500" />
            Jalons mensuels
          </h2>
          <div className="relative">
            <div className="absolute left-5 top-0 bottom-0 w-0.5 bg-gray-100" />
            <div className="space-y-4 pl-12">
              {synthesis.monthlyMilestones.map((m, i) => (
                <div key={`milestone-${m.month}-${i}`} className="relative animate-fade-in"
                  style={{ animationDelay: `${i * 60}ms` }}>
                  <div className="absolute -left-7 w-4 h-4 rounded-full bg-gradient-primary border-2 border-white" />
                  <div className="card-sm">
                    <p className="text-xs font-semibold text-primary-500 mb-1">Mois {m.month}</p>
                    <p className="font-medium text-gray-900 text-sm">{m.objective}</p>
                    {m.kpi && <p className="text-xs text-gray-400 mt-1">KPI : {m.kpi}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : null}

      {/* Next steps */}
      {synthesis.nextSteps?.length ? (
        <div className="card" style={{ background: 'linear-gradient(135deg,#F0F9FF,#FFF0F7)' }}>
          <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-500" />
            Prochaines étapes immédiates
          </h2>
          <ol className="space-y-3">
            {synthesis.nextSteps.map((step, i) => (
              <li key={`step-${i}`} className="flex items-start gap-3 text-sm text-gray-700">
                <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                  {i + 1}
                </span>
                {step}
              </li>
            ))}
          </ol>
        </div>
      ) : null}
    </div>
  );
}
