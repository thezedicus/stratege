'use client';

import Link from 'next/link';
import { Zap, ArrowRight, BarChart2, Target, TrendingUp } from 'lucide-react';

interface RightPanelProps {
  analysis?: {
    id?: string;
    input?: {
      activityType?: string;
      goal?: string;
      maturity?: string;
      budget?: number;
      monthlyBudget?: number;
    };
    swot?: { strengths?: string[]; weaknesses?: string[]; opportunities?: string[]; threats?: string[] };
    synthesis?: { score?: number; summary?: string };
  };
}

const QUICK_LINKS = [
  { href: '/wizard', label: 'Nouvelle analyse', icon: Zap, color: 'text-primary-500' },
  { href: '#swot',   label: 'Voir SWOT',         icon: BarChart2, color: 'text-emerald-500' },
  { href: '#ads',    label: 'Plan pub',            icon: Target, color: 'text-magenta-500' },
  { href: '#seo',    label: 'SEO & GEO',           icon: TrendingUp, color: 'text-purple-500' },
];

export default function RightPanel({ analysis }: RightPanelProps) {
  const inp = analysis?.input;
  const score = analysis?.synthesis?.score;

  return (
    <div className="p-5 space-y-6">
      {/* Score global */}
      {score !== undefined && (
        <div className="animate-fade-in">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Score stratégique</p>
          <div className="flex items-center gap-3">
            <div className="relative w-14 h-14 flex-shrink-0">
              <svg viewBox="0 0 56 56" className="w-14 h-14 -rotate-90">
                <circle cx="28" cy="28" r="24" fill="none" stroke="#f3f4f6" strokeWidth="5" />
                <circle
                  cx="28" cy="28" r="24"
                  fill="none"
                  stroke="url(#scoreGrad)"
                  strokeWidth="5"
                  strokeDasharray={`${(score / 100) * 150.8} 150.8`}
                  strokeLinecap="round"
                />
                <defs>
                  <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#38B6FF" />
                    <stop offset="100%" stopColor="#E20074" />
                  </linearGradient>
                </defs>
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-gray-900">
                {score}
              </span>
            </div>
            <div>
              <p className="font-semibold text-gray-900">Score global</p>
              <p className="text-xs text-gray-500">
                {score >= 70 ? 'Excellent potentiel' : score >= 50 ? 'Bon potentiel' : 'À optimiser'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Résumé projet */}
      {inp && (
        <div className="animate-fade-in delay-100">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Projet en cours</p>
          <div className="space-y-2">
            {[
              { l: 'Type', v: inp.activityType },
              { l: 'Objectif', v: inp.goal },
              { l: 'Maturité', v: inp.maturity },
              { l: 'Budget/mois', v: inp.monthlyBudget ? `${inp.monthlyBudget} €` : undefined },
            ].filter(r => r.v).map(({ l, v }) => (
              <div key={l} className="flex justify-between items-center text-sm">
                <span className="text-gray-400">{l}</span>
                <span className="font-medium text-gray-700 capitalize">{v}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Forces (top 3) */}
      {analysis?.swot?.strengths?.length ? (
        <div className="animate-fade-in delay-200">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Top forces</p>
          <ul className="space-y-2">
            {analysis.swot.strengths.slice(0, 3).map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-gray-600">
                <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                <span className="line-clamp-2">{s}</span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {/* Actions rapides */}
      <div className="animate-fade-in delay-300">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Actions rapides</p>
        <div className="space-y-1">
          {QUICK_LINKS.map(({ href, label, icon: Icon, color }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-gray-50
                         text-sm text-gray-700 font-medium transition-colors group"
            >
              <div className="flex items-center gap-2">
                <Icon className={`w-4 h-4 ${color}`} />
                {label}
              </div>
              <ArrowRight className="w-3.5 h-3.5 text-gray-300 group-hover:text-gray-500 transition-colors" />
            </Link>
          ))}
        </div>
      </div>

      {/* CTA nouvelle analyse */}
      <div className="animate-fade-in delay-400 pt-2 border-t border-gray-100">
        <Link
          href="/wizard"
          className="btn-primary w-full justify-center text-sm"
        >
          <Zap className="w-4 h-4" />
          Nouvelle analyse
        </Link>
      </div>
    </div>
  );
}
