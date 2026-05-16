'use client';

import { useState } from 'react';
import { TrendingUp, Search, Globe, Zap, AlertCircle, CheckCircle2, XCircle, Layers, ChevronDown } from 'lucide-react';

interface SeoTabProps {
  data?: {
    keywords?: Array<{ keyword: string; volume: string; difficulty: string; intent: string; priority?: string }>;
    technicalAudit?: Array<{ item: string; status: 'ok' | 'warning' | 'error'; recommendation?: string }>;
    geoStrategy?: Array<{ platform: string; action: string; priority?: string }>;
    contentStrategy?: { pillars?: string[]; frequency?: string; formats?: string[] };
    trends?: Array<{ trend: string; relevance?: string }>;
  };
  geo2025?: {
    stat_2025?: string;
    methodology_description?: string;
    authority_topics?: string[];
    content_clusters?: Array<{ pilier: string; clusters: string[] }>;
    geo_optimizations?: Array<{ action: string; impact: string }>;
    ai_search_tips?: string[];
    sea_ai?: {
      google_ai_max?: { description: string; avantages: string[]; quand_utiliser: string; conseil: string };
      smart_bidding?: { description: string; strategies: Array<{ nom: string; usage: string }>; conseil: string };
      ai_overviews?: { description: string; impact: string; opportunites: string[]; conseil: string };
      audience_signals?: { description: string; types: string[]; conseil: string };
    };
    priority_actions?: string[];
  };
  pagespeed?: {
    performance: number; seo: number; accessibility: number; bestPractices: number;
    lcp: string; fid: string; cls: string;
  };
}

const SCORE_COLOR = (s: number) => s >= 75 ? '#22c55e' : s >= 50 ? '#f59e0b' : '#ef4444';
const DIFF_BADGE: Record<string, string> = { faible: 'badge-success', moyen: 'badge-warning', élevé: 'badge-danger', easy: 'badge-success', medium: 'badge-warning', hard: 'badge-danger' };
const STATUS_ICON = {
  ok:      <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />,
  warning: <AlertCircle   className="w-4 h-4 text-amber-500 flex-shrink-0" />,
  error:   <XCircle       className="w-4 h-4 text-red-500 flex-shrink-0" />,
};
const IMPACT_COLOR: Record<string, string> = {
  'très élevé': 'badge-danger',
  'élevé':      'badge-warning',
  'moyen':      'badge-gray',
};

function ScoreRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 22; const circ = 2 * Math.PI * r; const dash = (score / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative w-14 h-14">
        <svg viewBox="0 0 56 56" className="w-14 h-14 -rotate-90">
          <circle cx="28" cy="28" r={r} fill="none" stroke="#f3f4f6" strokeWidth="5" />
          <circle cx="28" cy="28" r={r} fill="none" stroke={color} strokeWidth="5"
            strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-gray-900">{score}</span>
      </div>
      <span className="text-xs text-gray-500 text-center">{label}</span>
    </div>
  );
}

export default function SeoTab({ data, geo2025, pagespeed }: SeoTabProps) {
  const [expandedCluster, setExpandedCluster] = useState<number | null>(null);
  const [activeSeaTab, setActiveSeaTab] = useState<string>('google_ai_max');

  return (
    <div className="space-y-10">

      {/* ── PageSpeed ──────────────────────────────────────────────────────── */}
      {pagespeed && (
        <section className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" /> Scores PageSpeed (mobile)
          </h2>
          <div className="flex flex-wrap gap-6 justify-around mb-6">
            {[
              { s: pagespeed.performance,   l: 'Performance' },
              { s: pagespeed.seo,           l: 'SEO' },
              { s: pagespeed.accessibility, l: 'Accessibilité' },
              { s: pagespeed.bestPractices, l: 'Bonnes pratiques' },
            ].map(({ s, l }) => <ScoreRing key={l} score={s} label={l} color={SCORE_COLOR(s)} />)}
          </div>
          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-100">
            {[{ label: 'LCP', value: pagespeed.lcp, tip: 'Largest Contentful Paint' },
              { label: 'TBT', value: pagespeed.fid, tip: 'Total Blocking Time' },
              { label: 'CLS', value: pagespeed.cls, tip: 'Cumulative Layout Shift' }].map(({ label, value, tip }) => (
              <div key={label} className="text-center" title={tip}>
                <p className="text-lg font-bold text-gray-900">{value}</p>
                <p className="text-xs text-gray-400">{label}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ── GEO 2025 ───────────────────────────────────────────────────────── */}
      {geo2025 && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Globe className="w-5 h-5 text-primary-500" /> SEO & GEO 2025 — Autorité thématique
          </h2>
          {geo2025.stat_2025 && (
            <div className="mb-4 px-4 py-3 bg-primary-50 border border-primary-100 rounded-xl">
              <p className="text-sm font-semibold text-primary-700">📊 Stat clé 2025 : {geo2025.stat_2025}</p>
            </div>
          )}
          <p className="text-sm text-gray-500 mb-6">
            {geo2025.methodology_description ?? "En SEO 2025, la priorité est donnée à l'autorité thématique via des contenus piliers et des clusters, à l'intention de recherche et à l'optimisation pour les moteurs de réponse IA (GEO)."}
          </p>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Authority topics */}
            {geo2025.authority_topics?.length ? (
              <div className="card-sm">
                <p className="text-xs font-bold text-primary-600 uppercase tracking-wider mb-3">🏛️ Sujets d'autorité thématique</p>
                <ul className="space-y-2.5">
                  {geo2025.authority_topics.map((t, i) => (
                    <li key={`at-${i}`} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-primary-500 mt-2 flex-shrink-0" />{t}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
            {/* AI Search tips */}
            {geo2025.ai_search_tips?.length ? (
              <div className="card-sm bg-gradient-to-br from-primary-50 to-purple-50">
                <p className="text-xs font-bold text-purple-600 uppercase tracking-wider mb-3">🤖 Optimisation pour l'IA (GEO)</p>
                <ul className="space-y-2.5">
                  {geo2025.ai_search_tips.map((t, i) => (
                    <li key={`ai-${i}`} className="flex items-start gap-2 text-sm text-purple-700">
                      <span className="flex-shrink-0 mt-0.5">→</span>{t}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>

          {/* GEO optimizations */}
          {geo2025.geo_optimizations?.length ? (
            <div className="mb-6">
              <p className="text-sm font-bold text-gray-700 mb-3">⚡ Actions GEO prioritaires</p>
              <div className="space-y-2">
                {geo2025.geo_optimizations.map((opt, i) => (
                  <div key={`geo-opt-${i}`} className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl text-sm">
                    <span className={`badge flex-shrink-0 ${IMPACT_COLOR[opt.impact] ?? 'badge-gray'}`}>{opt.impact}</span>
                    <span className="text-gray-700">{opt.action}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          {/* Content clusters */}
          {geo2025.content_clusters?.length ? (
            <div>
              <p className="text-sm font-bold text-gray-700 mb-3">🕸️ Clusters de contenu recommandés</p>
              <div className="space-y-3">
                {geo2025.content_clusters.map((cluster, i) => (
                  <div key={`cluster-${i}`} className="card-sm overflow-hidden">
                    <button onClick={() => setExpandedCluster(expandedCluster === i ? null : i)}
                      className="w-full flex items-center justify-between text-left">
                      <span className="font-semibold text-gray-900 text-sm">📌 {cluster.pilier}</span>
                      <ChevronDown className={`w-4 h-4 text-gray-400 flex-shrink-0 transition-transform ${expandedCluster === i ? 'rotate-180' : ''}`} />
                    </button>
                    {expandedCluster === i && (
                      <div className="mt-3 pt-3 border-t border-gray-100 flex flex-wrap gap-2 animate-fade-in">
                        {cluster.clusters.map((c, j) => (
                          <span key={`cl-${i}-${j}`} className="badge badge-primary text-xs">{c}</span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          {/* Priority actions */}
          {geo2025.priority_actions?.length ? (
            <div className="mt-5 card bg-emerald-50 border-emerald-100">
              <p className="text-xs font-bold text-emerald-600 uppercase tracking-wider mb-3">✅ Plan d'action prioritaire SEO</p>
              <ol className="space-y-2">
                {geo2025.priority_actions.map((a, i) => (
                  <li key={`pa-${i}`} className="flex items-start gap-2 text-sm text-emerald-800">
                    <span className="w-5 h-5 rounded-full bg-emerald-500 text-white text-xs flex items-center justify-center flex-shrink-0 font-bold mt-0.5">{i + 1}</span>{a}
                  </li>
                ))}
              </ol>
            </div>
          ) : null}
        </section>
      )}

      {/* ── SEA / Google Ads IA ────────────────────────────────────────────── */}
      {geo2025?.sea_ai && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" /> SEA & Google Ads IA 2025
          </h2>
          <p className="text-sm text-gray-500 mb-5">
            Le SEA 2025 s'appuie sur l'IA Max, le Smart Bidding et les annonces dans les AI Overviews pour capter l'intention d'achat avec une précision accrue.
          </p>
          <div className="flex gap-2 mb-5 overflow-x-auto scrollbar-hide">
            {Object.keys(geo2025.sea_ai).map(key => (
              <button key={key}
                onClick={() => setActiveSeaTab(key)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all border-2
                  ${activeSeaTab === key ? 'border-primary-500 bg-primary-50 text-primary-700' : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'}`}>
                {key === 'google_ai_max' ? '🤖 AI Max' : key === 'smart_bidding' ? '💰 Smart Bidding' : key === 'ai_overviews' ? '🔍 AI Overviews' : '🎯 Audience Signals'}
              </button>
            ))}
          </div>

          {activeSeaTab === 'google_ai_max' && geo2025.sea_ai.google_ai_max && (() => {
            const s = geo2025.sea_ai!.google_ai_max!;
            return (
              <div className="card animate-fade-in">
                <h3 className="font-bold text-gray-900 mb-2">🤖 Performance Max avec IA Max</h3>
                <p className="text-sm text-gray-600 mb-4">{s.description}</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                  <div><p className="text-xs font-bold text-gray-500 mb-2">Avantages</p>
                    <ul className="space-y-1.5">{s.avantages.map((a, i) => <li key={i} className="flex gap-2 text-xs text-gray-600"><span className="text-emerald-500">✓</span>{a}</li>)}</ul>
                  </div>
                  <div>
                    <div className="bg-amber-50 rounded-xl p-3 mb-3"><p className="text-xs font-semibold text-amber-600 mb-1">⏰ Quand l'utiliser</p><p className="text-xs text-amber-700">{s.quand_utiliser}</p></div>
                    <div className="bg-primary-50 rounded-xl p-3"><p className="text-xs font-semibold text-primary-600 mb-1">💡 Conseil</p><p className="text-xs text-primary-700">{s.conseil}</p></div>
                  </div>
                </div>
              </div>
            );
          })()}
          {activeSeaTab === 'smart_bidding' && geo2025.sea_ai.smart_bidding && (() => {
            const s = geo2025.sea_ai!.smart_bidding!;
            return (
              <div className="card animate-fade-in">
                <h3 className="font-bold text-gray-900 mb-2">💰 Smart Bidding</h3>
                <p className="text-sm text-gray-600 mb-4">{s.description}</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
                  {s.strategies.map(strat => (
                    <div key={strat.nom} className="bg-gray-50 rounded-xl p-3">
                      <p className="font-semibold text-gray-900 text-sm">{strat.nom}</p>
                      <p className="text-xs text-gray-500 mt-1">{strat.usage}</p>
                    </div>
                  ))}
                </div>
                <div className="bg-primary-50 rounded-xl p-3"><p className="text-xs text-primary-700"><span className="font-bold">💡 </span>{s.conseil}</p></div>
              </div>
            );
          })()}
          {activeSeaTab === 'ai_overviews' && geo2025.sea_ai.ai_overviews && (() => {
            const s = geo2025.sea_ai!.ai_overviews!;
            return (
              <div className="card animate-fade-in">
                <h3 className="font-bold text-gray-900 mb-2">🔍 Google AI Overviews</h3>
                <p className="text-sm text-gray-600 mb-2">{s.description}</p>
                <div className="bg-amber-50 rounded-xl p-3 mb-4"><p className="text-xs text-amber-700"><span className="font-bold">Impact : </span>{s.impact}</p></div>
                <div><p className="text-xs font-bold text-gray-500 mb-2">Opportunités</p>
                  <ul className="space-y-2">{s.opportunites.map((o, i) => <li key={i} className="flex gap-2 text-sm text-gray-600"><span className="text-primary-500">→</span>{o}</li>)}</ul>
                </div>
                <div className="mt-3 bg-primary-50 rounded-xl p-3"><p className="text-xs text-primary-700"><span className="font-bold">💡 </span>{s.conseil}</p></div>
              </div>
            );
          })()}
          {activeSeaTab === 'audience_signals' && geo2025.sea_ai.audience_signals && (() => {
            const s = geo2025.sea_ai!.audience_signals!;
            return (
              <div className="card animate-fade-in">
                <h3 className="font-bold text-gray-900 mb-2">🎯 Signaux d'audience</h3>
                <p className="text-sm text-gray-600 mb-4">{s.description}</p>
                <ul className="space-y-2 mb-4">{s.types.map((t, i) => <li key={i} className="flex gap-2 text-sm text-gray-600"><span className="text-emerald-500">✓</span>{t}</li>)}</ul>
                <div className="bg-primary-50 rounded-xl p-3"><p className="text-xs text-primary-700"><span className="font-bold">💡 </span>{s.conseil}</p></div>
              </div>
            );
          })()}
        </section>
      )}

      {/* ── Mots-clés ──────────────────────────────────────────────────────── */}
      {data?.keywords?.length ? (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-primary-500" /> Mots-clés prioritaires
          </h2>
          <div className="overflow-x-auto rounded-2xl border border-gray-100">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>{['Mot-clé','Volume','Difficulté','Intention','Priorité'].map(h => (
                  <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">{h}</th>
                ))}</tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {data.keywords.map((kw, i) => (
                  <tr key={`kw-${i}-${kw.keyword}`} className="bg-white hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 font-medium text-gray-900 max-w-[180px] truncate" title={kw.keyword}>{kw.keyword}</td>
                    <td className="px-4 py-3 text-gray-500">{kw.volume}</td>
                    <td className="px-4 py-3"><span className={`badge ${DIFF_BADGE[kw.difficulty?.toLowerCase()] ?? 'badge-gray'}`}>{kw.difficulty}</span></td>
                    <td className="px-4 py-3 text-gray-500 capitalize">{kw.intent}</td>
                    <td className="px-4 py-3">{kw.priority && <span className={`badge ${kw.priority === 'haute' || kw.priority === 'high' ? 'badge-danger' : 'badge-gray'}`}>{kw.priority}</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ) : null}

      {/* ── Audit technique ────────────────────────────────────────────────── */}
      {data?.technicalAudit?.length ? (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-amber-500" /> Audit technique
          </h2>
          <div className="space-y-3">
            {data.technicalAudit.map((audit, i) => (
              <div key={`audit-${i}-${audit.item.slice(0,15)}`} className="card-sm flex items-start gap-3">
                {STATUS_ICON[audit.status]}
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 text-sm">{audit.item}</p>
                  {audit.recommendation && <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">{audit.recommendation}</p>}
                </div>
              </div>
            ))}
          </div>
        </section>
      ) : null}

      {/* ── Content strategy ───────────────────────────────────────────────── */}
      {data?.contentStrategy && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-500" /> Stratégie de contenu
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {data.contentStrategy.pillars?.length ? (
              <div className="card-sm sm:col-span-2">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Piliers de contenu</p>
                <ul className="space-y-2">{data.contentStrategy.pillars.map((p, i) => (
                  <li key={`pillar-${i}`} className="flex items-center gap-2 text-sm text-gray-700">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary-500 flex-shrink-0" />{p}
                  </li>
                ))}</ul>
              </div>
            ) : null}
            <div className="space-y-3">
              {data.contentStrategy.frequency && (
                <div className="card-sm"><p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Fréquence</p><p className="font-semibold text-gray-900 text-sm">{data.contentStrategy.frequency}</p></div>
              )}
              {data.contentStrategy.formats?.length ? (
                <div className="card-sm"><p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Formats</p>
                  <div className="flex flex-wrap gap-1.5">{data.contentStrategy.formats.map(f => <span key={f} className="badge badge-primary text-xs">{f}</span>)}</div>
                </div>
              ) : null}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
