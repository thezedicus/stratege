'use client';

import Link from 'next/link';
import { Zap, ArrowRight, BarChart2, Target, TrendingUp, Shield, Users, Star } from 'lucide-react';

const FEATURES = [
  {
    icon: BarChart2,
    title: 'Analyse SWOT',
    desc: 'Forces, faiblesses, opportunités et menaces détectées automatiquement selon votre secteur.',
    color: 'text-emerald-500',
    bg: 'bg-emerald-50',
  },
  {
    icon: Users,
    title: 'Personas client',
    desc: 'Profils détaillés de vos clients idéaux avec objectifs, douleurs et comportements.',
    color: 'text-primary-500',
    bg: 'bg-primary-50',
  },
  {
    icon: Target,
    title: 'Plan marketing',
    desc: "Stratégie de contenu, calendrier éditorial et répartition budgétaire personnalisée.",
    color: 'text-purple-500',
    bg: 'bg-purple-50',
  },
  {
    icon: TrendingUp,
    title: 'SEO & GEO',
    desc: 'Mots-clés prioritaires, audit technique et stratégie de référencement naturel.',
    color: 'text-amber-500',
    bg: 'bg-amber-50',
  },
  {
    icon: Shield,
    title: 'Plan publicitaire',
    desc: 'Mediaplan multi-canal avec budgets, audiences et créatifs recommandés.',
    color: 'text-magenta-500',
    bg: 'bg-pink-50',
  },
  {
    icon: Star,
    title: 'Synthèse 360°',
    desc: 'Tableau de bord unifié avec score stratégique, métriques clés et plan d\'action prioritisé.',
    color: 'text-orange-500',
    bg: 'bg-orange-50',
  },
];

const STEPS = [
  { n: '01', title: 'Décrivez votre projet', desc: 'Type d\'activité, budget, objectif et maturité en 2 minutes.' },
  { n: '02', title: 'Analyse automatique',  desc: 'Notre IA génère votre rapport 360° personnalisé instantanément.' },
  { n: '03', title: 'Passez à l\'action',   desc: 'Suivez votre plan et exportez votre rapport PDF complet.' },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="border-b border-gray-100 sticky top-0 bg-white/95 backdrop-blur-sm z-40">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-gray-900 text-lg">Stratège</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/wizard" className="btn-secondary text-sm hidden sm:inline-flex">
              Se connecter
            </Link>
            <Link href="/wizard" className="btn-primary text-sm">
              Commencer gratuitement
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="animate-fade-in">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-50 text-primary-600 text-sm font-semibold mb-6">
            <Zap className="w-3.5 h-3.5" />
            Analyse stratégique propulsée par l'IA
          </span>
          <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 leading-tight mb-6">
            Votre stratégie 360°<br />
            <span className="gradient-text">en 60 secondes</span>
          </h1>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto mb-10">
            SWOT, personas, marketing, SEO, publicité et plan d'action — tout ce dont vous avez besoin
            pour lancer et développer votre projet, généré automatiquement.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/wizard" className="btn-primary text-base px-8 py-3">
              <Zap className="w-5 h-5" />
              Générer mon analyse gratuite
              <ArrowRight className="w-4 h-4" />
            </Link>
            <a href="#features" className="btn-secondary text-base px-8 py-3">
              Voir les fonctionnalités
            </a>
          </div>
          <p className="text-sm text-gray-400 mt-4">Gratuit · Sans inscription · Export PDF inclus</p>
        </div>

        {/* Mock dashboard preview */}
        <div className="mt-16 animate-fade-in delay-200 relative">
          <div className="bg-gray-50 rounded-3xl border border-gray-200 p-6 text-left shadow-xl">
            <div className="flex gap-2 mb-4">
              {['🔍 Diagnostic','👥 Personas','💬 Vente','📣 Marketing','🔎 SEO & GEO','📱 Publicité','📊 Synthèse'].map((t, i) => (
                <span key={i} className={`px-3 py-1.5 rounded-lg text-xs font-medium ${i === 0 ? 'bg-primary-500 text-white' : 'bg-white text-gray-600 border border-gray-200'}`}>{t}</span>
              ))}
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: 'Forces', count: '4 identifiées', color: 'bg-emerald-50 border-emerald-100', dot: 'bg-emerald-500' },
                { label: 'Opportunités', count: '3 détectées', color: 'bg-blue-50 border-blue-100', dot: 'bg-blue-500' },
                { label: 'Score SEO', count: '78 / 100', color: 'bg-purple-50 border-purple-100', dot: 'bg-purple-500' },
                { label: 'Budget/mois', count: '200 € optimisés', color: 'bg-pink-50 border-pink-100', dot: 'bg-pink-500' },
              ].map(c => (
                <div key={c.label} className={`rounded-xl border p-4 ${c.color}`}>
                  <div className={`w-2 h-2 rounded-full ${c.dot} mb-2`} />
                  <p className="text-xs text-gray-500">{c.label}</p>
                  <p className="font-bold text-gray-900 text-sm mt-0.5">{c.count}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="bg-gray-50 py-20">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Tout ce qu'il vous faut pour réussir
            </h2>
            <p className="text-gray-500 text-lg max-w-xl mx-auto">
              6 modules complets générés en quelques secondes, adaptés à votre secteur et vos objectifs.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f, i) => (
              <div
                key={f.title}
                className="card hover:shadow-card-hover transition-shadow duration-200 animate-fade-in"
                style={{ animationDelay: `${i * 80}ms` }}
              >
                <div className={`w-10 h-10 rounded-xl ${f.bg} flex items-center justify-center mb-4`}>
                  <f.icon className={`w-5 h-5 ${f.color}`} />
                </div>
                <h3 className="font-bold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">Comment ça marche</h2>
            <p className="text-gray-500 text-lg">Simple, rapide, actionnable.</p>
          </div>
          <div className="space-y-6">
            {STEPS.map((s, i) => (
              <div
                key={s.n}
                className="flex gap-6 items-start animate-fade-in"
                style={{ animationDelay: `${i * 120}ms` }}
              >
                <div className="w-14 h-14 rounded-2xl bg-gradient-primary flex items-center justify-center flex-shrink-0 shadow-glow">
                  <span className="text-white font-bold text-sm">{s.n}</span>
                </div>
                <div>
                  <h3 className="font-bold text-gray-900 text-lg mb-1">{s.title}</h3>
                  <p className="text-gray-500">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-primary">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Prêt à accélérer votre croissance ?
          </h2>
          <p className="text-white/80 text-lg mb-8">
            Rejoignez des centaines d'entrepreneurs qui utilisent Stratège pour piloter leur développement.
          </p>
          <Link href="/wizard" className="inline-flex items-center gap-2 bg-white text-primary-600 font-bold px-8 py-3.5 rounded-xl hover:bg-gray-50 transition-colors text-base shadow-lg">
            <Zap className="w-5 h-5" />
            Lancer mon analyse gratuite
            <ArrowRight className="w-4 h-4" />
          </Link>
          <p className="text-white/60 text-sm mt-4">Aucune carte de crédit requise</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md bg-gradient-primary flex items-center justify-center">
              <Zap className="w-3 h-3 text-white" />
            </div>
            <span className="font-bold text-gray-700">Stratège</span>
          </div>
          <p className="text-sm text-gray-400">
            © {new Date().getFullYear()} Stratège · Analyse stratégique 360° propulsée par l'IA
          </p>
        </div>
      </footer>
    </div>
  );
}
