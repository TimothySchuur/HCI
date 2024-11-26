<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/shoes">Running Shoes</router-link>
    </nav>

    <!-- Canvas for Three.js -->
    <canvas ref="canvas"></canvas>

    <!-- Router View for Dynamic Pages -->
    <router-view />
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { setupThreeJS, fetchData } from './threeSetup.js';

export default defineComponent({
  name: 'App',
  setup() {
    const canvas = ref(null);
    const apiData = ref(null);

    const loadData = async () => {
      try {
        setupThreeJS(canvas.value);
        apiData.value = await fetchData();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    loadData();

    return { canvas, apiData };
  },
});
</script>

<style>
* {
  margin: 0;
}
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  height: 100vh;
  width: 100vw;
  background-color: rgb(13, 13, 13);
}
nav {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: rgb(33, 33, 33);
  width: 100%;
  justify-content: center;
}
nav a {
  color: white;
  text-decoration: none;
}
nav a:hover {
  text-decoration: underline;
}
canvas {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
