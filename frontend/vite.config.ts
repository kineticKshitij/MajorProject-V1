import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler']],
      },
    }),
  ],
  server: {
    allowedHosts: ['uninfected-heliocentrically-bruno.ngrok-free.dev'], // 👈 your ngrok domain
    host: true, // 👈 allows external connections
    port: 5173, // optional, ensures it matches your dev server
  },
})
