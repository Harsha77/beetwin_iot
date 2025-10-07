import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import frappeui from 'frappe-ui/vite';

export default defineConfig({
  plugins: [frappeui(), vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: `../${path.basename(path.resolve('..'))}/public/vertive`,
    emptyOutDir: true,
    target: 'es2018', // Update to es2018 or esnext
    chunkSizeWarningLimit: 1000,  // Increase chunk size limit to 1000 KiB
    rollupOptions: {
      output: {
        // Code splitting configuration for better chunking
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // Split vendor libraries into separate chunks
            return id.toString().split('node_modules/')[1].split('/')[0].toString();
          }
        }
      }
    },
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
  },
  define: {
    // Feature flags for Vue 3
    __VUE_OPTIONS_API__: true, // Enables the Options API (set this to false if you're only using Composition API)
    __VUE_PROD_DEVTOOLS__: false, // Disable Vue Devtools in production
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false, // Disable hydration mismatch details in production
  },
});
