'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Zap, ArrowLeft, ArrowRight, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';
import toast from 'react-hot-toast';
import { apiClient } from '@/lib/api';

export type WizardData = {
  activityType: string;
  budget: number;
  monthlyBudget: number;
  goal: string;
  maturity: string;
  websiteUrl: string;
};

const activityTypes = [
  { id: 'ecommerce', label: 'E-commerce', icon: '🛍️' },
  { id: 'saas', label: 'SaaS / Logiciel', icon: '💻' },
  { id: 'service', label: 'Service en ligne', icon: '🎯' },
  { id: 'website', label: 'Site vitrine', icon: '🌐' },
  { id: 'application', label: 'Application mobile', icon: '📱' },
  { id: 'content', label: 'Création de contenu', icon: '✍️' },
  { id: 'consulting', label: 'Conseil / Coaching', icon: '🧠' },
  { id: 'other', label: 'Autre', icon: '✨' },
];

const goals = [
  { id: 'awareness', label: 'Notoriété', desc: 'Faire connaître ma marque', icon: '📣' },
  { id: 'sales', label: 'Ventes', desc: 'Augmenter mon chiffre d\'affaires', icon: '💰' },
  { id: 'leads', label: 'Leads', desc: 'Générer des prospects qualifiés', icon: '🎯' },
  { id: 'traffic', label: 'Trafic', desc: 'Augmenter les visites', icon: '📈' },
];

const maturities = [
  { id: 'idea', label: 'Idée', desc: 'Projet en cours de réflexion', icon: '💡' },
  { id: 'inprogress', label: 'En cours', desc: 'Développement en cours', icon: '⚙️' },
  { id: 'launched', label: 'Lancé', desc: 'Déjà en activité', icon: '🚀' },
];

const TOTAL_STEPS = 5;

export default function WizardPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<WizardData>({
    activityType: '',
    budget: 500,
    monthlyBudget: 200,
    goal: '',
    maturity: '',
    websiteUrl: '',
  });

  const progress = ((step - 1) / TOTAL_STEPS) * 100;

  const canNext = () => {
    if (step === 1) return !!data.activityType;
    if (step === 2) return data.budget > 0 && data.monthlyBudget > 0;
    if (step === 3) return !!data.goal;
    if (step === 4) return !!data.maturity;
    return true;
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await apiClient.post('/api/analysis', data);
      const analysisId = res.data.id;
      router.push(`/dashboard/${analysisId}`);
    } catch {
      toast.error('Erreur lors de la génération de l\'analyse. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  const budgetAllocation = {
    ads: Math.round(data.monthlyBudget * 0.5),
    tools: Math.round(data.monthlyBudget * 0.25),
    content: Math.round(data.monthlyBudget * 0.25),
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 px-6 py-4">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors">
            <ArrowLeft className="w-4 h-4" />
            <span className="text-sm">Retour</span>
          </Link>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-primary flex items-center justify-center">
              <Zap className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="font-bold text-gray-900">Stratège</span>
          </div>
          <span className="text-sm text-gray-400">Étape {step}/{TOTAL_STEPS}</span>
        </div>
      </div>

      {/* Progress */}
      <div className="bg-white border-b border-gray-100 px-6 py-3">
        <div className="max-w-2xl mx-auto">
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
            <motion.div
              className="h-full progress-gradient rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.4, ease: 'easeInOut' }}
            />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-2xl">
          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h2 className="section-title text-3xl">Quel type d'activité ?</h2>
                <p className="section-subtitle text-base">Sélectionnez la catégorie qui correspond le mieux à votre projet.</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {activityTypes.map((a) => (
                    <button
                      key={a.id}
                      onClick={() => setData({ ...data, activityType: a.id })}
                      className={`p-4 rounded-2xl border-2 text-center transition-all duration-200 hover:-translate-y-0.5 ${
                        data.activityType === a.id
                          ? 'border-primary-500 bg-primary-50 shadow-card-hover'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      }`}
                    >
                      <span className="text-2xl block mb-2">{a.icon}</span>
                      <span className="text-sm font-medium text-gray-700">{a.label}</span>
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h2 className="section-title text-3xl">Votre budget</h2>
                <p className="section-subtitle text-base">Définissez votre capital disponible et budget mensuel marketing.</p>
                <div className="space-y-8">
                  <div className="card">
                    <label className="block text-sm font-semibold text-gray-700 mb-4">
                      Capital total disponible : <span className="gradient-text text-lg">{data.budget} €</span>
                    </label>
                    <input
                      type="range" min={10} max={1000} step={10}
                      value={data.budget}
                      onChange={(e) => setData({ ...data, budget: +e.target.value })}
                      className="w-full h-2 rounded-full appearance-none cursor-pointer"
                      style={{ accentColor: '#38B6FF' }}
                    />
                    <div className="flex justify-between text-xs text-gray-400 mt-1">
                      <span>10 €</span><span>1 000 €</span>
                    </div>
                  </div>
                  <div className="card">
                    <label className="block text-sm font-semibold text-gray-700 mb-4">
                      Budget mensuel marketing : <span className="gradient-text text-lg">{data.monthlyBudget} €</span>
                    </label>
                    <input
                      type="range" min={10} max={1000} step={10}
                      value={data.monthlyBudget}
                      onChange={(e) => setData({ ...data, monthlyBudget: +e.target.value })}
                      className="w-full h-2 rounded-full appearance-none cursor-pointer"
                      style={{ accentColor: '#E20074' }}
                    />
                    <div className="flex justify-between text-xs text-gray-400 mt-1">
                      <span>10 €</span><span>1 000 €</span>
                    </div>
                  </div>
                  <div className="card bg-gray-50">
                    <p className="text-sm font-semibold text-gray-700 mb-3">📊 Répartition suggérée ({data.monthlyBudget} €/mois)</p>
                    <div className="space-y-2">
                      {[
                        { label: 'Publicité (50%)', val: budgetAllocation.ads, color: '#38B6FF' },
                        { label: 'Outils (25%)', val: budgetAllocation.tools, color: '#E20074' },
                        { label: 'Contenu (25%)', val: budgetAllocation.content, color: '#8B5CF6' },
                      ].map((item) => (
                        <div key={item.label} className="flex items-center gap-3">
                          <span className="text-xs text-gray-500 w-28">{item.label}</span>
                          <div className="flex-1 h-2 bg-gray-200 rounded-full">
                            <div className="h-2 rounded-full" style={{ width: `${(item.val / data.monthlyBudget) * 100}%`, backgroundColor: item.color }} />
                          </div>
                          <span className="text-sm font-semibold text-gray-700 w-16 text-right">{item.val} €</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {step === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h2 className="section-title text-3xl">Votre objectif principal</h2>
                <p className="section-subtitle text-base">Sur quoi souhaitez-vous concentrer vos efforts ?</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {goals.map((g) => (
                    <button
                      key={g.id}
                      onClick={() => setData({ ...data, goal: g.id })}
                      className={`p-5 rounded-2xl border-2 text-left transition-all duration-200 hover:-translate-y-0.5 ${
                        data.goal === g.id
                          ? 'border-primary-500 bg-primary-50 shadow-card-hover'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      }`}
                    >
                      <span className="text-2xl block mb-2">{g.icon}</span>
                      <span className="font-semibold text-gray-900 block">{g.label}</span>
                      <span className="text-sm text-gray-500">{g.desc}</span>
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {step === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h2 className="section-title text-3xl">Maturité du projet</h2>
                <p className="section-subtitle text-base">À quel stade se trouve votre projet aujourd'hui ?</p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {maturities.map((m) => (
                    <button
                      key={m.id}
                      onClick={() => setData({ ...data, maturity: m.id })}
                      className={`p-5 rounded-2xl border-2 text-center transition-all duration-200 hover:-translate-y-0.5 ${
                        data.maturity === m.id
                          ? 'border-primary-500 bg-primary-50 shadow-card-hover'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      }`}
                    >
                      <span className="text-3xl block mb-3">{m.icon}</span>
                      <span className="font-semibold text-gray-900 block mb-1">{m.label}</span>
                      <span className="text-xs text-gray-500">{m.desc}</span>
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {step === 5 && (
              <motion.div
                key="step5"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <h2 className="section-title text-3xl">Avez-vous un site existant ?</h2>
                <p className="section-subtitle text-base">Optionnel — nous l'analyserons (performance, SEO, vitesse).</p>
                <div className="card">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">URL de votre site web</label>
                  <input
                    type="url"
                    placeholder="https://monsite.fr"
                    value={data.websiteUrl}
                    onChange={(e) => setData({ ...data, websiteUrl: e.target.value })}
                    className="input-field"
                  />
                  <p className="text-xs text-gray-400 mt-2">Nous utilisons Google PageSpeed Insights pour analyser votre site.</p>
                </div>
                <div className="card mt-6" style={{ background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF0F7 100%)' }}>
                  <h3 className="font-semibold text-gray-900 mb-4">Récapitulatif</h3>
                  <div className="space-y-2 text-sm">
                    {[
                      { l: 'Activité', v: activityTypes.find(a => a.id === data.activityType)?.label },
                      { l: 'Capital', v: `${data.budget} €` },
                      { l: 'Budget/mois', v: `${data.monthlyBudget} €` },
                      { l: 'Objectif', v: goals.find(g => g.id === data.goal)?.label },
                      { l: 'Maturité', v: maturities.find(m => m.id === data.maturity)?.label },
                    ].map(({ l, v }) => (
                      <div key={l} className="flex justify-between">
                        <span className="text-gray-500">{l}</span>
                        <span className="font-medium text-gray-900 flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                          {v}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Navigation */}
          <div className="flex justify-between items-center mt-8">
            <button
              onClick={() => setStep(s => s - 1)}
              disabled={step === 1}
              className="btn-secondary disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-4 h-4" />
              Précédent
            </button>
            {step < TOTAL_STEPS ? (
              <button
                onClick={() => setStep(s => s + 1)}
                disabled={!canNext()}
                className="btn-primary disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Suivant
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="btn-primary disabled:opacity-70"
              >
                {loading ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Analyse en cours...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    Générer mon analyse
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
