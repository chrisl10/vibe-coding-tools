# 09: Blog & Content Management

Source PRD: `research/source-prds/prd-phase-09-blog-content-management.md`

---

Read [guide15](15-build-an-independent-payload-cms.md) first for access, bounded public responses, pagination, preview and cache readiness. Code below is an illustrative route shape; check `res.ok`, validate the response contract, encode slug queries and limit public fields before implementation. Existing named serializers were hypothetical, not verified compatible APIs.

## Goal

Implement the blog using the CMS mode selected in Phase 1. Default is **Payload Collections** via REST. Fallback is **TypeScript-as-CMS** (static data objects, no Payload).

---

## CMS mode branch

| Mode | Data source | Admin | Image uploads |
|---|---|---|---|
| **Payload (default)** | Payload `posts` collection REST API | Payload admin at apps/cms URL | Payload Media collection |
| **TypeScript-as-CMS (fallback)** | `src/lib/content/blog.ts` static objects | Code editor | Committed licensed local assets by default |

---

## Mode A: Payload-default

For full Payload implementation details, read [guide15](15-build-an-independent-payload-cms.md).

### Blog listing page

```ts
// apps/web/src/routes/blog/+page.server.ts
import type { PageServerLoad } from './$types';
import { generateSEO } from '$lib/seo/generateSEO';
import { PAYLOAD_API_URL } from '$env/static/private';

export const load: PageServerLoad = async ({ fetch }) => {
  const res = await fetch(
    `${PAYLOAD_API_URL}/api/posts?where[_status][equals]=published&sort=-publishedAt&depth=1`
  );
  const { docs: posts } = await res.json();

  return {
    posts,
    seo: generateSEO({
      title: 'Blog',
      description: 'Articles, guides, and insights.',
      url: '/blog',
    }),
  };
};
```

### Blog post page

```ts
// apps/web/src/routes/blog/[slug]/+page.server.ts
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import { generateSEO } from '$lib/seo/generateSEO';
import { PAYLOAD_API_URL } from '$env/static/private';

export const load: PageServerLoad = async ({ params, fetch }) => {
  // Public route only. Authenticated preview is a separate no-store contract.
  const res = await fetch(
    `${PAYLOAD_API_URL}/api/posts?where[slug][equals]=${params.slug}&where[_status][equals]=published&depth=2`
  );
  const { docs } = await res.json();
  const post = docs?.[0];
  if (!post) throw error(404, 'Post not found');

  return {
    post,
    seo: generateSEO({
      title: post.title,
      description: post.meta?.description ?? post.excerpt,
      url: `/blog/${post.slug}`,
      type: 'article',
      image: post.heroImage?.url ?? post.meta?.image?.url,
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      author: post.author?.name,
    }),
  };
};
```

### Prerendering blog posts (SvelteKit)

```ts
// apps/web/src/routes/blog/[slug]/+page.server.ts
import type { EntryGenerator } from './$types';
import { PAYLOAD_API_URL } from '$env/static/private';

// Illustrative first page only; implement pagination before claiming all routes.
export const entries: EntryGenerator = async () => {
  const res = await fetch(`${PAYLOAD_API_URL}/api/posts?where[_status][equals]=published&select[slug]=true&limit=100`);
  const { docs } = await res.json();
  return docs.map((post: { slug: string }) => ({ slug: post.slug }));
};

export const prerender = true;
```

### Lexical rich text rendering

Choose a supported converter for the installed Payload version and the actual public renderer. Record its documented import, output, custom-node handling and HTML safety checks in guide15's contract. Do not copy a React component into Svelte, use a hypothetical `serializeLexicalToHtml`, or treat an unchecked HTML string as ready to render.

---

## Mode B: TypeScript-as-CMS fallback

Use only for sites that skip Payload. Blog posts are typed TypeScript objects prerendered at build time.

### Blog data file

```ts
// apps/web/src/lib/content/blog.ts
export interface BlogPost {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  content: string;       // HTML string
  category: string;
  tags: string[];
  authorName: string;
  authorSlug: string;
  publishedAt: string;   // ISO 8601
  updatedAt: string;
  featuredImage: string; // Absolute URL
  readTime: number;      // minutes
}

export const blogPosts: BlogPost[] = [
  {
    id: '1',
    slug: 'getting-started',
    title: 'Getting Started',
    excerpt: 'A brief introduction to our platform.',
    content: '<p>Full article content here...</p>',
    category: 'guides',
    tags: ['intro', 'quickstart'],
    authorName: 'Jane Smith',
    authorSlug: 'jane-smith',
    publishedAt: '2026-01-15T09:00:00Z',
    updatedAt: '2026-01-20T10:00:00Z',
    featuredImage: 'https://PUBLIC_SITE_URL/images/blog/getting-started.jpg',
    readTime: 5,
  },
];

export const getAllPosts = () => [...blogPosts].sort((a, b) =>
  new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
);

export const getPostBySlug = (slug: string) => blogPosts.find((p) => p.slug === slug);
```

### Static blog routes (TypeScript-as-CMS)

```ts
// apps/web/src/routes/blog/[slug]/+page.ts
import type { EntryGenerator } from './$types';
import { getAllPosts } from '$lib/content/blog';

export const entries: EntryGenerator = () =>
  getAllPosts().map((post) => ({ slug: post.slug }));

export const prerender = true;
```

---

## Assets in the TypeScript-as-CMS branch

For a code-owned site, use approved local assets committed alongside content. This branch does not need an upload API or Supabase Storage merely because it displays images. If editor uploads become a requirement, reopen the CMS/runtime decision and define upload authorization, file limits, durable storage and deletion in guide15's contract before implementation.

---

## Phase acceptance criteria

| ID | Criterion (Payload mode) | ID | Criterion (TypeScript fallback) |
|---|---|---|---|
| 9P.1 | `/blog` lists published posts from Payload REST | 9T.1 | `/blog` lists all `blogPosts` sorted newest-first |
| 9P.2 | `/blog/[slug]` renders Payload post content | 9T.2 | `/blog/[slug]` renders static HTML content |
| 9P.3 | Draft posts not visible on public site | 9T.3 | Adding entry to `blogPosts` → new static route at next build |
| 9P.4 | Article schema injected in `<svelte:head>` | 9T.4 | Article schema injected in `<svelte:head>` |
| 9P.5 | Blog post pages prerendered at build time via `entries()` | 9T.5 | Blog post pages prerendered at build time via `entries()` |
| 9P.6 | `payload-types.ts` types used for post shape | 9T.6 | `BlogPost` TypeScript interface enforced |
