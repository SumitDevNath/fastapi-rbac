import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
// export default defineConfig({
//   plugins: [react(), tailwindcss()],
//   server: {
//     port: 3000, // Runs frontend on port 3000 matching our backend CORS whitelist
//   },
// });

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    proxy: {
      "/dev-api": {
        target: "https://dev.surveillance.dghs.gov.bd",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/dev-api/, ""),
      },
    },
  },
});
