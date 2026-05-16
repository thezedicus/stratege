'use client';

import { motion } from 'framer-motion';
import { Download, CheckCircle2, TrendingUp, AlertCircle, Clock } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, LineChart, Line } from 'recharts';

type Action = { priority: number; action: string; timeline: string; effort: string; impact: string; category: string };
type SynthesisData = {
  swot?: any;
  personas?: any[];
  sales?: any;
  marketing?: any;
  seo?: any;
  ads?: any;
  input?: { activityType: string; budget: number; monthlyBudget: number; goal: string; maturity: string };
  synthesis?: {
    actions: Action[];
    roi: { month: number; pessimistic: number; realistic: number; optimistic: number }[];
    summary: string;
    keyMetrics: { label: string; value: string; trend: string }[];
    nextSteps: string[];
  };
};

const categoryColors: Record<string, string> = {
  SEO: 'badge-primary',
  Marketing: 'badge-magenta',
  Vente: 'bg-violet-50 text-violet-600 badge',
  Publicité: 'bg-amber-50 text-amber-600 badge',
  Contenu: 'bg-emerald-50 text-emerald-600 badge',
  Stratégie: 'bg-rose-50 text-rose-600 badge',
};
const effortColors: Record<string, string> = {
  Faible: 'text-emerald-500',
  Moyen: 'text-amber-500',
  Élevé: 'text-red-500',
};
const impactColors: Record<string, string> = {
  Fort: 'text-emerald-600 font-semibold',
  Moyen: 'text-amber-600',
  Faible: 'text-gray-500',
};

export default function SynthesisTab({ data }: { data?: SynthesisData }) {
  const s = data?.synthesis;

  if (!s) return <div className="card text-gray-400 text-center py-12">Synthèse non disponible</div>;

  const handleExport = async () => {
    const { default: jsPDF } = await import('jspdf');
    const doc = new jsPDF();
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(20);
    doc.text('Stratège — Rapport de synthèse', 20, 20);
    doc.setFontSize(11);
    doc.setFont('helvetica', 'normal');
    if (s.summary) {
      doc.text(doc.splitTextToSize(s.summary, 170), 20, 35);
    }
    let y = 65;
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(14);
    doc.text('Actions prioritaires', 20, y);
    y += 8;
    s.actions?.forEach((a) => {
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(11);
      doc.text(`${a.priority}. ${a.action}`, 20, y);
      y += 5;
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(9);
      doc.text(`Délai: ${a.timeline} | Effort: ${a.effort} | Impact: ${a.impact}`, 25, y);
      y += 8;
      if (y > 270) { doc.addPage(); y = 20; }
    });
    doc.save('stratege-synthese.pdf');
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="section-title">Rapport de Synthèse</h2>
          <p className="section-subtitle">Actions prioritaires, estimation ROI et prochaines étapes.</p>
        </div>
        <button onClick={handleExport} className="btn-primary text-sm">
          <Download className="w-4 h-4" />
          Export PDF
        </button>
      </div>

      {/* Summary */}
      {s.summary && (
        <div className="card" style={{ background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF0F7 100%)' }}>
          <h3 className="font-semibold text-gray-900 mb-3">💡 Résumé exécutif</h3>
          <p className="text-gray-700 leading-relaxed">{s.summary}</p>
        </div>
      )}

      {/* Key metrics */}
      {s.keyMetrics?.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {s.keyMetrics.map((m, i) => (
            <motion.div key={i} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.1 }} className="card text-center">
              <p className="text-xs text-gray-400 mb-1">{m.label}</p>
              <p className="text-2xl font-bold gradient-text">{m.value}</p>
              <p className={`text-xs mt-1 ${m.trend.startsWith('+') ? 'text-emerald-500' : 'text-gray-400'}`}>{m.trend}</p>
            </motion.div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ROI projection */}
        {s.roi?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">📈 Projection ROI (12 mois)</h3>
            <div className="h-52">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={s.roi} margin={{ top: 0, right: 10, bottom: 0, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                  <XAxis dataKey="month" tick={{ fontSize: 11 }} tickFormatter={(v) => `M${v}`} />
                  <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `${v}€`} />
                  <Tooltip formatter={(v, n) => [`${v} €`, n === 'realistic' ? 'Réaliste' : n === 'optimistic' ? 'Optimiste' : 'Pessimiste']} labelFormatter={(l) => `Mois ${l}`} />
                  <Line type="monotone" dataKey="optimistic" stroke="#38B6FF" strokeWidth={2} dot={false} strokeDasharray="5 5" />
                  <Line type="monotone" dataKey="realistic" stroke="#E20074" strokeWidth={2.5} dot={false} />
                  <Line type="monotone" dataKey="pessimistic" stroke="#d1d5db" strokeWidth={1.5} dot={false} strokeDasharray="3 3" />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="flex gap-4 mt-3 justify-center text-xs text-gray-500">
              {[
                { color: '#38B6FF', label: 'Optimiste' },
                { color: '#E20074', label: 'Réaliste' },
                { color: '#d1d5db', label: 'Pessimiste' },
              ].map(({ color, label }) => (
                <span key={label} className="flex items-center gap-1.5">
                  <span className="w-4 h-0.5 inline-block rounded-full" style={{ backgroundColor: color }} />
                  {label}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Next steps */}
        {s.nextSteps?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">🚀 Prochaines étapes immédiates</h3>
            <div className="space-y-3">
              {s.nextSteps.map((step, i) => (
                <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                  className="flex items-start gap-3 p-3 rounded-xl bg-gray-50">
                  <div className="w-6 h-6 rounded-full bg-gradient-primary flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">{i + 1}</span>
                  </div>
                  <p className="text-sm text-gray-700">{step}</p>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Priority actions */}
      {s.actions?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">⚡ Actions Prioritaires</h3>
          <div className="space-y-3">
            {s.actions.sort((a, b) => a.priority - b.priority).map((action, i) => (
              <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
                className="flex items-start gap-4 p-4 rounded-xl border border-gray-100 hover:border-primary-200 hover:bg-gray-50/50 transition-all">
                <div className="w-8 h-8 rounded-xl bg-gradient-primary flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-sm font-bold">{action.priority}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start gap-2 mb-1 flex-wrap">
                    <p className="font-medium text-gray-900 text-sm">{action.action}</p>
                    <span className={`${categoryColors[action.category] || 'badge bg-gray-100 text-gray-600'} text-xs`}>
                      {action.category}
                    </span>
                  </div>
                  <div className="flex gap-4 text-xs text-gray-500">
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{action.timeline}</span>
                    <span className={effortColors[action.effort] || 'text-gray-500'}>Effort : {action.effort}</span>
                    <span className={impactColors[action.impact] || 'text-gray-600'}>Impact : {action.impact}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
