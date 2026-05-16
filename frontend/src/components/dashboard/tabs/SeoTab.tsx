'use client';

import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

type SeoData = {
  keywords: { keyword: string; volume: string; difficulty: string; intent: string }[];
  onPageAudit: { item: string; status: 'ok' | 'warning' | 'error'; recommendation: string }[];
  geoTips: string[];
  googleAds: { campaign: string; keywords: string[]; budget: number; bidStrategy: string }[];
  trendingTopics: { topic: string; trend: string }[];
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

const statusConfig = {
  ok: { label: 'OK', cls: 'bg-emerald-100 text-emerald-700', icon: '✅' },
  warning: { label: 'Attention', cls: 'bg-amber-100 text-amber-700', icon: '⚠️' },
  error: { label: 'Erreur', cls: 'bg-red-100 text-red-700', icon: '❌' },
};

const ScoreRing = ({ score, label, color }: { score: number; label: string; color: string }) => {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="90" height="90" className="-rotate-90">
        <circle cx="45" cy="45" r={r} fill="none" stroke="#f3f4f6" strokeWidth="8" />
        <circle cx="45" cy="45" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" />
      </svg>
      <div className="text-center -mt-14">
        <span className="text-xl font-bold text-gray-900">{score}</span>
      </div>
      <span className="text-xs text-gray-500 mt-8">{label}</span>
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

      {/* PageSpeed scores */}
      {pagespeed && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-6">⚡ Audit PageSpeed Insights</h3>
          <div className="flex flex-wrap justify-around gap-4 mb-6">
            {[
              { label: 'Performance', score: pagespeed.performance, color: '#38B6FF' },
              { label: 'SEO', score: pagespeed.seo, color: '#10B981' },
              { label: 'Accessibilité', score: pagespeed.accessibility, color: '#8B5CF6' },
              { label: 'Best Practices', score: pagespeed.bestPractices, color: '#F59E0B' },
            ].map((item) => (
              <ScoreRing key={item.label} {...item} />
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'LCP', value: pagespeed.lcp, desc: 'Largest Contentful Paint' },
              { label: 'FID', value: pagespeed.fid, desc: 'First Input Delay' },
              { label: 'CLS', value: pagespeed.cls, desc: 'Cumulative Layout Shift' },
            ].map(({ label, value, desc }) => (
              <div key={label} className="p-3 bg-gray-50 rounded-xl text-center">
                <p className="text-xs text-gray-400 mb-1">{desc}</p>
                <p className="font-bold text-gray-900">{value}</p>
                <p className="text-xs text-gray-500">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Keywords */}
        {data.keywords?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">🔑 Mots-clés stratégiques</h3>
            <div className="space-y-2">
              {data.keywords.map((kw, i) => (
                <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
                  className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-gray-50 transition-colors">
                  <div className="flex-1">
                    <span className="font-medium text-sm text-gray-900">{kw.keyword}</span>
                    <span className="ml-2 text-xs text-gray-400">{kw.intent}</span>
                  </div>
                  <span className="badge bg-blue-50 text-blue-600 text-xs">{kw.volume}</span>
                  <span className={`badge text-xs ${kw.difficulty === 'Facile' ? 'badge-success' : kw.difficulty === 'Moyen' ? 'badge-warning' : 'bg-red-50 text-red-600 badge'}`}>
                    {kw.difficulty}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* On-page audit */}
        {data.onPageAudit?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">🔍 Audit On-Page</h3>
            <div className="space-y-2">
              {data.onPageAudit.map((item, i) => {
                const cfg = statusConfig[item.status];
                return (
                  <div key={i} className="p-3 rounded-xl bg-gray-50">
                    <div className="flex items-center gap-2 mb-1">
                      <span>{cfg.icon}</span>
                      <span className="font-medium text-sm text-gray-800">{item.item}</span>
                      <span className={`badge text-xs ml-auto ${cfg.cls}`}>{cfg.label}</span>
                    </div>
                    <p className="text-xs text-gray-500 ml-6">{item.recommendation}</p>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* GEO tips */}
      {data.geoTips?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">🤖 GEO — Generative Engine Optimization</h3>
          <p className="text-sm text-gray-500 mb-4">Optimisez votre contenu pour les moteurs de recherche génératifs (ChatGPT, Perplexity, Gemini).</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {data.geoTips.map((tip, i) => (
              <div key={i} className="p-3 rounded-xl bg-gradient-to-br from-primary-50 to-violet-50 border border-gray-100">
                <span className="text-sm text-gray-700">✨ {tip}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Google Ads campaigns */}
      {data.googleAds?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">🎯 Structure de campagnes Google Ads</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.googleAds.map((camp, i) => (
              <div key={i} className="p-4 rounded-xl border border-gray-100 bg-gray-50">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-sm text-gray-900">{camp.campaign}</h4>
                  <span className="badge-primary text-xs">{camp.budget} €/mois</span>
                </div>
                <p className="text-xs text-gray-500 mb-2">Stratégie : {camp.bidStrategy}</p>
                <div className="flex flex-wrap gap-1">
                  {camp.keywords.map((kw, j) => (
                    <span key={j} className="text-xs bg-white border border-gray-200 text-gray-600 px-2 py-0.5 rounded-lg">{kw}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Trending topics */}
      {data.trendingTopics?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">📈 Tendances Google (secteur)</h3>
          <div className="flex flex-wrap gap-3">
            {data.trendingTopics.map((t, i) => (
              <div key={i} className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-xl border border-gray-100">
                <span className="text-sm font-medium text-gray-800">{t.topic}</span>
                <span className={`text-xs font-medium ${t.trend === 'hausse' ? 'text-emerald-500' : t.trend === 'stable' ? 'text-amber-500' : 'text-red-500'}`}>
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
