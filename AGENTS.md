## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

## Image Asset Management & Performance Optimization

Always consult [IMAGE_OPTIMIZATION_GUIDE.md](./IMAGE_OPTIMIZATION_GUIDE.md) before adding or modifying images:
- **Master Assets**: High-resolution source images must be kept in the project repository (`Doc/images/master/`).
- **Production Assets**: Only display-sized, WebP-compressed images may be uploaded to `public/` (e.g. logos/icons <= 256px, < 30KB).
- **Automation**: Use `python scripts/optimize_image.py <source> -o public/ -s 256` to optimize.
- **Markup**: Always define `width` and `height` on all `<img>` elements to prevent layout shifts (CLS).
