import type { Metadata } from 'next';
import './globals.css';
import { Toaster } from 'react-hot-toast';

export const metadata: Metadata = {
  title: 'Stratège — Expert Virtuel en Stratégie Business',
  description: 'Analyse 360° de votre projet : stratégie, marketing, vente, communication. Recommandations personnalisées et actionnables.',
  keywords: 'stratégie business, marketing digital, vente, personas, SWOT, SEO',
  openGraph: {
    title: 'Stratège',
    description: 'Votre expert virtuel en stratégie business, marketing et vente',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-white min-h-screen">
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              borderRadius: '12px',
              boxShadow: '0 4px 24px -4px rgba(0,0,0,0.12)',
              fontSize: '14px',
            },
            success: { iconTheme: { primary: '#38B6FF', secondary: '#fff' } },
          }}
        />
      </body>
    </html>
  );
}
