'use client';

import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

type ContentPlan = { week: number; platform: string; format: string; topic: string; hashtags: string[] };
type MarketingData = {
  contentPlan: ContentPlan[];
  platforms: { name: string; priority: 'haute' | 'moyenne' | 'basse'; reason: string; frequency: string }[];
  budgetAllocation: { category: string; percentage: number; amount: number }[];
  rule8020: { focus: string[]; avoid: string[] };
  editorialCalendar: { day: string; content: string; format: string }[];
};

const COLORS = ['#38B6FF', '#E20074', '#8B5CF6', '#F59E0B', '#10B981'];
const priorityColors: Record<string, string> = { haute: 'badge-magenta', moyenne: 'badge-primary', basse: 'bg-gray-100 text-gray-600 badge' };

export default function MarketingTab({ data, input }: { data?: MarketingData; input?: any }) {
  if (!data) return <div className="card text-gray-400 text-center py-12">Données indisponibles</div>;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="section-title">Marketing Digital & Contenu</h2>
        <p className="section-subtitle">Plan de contenu, calendrier éditorial et répartition budgétaire selon la règle 80/20.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Budget allocation */}
        {data.budgetAllocation?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">💰 Répartition budgétaire</h3>
            <div className="flex items-center gap-4">
              <div className="w-40 h-40 flex-shrink-0">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={data.budgetAllocation} dataKey="percentage" cx="50%" cy="50%" outerRadius={60} strokeWidth={2}>
                      {data.budgetAllocation.map((_, i) => (
                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(v) => [`${v}%`, '']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex-1 space-y-2">
                {data.budgetAllocation.map((item, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                    <span className="text-sm text-gray-600 flex-1">{item.category}</span>
                    <span className="text-sm font-semibold text-gray-900">{item.amount} €</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Platforms */}
        {data.platforms?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">📱 Plateformes recommandées</h3>
            <div className="space-y-3">
              {data.platforms.map((p, i) => (
                <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                  className="flex items-start gap-3 p-3 rounded-xl bg-gray-50">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-sm text-gray-900">{p.name}</span>
                      <span className={priorityColors[p.priority]}>{p.priority}</span>
                    </div>
                    <p className="text-xs text-gray-500">{p.reason}</p>
                    <p className="text-xs text-gray-400 mt-1">📅 {p.frequency}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Rule 80/20 */}
      {data.rule8020 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="card bg-emerald-50 border border-emerald-100">
            <h3 className="font-semibold text-emerald-800 mb-3">✅ 80% — Ce qui génère des résultats</h3>
            <ul className="space-y-2">
              {data.rule8020.focus.map((item, i) => (
                <li key={i} className="text-sm text-emerald-700 flex items-start gap-2">
                  <span className="mt-0.5">→</span>{item}
                </li>
              ))}
            </ul>
          </div>
          <div className="card bg-red-50 border border-red-100">
            <h3 className="font-semibold text-red-800 mb-3">❌ 20% — À éviter ou minimiser</h3>
            <ul className="space-y-2">
              {data.rule8020.avoid.map((item, i) => (
                <li key={i} className="text-sm text-red-700 flex items-start gap-2">
                  <span className="mt-0.5">✗</span>{item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Content plan */}
      {data.contentPlan?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">📅 Plan de contenu — 4 semaines</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  {['Semaine', 'Plateforme', 'Format', 'Sujet', 'Hashtags'].map(h => (
                    <th key={h} className="text-left py-3 px-3 font-medium text-gray-500 text-xs uppercase">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.contentPlan.map((row, i) => (
                  <tr key={i} className={`border-b border-gray-50 ${i % 2 === 0 ? 'bg-gray-50/50' : ''}`}>
                    <td className="py-3 px-3"><span className="badge-primary text-xs">S{row.week}</span></td>
                    <td className="py-3 px-3 font-medium text-gray-800">{row.platform}</td>
                    <td className="py-3 px-3"><span className="badge bg-violet-50 text-violet-600 text-xs">{row.format}</span></td>
                    <td className="py-3 px-3 text-gray-600">{row.topic}</td>
                    <td className="py-3 px-3">
                      <div className="flex flex-wrap gap-1">
                        {row.hashtags?.slice(0, 3).map((h, j) => (
                          <span key={j} className="text-xs text-primary-500">#{h}</span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Editorial calendar */}
      {data.editorialCalendar?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">🗓️ Calendrier éditorial hebdomadaire</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
            {data.editorialCalendar.map((day, i) => (
              <div key={i} className="p-3 rounded-xl bg-gray-50 text-center">
                <p className="text-xs font-bold text-gray-400 uppercase mb-2">{day.day}</p>
                <p className="text-xs text-gray-700">{day.content}</p>
                <span className="text-xs text-primary-500 mt-1 block">{day.format}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
