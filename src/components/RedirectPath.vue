<template>
    <div class="container">
      <h1>Welcome to the Homepage</h1>
      <p>{{ statusMessage }}</p>
      <button v-if="!loggedIn" @click="redirectToLogin">Login</button>
      <button v-if="loggedIn && !stravaConnected" @click="redirectToStrava">Connect Strava</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        statusMessage: '',
        loggedIn: false,
        stravaConnected: false,
      };
    },
    methods: {
      async checkLoginStatus() {
        try {
          const response = await fetch('http://127.0.0.1:5000/check_strava', {
            method: 'GET',
            credentials: 'include', // Include session cookies
          });
  
          if (response.ok) {
            const data = await response.json();
            if (data.message === 'Please connect your Strava account first') {
              this.statusMessage = 'Please connect your Strava account to continue.';
              this.loggedIn = true;
              this.stravaConnected = false;
            } else {
              this.statusMessage = 'Welcome back! Redirecting to your homepage...';
              this.loggedIn = true;
              this.stravaConnected = true;
  
              // Redirect to homepage content after a short delay
              setTimeout(() => {
                this.$router.push('/homepage_content'); // Replace with your actual route
              }, 2000);
            }
          } else {
            // User is not logged in
            this.statusMessage = 'You need to log in to access the homepage.';
            this.loggedIn = false;
          }
        } catch (error) {
          console.error('Error checking login status:', error);
          this.statusMessage = 'An error occurred. Please try again later.';
        }
      },
      redirectToLogin() {
        this.$router.push('/login'); // Replace with your login route
      },
      redirectToStrava() {
        window.location.href = 'http://127.0.0.1:5000/check_strava'; // Strava connection route
      },
    },
    mounted() {
      this.checkLoginStatus();
    },
  };
  </script>
  
  <style scoped>
  .container {
    text-align: center;
    margin-top: 50px;
  }
  button {
    padding: 10px 20px;
    margin: 10px;
    background-color: #5cb85c;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background-color: #4cae4c;
  }
  </style>
  
