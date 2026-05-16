'use client';

import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

type AdCreative = { format: string; headline: string; description: string; cta: string; audience: string };
type AdsData = {
  facebook: { campaigns: { name: string; objective: string; budget: number; format: string; creatives: AdCreative[] }[] };
  google: { campaigns: { name: string; type: string; budget: number; keywords: string[] }[] };
  organic: { strategies: { channel: string; tactic: string; frequency: string; examples: string[] }[] };
  mediaplan: { platform: string; budget: number; reach: string; expectedCtr: string; expectedRoi: string }[];
};

export default function AdsTab({ data, input }: { data?: AdsData; input?: any }) {
  if (!data) return <div className="card text-gray-400 text-center py-12">Données indisponibles</div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Publicité Payante & Organique</h2>
        <p className="section-subtitle">Media plan Facebook/Instagram Ads, Google Ads et stratégies organiques personnalisées.</p>
      </div>

      {/* Media plan overview */}
      {data.mediaplan?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">📊 Media Plan — Vue d'ensemble</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  {['Plateforme', 'Budget/mois', 'Portée estimée', 'CTR prévu', 'ROI estimé'].map(h => (
                    <th key={h} className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.mediaplan.map((row, i) => (
                  <tr key={row.platform} className={`border-b border-gray-50 ${i % 2 === 0 ? 'bg-gray-50/50' : ''}`}>
                    <td className="py-3 px-4 font-medium text-gray-900">{row.platform}</td>
                    <td className="py-3 px-4"><span className="badge-primary">{row.budget} €</span></td>
                    <td className="py-3 px-4 text-gray-600">{row.reach}</td>
                    <td className="py-3 px-4 text-emerald-600 font-medium">{row.expectedCtr}</td>
                    <td className="py-3 px-4"><span className="badge-success">{row.expectedRoi}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-6 h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.mediaplan} margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                <XAxis dataKey="platform" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(v) => [`${v} €`, 'Budget']} />
                <Bar dataKey="budget" fill="#38B6FF" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Facebook/Instagram Ads */}
      {data.facebook?.campaigns?.length > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">📘 Facebook & Instagram Ads</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {data.facebook.campaigns.map((camp, i) => (
              <motion.div key={camp.name} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="card">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-900">{camp.name}</h4>
                  <span className="badge-primary text-xs">{camp.budget} €/mois</span>
                </div>
                <div className="flex gap-2 mb-4">
                  <span className="badge bg-blue-50 text-blue-600 text-xs">{camp.objective}</span>
                  <span className="badge bg-violet-50 text-violet-600 text-xs">{camp.format}</span>
                </div>
                {camp.creatives?.map((creative, j) => (
                  <div key={`${creative.format}-${j}`} className="p-3 bg-gray-50 rounded-xl mb-2 last:mb-0">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="badge text-xs bg-gray-200 text-gray-600">{creative.format}</span>
                      <span className="text-xs text-gray-400">→ {creative.audience}</span>
                    </div>
                    <p className="font-medium text-sm text-gray-900 mb-1">{creative.headline}</p>
                    <p className="text-xs text-gray-600 mb-2">{creative.description}</p>
                    <span className="inline-block px-3 py-1 bg-primary-500 text-white text-xs font-medium rounded-lg">{creative.cta}</span>
                  </div>
                ))}
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Google Ads */}
      {data.google?.campaigns?.length > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">🔴 Google Ads</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.google.campaigns.map((camp, i) => (
              <div key={camp.name} className="card">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-sm text-gray-900">{camp.name}</h4>
                  <span className="badge-magenta text-xs">{camp.budget} €</span>
                </div>
                <span className="badge bg-gray-100 text-gray-600 text-xs mb-3">{camp.type}</span>
                <div className="flex flex-wrap gap-1">
                  {camp.keywords.map((kw) => (
                    <span key={kw} className="text-xs bg-white border border-gray-200 text-gray-600 px-2 py-0.5 rounded-lg">{kw}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Organic strategies */}
      {data.organic?.strategies?.length > 0 && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-4">🌱 Stratégies Organiques</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.organic.strategies.map((strat) => (
              <div key={strat.channel} className="card">
                <div className="flex items-center gap-2 mb-3">
                  <h4 className="font-semibold text-gray-900">{strat.channel}</h4>
                  <span className="badge bg-emerald-50 text-emerald-600 text-xs">{strat.frequency}</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{strat.tactic}</p>
                <ul className="space-y-1">
                  {strat.examples.map((ex) => (
                    <li key={ex} className="text-xs text-gray-500 flex items-start gap-1.5">
                      <span className="text-primary-500 mt-0.5">•</span>{ex}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
