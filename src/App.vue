<template>
  <div id="app">
    <ShoeViewer />
  </div>
</template>
<script>
import { defineComponent } from 'vue';
import ShoeViewer from './components/ShoeViewer.vue';
export default defineComponent({
  name: 'App',
  components: {
    ShoeViewer
  }
});
</script>
<style>
*{
  margin: 0;
}
#app {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  height: 100vh;
  margin: 0;
  width: 100vw;
  background-color: rgb(13,13,13);
  z-index: -2;
}
</style>