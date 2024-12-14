<template>
    <div class="login-page">
      <div class="form-container" v-if="isLoginVisible">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <input type="email" v-model="loginEmail" placeholder="Email" required />
          <input type="password" v-model="loginPassword" placeholder="Password" required />
          <button type="submit">Login</button>
          <p class="error">{{ loginError }}</p>
        </form>
        <p>
          Don't have an account?
          <a href="#" @click="toggleForms">Sign Up</a>
        </p>
      </div>
  
      <div class="form-container" v-else>
        <h2>Sign Up</h2>
        <form @submit.prevent="handleSignUp">
          <input type="text" v-model="signupUsername" placeholder="Username" required />
          <input type="email" v-model="signupEmail" placeholder="Email" required />
          <input type="password" v-model="signupPassword" placeholder="Password" required />
          <button type="submit">Sign Up</button>
          <p class="error">{{ signupError }}</p>
        </form>
        <p>
          Already have an account?
          <a href="#" @click="toggleForms">Login</a>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';

  
  export default {
    name: 'LoginPage',
    setup() {
      const router = useRouter();
  
      // Reactive state
      const isLoginVisible = ref(true);
      const loginEmail = ref('');
      const loginPassword = ref('');
      const signupUsername = ref('');
      const signupEmail = ref('');
      const signupPassword = ref('');
      const loginError = ref('');
      const signupError = ref('');
  
      // Toggle between login and signup forms
      const toggleForms = () => {
        isLoginVisible.value = !isLoginVisible.value;
        loginError.value = '';
        signupError.value = '';
      };
      const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:5000/login', {
      email: loginEmail.value,
      password: loginPassword.value,
    });
    localStorage.setItem('authToken', response.data.token); // Save token
    console.log('Token stored:', response.data.token); // Debug
    router.push('/connect-strava'); // Redirect after login
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message);
  }
};  
      // Handle signup
      const handleSignUp = async () => {
        try {
          const response = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              username: signupUsername.value,
              email: signupEmail.value,
              password: signupPassword.value,
            }),
          });
  
          const data = await response.json();
          if (response.ok) {
            alert(data.message);
            toggleForms();
          } else {
            signupError.value = data.error;
          }
        } catch (error) {
          signupError.value = 'An error occurred. Please try again.';
        }
      };
  
      return {
        isLoginVisible,
        loginEmail,
        loginPassword,
        signupUsername,
        signupEmail,
        signupPassword,
        loginError,
        signupError,
        toggleForms,
        handleLogin,
        handleSignUp,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Reuse styles from previous example */
  </style>
  