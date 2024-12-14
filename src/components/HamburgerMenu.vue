<template>
  <div>
    <!-- Hamburger Menu Icon -->
    <div class="hamburger-menu" @click="toggleMenu">
      <div :class="['bar', { active: isOpen }]"></div>
      <div :class="['bar', { active: isOpen }]"></div>
      <div :class="['bar', { active: isOpen }]"></div>
    </div>

    <!-- The menu content that slides in -->
    <transition
      name="menu-slide"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div v-show="isOpen" class="menu-content">
        <h4>This is the menu content! Add your links or navigation here.</h4>
        <button class="logout-button" @click="logout">Logout</button>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'HamburgerMenu',
  data() {
    return {
      isOpen: false, // Track if the menu is open or closed
    };
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen; // Toggle the state of the menu
    },
    beforeEnter(el) {
      el.style.transform = 'translateX(100%)'; // Ensure the menu is off-screen initially
      el.style.opacity = '0'; // Start with opacity 0
    },
    enter(el, done) {
      // Force a reflow to ensure the transition happens smoothly
      el.offsetHeight; // This triggers a reflow
      el.style.transition = 'transform 0.3s ease-in-out, opacity 0.3s ease-in-out'; // Smooth transition for both
      el.style.transform = 'translateX(0)'; // Slide the menu into view
      el.style.opacity = '1'; // Fade in the menu
      done();
    },
    leave(el, done) {
      el.style.opacity = '0'; // Fade out the menu
      done();
    },
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
  margin: 0;
  padding: 0;
  top: 20px;
  right: 20px;
  width: 30px;
  height: 25px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  z-index: 1000;
}

.bar {
  width: 100%;
  height: 4px;
  background-color: #d6d6d6;
  transition: all 0.3s ease;
}

.bar.active:nth-child(1) {
  transform: translateY(9px) rotate(45deg); /* First bar becomes part of a cross */
}

.bar.active:nth-child(2) {
  opacity: 0; /* Middle bar disappears */
}

.bar.active:nth-child(3) {
  transform: translateY(-12px) rotate(-45deg); /* Last bar completes the cross */
}

/* Sliding menu content */
.menu-content {
  position: fixed;
  top: 0;
  right: 0; /* Start off-screen to the right */
  height: 100vh;
  width: 70%; /* Adjust width of the menu */
  background-color: #e7e7e7;
  overflow-y: auto;
  padding-top: 50px; /* Add padding so menu content doesn't stick to the top */
  z-index: 999; /* Ensure the menu is on top */
  opacity: 0; /* Start with opacity 0 */
}

/* Transition classes for sliding in and out */
.menu-slide-enter-active,
.menu-slide-leave-active {
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.menu-slide-enter,
.menu-slide-leave-to {
  transform: translateX(100%); /* Off-screen position */
  opacity: 0; /* Start with opacity 0 */
}

.menu-slide-enter-to,
.menu-slide-leave {
  transform: translateX(0); /* On-screen position */
  opacity: 1; /* Fade in/out */
}

.menu-content h4 {
  margin: 0;
  padding: 20px;
  text-align: right;
}

.logout-button {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #d32f2f;
}
</style>
