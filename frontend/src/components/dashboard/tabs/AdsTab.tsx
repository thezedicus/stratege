'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell } from 'recharts';
import { Target, Megaphone, Layers, Image, TrendingUp, Brain } from 'lucide-react';

interface AdsInput {
  monthlyBudget?: number;
  goal?: string;
  activityType?: string;
}

interface SeaStrategy {
  description: string;
  avantages?: string[];
  conseil?: string;
}

interface AdsTabProps {
  data?: {
    mediaplan?: Array<{
      platform: string;
      budget: number;
      reach: string;
      expectedRoi: string;
      objective?: string;
    }>;
    campaigns?: Array<{
      name: string;
      platform: string;
      type: string;
      budget: number;
      duration?: string;
      targetAudience?: string;
    }>;
    keywords?: string[];
    creatives?: Array<{
      format: string;
      copy?: string;
      cta?: string;
      platform?: string;
    }>;
    retargetingStrategies?: Array<{
      channel: string;
      audience: string;
      message?: string;
    }>;
    examples?: string[];
  };
  geo2025?: {
    sea_ai?: {
      google_ai_max?: SeaStrategy;
      smart_bidding?: SeaStrategy;
      ai_overviews?: SeaStrategy;
      audience_signals?: SeaStrategy;
    };
  };
  input?: AdsInput;
}

const SEA_TABS = [
  { key: 'google_ai_max',    label: 'AI Max',           emoji: '🤖' },
  { key: 'smart_bidding',    label: 'Smart Bidding',    emoji: '🎯' },
  { key: 'ai_overviews',     label: 'AI Overviews',     emoji: '🔍' },
  { key: 'audience_signals', label: 'Audience Signals', emoji: '👥' },
];

const PLATFORM_COLORS: Record<string, string> = {
  'Google Ads':    '#4285F4',
  'Meta Ads':      '#0866FF',
  'Facebook Ads':  '#1877F2',
  'Instagram':     '#E1306C',
  'TikTok Ads':    '#010101',
  'LinkedIn Ads':  '#0077B5',
  'YouTube Ads':   '#FF0000',
  'Twitter Ads':   '#1DA1F2',
  'Pinterest':     '#E60023',
  'Snapchat':      '#FFFC00',
};

const getColor = (platform: string, i: number) =>
  PLATFORM_COLORS[platform] ?? ['#38B6FF', '#E20074', '#8B5CF6', '#10B981', '#F59E0B'][i % 5];

export default function AdsTab({ data, geo2025, input }: AdsTabProps) {
  const [activeSeaTab, setActiveSeaTab] = useState<string>('google_ai_max');

  if (!data) {
    return (
      <div className="flex items-center justify-center py-20 text-gray-400">
        <div className="text-center">
          <Megaphone className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p>Données publicitaires non disponibles</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Media plan */}
      {data.mediaplan?.length ? (
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-6 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary-500" />
            Media Plan
            {input?.monthlyBudget ? (
              <span className="text-sm font-normal text-gray-500 ml-1">
                (budget total : {input.monthlyBudget} €/mois)
              </span>
            ) : null}
          </h2>

          {/* Bar chart */}
          <div style={{ height: 180 }} className="mb-6">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.mediaplan} barCategoryGap="30%">
                <XAxis
                  dataKey="platform"
                  tick={{ fontSize: 11, fill: '#9ca3af' }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis hide />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8, border: '1px solid #f3f4f6' }}
                  formatter={(v: number) => [`${v} €`, 'Budget']}
                />
                <Bar dataKey="budget" radius={[6, 6, 0, 0]}>
                  {data.mediaplan.map((row, i) => (
                    <Cell key={`bar-${row.platform}`} fill={getColor(row.platform, i)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Platform rows */}
          <div className="space-y-3">
            {data.mediaplan.map((row, i) => (
              <div key={`mp-${row.platform}`} className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                <div
                  className="w-3 h-3 rounded-full flex-shrink-0"
                  style={{ backgroundColor: getColor(row.platform, i) }}
                />
                <span className="font-semibold text-gray-900 text-sm w-28 flex-shrink-0 truncate" title={row.platform}>
                  {row.platform}
                </span>
                <span className="text-sm font-bold text-gray-900 w-20">{row.budget} €</span>
                <div className="flex-1 min-w-0 flex flex-wrap gap-2">
                  <span className="badge badge-primary text-xs truncate max-w-[120px]" title={row.reach}>
                    📣 {row.reach}
                  </span>
                  <span className="badge badge-success text-xs">
                    ROI {row.expectedRoi}
                  </span>
                  {row.objective && (
                    <span className="badge badge-gray text-xs truncate max-w-[100px]" title={row.objective}>
                      {row.objective}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Campaigns */}
      {data.campaigns?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-magenta-500" />
            Campagnes recommandées
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.campaigns.map((camp, i) => (
              <div key={`camp-${camp.name}-${i}`} className="card-sm">
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="font-bold text-gray-900 text-sm line-clamp-2 flex-1">{camp.name}</h3>
                  <span className="badge badge-primary text-xs flex-shrink-0">{camp.platform}</span>
                </div>
                <div className="flex flex-wrap gap-2 mb-2">
                  <span className="badge badge-gray text-xs">{camp.type}</span>
                  <span className="badge badge-success text-xs font-bold">{camp.budget} €</span>
                  {camp.duration && (
                    <span className="badge badge-gray text-xs">{camp.duration}</span>
                  )}
                </div>
                {camp.targetAudience && (
                  <p className="text-xs text-gray-500 line-clamp-2">👥 {camp.targetAudience}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Retargeting */}
      {data.retargetingStrategies?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-500" />
            Stratégies de retargeting
          </h2>
          <div className="space-y-3">
            {data.retargetingStrategies.map((strat, i) => (
              <div key={`retarget-${strat.channel}-${i}`} className="card-sm flex items-start gap-4">
                <div className="w-8 h-8 rounded-xl bg-purple-100 flex items-center justify-center flex-shrink-0">
                  <Layers className="w-4 h-4 text-purple-500" />
                </div>
                <div className="min-w-0">
                  <p className="font-semibold text-gray-900 text-sm">{strat.channel}</p>
                  <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">{strat.audience}</p>
                  {strat.message && (
                    <p className="text-xs text-gray-400 mt-1 line-clamp-2 italic">"{strat.message}"</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Creatives */}
      {data.creatives?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Image className="w-5 h-5 text-amber-500" />
            Créatifs recommandés
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.creatives.map((creative, i) => (
              <div key={`creative-${creative.format}-${i}`} className="card-sm">
                <div className="flex items-center gap-2 mb-2">
                  <span className="badge badge-warning text-xs">{creative.format}</span>
                  {creative.platform && (
                    <span className="badge badge-gray text-xs">{creative.platform}</span>
                  )}
                </div>
                {creative.copy && (
                  <p className="text-sm text-gray-700 mb-2 line-clamp-3 italic">"{creative.copy}"</p>
                )}
                {creative.cta && (
                  <span className="inline-flex items-center gap-1 text-xs font-semibold text-primary-600 bg-primary-50 px-2.5 py-1 rounded-full">
                    → {creative.cta}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* Keywords */}
      {data.keywords?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">🔑 Mots-clés publicitaires</h2>
          <div className="flex flex-wrap gap-2">
            {data.keywords.map((kw, i) => (
              <span key={`kw-${i}`} className="badge badge-primary">{kw}</span>
            ))}
          </div>
        </div>
      ) : null}

      {/* Examples */}
      {data.examples?.length ? (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">💡 Exemples d'annonces</h2>
          <div className="space-y-3">
            {data.examples.map((ex, i) => (
              <div key={`example-${i}`} className="card-sm flex items-start gap-3">
                <span className="text-amber-500 font-bold text-sm flex-shrink-0">{i + 1}.</span>
                <p className="text-sm text-gray-700">{ex}</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* ── SEA IA — Google AI 2025 (from geo2025 service) ─────────────────── */}
      {geo2025?.sea_ai && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Brain className="w-5 h-5 text-indigo-500" /> SEA IA — Publicité pilotée par l'IA (2025)
          </h2>
          <p className="text-sm text-gray-500 mb-5">
            Google intègre l'IA à toute sa suite publicitaire. Adoptez ces stratégies pour garder un avantage compétitif.
          </p>
          {/* SEA sub-tabs */}
          <div className="flex gap-2 flex-wrap mb-5">
            {SEA_TABS.map(tab => {
              const hasData = geo2025.sea_ai && (geo2025.sea_ai as Record<string, SeaStrategy | undefined>)[tab.key];
              if (!hasData) return null;
              return (
                <button
                  key={tab.key}
                  onClick={() => setActiveSeaTab(tab.key)}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium transition-all border-2
                    ${activeSeaTab === tab.key
                      ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                      : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'}`}
                >
                  <span>{tab.emoji}</span>{tab.label}
                </button>
              );
            })}
          </div>
          {(() => {
            const seaData = geo2025.sea_ai as Record<string, SeaStrategy | undefined>;
            const current = seaData[activeSeaTab];
            if (!current) return null;
            const tabMeta = SEA_TABS.find(t => t.key === activeSeaTab);
            return (
              <div className="card animate-fade-in">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">{tabMeta?.emoji}</span>
                  <h3 className="font-bold text-gray-900">{tabMeta?.label}</h3>
                </div>
                <p className="text-sm text-gray-700 mb-4 leading-relaxed">{current.description}</p>
                {current.avantages?.length ? (
                  <div className="mb-4">
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Avantages clés</p>
                    <div className="space-y-1.5">
                      {current.avantages.map((av, i) => (
                        <div key={`av-${i}`} className="flex items-start gap-2 text-sm text-gray-700">
                          <span className="text-indigo-500 font-bold flex-shrink-0">✓</span>{av}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : null}
                {current.conseil && (
                  <div className="bg-indigo-50 rounded-xl p-3">
                    <p className="text-sm text-indigo-700">
                      <span className="font-semibold">💡 Conseil pratique : </span>{current.conseil}
                    </p>
                  </div>
                )}
              </div>
            );
          })()}
        </section>
      )}
    </div>
  );
}
