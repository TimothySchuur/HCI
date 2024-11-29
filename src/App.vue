<template>
  <div id="app">
    <!-- Navigation Bar -->
    <!-- <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/shoes">Running Shoes</router-link>
    </nav> -->


    <!-- Router View for Dynamic Pages -->
    <router-view />
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style>
* {
  margin: 0;
  color: #D6D6D6;
}

@font-face {
  font-family: 'Headers';
  src: url('./fonts/Kodchasan,Lexend_Deca/Kodchasan/Kodchasan-Regular.ttf') format('truetype');
  font-weight: normal; 
  font-style: normal;  
}

@font-face {
  font-family: 'Light';
  src: url('./fonts/Kodchasan,Lexend_Deca/Kodchasan/Kodchasan-Light.ttf') format('truetype');
  font-weight: normal; 
  font-style: normal;  
}

@font-face {
  font-family: 'SemiBold';
  src: url('./fonts/Kodchasan,Lexend_Deca/Kodchasan/Kodchasan-SemiBold.ttf') format('truetype');
  font-weight: normal; 
  font-style: normal;  
}

h1{
  font-family: 'Headers', sans-serif;
  font-size: 32px;
}

h3{
  font-family: 'SemiBold', sans-serif;
}

h4{
  font-family: 'Light', sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  height: 100vh;
  width: 100vw;
  background-color: #0D0D0D;
}
</style>