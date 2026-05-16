import type { Metadata, Viewport } from 'next';
import { Toaster } from 'react-hot-toast';
import './globals.css';

export const metadata: Metadata = {
  title: 'Stratège — Analyse stratégique 360°',
  description: 'Générez votre plan marketing, SEO, publicité et commercial personnalisé en 60 secondes.',
  keywords: 'stratégie marketing, analyse SWOT, SEO, publicité, plan marketing',
  authors: [{ name: 'Stratège' }],
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              fontFamily: 'Inter, sans-serif',
              fontSize: '14px',
              borderRadius: '12px',
              boxShadow: '0 4px 12px rgb(0 0 0 / 0.1)',
            },
          }}
        />
      </body>
    </html>
  );
}
