'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Download, RefreshCw, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import SwotTab from '@/components/dashboard/tabs/SwotTab';
import PersonasTab from '@/components/dashboard/tabs/PersonasTab';
import SalesTab from '@/components/dashboard/tabs/SalesTab';
import MarketingTab from '@/components/dashboard/tabs/MarketingTab';
import SeoTab from '@/components/dashboard/tabs/SeoTab';
import AdsTab from '@/components/dashboard/tabs/AdsTab';
import SynthesisTab from '@/components/dashboard/tabs/SynthesisTab';

const TABS = [
  { id: 'swot', label: 'Diagnostic', icon: '🔍' },
  { id: 'personas', label: 'Personas', icon: '👥' },
  { id: 'sales', label: 'Vente', icon: '💬' },
  { id: 'marketing', label: 'Marketing', icon: '📣' },
  { id: 'seo', label: 'SEO & GEO', icon: '🔎' },
  { id: 'ads', label: 'Publicité', icon: '📱' },
  { id: 'synthesis', label: 'Synthèse', icon: '📊' },
];

export default function DashboardPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('swot');
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalysis();
  }, [id]);

  const fetchAnalysis = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/api/analysis/${id}`);
      setAnalysis(res.data);
    } catch {
      setError('Impossible de charger l\'analyse. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    const { default: jsPDF } = await import('jspdf');
    const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(24);
    doc.setTextColor(56, 182, 255);
    doc.text('Stratège — Rapport d\'analyse', 20, 30);
    doc.setFontSize(12);
    doc.setTextColor(100, 100, 100);
    doc.setFont('helvetica', 'normal');
    doc.text(`Généré le ${new Date().toLocaleDateString('fr-FR')}`, 20, 42);
    if (analysis?.swot) {
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(16);
      doc.setTextColor(0, 0, 0);
      doc.text('Analyse SWOT', 20, 60);
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(11);
      let y = 72;
      const sections = [
        { title: 'Forces', items: analysis.swot.strengths, color: [34, 197, 94] as [number, number, number] },
        { title: 'Faiblesses', items: analysis.swot.weaknesses, color: [245, 158, 11] as [number, number, number] },
        { title: 'Opportunités', items: analysis.swot.opportunities, color: [56, 182, 255] as [number, number, number] },
        { title: 'Menaces', items: analysis.swot.threats, color: [239, 68, 68] as [number, number, number] },
      ];
      sections.forEach(({ title, items, color }) => {
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(...color);
        doc.text(title, 20, y);
        y += 6;
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(60, 60, 60);
        items.forEach((item: string) => {
          doc.text(`• ${item}`, 26, y);
          y += 6;
        });
        y += 4;
      });
    }
    doc.save(`stratege-analyse-${id}.pdf`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 rounded-2xl bg-gradient-primary flex items-center justify-center mx-auto mb-4 animate-pulse">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Analyse en cours...</h2>
          <p className="text-gray-500 text-sm">Génération de votre rapport 360° personnalisé</p>
          <div className="flex justify-center gap-1 mt-4">
            {[0, 1, 2].map((i) => (
              <div key={i} className="w-2 h-2 rounded-full bg-primary-500 animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center card max-w-sm">
          <p className="text-red-500 mb-4">{error}</p>
          <Link href="/wizard" className="btn-primary">Relancer une analyse</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
                  <Zap className="w-4 h-4 text-white" />
                </div>
                <span className="font-bold text-gray-900">Stratège</span>
              </Link>
              <span className="text-gray-300">|</span>
              <span className="text-sm text-gray-500 hidden sm:block">Rapport d'analyse</span>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/wizard" className="btn-secondary text-sm px-4 py-2 hidden sm:flex">
                <ArrowLeft className="w-4 h-4" />
                Modifier
              </Link>
              <button onClick={fetchAnalysis} className="btn-secondary text-sm px-4 py-2">
                <RefreshCw className="w-4 h-4" />
                <span className="hidden sm:inline">Actualiser</span>
              </button>
              <button onClick={handleExportPDF} className="btn-primary text-sm px-4 py-2">
                <Download className="w-4 h-4" />
                <span className="hidden sm:inline">Export PDF</span>
              </button>
            </div>
          </div>
          {/* Tab bar */}
          <div className="flex gap-1 overflow-x-auto pb-px scrollbar-hide">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-1.5 px-4 py-3 text-sm font-medium whitespace-nowrap transition-all border-b-2 ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-500'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <span>{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {activeTab === 'swot' && <SwotTab data={analysis?.swot} input={analysis?.input} />}
            {activeTab === 'personas' && <PersonasTab data={analysis?.personas} />}
            {activeTab === 'sales' && <SalesTab data={analysis?.sales} personas={analysis?.personas} />}
            {activeTab === 'marketing' && <MarketingTab data={analysis?.marketing} input={analysis?.input} />}
            {activeTab === 'seo' && <SeoTab data={analysis?.seo} pagespeed={analysis?.pagespeed} />}
            {activeTab === 'ads' && <AdsTab data={analysis?.ads} input={analysis?.input} />}
            {activeTab === 'synthesis' && <SynthesisTab data={analysis} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
