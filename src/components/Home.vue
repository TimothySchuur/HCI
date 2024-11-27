<template>
    <div class="container">
      <h1>Athlete Profile</h1>
      <p v-if="athlete">Name: {{ athlete.firstname }} {{ athlete.lastname }}</p>
      <p v-else>Loading...</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        athlete: null,
      };
    },
    methods: {
      async fetchAthlete() {
        try {
          const response = await fetch('http://127.0.0.1:5000/homepage');
          if (response.ok) {
            this.athlete = await response.json();
          } else {
            console.error('Failed to fetch athlete data.');
          }
        } catch (error) {
          console.error('Error fetching athlete data:', error);
        }
      },
    },
    mounted() {
      this.fetchAthlete();
    },
  };
  </script>
  
  <style scoped>
  .container {
    text-align: center;
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  h1 {
    color: #333;
  }
  p {
    font-size: 18px;
  }
  </style>
  