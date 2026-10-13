import assert from 'node:assert/strict';
import { classifyRequest } from './cache-policy.mjs';
const origin = 'https://example.test';
const request = (path, options = {}) => ({ url: new URL(path, origin).href, method: 'GET', mode: 'cors', headers: new Headers(), ...options });
const cases = [
  [request('/public/assets/app.v1.css'), 'public-asset'],
  [request('/public/', { mode: 'navigate' }), 'public-navigation'],
  [request('/public/help', { mode: 'navigate' }), 'public-navigation'],
  [request('/public/assets/app.v1.css?tenant=a'), 'bypass'],
  [request('/public/assets/app.v1.css', { method: 'POST' }), 'bypass'],
  [request('/public/assets/app.v1.css', { method: 'HEAD' }), 'bypass'],
  [request('/public/assets/app.v1.css', { headers: new Headers({ authorization: 'synthetic' }) }), 'bypass'],
  [request('/public/assets/app.v1.css', { headers: new Headers({ cookie: 'synthetic' }) }), 'bypass'],
  [request('https://other.test/public/assets/app.v1.css'), 'bypass'],
  [request('/api/account'), 'bypass'],
  [request('/account', { mode: 'navigate' }), 'bypass'],
  [request('/public/tenant/account', { mode: 'navigate' }), 'bypass'],
];
for (const [input, expected] of cases) assert.equal(classifyRequest(input, origin), expected);
console.log(`PASS ${cases.length} synthetic request classification cases; browser/CacheStorage/install/app NOT_RUN`);
