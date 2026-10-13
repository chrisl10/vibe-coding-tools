// Pure classification example. Real URL, assets and public status need target review.
export const PUBLIC_ASSETS = new Set([
  '/public/offline.html', '/public/assets/app.v1.css', '/public/assets/logo.v1.svg',
]);
export const PUBLIC_PAGES = new Set(['/public/', '/public/help']);
export function classifyRequest(request, origin) {
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== origin || url.search ||
      request.headers.has('authorization') || request.headers.has('cookie')) return 'bypass';
  if (PUBLIC_ASSETS.has(url.pathname)) return 'public-asset';
  if (request.mode === 'navigate' && PUBLIC_PAGES.has(url.pathname)) return 'public-navigation';
  return 'bypass';
}
