/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gov: {
          navy: '#0f172a',
          blue: '#1e3a8a',
          saffron: '#ff9933',
          green: '#138808',
          accent: '#2563eb',
          slate: '#f8fafc',
        }
      }
    },
  },
  plugins: [],
}
