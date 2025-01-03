// import Router from "vue-router";
// import Shoes from "@/components/Shoes.vue";
import Register from "@/components/RegisterComponent.vue"; // Import the new component
// import Vue from 'vue';
// import Home from '@/components/RedirectPath.vue';
// import Login from '@/components/Login.vue';

import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/CushioningStatePage.vue';
import ComparePage from '@/views/ComparePage.vue';
import Shoes from '@/views/ShoeFinder.vue';
import Login from '@/views/LoginPage.vue';
import StravaPage from '@/views/StravaPage.vue';


const routes = [
  {
    path: '/compare',
    name: 'ComparePage',
    component: ComparePage,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: "/shoes",
    name: "Shoes",
    component: Shoes,
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

