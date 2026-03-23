/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "eco-green": "#2ecc71",
        "eco-dark": "#27ae60",
        navy: "#1a1a2e",
        "navy-light": "#16213e"
      }
    }
  },
  plugins: []
};
