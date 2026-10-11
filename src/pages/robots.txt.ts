export const GET = () =>
  new Response(
    'User-agent: *\nAllow: /\nSitemap: https://between-turns.netlify.app/sitemap-index.xml\n',
    { headers: { 'Content-Type': 'text/plain' } },
  );
