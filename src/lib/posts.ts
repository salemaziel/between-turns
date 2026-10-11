import { getCollection } from 'astro:content';
export type Kind = 'essays' | 'journal';
export const slugOf = (id: string) => id.replace(/\\/g, '/').replace(/^.*\//, '').replace(/\.(md|markdown)$/, '');
// Single source of truth for "what is published": not a draft, not future-dated, newest first.
export async function livePosts(collection: Kind, now = new Date()) {
  const posts = await getCollection(collection, ({ data }) => !data.draft && data.pubDate <= now);
  return posts
    .sort((a, b) => +b.data.pubDate - +a.data.pubDate)
    .map(entry => ({ entry, slug: slugOf(entry.id), href: `/${collection}/${slugOf(entry.id)}/` }));
}
export async function livePostsAll() {
  const [e, j] = await Promise.all([livePosts('essays'), livePosts('journal')]);
  return [...e, ...j].sort((a, b) => +b.entry.data.pubDate - +a.entry.data.pubDate);
}
