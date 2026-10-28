import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';

export async function GET(context) {
	const apps = await getCollection('apps');
	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: apps.map((app) => ({
			title: app.data.title,
			description: app.data.description,
			pubDate: app.data.releaseDate,
			link: `/apps/${app.id}/`,
		})),
	});
}
