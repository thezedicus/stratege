'use client';

import { motion } from 'framer-motion';
import { Download, Clock } from 'lucide-react';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
} from 'recharts';
import toast from 'react-hot-toast';

type Action = {
  priority: number;
  action: string;
  timeline: string;
  effort: string;
  impact: string;
  category: string;
};
type RoiPoint = { month: number; pessimistic: number; realistic: number; optimistic: number };
type KeyMetric = { label: string; value: string; trend: string };
type Synthesis = {
  actions: Action[];
  roi: RoiPoint[];
  summary: string;
  keyMetrics: KeyMetric[];
  nextSteps: string[];
};

type FullAnalysis = {
  synthesis?: Synthesis;
  input?: Record<string, unknown>;
};

const CATEGORY_COLORS: Record<string, string> = {
  SEO:       'bg-blue-50 text-blue-600',
  Marketing: 'bg-pink-50 text-pink-600',
  Vente:     'bg-violet-50 text-violet-600',
  Publicité: 'bg-amber-50 text-amber-600',
  Contenu:   'bg-emerald-50 text-emerald-600',
  Stratégie: 'bg-rose-50 text-rose-600',
};
const EFFORT_COLORS: Record<string, string> = {
  Faible: 'text-emerald-500',
  Moyen:  'text-amber-500',
  Élevé:  'text-red-500',
};
const IMPACT_COLORS: Record<string, string> = {
  Fort:   'text-emerald-600 font-semibold',
  Moyen:  'text-amber-600',
  Faible: 'text-gray-400',
};

export default function SynthesisTab({ data }: { data?: FullAnalysis }) {
  const s = data?.synthesis;

  const handleExport = async () => {
    try {
      const { default: jsPDF } = await import('jspdf');
      const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(22);
      doc.setTextColor(56, 182, 255);
      doc.text('Stratège — Rapport de Synthèse', 20, 25);

      doc.setFontSize(10);
      doc.setTextColor(150, 150, 150);
      doc.setFont('helvetica', 'normal');
      doc.text(`Généré le ${new Date().toLocaleDateString('fr-FR')}`, 20, 33);

      if (s?.summary) {
        doc.setFontSize(11);
        doc.setTextColor(60, 60, 60);
        const lines = doc.splitTextToSize(s.summary, 170) as string[];
        doc.text(lines, 20, 44);
      }

      let y = 70;

      if ((s?.keyMetrics?.length ?? 0) > 0) {
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text('Métriques clés', 20, y);
        y += 8;
        s!.keyMetrics.forEach((m) => {
          doc.setFont('helvetica', 'normal');
          doc.setFontSize(10);
          doc.setTextColor(60, 60, 60);
          doc.text(`${m.label}: ${m.value} (${m.trend})`, 25, y);
          y += 7;
        });
        y += 4;
      }

      if ((s?.actions?.length ?? 0) > 0) {
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text('Actions prioritaires', 20, y);
        y += 8;
        [...(s!.actions)].sort((a, b) => a.priority - b.priority).forEach((a) => {
          if (y > 265) { doc.addPage(); y = 20; }
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(10);
          doc.setTextColor(56, 182, 255);
          doc.text(`${a.priority}. ${a.action}`, 20, y);
          y += 5;
          doc.setFont('helvetica', 'normal');
          doc.setFontSize(9);
          doc.setTextColor(100, 100, 100);
          doc.text(`Délai: ${a.timeline} | Effort: ${a.effort} | Impact: ${a.impact} | Catégorie: ${a.category}`, 26, y);
          y += 8;
        });
      }

      if ((s?.nextSteps?.length ?? 0) > 0) {
        if (y > 240) { doc.addPage(); y = 20; }
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text('Prochaines étapes', 20, y);
        y += 8;
        s!.nextSteps.forEach((step, i) => {
          if (y > 265) { doc.addPage(); y = 20; }
          doc.setFont('helvetica', 'normal');
          doc.setFontSize(10);
          doc.setTextColor(60, 60, 60);
          const lines = doc.splitTextToSize(`${i + 1}. ${step}`, 165) as string[];
          doc.text(lines, 25, y);
          y += lines.length * 6;
        });
      }

      doc.save('stratege-synthese.pdf');
      toast.success('PDF exporté avec succès !');
    } catch {
      toast.error("Échec de l'export PDF. Réessayez.");
    }
  };

  if (!s) {
    return (
      <div className="card text-center py-16">
        <p className="text-4xl mb-3">📊</p>
        <p className="text-gray-500">Synthèse non disponible</p>
      </div>
    );
  }

  const hasRoi = (s.roi?.length ?? 0) > 0 && s.roi.some(p => p.realistic > 0);

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-start justify-between gap-4 flex-wrap">
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
        <div className="rounded-2xl p-6" style={{ background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF0F7 100%)' }}>
          <h3 className="font-semibold text-gray-900 mb-3">💡 Résumé exécutif</h3>
          <p className="text-gray-700 leading-relaxed">{s.summary}</p>
        </div>
      )}

      {/* Key metrics */}
      {(s.keyMetrics?.length ?? 0) > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {s.keyMetrics.map((m, i) => (
            <motion.div
              key={`metric-${i}`}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.1 }}
              className="card text-center"
            >
              <p className="text-xs text-gray-400 mb-1 leading-tight">{m.label}</p>
              <p className="text-xl font-bold gradient-text">{m.value}</p>
              <p className={`text-xs mt-1 ${m.trend.startsWith('+') ? 'text-emerald-500' : 'text-gray-400'}`}>
                {m.trend}
              </p>
            </motion.div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ROI chart */}
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">📈 Projection ROI — 12 mois</h3>
          {hasRoi ? (
            <>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={s.roi} margin={{ top: 4, right: 10, bottom: 0, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                    <XAxis dataKey="month" tick={{ fontSize: 11 }} tickFormatter={(v: number) => `M${v}`} />
                    <YAxis tick={{ fontSize: 11 }} tickFormatter={(v: number) => `${v}€`} width={50} />
                    <Tooltip
                      formatter={(v: number, n: string) => [
                        `${v.toLocaleString('fr-FR')} €`,
                        n === 'realistic' ? 'Réaliste' : n === 'optimistic' ? 'Optimiste' : 'Pessimiste',
                      ]}
                      labelFormatter={(l: number) => `Mois ${l}`}
                    />
                    <Line type="monotone" dataKey="optimistic" stroke="#38B6FF" strokeWidth={2} dot={false} strokeDasharray="5 5" />
                    <Line type="monotone" dataKey="realistic"  stroke="#E20074" strokeWidth={2.5} dot={false} />
                    <Line type="monotone" dataKey="pessimistic" stroke="#d1d5db" strokeWidth={1.5} dot={false} strokeDasharray="3 3" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="flex gap-4 mt-3 justify-center text-xs text-gray-500 flex-wrap">
                {[
                  { color: '#38B6FF', label: 'Optimiste' },
                  { color: '#E20074', label: 'Réaliste' },
                  { color: '#d1d5db', label: 'Pessimiste' },
                ].map(({ color, label }) => (
                  <span key={label} className="flex items-center gap-1.5">
                    <span className="w-5 h-0.5 inline-block rounded-full" style={{ backgroundColor: color }} />
                    {label}
                  </span>
                ))}
              </div>
            </>
          ) : (
            <div className="h-52 flex flex-col items-center justify-center text-center text-gray-400">
              <p className="text-3xl mb-2">📊</p>
              <p className="text-sm">La projection ROI nécessite un budget mensuel plus élevé.</p>
              <p className="text-xs mt-1">Concentrez-vous sur les actions prioritaires ci-dessous.</p>
            </div>
          )}
        </div>

        {/* Next steps */}
        {(s.nextSteps?.length ?? 0) > 0 && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">🚀 Prochaines étapes immédiates</h3>
            <div className="space-y-3">
              {s.nextSteps.map((step, i) => (
                <motion.div
                  key={`step-${i}`}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.07 }}
                  className="flex items-start gap-3 p-3 rounded-xl bg-gray-50"
                >
                  <div
                    className="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 text-white text-xs font-bold"
                    style={{ background: 'linear-gradient(135deg, #38B6FF 0%, #E20074 100%)' }}
                  >
                    {i + 1}
                  </div>
                  <p className="text-sm text-gray-700">{step}</p>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Priority actions */}
      {(s.actions?.length ?? 0) > 0 && (
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">⚡ Actions Prioritaires</h3>
          <div className="space-y-3">
            {[...s.actions].sort((a, b) => a.priority - b.priority).map((action, i) => (
              <motion.div
                key={`action-${action.priority}-${i}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="flex items-start gap-4 p-4 rounded-xl border border-gray-100 hover:border-primary-200 hover:bg-gray-50/50 transition-all"
              >
                <div
                  className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 text-white text-sm font-bold"
                  style={{ background: 'linear-gradient(135deg, #38B6FF 0%, #E20074 100%)' }}
                >
                  {action.priority}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start gap-2 mb-1.5 flex-wrap">
                    <p className="font-medium text-gray-900 text-sm">{action.action}</p>
                    <span className={`badge text-xs ${CATEGORY_COLORS[action.category] ?? 'bg-gray-100 text-gray-600'}`}>
                      {action.category}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />{action.timeline}
                    </span>
                    <span className={EFFORT_COLORS[action.effort] ?? 'text-gray-500'}>
                      Effort : {action.effort}
                    </span>
                    <span className={IMPACT_COLORS[action.impact] ?? 'text-gray-600'}>
                      Impact : {action.impact}
                    </span>
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
