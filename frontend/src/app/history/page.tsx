'use client';

import { Clock, Zap } from 'lucide-react';
import Link from 'next/link';
import AppShell from '@/components/layout/AppShell';

export default function HistoryPage() {
  return (
    <AppShell>
      <div className="min-h-screen flex items-center justify-center px-6">
        <div className="text-center max-w-sm">
          <div className="w-14 h-14 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <Clock className="w-7 h-7 text-gray-400" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Historique</h2>
          <p className="text-gray-500 text-sm mb-6">
            L&apos;historique de vos analyses sera disponible prochainement.
            Pour l&apos;instant, chaque analyse est accessible via son lien unique.
          </p>
          <Link href="/wizard" className="btn-primary">
            <Zap className="w-4 h-4" />
            Nouvelle analyse
          </Link>
        </div>
      </div>
    </AppShell>
  );
}
