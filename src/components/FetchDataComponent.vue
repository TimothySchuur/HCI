<template>
    <div>
      <h1>Data from Backend</h1>
      <p>{{ message }}</p>
      <button @click="loadData">Fetch Data</button>
    </div>
  </template>
  
  <script>
  import { fetchData } from '../api';
  
  export default {
    data() {
      return {
        message: '',
      };
    },
    methods: {
      async loadData() {
        try {
          const response = await fetchData();
          this.message = response.data.message;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
    },
  };
  </script>
  