<template>
  <div id="app">
    <!-- Add the HamburgerMenu Component -->
    <HamburgerMenu />
    <!-- Navigation Bar -->
    <!-- <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/shoes">Running Shoes</router-link>
    </nav> -->


    <!-- Router View for Dynamic Pages -->
     <div class="content">
        <router-view />
    </div>
    <NavBar />
  </div>
</template>

<script>
import HamburgerMenu from '@/components/HamburgerMenu.vue'; 
import NavBar from '@/components/NavBar.vue'; // Import the component
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
  components: { HamburgerMenu, NavBar}, 
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
  position: relative;
  height: 100vh;
  width: 100%;
  background-color: #0D0D0D;
  /* padding: 0 20px 0 20px; */
}

.content {
  display: flex;
  width: 100%;
  justify-content: center; 
}


</style>