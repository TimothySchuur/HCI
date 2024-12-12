import Router from "vue-router";
import Shoes from "@/components/Shoes.vue";
import Register from "@/components/Register.vue"; // Import the new component
import Vue from 'vue';
import Homepage from '@/components/HomePage.vue';
import Login from '@/components/Login.vue';
import HomepageContent from '@/components/HomepageContent.vue';

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

