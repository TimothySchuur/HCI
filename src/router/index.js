import Shoes from "@/components/Shoes.vue";

const routes = [
  {
    path: "/shoes",
    name: "Shoes",
    component: Shoes,
  },
];

export default new VueRouter({
  mode: "history",
  routes,
});

