<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="register">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
      <p>{{ successMessage }}</p>
    </div>
  </template>
  
  <script>
  import { registerUser } from '../api';
  
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        successMessage: '',
      };
    },
    methods: {
      async register() {
        try {
          const userData = {
            username: this.username,
            email: this.email,
            password: this.password,
          };
          const response = await registerUser(userData);
          this.successMessage = response.data.message;
        } catch (error) {
          console.error('Error registering user:', error);
        }
      },
    },
  };
  </script>
  