import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    svgr({
      svgrOptions: {
        icon: true,
        // This will transform your SVG to a React component
        exportType: "named",
        namedExport: "ReactComponent",
      },
    }),
  ],
  server: {
    port: 17167,
    proxy: {
      // Proxy para todas las rutas relevantes del backend
      '^/(inmates|photos|llamadas|alerts|auth|api|transcriptions|stream|client|special|fingerprint|analyze_call|photo)': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/llamadas-por-dia': 'http://localhost:8000', // (opcional, por compatibilidad)
      '/alerts': 'http://localhost:8000', // (opcional, por compatibilidad)
    },
  },
});
