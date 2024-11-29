import { createRouter, createWebHistory } from 'vue-router';
import CushioningStatePage from '@/views/CushioningStatePage.vue';
import ShoesComponent from '@/components/ShoesComponent.vue';
import ShoeViewer from '@/components/ShoeViewer.vue';
import FetchData from '@/components/FetchDataComponent.vue';
import RegisterComponent from '@/components/RegisterComponent.vue';
import Shoes from "@/components/Shoes.vue";

const routes = [
  {
    path: '/home',
    name: 'CushioningStatePage',
    component: CushioningStatePage,
  },
  {
    path: "/shoes",
    name: "Shoes",
    component: Shoes,
  },
  {
    path: '/shoes-component',
    name: 'ShoesComponent',
    component: ShoesComponent,
  },
  {
    path: '/shoe-view',
    name: 'ShoeViewer',
    component: ShoeViewer,
  },
  {
    path: '/fetch-data',
    name: 'FetchData',
    component: FetchData,
  },
  {
    path: '/register',
    name: 'RegisterComponent',
    component: RegisterComponent,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


