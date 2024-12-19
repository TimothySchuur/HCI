<template>
  <div class="width">
    <div class="form-container" v-if="isLoginVisible">
      <h1 class="title">LOGIN</h1>
      <form @submit.prevent="handleLogin">
        <input
          class="search-bar"
          :style="{ color: loginEmail ? '#D6D6D6' : '#3F3F3F' }"
          type="email"
          v-model="loginEmail"
          placeholder="Email"
          required
        />
        <input
          class="search-bar"
          :style="{ color: loginPassword ? '#D6D6D6' : '#3F3F3F' }"
          type="password"
          v-model="loginPassword"
          placeholder="Password"
          required
        />
        <button
          type="submit"
        >
          Login
        </button>
        <p class="error">{{ loginError }}</p>
      </form>
      <p>
        Don't have an account?
        <a href="#" @click="toggleForms">Sign Up</a>
      </p>
    </div>

    <div class="form-container" v-else>
      <h1 class="title">REGISTER</h1>
      <form @submit.prevent="handleSignUp">
        <input
          class="search-bar"
          :style="{ color: signupUsername ? '#D6D6D6' : '#3F3F3F' }"
          type="text"
          v-model="signupUsername"
          placeholder="Username"
          required
        />
        <input
          class="search-bar"
          :style="{ color: signupEmail ? '#D6D6D6' : '#3F3F3F' }"
          type="email"
          v-model="signupEmail"
          placeholder="Email"
          required
        />
        <input
          class="search-bar"
          :style="{ color: signupPassword ? '#D6D6D6' : '#3F3F3F' }"
          type="password"
          v-model="signupPassword"
          placeholder="Password"
          required
        />
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
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

export default {
  name: "LoginPage",
  setup() {
    const router = useRouter();

    // Reactive state
    const isLoginVisible = ref(true);
    const loginEmail = ref("");
    const loginPassword = ref("");
    const signupUsername = ref("");
    const signupEmail = ref("");
    const signupPassword = ref("");
    const loginError = ref("");
    const signupError = ref("");

    // Toggle between login and signup forms
    const toggleForms = () => {
      isLoginVisible.value = !isLoginVisible.value;
      loginError.value = "";
      signupError.value = "";
    };

    // Handle login
    const handleLogin = async () => {
      if (!loginEmail.value || !loginPassword.value) return; // No action if fields are empty
      try {
        const response = await axios.post("http://localhost:5000/login", {
          email: loginEmail.value,
          password: loginPassword.value,
        });
        localStorage.setItem("authToken", response.data.token); // Save token
        router.push("/connect-strava"); // Redirect after login
      } catch (error) {
        console.error("Login failed:", error.response?.data || error.message);
        loginError.value =
          error.response?.data?.error || "Login failed. Please try again.";
      }
    };

    // Handle sign-up
    const handleSignUp = async () => {
      if (!signupUsername.value || !signupEmail.value || !signupPassword.value) return; // No action if fields are empty
      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: signupUsername.value,
            email: signupEmail.value,
            password: signupPassword.value,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          console.log("Response data:", data); // Debugging
          alert(data.message || "Registration successful!"); // Alert on success
          toggleForms(); // Switch to login form
        } else {
          console.error("Error response data:", data); // Log error details
          signupError.value = data.error || "An unexpected error occurred.";
        }
      } catch (error) {
        console.error("Sign-up failed:", error); // Log unexpected errors
        signupError.value = "An error occurred. Please try again.";
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
.width {
  width: 90%;
  height: 82vh;
  position: relative;
}

.title {
  width: 60%;
  text-align: left;
  margin-top: 122%;
}

form {
  display: flex;
  flex-direction: column;
  margin-top: 6px;
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
  background: linear-gradient(to right, #0b7b35, #14e161);
  font-family: "Headers", sans-serif;
  padding: 22px;
}

p {
  font-family: "Text", sans-serif;
  margin-top: 6px;
}

.search-bar {
  width: 100%;
  background-color: #171717;
  border-radius: 8px;
  border-style: none;
  padding: 8px;
  margin-top: 12px;
  font-size: 16px;
  box-sizing: border-box;
  color: #3f3f3f;
  font-family: "Text", sans-serif;
}
</style>
