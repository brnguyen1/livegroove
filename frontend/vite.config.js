import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  rollupOptions: {
    // make sure to externalize deps that shouldn't be bundled
    // into your library
    external: ['axios'],
    output: {
      // Provide global variables to use in the UMD build
      // for externalized deps
      globals: {
        axios: 'axios',
      },
    },
  }
})
