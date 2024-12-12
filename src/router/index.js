import { createRouter, createWebHistory } from 'vue-router';
import CushioningStatePage from '@/views/CushioningStatePage.vue';
import ComparePage from '@/views/ComparePage.vue';
import ShoeFinderPage from '@/views/ShoeFinder.vue';
import LoginPage from '@/views/LoginPage.vue';
import StravaPage from '@/views/StravaPage.vue';

const routes = [
  {
    path: '/',
    name: 'CushioningStatePage',
    component: CushioningStatePage,
  },
  {
    path: '/compare-shoes',
    name: 'ComparePage',
    component: ComparePage
  },
  {
    path: '/shoe-finder',
    name: 'ShoeFinderPage',
    component: ShoeFinderPage,
  },
  {
    path: '/login-page',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/connect-strava',
    name: 'StravaPage',
    component: StravaPage,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

