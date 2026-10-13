// Adapt in the existing router. View files must be real owned application files.
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
const routes: RouteRecordRaw[] = [
  { path: '/records/:id', name: 'record', component: () => import('./RecordView.vue'), props: true },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('./NotFoundView.vue') }
]
export const router = createRouter({ history: createWebHistory(), routes })
// HTML history deep-link fallback requires independently authorized host configuration.
// In a reused view: useRecord(() => props.id); never fetch only in onMounted.
// Navigation guards do not establish server authorization.
