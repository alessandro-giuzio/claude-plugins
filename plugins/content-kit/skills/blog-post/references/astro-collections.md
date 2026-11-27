# Reading an Astro content collection

## Where the schema is

- Astro 5+: `src/content.config.ts`. Older projects: `src/content/config.ts`.
- Look for `defineCollection({ loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }), schema: z.object({ … }) })`. The `base` is the folder for new files; the `pattern` says which extensions are allowed.
- Field types come from `z` (Zod): `z.string()`, `z.coerce.date()`, `z.enum([...])` (allowed values: use one of them), `z.boolean().default(false)` (often `draft`), `image()` (local image: path must exist at build time), `.optional()`.

## Frontmatter

- Copy field names and order from a recent post; fill every required field.
- Dates: the format recent posts use (usually `2026-11-27`). A future publish date may be how the site schedules posts; ask if unsure.
- `image()` fields fail the build if the file doesn't exist. Use a placeholder only if the schema allows a string or the field is optional; otherwise point to an existing generic image and say so in the report.

## Drafts

Common patterns: a `draft: true` field filtered out in `getCollection('blog', ({ data }) => !data.draft)`; or a future `pubDate` filtered by date. Check how the site's blog index and RSS filter posts before relying on either.

## Checks

- `npx astro check` and `npm run build` validate frontmatter against the schema.
- Internal links: confirm `src/pages/<path>.astro` or a collection entry exists for each link; mind the site's trailing-slash convention.
