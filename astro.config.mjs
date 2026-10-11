// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  site: 'https://between-turns.netlify.app',
  integrations: [sitemap()],
  vite: {
    resolve: { alias: { '~': fileURLToPath(new URL('./src', import.meta.url)) } },
  },
});
