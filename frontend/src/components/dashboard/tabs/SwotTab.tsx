'use client';

import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Zap, AlertTriangle } from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts';

type SwotData = {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
  score: { innovation: number; market: number; budget: number; maturity: number; digital: number };
};

const quadrants = [
  { key: 'strengths', label: 'Forces', icon: TrendingUp, cls: 'swot-strength', color: 'text-green-700', badge: 'bg-green-100 text-green-700' },
  { key: 'weaknesses', label: 'Faiblesses', icon: TrendingDown, cls: 'swot-weakness', color: 'text-amber-700', badge: 'bg-amber-100 text-amber-700' },
  { key: 'opportunities', label: 'Opportunités', icon: Zap, cls: 'swot-opportunity', color: 'text-blue-700', badge: 'bg-blue-100 text-blue-700' },
  { key: 'threats', label: 'Menaces', icon: AlertTriangle, cls: 'swot-threat', color: 'text-red-700', badge: 'bg-red-100 text-red-700' },
];

export default function SwotTab({ data, input }: { data?: SwotData; input?: any }) {
  if (!data) return <div className="card text-gray-400 text-center py-12">Données indisponibles</div>;

  const radarData = data.score ? [
    { subject: 'Innovation', A: data.score.innovation },
    { subject: 'Marché', A: data.score.market },
    { subject: 'Budget', A: data.score.budget },
    { subject: 'Maturité', A: data.score.maturity },
    { subject: 'Digital', A: data.score.digital },
  ] : [];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Diagnostic Stratégique</h2>
        <p className="section-subtitle">Analyse SWOT personnalisée basée sur votre secteur, budget et maturité de projet.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* SWOT grid */}
        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {quadrants.map(({ key, label, icon: Icon, cls, color, badge }, i) => (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`card ${cls}`}
            >
              <div className="flex items-center gap-2 mb-4">
                <Icon className={`w-5 h-5 ${color}`} />
                <span className={`font-bold text-sm px-2 py-0.5 rounded-full ${badge}`}>{label}</span>
              </div>
              <ul className="space-y-2">
                {(data[key as keyof SwotData] as string[]).map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="mt-1 w-1.5 h-1.5 rounded-full bg-current flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Radar */}
        {radarData.length > 0 && (
          <div className="card flex flex-col">
            <h3 className="font-semibold text-gray-900 mb-4">Score stratégique</h3>
            <div className="flex-1 min-h-[260px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#f0f0f0" />
                  <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12, fill: '#6b7280' }} />
                  <Radar name="Score" dataKey="A" stroke="#38B6FF" fill="#38B6FF" fillOpacity={0.25} strokeWidth={2} />
                  <Tooltip formatter={(v) => [`${v}/100`, 'Score']} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 space-y-2">
              {data.score && Object.entries(data.score).map(([k, v]) => (
                <div key={k} className="flex items-center gap-2">
                  <span className="text-xs text-gray-500 w-20 capitalize">{k}</span>
                  <div className="flex-1 h-1.5 bg-gray-100 rounded-full">
                    <div className="h-1.5 rounded-full progress-gradient" style={{ width: `${v}%` }} />
                  </div>
                  <span className="text-xs font-medium text-gray-700 w-8 text-right">{v}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
