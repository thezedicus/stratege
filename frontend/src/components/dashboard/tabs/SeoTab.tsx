'use client';

import { motion } from 'framer-motion';

type Keyword = { keyword: string; volume: string; difficulty: string; intent: string };
type AuditItem = { item: string; status: 'ok' | 'warning' | 'error'; recommendation: string };
type GoogleAdsCampaign = { campaign: string; keywords: string[]; budget: number; bidStrategy: string };
type TrendingTopic = { topic: string; trend: string };

type SeoData = {
  keywords: Keyword[];
  onPageAudit: AuditItem[];
  geoTips: string[];
  googleAds: GoogleAdsCampaign[];
  trendingTopics: TrendingTopic[];
};

type PagespeedData = {
  performance: number;
  seo: number;
  accessibility: number;
  bestPractices: number;
  lcp: string;
  fid: string;
  cls: string;
};

const STATUS_CONFIG = {
  ok:      { label: 'OK',       cls: 'bg-emerald-100 text-emerald-700', icon: '✅' },
  warning: { label: 'Attention', cls: 'bg-amber-100 text-amber-700',    icon: '⚠️' },
  error:   { label: 'Erreur',    cls: 'bg-red-100 text-red-700',        icon: '❌' },
} as const;

const DIFFICULTY_COLORS: Record<string, string> = {
  Facile: 'bg-emerald-50 text-emerald-600',
  Moyen:  'bg-amber-50 text-amber-600',
  Élevé:  'bg-red-50 text-red-600',
};

/** Circular progress ring — positions score in the center using absolute overlay */
const ScoreRing = ({ score, label, color }: { score: number; label: string; color: string }) => {
  const r = 32;
  const circ = 2 * Math.PI * r;
  const dash = Math.min(1, score / 100) * circ;
  const scoreColor = score >= 75 ? '#10B981' : score >= 50 ? '#F59E0B' : '#EF4444';

  return (
    <div className="flex flex-col items-center gap-2 min-w-[80px]">
      <div className="relative w-[80px] h-[80px]">
        <svg width="80" height="80" viewBox="0 0 80 80" className="-rotate-90">
          <circle cx="40" cy="40" r={r} fill="none" stroke="#f3f4f6" strokeWidth="8" />
          <circle
            cx="40" cy="40" r={r}
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeDasharray={`${dash} ${circ}`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-bold" style={{ color: scoreColor }}>{score}</span>
        </div>
      </div>
      <span className="text-xs text-gray-500 text-center leading-tight">{label}</span>
    </div>
  );
};

export default function SeoTab({ data, pagespeed }: { data?: SeoData; pagespeed?: PagespeedData }) {
  if (!data) return <div className="card text-gray-400 text-center py-12">Données indisponibles</div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">SEO, SEA & GEO</h2>
        <p className="section-subtitle">Audit on-page, mots-clés stratégiques, campagnes Google Ads et optimisation GEO.</p>
      </div>

      {/* PageSpeed */}
      {pagespeed && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-6">⚡ Audit PageSpeed Insights</h3>
          <div className="flex flex-wrap justify-around gap-6 mb-6">
            {[
              { label: 'Performance',     score: pagespeed.performance,    color: '#38B6FF' },
              { label: 'SEO',             score: pagespeed.seo,             color: '#10B981' },
              { label: 'Accessibilité',   score: pagespeed.accessibility,  color: '#8B5CF6' },
              { label: 'Best Practices',  score: pagespeed.bestPractices,  color: '#F59E0B' },
            ].map((item) => (
              <ScoreRing key={item.label} {...item} />
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'LCP',  value: pagespeed.lcp, desc: 'Largest Contentful Paint' },
              { label: 'TBT',  value: pagespeed.fid, desc: 'Total Blocking Time' },
              { label: 'CLS',  value: pagespeed.cls, desc: 'Cumulative Layout Shift' },
            ].map(({ label, value, desc }) => (
              <div key={label} className="p-3 bg-gray-50 rounded-xl text-center">
                <p className="text-xs text-gray-400 mb-1">{desc}</p>
                <p className="font-bold text-gray-900 text-sm">{value}</p>
                <p className="text-xs text-gray-500">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Keywords */}
        {(data.keywords?.length ?? 0) > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">🔑 Mots-clés stratégiques</h3>
            <div className="space-y-1">
              {data.keywords.map((kw, i) => (
                <motion.div
                  key={`kw-${i}`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.04 }}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-50 transition-colors"
                >
                  <div className="flex-1 min-w-0">
                    <span className="font-medium text-sm text-gray-900">{kw.keyword}</span>
                    <span className="ml-2 text-xs text-gray-400">{kw.intent}</span>
                  </div>
                  <span className="badge bg-blue-50 text-blue-600 flex-shrink-0">{kw.volume}</span>
                  <span className={`badge flex-shrink-0 ${DIFFICULTY_COLORS[kw.difficulty] ?? 'bg-gray-100 text-gray-600'}`}>
                    {kw.difficulty}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* On-page audit */}
        {(data.onPageAudit?.length ?? 0) > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">🔍 Audit On-Page</h3>
            <div className="space-y-2">
              {data.onPageAudit.map((item, i) => {
                const cfg = STATUS_CONFIG[item.status] ?? STATUS_CONFIG.warning;
                return (
                  <div key={`audit-${i}`} className="p-3 rounded-xl bg-gray-50">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className="text-sm flex-shrink-0">{cfg.icon}</span>
                      <span className="font-medium text-sm text-gray-800 flex-1">{item.item}</span>
                      <span className={`badge ml-auto ${cfg.cls}`}>{cfg.label}</span>
                    </div>
                    <p className="text-xs text-gray-500 ml-6">{item.recommendation}</p>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* GEO */}
      {(data.geoTips?.length ?? 0) > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-2">🤖 GEO — Generative Engine Optimization</h3>
          <p className="text-sm text-gray-500 mb-4">
            Optimisez votre contenu pour les moteurs génératifs (ChatGPT, Perplexity, Gemini).
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {data.geoTips.map((tip, i) => (
              <div
                key={`geo-${i}`}
                className="p-3 rounded-xl border border-gray-100"
                style={{ background: 'linear-gradient(135deg, #EBF8FF 0%, #F5F3FF 100%)' }}
              >
                <span className="text-sm text-gray-700">✨ {tip}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Google Ads */}
      {(data.googleAds?.length ?? 0) > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">🎯 Structure de campagnes Google Ads</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.googleAds.map((camp, i) => (
              <div key={`camp-${i}`} className="p-4 rounded-xl border border-gray-100 bg-gray-50">
                <div className="flex items-center justify-between mb-2 gap-2 flex-wrap">
                  <h4 className="font-semibold text-sm text-gray-900">{camp.campaign}</h4>
                  <span className="badge-primary">{camp.budget} €/mois</span>
                </div>
                <p className="text-xs text-gray-500 mb-3">Stratégie : {camp.bidStrategy}</p>
                <div className="flex flex-wrap gap-1">
                  {(camp.keywords ?? []).map((kw, j) => (
                    <span key={`ck-${j}`} className="text-xs bg-white border border-gray-200 text-gray-600 px-2 py-0.5 rounded-lg">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Trending topics */}
      {(data.trendingTopics?.length ?? 0) > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">📈 Tendances secteur</h3>
          <div className="flex flex-wrap gap-3">
            {data.trendingTopics.map((t, i) => (
              <div key={`trend-${i}`} className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-xl border border-gray-100">
                <span className="text-sm font-medium text-gray-800">{t.topic}</span>
                <span className={`text-sm font-bold ${
                  t.trend === 'hausse' ? 'text-emerald-500' :
                  t.trend === 'stable' ? 'text-amber-500' : 'text-red-500'
                }`}>
                  {t.trend === 'hausse' ? '↑' : t.trend === 'stable' ? '→' : '↓'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
