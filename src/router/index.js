import Router from "vue-router";
import Shoes from "@/components/Shoes.vue";
import Register from "@/components/Register.vue"; // Import the new component
import Vue from 'vue';
import Homepage from '@/components/HomePage.vue';
import Login from '@/components/Login.vue';
import HomepageContent from '@/components/HomepageContent.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Homepage',
      component: Homepage,
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
      path: "/register", // Define the new route path
      name: "Register", // Give it a unique name
      component: Register, // Assign the component to render
    },
  ],
});


