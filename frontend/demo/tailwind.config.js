/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        century: ['"Century Gothic"', 'sans-serif'],
        italiana: ['Italiana', 'serif']
      },
      animation: {
    glowSweep: 'glowSweep 3s ease-in-out infinite',
  },
  keyframes: {
    glowSweep: {
      '0%': {
        backgroundPosition: '200% 0%',
      },
      '100%': {
        backgroundPosition: '-200% 0%',
      },
    },
  },
    },
  },
  plugins: [],
};
