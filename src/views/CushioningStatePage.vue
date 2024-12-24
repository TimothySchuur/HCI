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
                <div class="content profile">
                  <div class="center">
                    <h3 class="margin name">Main Shoe:</h3>
                    <h4 class="margin shoe">{{ selectedShoe }}</h4>
                    <p>Mileage Run: {{ kmRan }} KM</p>
                    <p>Mileage Remaining: {{ mileage_remaining }} KM</p>
                    <p>Cushioning: {{ cushioningPercentage.toFixed(2) }}%</p>
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
          <!-- Add a Shoe -->
          <button class="add-shoe-button" @click="toggleShoeDropdown">Add a Shoe</button>
          <div v-if="showShoeDropdown" class="shoe-dropdown">
            <ul>
              <li v-for="shoe in allShoes" :key="shoe.id" @click="addShoeToAccount(shoe)">
                {{ shoe.shoe_brand }} - {{ shoe.model_name }}
              </li>
            </ul>
          </div>
        </div>
        <!-- User Shoes Overview -->
        <div v-if="userShoes.length > 0" class="user-shoes-list">
          <h3>Your Shoes</h3>
          <ul>
            <li v-for="shoe in userShoes" :key="shoe.id" class="shoe-item">
              <p><strong>{{ shoe.shoe_brand }} - {{ shoe.model_name }}</strong></p>
              <p>Mileage Run: {{ shoe.mileage_run }} KM</p>
              <p>Mileage Remaining: {{ shoe.mileage_remaining }} KM</p>
              <p>Cushioning: {{ shoe.cushioning_percentage.toFixed(2) }}%</p>
              <button @click="showShoeOptions(shoe.id)" v-if="shoe.id !== selectedShoeId">
                Options
              </button>
              <!-- Shoe Options -->
              <div v-if="shoe.id === showOptionsForShoeId">
                <button @click="setAsMainShoe(shoe)">Set as Default</button>
                <button @click="closeShoeOptions">Cancel</button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No shoes added yet.</p>
        </div>
      </div>
      <!-- Activities List -->
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
    <!-- Shoe Selection Modal -->
    <div v-if="shoeSelectionOpen" class="modal">
      <h2>Select a Shoe</h2>
      <ul>
        <li v-for="shoe in shoes" :key="shoe.id" @click="setMainShoe(shoe.id)">
          {{ shoe.shoe_brand }} - {{ shoe.model_name }}
        </li>
      </ul>
      <button @click="closeShoeSelection">Close</button>
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
    const cushioningPercentage = ref(0);
    const userShoes = ref([]);
    const kmRan = ref(0); // Initialize mileage run
    const mileage_remaining = ref(0); // Initialize total mileage allowed
    const activities = ref([]);
    const allShoes = ref([]);
    const selectedShoeId = ref(null);
    const showOptionsForShoeId = ref(null);
    const showShoeDropdown = ref(false);

    const toggleShoeDropdown = () => {
      showShoeDropdown.value = !showShoeDropdown.value;
    };

    // Navigate to /login
    const goToLogin = () => {
      router.push('/login');
    };

    // Profile page toggle
    const profilePage = async () => {
      if (profileClicked.value) {
        // If navigating back to the homepage, refresh mileage data
        await fetchMileageRun();
      }
      profileClicked.value = !profileClicked.value; // Toggle the profile view
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

        // Update username and login status
        username.value = response.data.username;
        isLoggedIn.value = true;

        // Update main shoe
        if (response.data.mainShoe) {
          const mainShoe = response.data.mainShoe;
          selectedShoe.value = `${mainShoe.shoe_brand} - ${mainShoe.model_name}`;
          cushioningPercentage.value = mainShoe.cushioning_percentage || 0;
          kmRan.value = mainShoe.mileage_run || 0;
          mileage_remaining.value = mainShoe.mileage_remaining || 0;
        } else {
          selectedShoe.value = 'No main shoe selected';
          cushioningPercentage.value = 0;
          kmRan.value = 0;
          mileage_remaining.value = 0;
        }

        // Update user shoes
        if (response.data.userShoes) {
          userShoes.value = response.data.userShoes.map(shoe => ({
            ...shoe,
            cushioningPercentage: shoe.cushioning_percentage || 0,
          }));
        } else {
          userShoes.value = [];
        }

        console.log('User profile data:', response.data);
      } catch (error) {
        console.error('Error fetching user profile:', error.response?.data || error.message);
      }
    };

    const setMainShoe = async (shoeId) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        await axios.post(`http://localhost:5000/user/set-main-shoe/${shoeId}`, null, {
          headers: { Authorization: `Bearer ${token}` },
        });
        console.log('Main shoe updated');
        await fetchUserProfile(); // Refresh profile data
      } catch (error) {
        console.error('Error setting main shoe:', error.response?.data || error.message);
      }
    };


    // Remove a shoe from the user's account
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
        // Remove the shoe locally from the list
        userShoes.value = userShoes.value.filter((shoe) => shoe.id !== shoeId);
        console.log('Shoe removed:', shoeId);
      } catch (error) {
        console.error('Error removing shoe:', error.response?.data || error.message);
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

    // Add shoe to user's account without changing the main shoe
    const selectShoe = async (shoe) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        await axios.post(
          'http://localhost:5000/user/add-shoe',
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Refresh the list of shoes without modifying the main shoe
        userShoes.value.push({
          id: shoe.id,
          shoe_brand: shoe.shoe_brand,
          model_name: shoe.model_name,
          mileage_run: 0, // Initialize mileage for a new shoe
          mileage_remaining: shoe.mileage || 0, // Assume full mileage for a new shoe
          cushioningPercentage: 100, // Assume 100% cushioning for a new shoe
        });

        console.log(`Shoe added to user's account: ${shoe.shoe_brand} - ${shoe.model_name}`);
        closeShoeSelection();
      } catch (error) {
        console.error('Error adding shoe:', error.response?.data || error.message);
      }
    };

    const fetchAllShoes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/shoes');
        allShoes.value = response.data;
      } catch (error) {
        console.error('Error fetching shoes:', error.response?.data || error.message);
      }
    };

    // Add a shoe to user's account
    const addShoeToAccount = async (shoe) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        await axios.post(
          'http://localhost:5000/user/add-shoe',
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        userShoes.value.push({
          id: shoe.id,
          shoe_brand: shoe.shoe_brand,
          model_name: shoe.model_name,
          mileage_run: 0,
          mileage_remaining: shoe.mileage,
          cushioning_percentage: 100,
        });
        console.log(`Added shoe to user: ${shoe.shoe_brand} - ${shoe.model_name}`);
        showShoeDropdown.value = false;
      } catch (error) {
        console.error('Error adding shoe:', error.response?.data || error.message);
      }
    };

    // Show options for a specific shoe
    const showShoeOptions = (shoeId) => {
      showOptionsForShoeId.value = shoeId;
    };

    // Close shoe options
    const closeShoeOptions = () => {
      showOptionsForShoeId.value = null;
    };

    // Set a shoe as the main shoe
    const setAsMainShoe = async (shoe) => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        await axios.post(
          'http://localhost:5000/user/set-main-shoe',
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        selectedShoeId.value = shoe.id;
        console.log(`Set shoe as main: ${shoe.shoe_brand} - ${shoe.model_name}`);
        closeShoeOptions();
      } catch (error) {
        console.error('Error setting main shoe:', error.response?.data || error.message);
      }
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

        // Update mileage run and remaining mileage
        kmRan.value = response.data.mileage_run; // Update kmRan with mileage_run
        mileage_remaining.value = response.data.mileage_remaining; // Update mileage_remaining

        // Fetch and set cushioning percentage
        const percentageResponse = await axios.get('http://localhost:5000/cushioning-percentage', {
          headers: { Authorization: `Bearer ${token}` },
        });

        cushioningPercentage.value = percentageResponse.data.cushioning_percentage; // Update cushioning percentage
      } catch (error) {
        console.error('Error fetching mileage_run or cushioning percentage:', error.response?.data || error.message);
      }
    };
  
    const fetchActivities = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('No token found in localStorage');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/activities', {
          headers: { Authorization: `Bearer ${token}` },
        });
        activities.value = response.data; // Update activities array with fetched data
      } catch (error) {
        console.error('Error fetching activities:', error.response?.data || error.message);
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
        // Optionally, remove the activity from the list after adding
        removeActivity(index);
      } catch (error) {
        console.error('Error adding activity:', error.response?.data || error.message);
      }
    };

    const removeActivity = (index) => {
      activities.value.splice(index, 1); // Remove activity from the array
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

    const progressGradient = computed(() => {
      const brightnessFactor = cushioningPercentage.value / 100;
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
      mileage_remaining,
      fetchActivities,
      addActivity,
      removeActivity,
      selectShoeForHomepage,
      userShoes,
      selectedShoeId,
      mainShoe,
      setAsMainShoe,
      showShoeOptions,
      closeShoeOptions,
      addShoeToAccount,
      toggleShoeDropdown,
      showShoeDropdown,
      showOptionsForShoeId,
      allShoes,
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

  </style>
  