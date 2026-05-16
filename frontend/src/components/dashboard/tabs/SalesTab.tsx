'use client';

import { useState } from 'react';
import { MessageSquare, Phone, Mail, ChevronRight, AlertTriangle, Zap, Brain, ChevronDown } from 'lucide-react';

interface SalesTabProps {
  data?: {
    scripts?: Array<{ title: string; type: string; content: string; keyPoints?: string[] }>;
    objections?: Array<{ objection: string; response: string }>;
    emailTemplates?: Array<{ subject: string; body: string; type: string }>;
    strategies?: Array<{ name: string; description: string; steps?: string[] }>;
  };
  copywriting?: {
    description?: string;
    aida?: Record<string, { principe: string; exemple: string; formules: string[]; conseil: string }>;
    triggers?: Array<{ trigger: string; definition: string; exemple: string; usage: string; avertissement: string }>;
    copywriting_principles?: string[];
  };
}

const TYPE_LABELS: Record<string, { label: string; color: string }> = {
  cold_call:     { label: 'Appel à froid',     color: 'text-blue-500' },
  follow_up:     { label: 'Suivi',              color: 'text-green-500' },
  discovery:     { label: 'Découverte',         color: 'text-purple-500' },
  email_outreach:{ label: 'Email prospection',  color: 'text-amber-500' },
  email_followup:{ label: 'Email suivi',        color: 'text-orange-500' },
};

const AIDA_META: Record<string, { emoji: string; color: string; bg: string }> = {
  attention: { emoji: '🎯', color: 'text-red-600',     bg: 'bg-red-50 border-red-200' },
  interest:  { emoji: '💡', color: 'text-amber-600',   bg: 'bg-amber-50 border-amber-200' },
  desire:    { emoji: '💜', color: 'text-purple-600',  bg: 'bg-purple-50 border-purple-200' },
  action:    { emoji: '🚀', color: 'text-emerald-600', bg: 'bg-emerald-50 border-emerald-200' },
};

export default function SalesTab({ data, copywriting }: SalesTabProps) {
  const [activeScript, setActiveScript] = useState(0);
  const [activeTrigger, setActiveTrigger] = useState<number | null>(null);

  const scripts = data?.scripts ?? [];
  const currentScript = scripts[activeScript] ?? null;

  return (
    <div className="space-y-10">

      {/* ── Scripts de vente ───────────────────────────────────────────────── */}
      {scripts.length > 0 && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Phone className="w-5 h-5 text-primary-500" /> Scripts de vente
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="space-y-2">
              {scripts.map((script, i) => {
                const meta = TYPE_LABELS[script.type] ?? { label: script.type, color: 'text-gray-500' };
                return (
                  <button
                    key={`script-${i}-${script.type}`}
                    onClick={() => setActiveScript(i)}
                    className={`w-full text-left p-3 rounded-xl border-2 transition-all text-sm
                      ${activeScript === i ? 'border-primary-500 bg-primary-50' : 'border-gray-200 bg-white hover:border-gray-300'}`}
                  >
                    <span className="font-medium text-gray-700 block truncate">{script.title}</span>
                    <span className={`text-xs mt-0.5 block ${meta.color}`}>{meta.label}</span>
                  </button>
                );
              })}
            </div>
            {currentScript && (
              <div className="lg:col-span-2 card">
                <h3 className="font-bold text-gray-900 mb-3">{currentScript.title}</h3>
                <div className="bg-gray-50 rounded-xl p-4 mb-4">
                  <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap break-words">{currentScript.content}</p>
                </div>
                {currentScript.keyPoints?.length ? (
                  <div>
                    <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Points clés</p>
                    <ul className="space-y-1.5">
                      {currentScript.keyPoints.map((kp, j) => (
                        <li key={`kp-${j}`} className="flex items-start gap-2 text-sm text-gray-600">
                          <ChevronRight className="w-3.5 h-3.5 text-primary-500 mt-0.5 flex-shrink-0" />{kp}
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </div>
            )}
          </div>
        </section>
      )}

      {/* ── AIDA Copywriting ───────────────────────────────────────────────── */}
      {copywriting?.aida && (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" /> Structure AIDA — Copywriting persuasif
          </h2>
          <p className="text-sm text-gray-500 mb-5">
            {copywriting.description ?? "Le copywriting fusionne sciences comportementales et rédaction persuasive pour produire des pages de vente, emails et posts qui déclenchent l'action."}
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(copywriting.aida).map(([step, content]) => {
              const meta = AIDA_META[step] ?? { emoji: '📌', color: 'text-gray-600', bg: 'bg-gray-50 border-gray-200' };
              return (
                <div key={`aida-${step}`} className={`rounded-2xl border-2 p-5 ${meta.bg}`}>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-2xl">{meta.emoji}</span>
                    <h3 className={`font-bold text-lg ${meta.color} uppercase`}>{step}</h3>
                  </div>
                  <p className="text-sm font-semibold text-gray-900 mb-2">{content.principe}</p>
                  <div className="bg-white/70 rounded-xl p-3 mb-3">
                    <p className="text-xs font-semibold text-gray-500 mb-1">Exemple :</p>
                    <p className="text-sm text-gray-700 italic">"{content.exemple}"</p>
                  </div>
                  <div className="space-y-1 mb-3">
                    <p className="text-xs font-semibold text-gray-500">Formules testées :</p>
                    {content.formules.map((f, i) => (
                      <p key={`f-${i}`} className="text-xs text-gray-600 flex gap-1.5">
                        <span className={`font-bold ${meta.color} flex-shrink-0`}>→</span>{f}
                      </p>
                    ))}
                  </div>
                  <div className="bg-white/50 rounded-lg px-3 py-2">
                    <p className="text-xs text-gray-500"><span className="font-semibold">💡 Conseil : </span>{content.conseil}</p>
                  </div>
                </div>
              );
            })}
          </div>
          {copywriting.copywriting_principles?.length ? (
            <div className="mt-4 card-sm bg-gray-50">
              <p className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">📐 Principes universels du copywriting</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {copywriting.copywriting_principles.map((p, i) => (
                  <div key={`cp-${i}`} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-primary-500 font-bold flex-shrink-0">{i + 1}.</span>{p}
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </section>
      )}

      {/* ── Déclencheurs psychologiques ────────────────────────────────────── */}
      {copywriting?.triggers?.length ? (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-500" /> Déclencheurs psychologiques
          </h2>
          <p className="text-sm text-gray-500 mb-5">
            Les sciences comportementales identifient des leviers cognitifs qui guident la décision d'achat — à utiliser avec éthique et authenticité.
          </p>
          <div className="space-y-3">
            {copywriting.triggers.map((trig, i) => {
              const isOpen = activeTrigger === i;
              return (
                <div key={`trig-${i}`} className="card-sm overflow-hidden">
                  <button onClick={() => setActiveTrigger(isOpen ? null : i)} className="w-full flex items-center gap-3 text-left">
                    <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center flex-shrink-0">
                      <span className="text-purple-600 font-bold text-sm">{i + 1}</span>
                    </div>
                    <span className="font-semibold text-gray-900 text-sm flex-1">{trig.trigger}</span>
                    <ChevronDown className={`w-4 h-4 text-gray-400 flex-shrink-0 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                  </button>
                  {isOpen && (
                    <div className="mt-3 pt-3 border-t border-gray-100 grid grid-cols-1 sm:grid-cols-2 gap-3 animate-fade-in">
                      <div className="bg-gray-50 rounded-xl p-3">
                        <p className="text-xs font-semibold text-gray-500 mb-1">Définition</p>
                        <p className="text-sm text-gray-700">{trig.definition}</p>
                      </div>
                      <div className="bg-primary-50 rounded-xl p-3">
                        <p className="text-xs font-semibold text-primary-600 mb-1">Exemple concret</p>
                        <p className="text-sm text-primary-700 italic">"{trig.exemple}"</p>
                      </div>
                      <div className="bg-emerald-50 rounded-xl p-3">
                        <p className="text-xs font-semibold text-emerald-600 mb-1">Usage recommandé</p>
                        <p className="text-sm text-emerald-700">{trig.usage}</p>
                      </div>
                      <div className="bg-amber-50 rounded-xl p-3">
                        <p className="text-xs font-semibold text-amber-600 mb-1">⚠ Avertissement</p>
                        <p className="text-sm text-amber-700">{trig.avertissement}</p>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      ) : null}

      {/* ── Objections ─────────────────────────────────────────────────────── */}
      {data?.objections?.length ? (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" /> Gestion des objections
          </h2>
          <div className="space-y-4">
            {data.objections.map((obj, i) => (
              <div key={`obj-${i}-${obj.objection.slice(0,20)}`} className="card border-l-4 border-l-amber-400">
                <p className="font-semibold text-gray-900 mb-2 text-sm">💬 &ldquo;{obj.objection}&rdquo;</p>
                <p className="text-sm text-gray-600 leading-relaxed">{obj.response}</p>
              </div>
            ))}
          </div>
        </section>
      ) : null}

      {/* ── Email templates ────────────────────────────────────────────────── */}
      {data?.emailTemplates?.length ? (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Mail className="w-5 h-5 text-primary-500" /> Templates d'emails
          </h2>
          <div className="space-y-4">
            {data.emailTemplates.map((tpl, i) => (
              <details key={`email-${i}-${tpl.type}`} className="card group">
                <summary className="cursor-pointer font-semibold text-gray-900 text-sm flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <Mail className="w-4 h-4 text-primary-400 flex-shrink-0" />
                    Objet : {tpl.subject}
                  </span>
                  <ChevronRight className="w-4 h-4 text-gray-400 group-open:rotate-90 transition-transform flex-shrink-0" />
                </summary>
                <div className="mt-4 bg-gray-50 rounded-xl p-4">
                  <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap break-words">{tpl.body}</p>
                </div>
              </details>
            ))}
          </div>
        </section>
      ) : null}

      {/* ── Stratégies commerciales ────────────────────────────────────────── */}
      {data?.strategies?.length ? (
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-purple-500" /> Stratégies commerciales
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {data.strategies.map((strat, i) => (
              <div key={`strat-${i}-${strat.name}`} className="card">
                <h3 className="font-bold text-gray-900 mb-2 text-sm">{strat.name}</h3>
                <p className="text-sm text-gray-500 mb-3">{strat.description}</p>
                {strat.steps?.length ? (
                  <ol className="space-y-1.5">
                    {strat.steps.map((step, j) => (
                      <li key={`step-${i}-${j}`} className="flex items-start gap-2 text-xs text-gray-600">
                        <span className="w-4 h-4 rounded-full bg-primary-100 text-primary-600 text-xs flex items-center justify-center flex-shrink-0 mt-0.5 font-bold">{j + 1}</span>
                        {step}
                      </li>
                    ))}
                  </ol>
                ) : null}
              </div>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
