<template>
  <div>
    <!-- Display "Log In" button if user is not logged in -->
    <div v-if="!isLoggedIn" class="center-login">
      <h1>Welcome to Cushioning State</h1>
      <button @click="goToLogin">Log In</button>
    </div>
    <!-- Display the main page content if user is logged in -->
    <div v-else>
      <div class="width" v-if="!profileClicked">
        <h1 class="title">CUSHIONING STATE</h1>
        <div class="main">
          <div class="container top">
            <div class="content top-c">
              <ShoeViewer :progress-gradient="progressGradient" />
            </div>
          </div>
          <div style="display: flex; flex-direction: row;">
            <div class="container">
              <div class="content progress-bar">
                <div class="dashed-line"></div>
                <div
                  class="progress"
                  :style="{ height: cushioningPercentage + '%', background: progressGradient }"
                ></div>
                <div class="col">
                  <p style="color: #171717; font-family: 'SemiBold', sans-serif">{{ totalMileageAllowed }} KM</p>
                  <p style="color: #171717; font-family: 'Light', sans-serif">REMAINING</p>
                </div>
              </div>
            </div>
            <div style="display: flex; flex-direction: column">
              <div class="container">
                <div class="content km-ran">
                  <div class="center">
                    <h1>{{ kmRan }} KM</h1> <!-- Dynamically display the mileage_run value -->
                    <h4>RAN</h4>
                  </div>
                </div>
              </div>
              <div class="container">
                <div @click="profilePage" class="content profile">
                  <div class="center">
                    <img class="profile-img" src="../img/profile-circle.svg" />
                    <h3 class="margin name">{{ username }}</h3>
                    <!-- Display selected shoe or fallback message -->
                    <h4 class="margin shoe">{{ selectedShoe }}</h4>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Profile Page -->
      <div v-else>
        <h2>Profile Page</h2>
        <button @click="profilePage">Go back</button>
        <div>
          <button class="add-shoe-button" @click="openShoeSelection">Add a Shoe</button>
        </div>
        <div v-if="activities.length > 0">
          <ul class="activity-list">
            <li
              v-for="(activity, index) in activities"
              :key="index"
              class="activity-item"
            >
              <strong>{{ activity.name }}</strong>
              <p>Distance: {{ activity.distance }} meters</p>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>Loading activities...</p>
        </div>
      </div>

      <!-- Shoe Selection Modal -->
      <div v-if="shoeSelectionOpen" class="modal">
        <h2>Select a Shoe</h2>
        <ul>
          <li v-for="shoe in shoes" :key="shoe.id" @click="selectShoe(shoe)">
            {{ shoe.shoe_brand }} - {{ shoe.model_name }}
          </li>
        </ul>
        <button @click="closeShoeSelection">Close</button>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ShoeViewer from '@/components/ShoeViewer.vue';

export default {
  name: 'CushioningStatePage',
  components: { ShoeViewer },
  setup() {
    const router = useRouter();
    const isLoggedIn = ref(false);
    const username = ref('');
    const selectedShoe = ref('');
    const shoes = ref([]);
    const shoeSelectionOpen = ref(false);
    const profileClicked = ref(false);
    const cushioningPercentage = 79;
    const kmRan = ref(0); // Initialize mileage run
    const totalMileageAllowed = ref(0); // Initialize total mileage allowed
    const activities = ref([]);

    // Navigate to /login
    const goToLogin = () => {
      router.push('/login');
    };

    // Profile page toggle
    const profilePage = () => {
      profileClicked.value = !profileClicked.value;
    };

    const fetchUserProfile = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/user-profile', {
          headers: { Authorization: `Bearer ${token}` },
        });

        username.value = response.data.username; // Update username
        isLoggedIn.value = true; // Mark user as logged in

        // Check and set shoe data
        if (response.data.shoe) {
          selectedShoe.value = `${response.data.shoe.shoe_brand} - ${response.data.shoe.model_name}`;
        } else {
          selectedShoe.value = 'No shoe selected';
        }

        // Check and set mileage data
        if (response.data.mileage) {
          kmRan.value = response.data.mileage.mileage_run; // Update mileage run
          totalMileageAllowed.value = response.data.mileage.total_mileage_allowed; // Update total mileage allowed
        } else {
          kmRan.value = 0; // Default value if no data
          totalMileageAllowed.value = 0; // Default value if no data
        }
      } catch (error) {
        console.error('Error fetching user profile:', error.response?.data || error.message);
      }
    };



    // Fetch available shoes
    const fetchShoes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/shoes');
        shoes.value = response.data;
      } catch (error) {
        console.error('Error fetching shoes:', error.response?.data || error.message);
      }
    };

    // Add shoe to user's account
    const selectShoe = async (shoe) => {
      const token = localStorage.getItem('authToken');
      try {
        await axios.post(
          'http://localhost:5000/user/add-shoe',
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        selectedShoe.value = `${shoe.shoe_brand} - ${shoe.model_name}`;
        closeShoeSelection();
      } catch (error) {
        console.error('Error adding shoe:', error.response?.data || error.message);
      }
    };

    const openShoeSelection = () => {
      shoeSelectionOpen.value = true;
      fetchShoes();
    };

    const closeShoeSelection = () => {
      shoeSelectionOpen.value = false;
    };

    // Fetch mileage_run and total_mileage_allowed
    const fetchMileageRun = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/user/mileage-run', {
          headers: { Authorization: `Bearer ${token}` },
        });
        kmRan.value = response.data.mileage_run; // Update kmRan with mileage_run
        totalMileageAllowed.value = response.data.total_mileage_allowed; // Update totalMileageAllowed
      } catch (error) {
        console.error('Error fetching mileage_run:', error.response?.data || error.message);
      }
    };

    const checkLoginStatus = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        router.push('/login'); // Redirect if no token
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/verify-token', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.status === 200) {
          isLoggedIn.value = true; // Mark user as logged in
          await fetchUserProfile(); // Fetch user profile and shoe data
        } else {
          router.push('/login'); // Redirect if token is invalid
        }
      } catch (error) {
        console.error('Token validation failed:', error);
        router.push('/login'); // Redirect if error occurs
      }
    };

    // Computed property for dynamic gradient
    const progressGradient = computed(() => {
      const brightnessFactor = cushioningPercentage / 100;
      const adjustedTopColor = `rgb(
        ${10 + (245 - 10) * (1 - brightnessFactor)}, 
        ${122 + (203 - 122) * (1 - brightnessFactor)}, 
        ${52 + (191 - 52) * (1 - brightnessFactor)})`;
      return `linear-gradient(to top, #C5CBBF, ${adjustedTopColor})`;
    });

    // Component mounted
    onMounted(() => {
      checkLoginStatus(); // Verify if the user is logged in
    });

    return {
      isLoggedIn,
      username,
      selectedShoe,
      shoes,
      shoeSelectionOpen,
      profileClicked,
      cushioningPercentage,
      kmRan,
      goToLogin,
      profilePage,
      openShoeSelection,
      closeShoeSelection,
      selectShoe,
      progressGradient,
      activities,
      fetchMileageRun,
      totalMileageAllowed
    };
  },
};
</script>



<style scoped>
  .center-login {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    flex-direction: column;
    text-align: center;
  }
  button {
    background-color: #42b983;
    border: none;
    padding: 10px 20px;
    color: white;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background-color: #357a6f;
  }
  .width{
    width: 90%;
    position: absolute;
    left:50%;
    transform: translateX(-50%);
  }

  button {
    background-color: #42b983;
    border: none;
    padding: 10px 20px;
    color: white;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #357a6f;
  }

  .title{
    width: 60%;
    text-align: left;
    margin-top: 22.8%;
  }

  .container{
    width: 45vw;
    border-radius: 8px;
    margin: 6px;
    display: flex; 
    justify-content: center; 
  }

  .content{
background-color: #171717;
    padding: 6px;
    border-radius: 8px;
    display: flex;
    justify-content: center; 
    position: relative;
  }

  .main{
    display: flex;
    justify-content: center;
    flex-direction: column;
  }

  .top{
    width: 97%;
    height: 210px;
  }
  
  .top-c{
    padding: 10px;
    width: 100%;
  }


  .km-ran{
    height: 125px;
  }

  .profile{
    height: 211.5px;
  }

  .center{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center; 
    align-items: center;
    flex-direction: column;
  }

  .profile-img{
    width: 60px;
    stroke: #D6D6D6;
    color: #D6D6D6;
    padding: 2px;
  }

  .margin{
    margin-top: 2px;
  }

  h3{
    font-size: 16px;
  }

  .name{
    font-size: 20px;
    padding: 2px;
  }

.shoe{
  text-align:center;
  padding: 2px 3px 2px 3px;
  font-size: 16px;
}

.progress-bar {
  height: 360px;
  width: 100%;
  position: relative;
  background-color: #171717; /* Match the container background */
  border-radius: 8px;
  overflow: hidden; /* Prevent overflow of content */
}

.progress {
  width: 100%;
  position: absolute;
  bottom: 0;
  border-radius: 0 0 8px 8px;
  /* background: linear-gradient(to top, #C5CBBF, #0A7A34); Gradient to match your design */
  transition: height 0.3s ease; /* Smooth height transitions */
}

.dashed-line {
  position: absolute;
  bottom: 72px; /* Adjust height above bottom */
  width: 90%; /* Ensure it doesn't touch the edges */
  left: 5%; /* Center horizontally */
  z-index: 10; /* Place above the progress bar */
  border-top: 1px dashed #171717; /* Adjust color and thickness */
  background-color: transparent; /* Ensure no background */
}

.col{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: absolute;
  bottom: 18px;
}

  </style>
  