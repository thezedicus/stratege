'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Zap, LayoutDashboard, Wand2, History, Settings,
  ChevronLeft, ChevronRight, Menu, X
} from 'lucide-react';

const NAV_ITEMS = [
  { href: '/',        label: 'Accueil',    icon: LayoutDashboard },
  { href: '/wizard',  label: 'Nouvelle analyse', icon: Wand2 },
  { href: '/history', label: 'Historique', icon: History },
];

interface AppShellProps {
  children: React.ReactNode;
  rightPanel?: React.ReactNode;
}

export default function AppShell({ children, rightPanel }: AppShellProps) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* ── Mobile overlay ──────────────────────────────── */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* ── Left sidebar ────────────────────────────────── */}
      <aside
        className={`
          fixed top-0 left-0 h-full z-50 flex flex-col bg-white border-r border-gray-100
          transition-all duration-300 ease-in-out shadow-sm
          ${collapsed ? 'w-16' : 'w-64'}
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:static lg:z-auto
        `}
      >
        {/* Logo */}
        <div className={`flex items-center h-16 px-4 border-b border-gray-100 flex-shrink-0 ${collapsed ? 'justify-center' : 'gap-3'}`}>
          <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center flex-shrink-0">
            <Zap className="w-4 h-4 text-white" />
          </div>
          {!collapsed && (
            <span className="font-bold text-gray-900 text-lg">Stratège</span>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 space-y-1 px-2 overflow-y-auto scrollbar-hide">
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
            const active = pathname === href || (href !== '/' && pathname.startsWith(href));
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setMobileOpen(false)}
                title={collapsed ? label : undefined}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                  transition-all duration-150 group
                  ${active
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }
                  ${collapsed ? 'justify-center' : ''}
                `}
              >
                <Icon className={`w-4 h-4 flex-shrink-0 ${active ? 'text-primary-500' : ''}`} />
                {!collapsed && <span>{label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Settings + collapse toggle */}
        <div className="border-t border-gray-100 px-2 py-3 space-y-1">
          <Link
            href="/settings"
            title={collapsed ? 'Paramètres' : undefined}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-gray-600
              hover:bg-gray-50 hover:text-gray-900 transition-all duration-150
              ${collapsed ? 'justify-center' : ''}`}
          >
            <Settings className="w-4 h-4 flex-shrink-0" />
            {!collapsed && <span>Paramètres</span>}
          </Link>

          <button
            onClick={() => setCollapsed(c => !c)}
            title={collapsed ? 'Développer' : 'Réduire'}
            className={`hidden lg:flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium
              text-gray-400 hover:bg-gray-50 hover:text-gray-700 transition-all duration-150
              ${collapsed ? 'justify-center' : ''}`}
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            {!collapsed && <span className="text-xs">Réduire</span>}
          </button>
        </div>
      </aside>

      {/* ── Mobile header ───────────────────────────────── */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-30 bg-white border-b border-gray-100 h-14 flex items-center px-4 gap-3">
        <button
          onClick={() => setMobileOpen(true)}
          className="p-2 rounded-lg hover:bg-gray-100 text-gray-600"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-gradient-primary flex items-center justify-center">
            <Zap className="w-3.5 h-3.5 text-white" />
          </div>
          <span className="font-bold text-gray-900">Stratège</span>
        </div>
      </div>

      {/* ── Main content ────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0 pt-14 lg:pt-0">
        <main className="flex-1 flex min-h-0">
          <div className="flex-1 min-w-0 overflow-y-auto">
            {children}
          </div>

          {/* ── Right panel ─────────────────────────────── */}
          {rightPanel && (
            <aside className="hidden xl:flex w-80 flex-col border-l border-gray-100 bg-white overflow-y-auto scrollbar-thin">
              {rightPanel}
            </aside>
          )}
        </main>
      </div>
    </div>
  );
}
