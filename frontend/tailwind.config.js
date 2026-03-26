/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef6ff',
          500: '#2f78ff',
          700: '#1f53b3'
        }
      }
    }
  },
  plugins: []
};
