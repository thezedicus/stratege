'use client';

import { Settings } from 'lucide-react';
import AppShell from '@/components/layout/AppShell';

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="min-h-screen flex items-center justify-center px-6">
        <div className="text-center max-w-sm">
          <div className="w-14 h-14 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <Settings className="w-7 h-7 text-gray-400" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Paramètres</h2>
          <p className="text-gray-500 text-sm">
            Les paramètres du compte arrivent prochainement.
          </p>
        </div>
      </div>
    </AppShell>
  );
}
