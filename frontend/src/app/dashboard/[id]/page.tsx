'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Download, RefreshCw } from 'lucide-react';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import AppShell from '@/components/layout/AppShell';
import RightPanel from '@/components/layout/RightPanel';
import SwotTab from '@/components/dashboard/tabs/SwotTab';
import PersonasTab from '@/components/dashboard/tabs/PersonasTab';
import SalesTab from '@/components/dashboard/tabs/SalesTab';
import MarketingTab from '@/components/dashboard/tabs/MarketingTab';
import SeoTab from '@/components/dashboard/tabs/SeoTab';
import AdsTab from '@/components/dashboard/tabs/AdsTab';
import SynthesisTab from '@/components/dashboard/tabs/SynthesisTab';

const TABS = [
  { id: 'swot',      label: 'Diagnostic', icon: '🔍' },
  { id: 'personas',  label: 'Personas',   icon: '👥' },
  { id: 'sales',     label: 'Vente',      icon: '💬' },
  { id: 'marketing', label: 'Marketing',  icon: '📣' },
  { id: 'seo',       label: 'SEO & GEO',  icon: '🔎' },
  { id: 'ads',       label: 'Publicité',  icon: '📱' },
  { id: 'synthesis', label: 'Synthèse',   icon: '📊' },
];

export default function DashboardPage() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState('swot');
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => { fetchAnalysis(); }, [id]);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await apiClient.get(`/api/analysis/${id}`);
      setAnalysis(res.data);
    } catch {
      setError("Impossible de charger l'analyse. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    const { default: jsPDF } = await import('jspdf');
    const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    const pageH = 297, marginL = 20, maxW = 170;

    const ensurePage = (y: number, needed = 10): number => {
      if (y + needed > pageH - 15) { doc.addPage(); return 20; }
      return y;
    };

    const sectionTitle = (text: string, y: number, rgb: [number,number,number] = [0,0,0]): number => {
      y = ensurePage(y, 14);
      doc.setFont('helvetica','bold'); doc.setFontSize(14);
      doc.setTextColor(...rgb);
      doc.text(text, marginL, y);
      doc.setDrawColor(...rgb); doc.setLineWidth(0.4);
      doc.line(marginL, y + 2, marginL + maxW, y + 2);
      return y + 10;
    };

    const bullet = (text: string, y: number, indent = 26): number => {
      const lines = doc.splitTextToSize(`• ${text}`, maxW - (indent - marginL));
      y = ensurePage(y, lines.length * 5 + 2);
      doc.setFont('helvetica','normal'); doc.setFontSize(10);
      doc.setTextColor(60,60,60);
      doc.text(lines, indent, y);
      return y + lines.length * 5 + 1;
    };

    // Cover
    doc.setFont('helvetica','bold'); doc.setFontSize(26);
    doc.setTextColor(56,182,255); doc.text('Stratège', marginL, 32);
    doc.setFontSize(14); doc.setTextColor(226,0,116);
    doc.text("Rapport d'analyse stratégique 360°", marginL, 42);
    doc.setFont('helvetica','normal'); doc.setFontSize(10);
    doc.setTextColor(120,120,120);
    doc.text(`Généré le ${new Date().toLocaleDateString('fr-FR')} · ID ${id}`, marginL, 52);
    if (analysis?.input) {
      const i = analysis.input;
      doc.setFontSize(11); doc.setTextColor(60,60,60);
      doc.text([
        `Activité : ${i.activityType}   |   Objectif : ${i.goal}   |   Maturité : ${i.maturity}`,
        `Capital total : ${i.budget} €   |   Budget mensuel : ${i.monthlyBudget} €`,
      ], marginL, 64);
    }
    let y = 82;

    // SWOT
    if (analysis?.swot) {
      y = sectionTitle('1. Analyse SWOT', y);
      const swotSecs = [
        { title: '✅ Forces',       items: analysis.swot.strengths,     color: [34,197,94]  as [number,number,number] },
        { title: '⚠️ Faiblesses',  items: analysis.swot.weaknesses,    color: [245,158,11] as [number,number,number] },
        { title: '🚀 Opportunités', items: analysis.swot.opportunities, color: [56,182,255] as [number,number,number] },
        { title: '🔴 Menaces',      items: analysis.swot.threats,       color: [239,68,68]  as [number,number,number] },
      ];
      swotSecs.forEach(({ title, items, color }) => {
        y = ensurePage(y, 12);
        doc.setFont('helvetica','bold'); doc.setFontSize(11);
        doc.setTextColor(...color); doc.text(title, marginL, y); y += 6;
        (items as string[]).forEach(item => { y = bullet(item, y); });
        y += 3;
      });
    }

    // Personas
    if (analysis?.personas?.length) {
      y = sectionTitle('2. Personas', y);
      (analysis.personas as any[]).forEach((p, i) => {
        y = ensurePage(y, 20);
        doc.setFont('helvetica','bold'); doc.setFontSize(11);
        doc.setTextColor(56,182,255);
        doc.text(`Persona ${i+1} — ${p.name}, ${p.age} ans · ${p.job}`, marginL, y); y += 6;
        if (p.goals?.length) y = bullet(`Objectifs : ${(p.goals as string[]).join(', ')}`, y);
        if (p.painPoints?.length) y = bullet(`Douleurs : ${(p.painPoints as string[]).join(', ')}`, y);
        y += 2;
      });
    }

    // Marketing
    if (analysis?.marketing) {
      y = sectionTitle('3. Marketing & Contenu', y);
      if (analysis.marketing.platforms?.length) {
        doc.setFont('helvetica','bold'); doc.setFontSize(10); doc.setTextColor(80,80,80);
        y = ensurePage(y, 8); doc.text('Plateformes recommandées :', marginL, y); y += 6;
        (analysis.marketing.platforms as any[]).forEach(p => {
          y = bullet(`${p.name} (${p.priority}) — ${p.frequency}`, y);
        });
      }
      if (analysis.marketing.budgetAllocation?.length) {
        y = ensurePage(y, 8);
        doc.setFont('helvetica','bold'); doc.setFontSize(10); doc.setTextColor(80,80,80);
        doc.text('Répartition budgétaire :', marginL, y); y += 6;
        (analysis.marketing.budgetAllocation as any[]).forEach(b => {
          y = bullet(`${b.category} : ${b.percentage}% → ${b.amount} €/mois`, y);
        });
      }
    }

    // SEO
    if (analysis?.seo?.keywords?.length) {
      y = sectionTitle('4. SEO — Mots-clés prioritaires', y);
      (analysis.seo.keywords as any[]).slice(0, 8).forEach(kw => {
        y = bullet(`${kw.keyword}  [vol: ${kw.volume}] · diff: ${kw.difficulty} · ${kw.intent}`, y);
      });
    }

    // Ads
    if (analysis?.ads?.mediaplan?.length) {
      y = sectionTitle('5. Media Plan Publicitaire', y);
      (analysis.ads.mediaplan as any[]).forEach(row => {
        y = bullet(`${row.platform} — ${row.budget} €/mois · Portée: ${row.reach} · ROI: ${row.expectedRoi}`, y);
      });
    }

    // Synthesis
    if (analysis?.synthesis) {
      const s = analysis.synthesis;
      y = sectionTitle('6. Synthèse & Recommandations', y);
      if (s.keyMetrics) {
        doc.setFont('helvetica','bold'); doc.setFontSize(10); doc.setTextColor(80,80,80);
        y = ensurePage(y, 8); doc.text('Métriques clés :', marginL, y); y += 6;
        Object.entries(s.keyMetrics as Record<string,string|number>).forEach(([k,v]) => {
          y = bullet(`${k} : ${v}`, y);
        });
      }
      if (s.summary) {
        y = ensurePage(y, 10);
        doc.setFont('helvetica','bold'); doc.setFontSize(10); doc.setTextColor(80,80,80);
        doc.text('Résumé stratégique :', marginL, y); y += 6;
        const lines = doc.splitTextToSize(s.summary as string, maxW);
        y = ensurePage(y, lines.length * 5);
        doc.setFont('helvetica','normal'); doc.setFontSize(10); doc.setTextColor(60,60,60);
        doc.text(lines, marginL, y); y += lines.length * 5 + 4;
      }
      if (s.priorities?.length) {
        y = ensurePage(y, 8);
        doc.setFont('helvetica','bold'); doc.setFontSize(10); doc.setTextColor(80,80,80);
        doc.text('Priorités :', marginL, y); y += 6;
        (s.priorities as string[]).forEach(p => { y = bullet(p, y); });
      }
    }

    doc.save(`stratege-analyse-${id}.pdf`);
  };

  if (loading) {
    return (
      <AppShell>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-gradient-primary flex items-center justify-center mx-auto mb-4 animate-pulse">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" strokeWidth="2" strokeLinecap="round" d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Chargement...</h2>
            <p className="text-gray-500 text-sm">Récupération de votre rapport 360°</p>
            <div className="flex justify-center gap-1 mt-4">
              {[0,1,2].map(i => (
                <div key={i} className="w-2 h-2 rounded-full bg-primary-500 animate-bounce"
                  style={{ animationDelay: `${i * 0.15}s` }} />
              ))}
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  if (error) {
    return (
      <AppShell>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center card max-w-sm animate-fade-in">
            <p className="text-red-500 mb-4">{error}</p>
            <div className="flex gap-3 justify-center">
              <button onClick={fetchAnalysis} className="btn-secondary text-sm">Réessayer</button>
              <Link href="/wizard" className="btn-primary text-sm">Nouvelle analyse</Link>
            </div>
          </div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell rightPanel={<RightPanel analysis={analysis} />}>
      {/* Sticky tab header */}
      <div className="bg-white border-b border-gray-100 sticky top-0 z-30">
        <div className="px-6 py-3 flex items-center justify-between">
          <div>
            <h1 className="font-bold text-gray-900 text-sm">Rapport d'analyse</h1>
            <p className="text-xs text-gray-400">ID {id}</p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={fetchAnalysis} className="btn-secondary text-xs px-3 py-1.5">
              <RefreshCw className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Actualiser</span>
            </button>
            <button onClick={handleExportPDF} className="btn-primary text-xs px-3 py-1.5">
              <Download className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Export PDF</span>
            </button>
          </div>
        </div>
        {/* Tabs */}
        <div className="flex gap-0 overflow-x-auto scrollbar-hide px-2 pb-0">
          {TABS.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-1.5 px-4 py-3 text-sm font-medium whitespace-nowrap
                transition-all border-b-2 -mb-px
                ${activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-200'
                }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      <div className="p-6 max-w-5xl mx-auto w-full">
        <div key={activeTab} className="animate-fade-in">
          {activeTab === 'swot'      && <SwotTab
                                          data={analysis?.swot}
                                          qqoqccp={analysis?.qqoqccp}
                                          pestel={analysis?.pestel}
                                          microEnv={analysis?.microEnv}
                                          competitive={analysis?.competitive}
                                          input={analysis?.input}
                                        />}
          {activeTab === 'personas'  && <PersonasTab  data={analysis?.personas} />}
          {activeTab === 'sales'     && <SalesTab     data={analysis?.sales}    copywriting={analysis?.copywriting} />}
          {activeTab === 'marketing' && <MarketingTab data={analysis?.marketing} copywriting={analysis?.copywriting} input={analysis?.input} />}
          {activeTab === 'seo'       && <SeoTab       data={analysis?.seo}       geo2025={analysis?.geo2025} pagespeed={analysis?.pagespeed} />}
          {activeTab === 'ads'       && <AdsTab       data={analysis?.ads}       geo2025={analysis?.geo2025} input={analysis?.input} />}
          {activeTab === 'synthesis' && <SynthesisTab data={analysis} />}
        </div>
      </div>
    </AppShell>
  );
}
