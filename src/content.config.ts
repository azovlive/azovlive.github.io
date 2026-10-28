import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const apps = defineCollection({
	// Load Markdown and MDX files in the `src/content/apps/` directory.
	loader: glob({ base: './src/content/apps', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Release date
			releaseDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			// App icon (can be an emoji like '🚀' or an image path / URL)
			icon: z.string().optional(),
			// Download link
			downloadUrl: z.string().url().optional(),
			// App version
			version: z.string().optional(),
			// Category/Tag
			category: z.string().optional(),
			// Supported platforms (e.g. ['Windows', 'macOS', 'Android', 'iOS', 'Web'])
			platforms: z.array(z.string()).optional(),
			// Optional hero image / preview banner
			heroImage: z.optional(image()),
			// Featured on top
			featured: z.boolean().optional().default(false),
		}),
});

export const collections = { apps };
