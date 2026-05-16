/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#38B6FF',
          50: '#EBF8FF',
          100: '#D1F0FF',
          500: '#38B6FF',
          600: '#0EA5E9',
          700: '#0284C7',
        },
        magenta: {
          DEFAULT: '#E20074',
          50: '#FFF0F7',
          100: '#FFD6EC',
          500: '#E20074',
          600: '#BE005F',
        },
        danger: '#FF3131',
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '16px',
      },
      boxShadow: {
        card: '0 4px 24px -4px rgba(0,0,0,0.08)',
        'card-hover': '0 8px 40px -8px rgba(56,182,255,0.2)',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #38B6FF 0%, #E20074 100%)',
        'gradient-hero': 'linear-gradient(135deg, #F0F9FF 0%, #FFF0F7 100%)',
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: { from: { opacity: '0', transform: 'translateY(20px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
};
