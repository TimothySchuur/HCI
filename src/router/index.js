import { createRouter, createWebHistory } from 'vue-router';
import CushioningStatePage from '@/views/CushioningStatePage.vue';
import ComparePage from '@/views/ComparePage.vue';
import ShoeFinderPage from '@/views/ShoeFinder.vue';

// import RegisterComponent from '@/components/RegisterComponent.vue';

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
  }



  // {
  //   path: '/register',
  //   name: 'RegisterComponent',
  //   component: RegisterComponent,
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

