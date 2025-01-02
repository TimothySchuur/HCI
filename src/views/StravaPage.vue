<template>
    <div class="container">
      <div class="height">
      <h1 class="title">STRAVA CONNECT</h1>
      <p>To proceed, please connect your Strava account to synchronize your data.</p>
      <button @click="connectStrava">CONNECT</button>
    </div>
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
    width: 90%;
  height: 100vh;
  position: relative;
  }
  
  .title {
  width: 60%;
  text-align: left;
  /* margin-top: 122%; */
}
  .height{
position: absolute;
  width: 100%;
  bottom: 180px;
  }

  p {
  margin-top: 18px;
  width: 100%;
  text-align: left;
  font-family: 'Text', sans-serif;
  }
  
  button {
    margin-top: 18px;
  width: 100%;
  box-sizing: border-box;
  padding: 16px;
  border-radius: 8px;
  color: #d6d6d6;
  font-size: 22px;
  font-family: "Light", sans-serif;
  border: none;
  background: linear-gradient(to right, #e02b07, #fc6e02);
  font-family: "Headers", sans-serif;
  padding: 22px;
  }

  </style>
  