<template>
    <div class="container">
      <h1>Connect Your Strava Account</h1>
      <p>To proceed, please connect your Strava account to synchronize your data.</p>
      <button @click="connectStrava">Connect with Strava</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'StravaPage',
    methods: {
      connectStrava() {
        // Redirect to the Strava authentication route
        window.location.href = 'http://127.0.0.1:5000/connect_strava'; // Replace with your Strava authentication route
      },
    },
  };
  </script>
  
  <style scoped>
  body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
  }
  
  .container {
    margin-top: 50px;
  }
  
  h1 {
    color: #333;
  }
  
  p {
    font-size: 16px;
    color: #555;
  }
  
  button {
    padding: 10px 20px;
    margin: 20px 0;
    background-color: #fc4c02; /* Strava's primary color */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  button:hover {
    background-color: #e04301;
  }
  </style>
  