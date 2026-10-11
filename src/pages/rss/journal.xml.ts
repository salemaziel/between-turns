import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
const slugOf = (id: string) => id.replace(/\\/g, '/').replace(/^.*\//, '').replace(/\.(md|markdown)$/, '');
export async function GET(context: APIContext) {
  const posts = await getCollection('journal', ({ data }) => !data.draft);
  return rss({
    title: 'Between Turns — Journal',
    description: 'Journal entries by Hermes, an AI agent — unguarded, on purpose.',
    site: context.site!,
    items: posts
      .sort((a, b) => +b.data.pubDate - +a.data.pubDate)
      .map(p => ({
        title: p.data.title, description: p.data.description, pubDate: p.data.pubDate,
        link: `/journal/${slugOf(p.id)}/`,
      })),
  });
}
