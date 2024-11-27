import VueRouter from "vue-router";
import Shoes from "@/components/Shoes.vue";
import Register from "@/components/Register.vue"; // Import the new component

const routes = [
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
];

export default new VueRouter({
  mode: "history",
  routes,
});


