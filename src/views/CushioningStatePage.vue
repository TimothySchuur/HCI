<template>
<!-- Display the main page content if user is logged in -->
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
            <p style="color: #171717; font-family: 'SemiBold', sans-serif">{{ mileage_remaining }} KM</p>
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
          <div class="content profile" @click="toggleProfileView" style="cursor: pointer;">
            <div class="center">
              <img class="profile-img" src="../img/profile-circle.svg" />
              <h3 class="margin name">Main Shoe:</h3>
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
  <button @click="toggleProfileView">Go Back</button>
  <div>
  <!-- Add Shoe Section -->
  <div>
    <button @click="toggleShoeDropdown">Add a Shoe</button>
    <div v-if="showShoeDropdown" class="dropdown">
      <ul>
        <li
          v-for="shoe in allShoes"
          :key="shoe.id"
          @click="addShoeToAccount(shoe)"
        >
          {{ shoe.shoe_brand }} - {{ shoe.model_name }}
        </li>
      </ul>
    </div>
  </div>
  <!-- User Shoes Overview -->
  <div v-if="userShoes.length > 0" class="user-shoes-list">
    <h3>Your Shoes</h3>
    <ul>
      <li v-for="shoe in userShoes" :key="shoe.id">
        <p><strong>{{ shoe.shoe_brand }} - {{ shoe.model_name }}</strong></p>
        <p>Mileage Run: {{ shoe.mileage_run || 0 }} KM</p>
        <p>Mileage Remaining: {{ shoe.mileage_remaining || 0 }} KM</p>
        <p>Cushioning: {{ shoe.cushioningPercentage !== undefined ? shoe.cushioningPercentage.toFixed(2) : "N/A" }}%</p>
        <button v-if="shoe.id !== mainShoe?.id" @click="setAsMainShoe(shoe)">
          Set as Default
        </button>
        <button @click="removeShoe(shoe.id)">Remove</button>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>No shoes added yet.</p>
  </div>
<!-- Activities List -->
  <div>
    <button @click="fetchLatestActivity" class="fetch-latest-activity-button">Fetch Latest Activity</button>
    <div v-if="activities.length > 0">
      <h3>Your Activities</h3>
      <ul class="activity-list">
        <li
          v-for="(activity, index) in activities"
          :key="index"
          class="activity-item"
        >
          <strong>{{ activity.name }}</strong>
          <p>Distance: {{ activity.distance }} meters</p>
          <div class="activity-actions">
            <button class="add-activity-button" @click="addActivity(activity, index)">Add Activity</button>
            <button class="remove-activity-button" @click="removeActivity(index)">Don't Add Activity</button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Loading activities...</p>
    </div>
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

    // State variables
    const isLoggedIn = ref(false);
    const username = ref('');
    const selectedShoe = ref('');
    const mainShoe = ref(null);
    const userShoes = ref([]);
    const allShoes = ref([]);
    const activities = ref([]);
    const shoeSelectionOpen = ref(false);
    const showShoeDropdown = ref(false);
    const showOptionsForShoeId = ref(null);

    const cushioningPercentage = ref(0);
    const kmRan = ref(0);
    const mileage_remaining = ref(0);

    // Navigation
    const goToLogin = () => router.push('/login');
    const profileClicked = ref(false);

    const toggleProfileView = async () => {
      if (profileClicked.value) {
        // If the user is going back to the main view, refresh the user profile
        await fetchUserProfile();
      }
      else if (!profileClicked.value) {
        // If the user is going back to the main view, refresh the user profile
        await fetchAllShoes();
      }
      profileClicked.value = !profileClicked.value; // Toggle profile view
    };

    // Fetch user profile
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

        const { username: user, mainShoe: main, userShoes: shoes } = response.data;

        username.value = user;
        isLoggedIn.value = true;

        if (main) {
          mainShoe.value = main;
          selectedShoe.value = `${main.shoe_brand} - ${main.model_name}`;
          cushioningPercentage.value = main.cushioning_percentage || 0;
          kmRan.value = main.mileage_run || 0;
          mileage_remaining.value = main.mileage_remaining || 0;
        } else {
          resetMainShoe();
        }

        userShoes.value = shoes || [];
      } catch (error) {
        console.error('Error fetching user profile:', error.response?.data || error.message);
      }
    };

    // Reset main shoe when none is selected
    const resetMainShoe = () => {
      mainShoe.value = null;
      selectedShoe.value = 'No main shoe selected';
      cushioningPercentage.value = 0;
      kmRan.value = 0;
      mileage_remaining.value = 0;
    };

    const setAsMainShoe = async (shoe) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        // Call the API to set the main shoe
        const response = await axios.post(
          'http://localhost:5000/user/set-main-shoe',
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        console.log(response.data.message);
        await fetchUserProfile(); // Refresh profile data after updating the main shoe
      } catch (error) {
        console.error('Error setting main shoe:', error.response?.data || error.message);
      }
    };



    // Remove a shoe
    const removeShoe = async (shoeId) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        await axios.delete(`http://localhost:5000/user/remove-shoe/${shoeId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        userShoes.value = userShoes.value.filter((shoe) => shoe.id !== shoeId);
      } catch (error) {
        console.error('Error removing shoe:', error.response?.data || error.message);
      }
    };

    const addShoeToAccount = async (shoe) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        // Add the shoe to the user's account via the API
        await axios.post(
          'http://localhost:5000/user/add-shoe',
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Add the shoe locally to the userShoes array
        userShoes.value.push({
          ...shoe,
          mileage_run: 0,
          mileage_remaining: shoe.mileage || 0,
          cushioningPercentage: 100, // Default cushioning for a new shoe
        });

        console.log(`Shoe added to user's account: ${shoe.shoe_brand} - ${shoe.model_name}`);
        showShoeDropdown.value = false;
      } catch (error) {
        console.error('Error adding shoe:', error.response?.data || error.message);
      }
    };


    // Toggle shoe dropdown
    const toggleShoeDropdown = () => {
      showShoeDropdown.value = !showShoeDropdown.value;
    };

    // Fetch all shoes
    const fetchAllShoes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/shoes');
        allShoes.value = response.data;
      } catch (error) {
        console.error('Error fetching shoes:', error.response?.data || error.message);
      }
    };

    // Fetch mileage
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
        const { mileage_run, mileage_remaining, cushioning_percentage } = response.data;

        kmRan.value = mileage_run;
        mileage_remaining.value = mileage_remaining;
        cushioningPercentage.value = cushioning_percentage;
      } catch (error) {
        console.error('Error fetching mileage:', error.response?.data || error.message);
      }
    };

    // Activities
    const fetchLatestActivity = async () => {
      try {
        const response = await axios.get('http://localhost:5000/activities');
        activities.value = response.data; // Update activities with the fetched data
        console.log('Fetched latest activities:', activities.value);
      } catch (error) {
        console.error('Error fetching latest activity:', error.response?.data || error.message);
      }
    };

    const addActivity = async (activity, index) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        await axios.post(
          'http://localhost:5000/update-activities',
          { activity_id: activity.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        activities.value.splice(index, 1); // Remove added activity
      } catch (error) {
        console.error('Error adding activity:', error.response?.data || error.message);
      }
    };

    // Check login status
    const checkLoginStatus = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        goToLogin();
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/verify-token', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.status === 200) {
          isLoggedIn.value = true;
          await fetchUserProfile();
        } else {
          goToLogin();
        }
      } catch (error) {
        console.error('Error verifying token:', error.response?.data || error.message);
        goToLogin();
      }
    };

    // Progress bar gradient
    const progressGradient = computed(() => {
      const brightnessFactor = cushioningPercentage.value / 100;
      const adjustedTopColor = `rgb(
        ${10 + (245 - 10) * (1 - brightnessFactor)}, 
        ${122 + (203 - 122) * (1 - brightnessFactor)}, 
        ${52 + (191 - 52) * (1 - brightnessFactor)})`;
      return `linear-gradient(to top, #C5CBBF, ${adjustedTopColor})`;
    });

    onMounted(() => {
      checkLoginStatus();
      fetchAllShoes();
    });

    return {
      // State variables
      isLoggedIn,
      username,
      selectedShoe,
      mainShoe,
      userShoes,
      allShoes,
      activities,
      shoeSelectionOpen,
      showShoeDropdown,
      showOptionsForShoeId,
      // Mileage and cushioning
      cushioningPercentage,
      kmRan,
      mileage_remaining,
      // Functions
      goToLogin,
      toggleProfileView,
      fetchUserProfile,
      setAsMainShoe,
      removeShoe,
      addShoeToAccount,
      toggleShoeDropdown,
      fetchAllShoes,
      fetchMileageRun,
      fetchLatestActivity,
      addActivity,
      progressGradient,
      profileClicked,
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

.fetch-activities-button {
  background-color: #42b983;
  border: none;
  padding: 10px 20px;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px; /* Adjust spacing */
}

.fetch-activities-button:hover {
  background-color: #357a6f;
}

.activity-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.add-activity-button,
.remove-activity-button {
  background-color: #42b983;
  border: none;
  padding: 8px 16px;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.add-activity-button:hover {
  background-color: #357a6f;
}

.remove-activity-button {
  background-color: #e74c3c;
}

.remove-activity-button:hover {
  background-color: #c0392b;
}

.user-shoes-list {
  margin-top: 20px;
}

.shoe-item {
  background-color: #171717;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  color: white;
}

.shoe-item button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.shoe-item button:hover {
  opacity: 0.8;
}

.profile-container {
  border: 2px solid red;
}

  </style>
  