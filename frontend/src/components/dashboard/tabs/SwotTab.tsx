'use client';

import { useState } from 'react';
import { CheckCircle2, AlertTriangle, Rocket, Shield, HelpCircle, Globe, Users, ChevronDown } from 'lucide-react';

/* ─── Types ─────────────────────────────────────────────────────────────────── */
interface SwotTabProps {
  data?: {
    strengths?: string[];
    weaknesses?: string[];
    opportunities?: string[];
    threats?: string[];
  };
  qqoqccp?: {
    description?: string;
    questions?: Record<string, { question: string; reponse: string; action: string }>;
    goal_focus?: string;
    maturity_note?: string;
  };
  pestel?: {
    description?: string;
    dimensions?: Record<string, Array<{ facteur: string; impact: string; note: string }>>;
  };
  microEnv?: {
    description?: string;
    acteurs?: Record<string, { pouvoir: string; description: string; levier: string }>;
  };
  competitive?: {
    description?: string;
    direct_rivals?: string[];
    indirect_rivals?: string[];
    competitive_matrix?: Array<{ critere: string; vous: string; leader: string; note: string }>;
    positioning_opportunity?: string;
    moat?: string;
  };
  input?: {
    activityType?: string;
    goal?: string;
    maturity?: string;
    budget?: number;
    monthlyBudget?: number;
  };
}

/* ─── Constants ─────────────────────────────────────────────────────────────── */
const SWOT_SECTIONS = [
  { key: 'strengths'     as const, title: 'Forces',       subtitle: 'Avantages compétitifs internes',  icon: CheckCircle2, emoji: '✅', border: 'border-emerald-200', header: 'bg-emerald-50',  dot: 'bg-emerald-500',  text: 'text-emerald-600' },
  { key: 'weaknesses'    as const, title: 'Faiblesses',    subtitle: 'Points à améliorer',              icon: AlertTriangle, emoji: '⚠️', border: 'border-amber-200',  header: 'bg-amber-50',   dot: 'bg-amber-500',    text: 'text-amber-600' },
  { key: 'opportunities' as const, title: 'Opportunités',  subtitle: 'Facteurs externes favorables',   icon: Rocket,        emoji: '🚀', border: 'border-blue-200',   header: 'bg-blue-50',    dot: 'bg-primary-500',  text: 'text-primary-600' },
  { key: 'threats'       as const, title: 'Menaces',       subtitle: 'Risques externes à anticiper',   icon: Shield,        emoji: '🔴', border: 'border-red-200',    header: 'bg-red-50',     dot: 'bg-red-500',      text: 'text-red-600' },
];

const QQOQCCP_LABELS: Record<string, { label: string; emoji: string }> = {
  qui:      { label: 'QUI ?',     emoji: '👤' },
  quoi:     { label: 'QUOI ?',    emoji: '📦' },
  ou:       { label: 'OÙ ?',      emoji: '📍' },
  quand:    { label: 'QUAND ?',   emoji: '⏰' },
  comment:  { label: 'COMMENT ?', emoji: '⚙️' },
  combien:  { label: 'COMBIEN ?', emoji: '💰' },
  pourquoi: { label: 'POURQUOI ?',emoji: '🎯' },
};

const IMPACT_BADGE: Record<string, string> = {
  positif: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  négatif: 'bg-red-50    text-red-700    border-red-200',
  neutre:  'bg-gray-100  text-gray-600   border-gray-200',
};

const POUVOIR_COLOR: Record<string, string> = {
  'très élevé': 'text-red-600',
  'élevé':      'text-amber-600',
  'moyen':      'text-blue-600',
  'faible':     'text-emerald-600',
};

const PESTEL_COLORS: Record<string, string> = {
  politique:     'bg-blue-50   border-blue-200   text-blue-700',
  economique:    'bg-green-50  border-green-200  text-green-700',
  socioculturel: 'bg-purple-50 border-purple-200 text-purple-700',
  technologique: 'bg-cyan-50   border-cyan-200   text-cyan-700',
  ecologique:    'bg-emerald-50 border-emerald-200 text-emerald-700',
  legal:         'bg-amber-50  border-amber-200  text-amber-700',
};

const PESTEL_ICONS: Record<string, string> = {
  politique: '🏛️', economique: '📈', socioculturel: '👥',
  technologique: '💻', ecologique: '🌿', legal: '⚖️',
};

const MATURITY_LABELS: Record<string, string> = { idea: 'Idée', inprogress: 'En cours', launched: 'Lancé' };
const GOAL_LABELS: Record<string, string>     = { awareness: 'Notoriété', sales: 'Ventes', leads: 'Leads', traffic: 'Trafic' };
const ACTIVITY_LABELS: Record<string, string> = {
  ecommerce: 'E-commerce', saas: 'SaaS', service: 'Service en ligne',
  website: 'Site vitrine', application: 'App mobile', content: 'Création contenu',
  consulting: 'Conseil', other: 'Autre',
};

/* ─── Component ─────────────────────────────────────────────────────────────── */
export default function SwotTab({ data, qqoqccp, pestel, microEnv, competitive, input }: SwotTabProps) {
  const [activeQQ, setActiveQQ]       = useState<string | null>(null);
  const [expandedPestel, setExpandedPestel] = useState<string | null>(null);

  return (
    <div className="space-y-10">

      {/* ── Context badges ─────────────────────────────────────────────────── */}
      {input && (
        <div className="flex flex-wrap gap-2 animate-fade-in">
          {input.activityType  && <span className="badge badge-primary">{ACTIVITY_LABELS[input.activityType] ?? input.activityType}</span>}
          {input.goal          && <span className="badge badge-success">🎯 {GOAL_LABELS[input.goal] ?? input.goal}</span>}
          {input.maturity      && <span className="badge badge-gray">{MATURITY_LABELS[input.maturity] ?? input.maturity}</span>}
          {input.monthlyBudget && <span className="badge badge-warning">💰 {input.monthlyBudget} €/mois</span>}
        </div>
      )}

      {/* ── SWOT Grid ──────────────────────────────────────────────────────── */}
      {data && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2">🔍 Analyse SWOT</h2>
          <p className="text-sm text-gray-500 mb-5">
            L'analyse SWOT structure toute réflexion stratégique en croisant forces et faiblesses internes
            avec opportunités et menaces externes pour poser un diagnostic objectif et actionnable.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {SWOT_SECTIONS.map((s, si) => {
              const items = data[s.key] ?? [];
              return (
                <div key={s.key} className={`rounded-2xl border-2 ${s.border} overflow-hidden animate-fade-in`}
                  style={{ animationDelay: `${si * 80}ms` }}>
                  <div className={`${s.header} px-5 py-4 flex items-center gap-3`}>
                    <s.icon className={`w-5 h-5 ${s.text}`} />
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-900">{s.emoji} {s.title}</h3>
                      <p className="text-xs text-gray-500">{s.subtitle}</p>
                    </div>
                    <span className={`w-6 h-6 rounded-full ${s.dot} text-white text-xs font-bold flex items-center justify-center`}>{items.length}</span>
                  </div>
                  <div className="bg-white px-5 py-4">
                    {items.length > 0 ? (
                      <ul className="space-y-2.5">
                        {items.map((item, j) => (
                          <li key={`${s.key}-${j}`} className="flex items-start gap-2.5 text-sm text-gray-700">
                            <span className={`w-1.5 h-1.5 rounded-full ${s.dot} mt-2 flex-shrink-0`} />
                            <span className="leading-relaxed">{item}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-sm text-gray-400 italic">Aucun élément</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
          {/* Insight card */}
          <div className="mt-5 card" style={{ background: 'linear-gradient(135deg,#F0F9FF,#FFF0F7)' }}>
            <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
              <Rocket className="w-4 h-4 text-primary-500" /> Insight stratégique
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
              {SWOT_SECTIONS.map(s => (
                <div key={s.key}>
                  <p className={`text-3xl font-bold ${s.text}`}>{(data[s.key] ?? []).length}</p>
                  <p className="text-xs text-gray-500 mt-1">{s.title}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ── QQOQCCP ────────────────────────────────────────────────────────── */}
      {qqoqccp?.questions && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2">❓ QQOQCCP — Questionnement stratégique</h2>
          <p className="text-sm text-gray-500 mb-1">
            {qqoqccp.description ?? "Le QQOQCCP systématise le questionnement pour ne laisser aucune zone d'ombre dans la compréhension d'une situation ou d'un besoin client."}
          </p>
          {qqoqccp.goal_focus && (
            <div className="mb-4 px-4 py-2.5 bg-primary-50 border border-primary-100 rounded-xl text-sm text-primary-700">
              💡 {qqoqccp.goal_focus}
            </div>
          )}
          <div className="space-y-3">
            {Object.entries(qqoqccp.questions).map(([key, val]) => {
              const meta   = QQOQCCP_LABELS[key] ?? { label: key.toUpperCase(), emoji: '❓' };
              const isOpen = activeQQ === key;
              return (
                <div key={`qq-${key}`} className="card-sm overflow-hidden">
                  <button
                    onClick={() => setActiveQQ(isOpen ? null : key)}
                    className="w-full flex items-center gap-3 text-left"
                  >
                    <span className="text-xl flex-shrink-0">{meta.emoji}</span>
                    <div className="flex-1 min-w-0">
                      <span className="text-xs font-bold text-primary-500 block">{meta.label}</span>
                      <span className="text-sm font-semibold text-gray-900">{val.question}</span>
                    </div>
                    <ChevronDown className={`w-4 h-4 text-gray-400 flex-shrink-0 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                  </button>
                  {isOpen && (
                    <div className="mt-3 pt-3 border-t border-gray-100 space-y-2 animate-fade-in">
                      <div className="bg-gray-50 rounded-xl p-3">
                        <p className="text-xs font-semibold text-gray-500 mb-1">Analyse</p>
                        <p className="text-sm text-gray-700">{val.reponse}</p>
                      </div>
                      <div className="bg-primary-50 rounded-xl p-3">
                        <p className="text-xs font-semibold text-primary-600 mb-1">→ Action recommandée</p>
                        <p className="text-sm text-primary-700">{val.action}</p>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          {qqoqccp.maturity_note && (
            <p className="mt-3 text-xs text-gray-400 italic">📌 {qqoqccp.maturity_note}</p>
          )}
        </section>
      )}

      {/* ── PESTEL ─────────────────────────────────────────────────────────── */}
      {pestel?.dimensions && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2">🌍 Analyse PESTEL</h2>
          <p className="text-sm text-gray-500 mb-5">
            {pestel.description ?? "L'analyse PESTEL cartographie le macro-environnement — ces forces externes que l'entreprise ne contrôle pas mais qu'elle doit impérativement anticiper."}
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(pestel.dimensions).map(([dim, items]) => {
              const color  = PESTEL_COLORS[dim] ?? 'bg-gray-50 border-gray-200 text-gray-700';
              const icon   = PESTEL_ICONS[dim]  ?? '📋';
              const isOpen = expandedPestel === dim;
              return (
                <div key={`pestel-${dim}`} className={`rounded-2xl border-2 overflow-hidden ${color.split(' ').slice(0,2).join(' ')}`}>
                  <button
                    onClick={() => setExpandedPestel(isOpen ? null : dim)}
                    className="w-full px-4 py-3 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{icon}</span>
                      <span className={`font-bold capitalize text-sm ${color.split(' ')[2]}`}>{dim}</span>
                      <span className="text-xs text-gray-400">({(items as any[]).length})</span>
                    </div>
                    <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                  </button>
                  {isOpen && (
                    <div className="bg-white px-4 pb-4 space-y-3 animate-fade-in">
                      {(items as Array<{ facteur: string; impact: string; note: string }>).map((item, i) => (
                        <div key={`p-${dim}-${i}`} className="bg-gray-50 rounded-xl p-3">
                          <div className="flex items-start justify-between gap-2 mb-1">
                            <p className="text-sm font-semibold text-gray-900 flex-1">{item.facteur}</p>
                            <span className={`badge border text-xs flex-shrink-0 ${IMPACT_BADGE[item.impact] ?? IMPACT_BADGE.neutre}`}>
                              {item.impact}
                            </span>
                          </div>
                          <p className="text-xs text-gray-500">{item.note}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* ── Micro-environnement ────────────────────────────────────────────── */}
      {microEnv?.acteurs && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2">🔗 Micro-environnement</h2>
          <p className="text-sm text-gray-500 mb-5">
            {microEnv.description ?? "Le micro-environnement englobe les acteurs en interaction directe dont le pouvoir de négociation et l'influence modèlent la chaîne de valeur au quotidien."}
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(microEnv.acteurs).map(([acteur, info]) => {
              const i = info as { pouvoir: string; description: string; levier: string };
              return (
                <div key={`micro-${acteur}`} className="card-sm">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-gray-400" />
                      <span className="font-bold text-gray-900 capitalize text-sm">{acteur}</span>
                    </div>
                    <span className={`text-xs font-bold ${POUVOIR_COLOR[i.pouvoir] ?? 'text-gray-500'}`}>
                      Pouvoir : {i.pouvoir}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{i.description}</p>
                  <div className="bg-emerald-50 rounded-lg px-3 py-2">
                    <p className="text-xs text-emerald-700"><span className="font-semibold">Levier : </span>{i.levier}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* ── Analyse concurrentielle ────────────────────────────────────────── */}
      {competitive && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2">⚔️ Analyse concurrentielle</h2>
          <p className="text-sm text-gray-500 mb-5">
            {competitive.description ?? "L'analyse concurrentielle identifie rivaux directs et indirects et révèle les avantages compétitifs inexploités."}
          </p>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Rivaux */}
            <div className="space-y-4">
              {competitive.direct_rivals?.length ? (
                <div className="card-sm">
                  <p className="text-xs font-bold text-red-500 uppercase tracking-wider mb-3">⚡ Concurrents directs</p>
                  <ul className="space-y-2">
                    {competitive.direct_rivals.map((r, i) => (
                      <li key={`dr-${i}`} className="flex items-center gap-2 text-sm text-gray-700">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-400 flex-shrink-0" />{r}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
              {competitive.indirect_rivals?.length ? (
                <div className="card-sm">
                  <p className="text-xs font-bold text-amber-500 uppercase tracking-wider mb-3">💡 Concurrents indirects</p>
                  <ul className="space-y-2">
                    {competitive.indirect_rivals.map((r, i) => (
                      <li key={`ir-${i}`} className="flex items-center gap-2 text-sm text-gray-700">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-400 flex-shrink-0" />{r}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
              {competitive.moat && (
                <div className="card-sm bg-primary-50 border-primary-100">
                  <p className="text-xs font-bold text-primary-600 uppercase tracking-wider mb-2">🏰 Votre moat</p>
                  <p className="text-sm text-primary-700">{competitive.moat}</p>
                </div>
              )}
            </div>

            {/* Matrice compétitive */}
            {competitive.competitive_matrix?.length ? (
              <div className="lg:col-span-2 card-sm overflow-x-auto">
                <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">📊 Matrice compétitive</p>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-100">
                      <th className="text-left py-2 pr-3 text-xs text-gray-500 font-semibold">Critère</th>
                      <th className="text-center py-2 px-3 text-xs text-primary-600 font-bold">Vous</th>
                      <th className="text-center py-2 px-3 text-xs text-gray-500 font-semibold">Leader</th>
                      <th className="text-left py-2 pl-3 text-xs text-gray-500 font-semibold">Note</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {competitive.competitive_matrix.map((row, i) => (
                      <tr key={`cm-${i}`} className="hover:bg-gray-50">
                        <td className="py-2.5 pr-3 font-medium text-gray-900 text-xs">{row.critere}</td>
                        <td className="py-2.5 px-3 text-center text-base">{row.vous}</td>
                        <td className="py-2.5 px-3 text-center text-base">{row.leader}</td>
                        <td className="py-2.5 pl-3 text-xs text-gray-500 max-w-[180px]">
                          <span className="line-clamp-2">{row.note}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {competitive.positioning_opportunity && (
                  <div className="mt-4 bg-emerald-50 rounded-xl px-4 py-3">
                    <p className="text-xs font-bold text-emerald-600 mb-1">🎯 Opportunité de positionnement</p>
                    <p className="text-sm text-emerald-700">{competitive.positioning_opportunity}</p>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </section>
      )}
    </div>
  );
}
