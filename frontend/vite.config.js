import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  preview: {
    host: "0.0.0.0",
    port: process.env.PORT || 4173,
    allowedHosts: [
      "fifa-2026-frontend.onrender.com",
      "localhost",
      "127.0.0.1"
    ]
  }
});