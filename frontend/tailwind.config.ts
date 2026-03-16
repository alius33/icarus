import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    screens: {
      fold: "500px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
    },
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        forest: {
          50:  "#F1F2ED",
          100: "#E3E5DA",
          200: "#C8CDB5",
          300: "#A2AC82",
          400: "#8A9A6A",
          500: "#5B6D49",
          600: "#4A5C3A",
          700: "#3A4A2D",
          800: "#1E3310",
          900: "#0C3C01",
          950: "#2E2D1D",
        },
      },
    },
  },
  plugins: [typography],
};
export default config;
