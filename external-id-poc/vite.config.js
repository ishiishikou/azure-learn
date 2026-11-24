import { defineConfig } from 'vite';
import { resolve } from 'node:path';
export default defineConfig({
  build: { rollupOptions: { input: {
    home: resolve(import.meta.dirname, 'index.html'),
    dashboard: resolve(import.meta.dirname, 'dashboard.html'),
    redirect: resolve(import.meta.dirname, 'redirect.html')
  }}}
});
