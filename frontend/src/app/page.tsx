'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  BarChart3, Users, Target, TrendingUp, Zap, ArrowRight,
  CheckCircle2, Star, Brain, Rocket
} from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'Diagnostic Stratégique',
    desc: 'Analyse SWOT automatisée, forces & faiblesses selon votre secteur et budget.',
    color: 'text-primary-500',
    bg: 'bg-primary-50',
  },
  {
    icon: Users,
    title: 'Personas & Psychologie',
    desc: '5 personas détaillés avec SONCAS, AIDA, SPIN et leviers d\'achat impulsif.',
    color: 'text-magenta-500',
    bg: 'bg-magenta-50',
  },
  {
    icon: Target,
    title: 'Stratégie de Vente',
    desc: 'Scripts personnalisés, techniques de closing et messages par persona.',
    color: 'text-violet-500',
    bg: 'bg-violet-50',
  },
  {
    icon: TrendingUp,
    title: 'SEO, SEA & GEO',
    desc: 'Audit on-page, suggestions de mots-clés, campagnes Google Ads structurées.',
    color: 'text-emerald-500',
    bg: 'bg-emerald-50',
  },
  {
    icon: BarChart3,
    title: 'Marketing Digital',
    desc: 'Plan de contenu, calendrier éditorial, règle 80/20 et recommandations plateformes.',
    color: 'text-amber-500',
    bg: 'bg-amber-50',
  },
  {
    icon: Rocket,
    title: 'Rapport de Synthèse',
    desc: 'Actions prioritaires, estimation ROI et export PDF de votre analyse complète.',
    color: 'text-rose-500',
    bg: 'bg-rose-50',
  },
];

const steps = [
  { n: '01', title: 'Décrivez votre projet', desc: 'Activité, budget, objectifs et maturité en 5 minutes.' },
  { n: '02', title: 'Analyse en temps réel', desc: 'Notre moteur génère votre diagnostic 360° personnalisé.' },
  { n: '03', title: 'Passez à l\'action', desc: 'Suivez les recommandations priorisées et exportez en PDF.' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-gray-900 text-lg">Stratège</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/wizard" className="btn-primary text-sm px-5 py-2.5">
              Commencer gratuitement
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6" style={{ background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF0F7 100%)' }}>
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="badge-primary mb-4 inline-flex">
              <Star className="w-3 h-3 mr-1" />
              Expert virtuel disponible 24h/24
            </span>
            <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-6">
              Votre expert en{' '}
              <span className="gradient-text">stratégie business</span>
              {' '}à portée de main
            </h1>
            <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
              Qualifiez votre projet en 5 minutes et obtenez une analyse 360° complète :
              SWOT, personas, scripts de vente, plan SEO, media plan et ROI estimé.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/wizard" className="btn-primary text-base px-8 py-4">
                Analyser mon projet
                <ArrowRight className="w-5 h-5" />
              </Link>
              <a href="#fonctionnalites" className="btn-secondary text-base px-8 py-4">
                Voir les fonctionnalités
              </a>
            </div>
            <div className="flex items-center justify-center gap-6 mt-8 text-sm text-gray-500">
              {['Gratuit', 'Sans inscription', 'Résultats immédiats'].map((t) => (
                <span key={t} className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                  {t}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section id="fonctionnalites" className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Une analyse complète en un clic</h2>
            <p className="text-gray-500 text-lg max-w-xl mx-auto">
              Tous les outils d'un consultant senior, accessibles instantanément.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                className="card-hover"
              >
                <div className={`w-12 h-12 rounded-2xl ${f.bg} flex items-center justify-center mb-4`}>
                  <f.icon className={`w-6 h-6 ${f.color}`} />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Comment ça fonctionne ?</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((s, i) => (
              <motion.div
                key={s.n}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.15 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="w-14 h-14 rounded-2xl bg-gradient-primary text-white text-xl font-bold flex items-center justify-center mx-auto mb-4">
                  {s.n}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{s.title}</h3>
                <p className="text-gray-500 text-sm">{s.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-2xl mx-auto text-center">
          <div className="card" style={{ background: 'linear-gradient(135deg, #F0F9FF 0%, #FFF0F7 100%)' }}>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Prêt à accélérer votre croissance ?</h2>
            <p className="text-gray-600 mb-8">Commencez votre analyse 360° en moins de 5 minutes. Gratuit, sans compte requis.</p>
            <Link href="/wizard" className="btn-primary text-base px-8 py-4 inline-flex">
              Lancer mon analyse
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8 px-6 text-center text-sm text-gray-400">
        <div className="flex items-center justify-center gap-2 mb-2">
          <div className="w-6 h-6 rounded-md bg-gradient-primary flex items-center justify-center">
            <Zap className="w-3 h-3 text-white" />
          </div>
          <span className="font-semibold text-gray-600">Stratège</span>
        </div>
        <p>© {new Date().getFullYear()} Stratège — Expert virtuel en stratégie business</p>
      </footer>
    </div>
  );
}
