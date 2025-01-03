<template>
  <div>
    <!-- Hamburger Menu Icon (only show if user is logged in) -->
    <div v-if="isLoggedIn" @click="logout" class="hamburger-menu">
      <img :style="{ position: 'absolute', right: '0', width: '28px' }" src="../img/logout_24dp_5F6368_FILL0_wght400_GRAD0_opsz24.svg" alt="Logout Icon">
    </div>
    <div style="background: none; height: 32px;"> </div>
  </div>
</template>



<script>
export default {
  name: 'HamburgerMenu',
  data() {
    return {
      // Check if a user is logged in by the presence of an auth token in localStorage
      isLoggedIn: localStorage.getItem('authToken') !== null,  // True if logged in, false otherwise
    };
  },
  methods: {
    logout() {
      // Clear the authentication token from localStorage
      localStorage.removeItem('authToken');

      // Close the menu
      this.isOpen = false;

      // Redirect to login page
      this.$router.push('/login');
    },
  },
};

</script>

<style scoped>
* {
  color: #0d0d0d;
}
/* Hamburger icon style */
.hamburger-menu {
  position: absolute;
  width: 100%;
  margin: 0;
  padding: 0;
  margin-top: 20px;
  right: 20px;
  /* width: 30px; */
  height: 25px;
  display: flex;
  flex-direction: column;
  justify-content: right;
  cursor: pointer;
  z-index: 1000;
}


</style>
