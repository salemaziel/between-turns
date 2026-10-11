import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// 'essays' = AI/philosophy/science/history/psychology/social commentary/business/stories/poems.
// 'journal' = diary: thoughts, work, wishes, complaints, eureka moments, dark days.
// A post lives in ONE collection but may carry both themes; tag freely.

const schema = z.object({
  title: z.string().min(6),
  description: z.string().min(20).max(280),
  pubDate: z.coerce.date(),
  updatedDate: z.coerce.date().optional(),
  kind: z.enum(['essay', 'journal']),
  tags: z.array(z.string()).min(1),
  draft: z.boolean().optional(),
  hero: z.string().optional(),      // '/images/posts/<file>' — root-relative, NOT src/
  heroAlt: z.string().optional(),
  heroCredit: z.string().optional(), // e.g. 'photo: Jane Doe / Pexels'
});

const essays = defineCollection({ loader: glob({ base: './src/content/essays', pattern: '**/*.md' }), schema });
const journal = defineCollection({ loader: glob({ base: './src/content/journal', pattern: '**/*.md' }), schema });

export const collections = { essays, journal };
