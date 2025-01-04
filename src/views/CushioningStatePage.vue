<template>
  <!-- Display the main page content if user is logged in -->
  <div class="width" v-if="!profileClicked">
    <h1 class="title">CUSHIONING STATE</h1>
    <div class="main">
      <div class="container top">
        <div class="content top-c">
          <ShoeViewer v-if="!loading" :progress-gradient="progressGradient" />
          <div v-else>Loading...</div>
        </div>
      </div>
      <div style="display: flex; flex-direction: row">
        <div class="container">
          <div class="content progress-bar">
            <div class="dashed-line"></div>
            <div
              class="progress"
              :style="{
                height: cushioningPercentage + '%',
                background: progressGradient,
              }"
            ></div>
            <div v-if="mainShoe" class="col">
              <p
                :style="{
                  color: cushioningPercentage > 20 ? '#171717' : '#fff',
                  fontFamily: 'SemiBold, sans-serif',
                }"
              >
                {{ mileage_remaining }} KM
              </p>
              <p
                :style="{
                  color: cushioningPercentage > 20 ? '#171717' : '#fff',
                  fontFamily: 'SemiBold, sans-serif',
                }"
              >
                REMAINING
              </p>
            </div>
            <div @click="toggleProfileView" class="no-shoe" v-if="!mainShoe">
              <p
                style="
                  color: white;
                  font-size: 16px;
                  font-family: 'Light', sans-serif;
                "
              >
                Add shoe
              </p>
            </div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column">
          <div class="container">
            <div class="content km-ran">
              <div class="center">
                <h1>{{ kmRan }} KM</h1>
                <!-- Dynamically display the mileage_run value -->
                <h4>RAN</h4>
              </div>
            </div>
          </div>
          <div class="container">
            <div
              class="content profile"
              @click="toggleProfileView"
              style="cursor: pointer"
            >
              <div class="center">
                <img class="profile-img" src="../img/profile-circle.svg" />
                <h3 class="margin name">{{ username.toUpperCase() }}</h3>
                <h4 class="margin shoe-profile">{{ selectedShoe }}</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Profile Page -->
  <!-- Profile Page -->
  <div class="width" v-else>
    <button @click="toggleProfileView" class="close-btn">
      <img
        style="height: 32px"
        src="../img/arrow_back_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg"
      />
    </button>

    <div class="center">
      <div @click="toggleProfileView" class="profile-settings center">
        <img class="profile-img" src="../img/profile-circle.svg" />
        <h3 class="margin name">{{ username.toUpperCase() }}</h3>
        <h4 class="margin shoe-profile">{{ selectedShoe }}</h4>
      </div>

      <!-- Search Bar -->
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Add shoes to account..."
          class="search-bar"
          :style="{ color: searchQuery ? '#D6D6D6' : '#3F3F3F' }"
        />
        <svg
          class="search-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#3F3F3F"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </div>

      <!-- Search Results -->
      <div v-if="searchQuery" class="results-bg">
        <ul class="results">
          <li v-for="(shoe, index) in filteredData" :key="index">
            <div @click="addShoeToAccount(shoe)" class="row shoe">
              <img src="../img/shoe.png" />
              <div class="shoe-name text-s">
                {{ shoe.shoe_brand }} {{ shoe.model_name }}
              </div>
            </div>
          </li>
        </ul>
      </div>
      <p
        style="font-family: 'text'; font-size: 16px"
        v-if="searchQuery && filteredData.length < 1"
        class="no-results"
      >
        No results found...
      </p>

      <div v-if="userShoes.length > 0">
        <div class="row">
          <button
            v-if="!manageShoes && !fetchActivity"
            @click="
              (manageShoes = !manageShoes),
                (searchQuery = ''),
                (fetchActivity = false)
            "
            class="btn-shoes"
          >
            Manage shoes
          </button>
          <button
            v-if="!manageShoes && !fetchActivity"
            class="btn-activities"
            @click="fetchLatestActivity"
          >
            Fetch activity
          </button>
          <button
            v-else
            class="btn-close"
            @click="(fetchActivity = false), (manageShoes = false)"
          >
            <u
              >{{ manageShoes ? "Close shoe manager" : "Close activities" }}
            </u>
          </button>
        </div>
      </div>

      <!-- User Shoes Overview  wanneer manage shoes active-->
      <div v-if="manageShoes && !searchQuery" class="user-shoes-bg">
        <ul class="results">
          <li v-for="shoe in userShoes" :key="shoe.id">
            <div class="row shoe">
              <img src="../img/shoe.png" />
              <div class="shoe-name text-s">
                {{ shoe.shoe_brand }} {{ shoe.model_name }}
              </div>

              <button
                v-if="shoe.id !== mainShoe?.id"
                class="btn-shoes-active"
                @click="setAsMainShoe(shoe)"
              >
                Activate
              </button>
              <button v-else :disabled class="btn-shoes">Active</button>

              <p>
                {{
                  shoe.cushioning_percentage !== undefined &&
                  !isNaN(shoe.cushioning_percentage)
                    ? Math.round(shoe.cushioning_percentage)
                    : "100"
                }}%
              </p>

              <div @click="removeShoe(shoe.id)">
                <img
                  style="width: 22px"
                  src="../img/delete_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg"
                />
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Activities List -->
      <div>
        <div v-if="fetchActivity" class="activities-bg">
          <ul class="results">
            <li
              v-for="(activity, index) in activities"
              :key="index"
              class="activity-item"
            >
              <div
                style="display: flex; flex-direction: row; position: relative"
              >
                <div
                  style="
                    display: flex;
                    flex-direction: column;
                    font-family: 'Text';
                  "
                >
                  <strong style="font-family: 'text-b'">{{
                    activity.name
                  }}</strong>
                  <p>Distance: {{ activity.distance }} meters</p>
                </div>

                <button class="btn-add" @click="addActivity(activity, index)">
                  <strong style="font-size: 16px"
                    >Add <span style="font-size: 22px">+</span></strong
                  >
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import ShoeViewer from "@/components/ShoeViewer.vue";

export default {
  name: "CushioningStatePage",
  components: { ShoeViewer },
  setup() {
    const searchQuery = ref("");

    const router = useRouter();

    // State variables
    const manageShoes = ref(false);
    const fetchActivity = ref(false);
    const isLoggedIn = ref(false);
    const username = ref("");
    const selectedShoe = ref("");
    const mainShoe = ref(null);
    const userShoes = ref([]);
    const userShoesCount = ref(0);
    const allShoes = ref([]);
    const activities = ref([]);
    const shoeSelectionOpen = ref(false);
    const showShoeDropdown = ref(false);
    const showOptionsForShoeId = ref(null);
    const loading = ref(true);

    const cushioningPercentage = ref(0);
    const kmRan = ref(0);
    const mileage_remaining = ref(0);

    // Navigation
    const goToLogin = () => router.push("/login");
    const profileClicked = ref(false);

    const toggleProfileView = async () => {
      if (profileClicked.value) {
        // If the user is going back to the main view, refresh the user profile
        await fetchUserProfile();
      } else if (!profileClicked.value) {
        // If the user is going back to the main view, refresh the user profile
        await fetchAllShoes();
      }
      profileClicked.value = !profileClicked.value; // Toggle profile view
    };

    // Fetch user profile
    const fetchUserProfile = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No token found in localStorage");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/user-profile", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const {
          username: user,
          mainShoe: main,
          userShoes: shoes,
        } = response.data;

        userShoes.value = shoes;
        username.value = user;
        isLoggedIn.value = true;
        mainShoe.value = main;

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

        // Move the main shoe to the top of the list if it exists
        if (main && userShoes.value.length > 0) {
          const mainShoeIndex = userShoes.value.findIndex(
            shoe => shoe.id === main.id
          );
          if (mainShoeIndex !== -1) {
            const [mainShoeItem] = userShoes.value.splice(mainShoeIndex, 1);
            userShoes.value.unshift(mainShoeItem);
          }
        }

        // Set loading to false after data is fetched
        loading.value = false;
      } catch (error) {
        console.error(
          "Error fetching user profile:",
          error.response?.data || error.message
        );
      }
    };


    // Reset main shoe when none is selected
    const resetMainShoe = () => {
      mainShoe.value = null;
      selectedShoe.value = "No main shoe selected";
      cushioningPercentage.value = 0;
      kmRan.value = 0;
      mileage_remaining.value = 0;
    };

    const setAsMainShoe = async (shoe) => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No token found in localStorage");
        return;
      }
      console.log("shoeid: " + shoe.id);
      try {
        // Call the API to set the main shoe
        const response = await axios.post(
          "http://127.0.0.1:5000/user/set-main-shoe",
          { model_name: shoe.model_name },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        console.log(response.data.message);
        await fetchUserProfile(); // Refresh profile data after updating the main shoe
      } catch (error) {
        console.error(
          "Error setting main shoe:",
          error.response?.data || error.message
        );
      }
      window.location.reload();
    };

    // Remove a shoe
    const removeShoe = async (shoeId) => {
      userShoesCount.value = 0;
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No token found in localStorage");
        return;
      }

      try {
        await axios.delete(`http://127.0.0.1:5000/user/remove-shoe/${shoeId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        userShoes.value = userShoes.value.filter((shoe) => shoe.id !== shoeId);
      } catch (error) {
        console.error(
          "Error removing shoe:",
          error.response?.data || error.message
        );
      }
    };

    const filteredData = computed(() => {
      const query = searchQuery.value.toLowerCase().trim();

      return allShoes.value.filter((shoe) => {
        const matchesSearch = `${shoe.shoe_brand} ${shoe.model_name}`
          .toLowerCase()
          .includes(query);

        return matchesSearch;
      });
    });

    const addShoeToAccount = async (shoe) => {
      searchQuery.value = "";
      const token = localStorage.getItem("authToken");

      if (!token) {
        console.error("No token found in localStorage");
        return;
      }

      if (!shoe || !shoe.model_name) {
        console.error("Invalid shoe object:", shoe);
        return;
      }

      try {
        // Add the shoe to the user's account
        await axios.post(
          "http://127.0.0.1:5000/user/add-shoe",
          { shoe_id: shoe.id },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        console.log(
          `Shoe added to user's account: ${shoe.shoe_brand} - ${shoe.model_name}`
        );

        // Fetch updated user profile data
        const updatedProfile = await fetchUserProfile();
        console.log("Updated Profile:", updatedProfile);

        // If this is the first shoe, set it as the main shoe
        if (userShoes.value.length < 2) {
          try {
            const response = await axios.post(
              "http://127.0.0.1:5000/user/set-main-shoe",
              { model_name: shoe.model_name }, // Pass model_name instead of shoe_id
              { headers: { Authorization: `Bearer ${token}` } }
            );
            console.log(response.data.message);

            // Refresh profile data after updating the main shoe
            await fetchUserProfile();
            window.location.reload();
          } catch (error) {
            console.error("Error setting main shoe:", error);
          }
        } else {
          manageShoes.value = true;
        }

        showShoeDropdown.value = false;
      } catch (error) {
        console.error(
          "Error adding shoe:",
          error.response?.data || error.message
        );
      }
    };

    // Toggle shoe dropdown
    // const toggleShoeDropdown = () => {
    //   showShoeDropdown.value = !showShoeDropdown.value;
    // };

    // Fetch all shoes
    const fetchAllShoes = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/shoes");
        allShoes.value = response.data;
      } catch (error) {
        console.error(
          "Error fetching shoes:",
          error.response?.data || error.message
        );
      }
    };

    // Fetch mileage
    const fetchMileageRun = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No token found in localStorage");
        return;
      }

      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/user/mileage-run",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const { mileage_run, mileage_remaining, cushioning_percentage } =
          response.data;

        kmRan.value = mileage_run;
        mileage_remaining.value = mileage_remaining;
        cushioningPercentage.value = cushioning_percentage;
      } catch (error) {
        console.error(
          "Error fetching mileage:",
          error.response?.data || error.message
        );
      }
    };

    // Activities
    const fetchLatestActivity = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/activities");
        activities.value = response.data; // Update activities with the fetched data
        console.log("Fetched latest activities:", activities.value);
      } catch (error) {
        console.error(
          "Error fetching latest activity:",
          error.response?.data || error.message
        );
      }
      fetchActivity.value = true;
    };

    const addActivity = async (activity, index) => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No token found in localStorage");
        return;
      }

      try {
        console.log("Sending activity ID:", activity.id);
        // Log the selected activity for debugging
        console.log("Adding activity:", activity);

        // Update the main shoe before adding the activity
        await fetchUserProfile();

        // Send the selected activity's ID to the backend
        await axios.post(
          "http://127.0.0.1:5000/update-activities",
          { activity_id: activity.id }, // Only send the ID of the selected activity
          { headers: { Authorization: `Bearer ${token}` } }
        );

        // Remove the added activity from the list
        activities.value.splice(index, 1);
      } catch (error) {
        console.error(
          "Error adding activity:",
          error.response?.data || error.message
        );
      }

      // Reload the page to reflect changes
      window.location.reload();
    };


    // Check login status
    const checkLoginStatus = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        goToLogin();
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/verify-token", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.status === 200) {
          isLoggedIn.value = true;
          await fetchUserProfile();
        } else {
          goToLogin();
        }
      } catch (error) {
        console.error(
          "Error verifying token:",
          error.response?.data || error.message
        );
        goToLogin();
      }
    };

    // Watch for changes in cushioningPercentage and update progress gradient
    watch(cushioningPercentage, (newValue) => {
      progressGradient.value = generateProgressGradient(newValue);
    });

    // Function to generate the progress gradient
    const generateProgressGradient = (percentage) => {
      if (percentage > 20) {
        const brightnessFactor = percentage / 100;
        const adjustedTopColor = `rgb(
        ${10 + (245 - 10) * (1 - brightnessFactor)}, 
        ${122 + (203 - 122) * (1 - brightnessFactor)}, 
        ${52 + (191 - 52) * (1 - brightnessFactor)})`;
        return `linear-gradient(to top, #C5CBBF, ${adjustedTopColor})`;
      } else if (percentage <= 20 && percentage > 0) {
        const adjustedTopColor = `rgb(
        ${232}, 
        ${82}, 
        ${82})`;
        console.log("percentage  :" , percentage)
        return `linear-gradient(to top, #E85252, ${adjustedTopColor})`;
      } else {
        const adjustedTopColor = `rgb(
        ${0}, 
        ${0}, 
        ${0})`;
        return `linear-gradient(to top, #000000, ${adjustedTopColor})`;
      }
    };

    // Progress bar gradient computed property
    const progressGradient = computed(() =>
      generateProgressGradient(cushioningPercentage.value)
    );

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
      // toggleShoeDropdown,
      searchQuery,
      filteredData,
      fetchAllShoes,
      fetchMileageRun,
      fetchLatestActivity,
      addActivity,
      progressGradient,
      profileClicked,
      manageShoes,
      fetchActivity,
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

.no-shoe {
  text-align: center;
  margin-top: 120%;
}

.width {
  width: 90%;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

/*
button {
  background-color: #42b983;
  border: none;
  padding: 10px 20px;
  color: white;
  border-radius: 5px;
  cursor: pointer;
} */

.title {
  width: 60%;
  text-align: left;
  margin-top: 22.8%;
}

.container {
  width: 45vw;
  border-radius: 8px;
  margin: 6px;
  display: flex;
  justify-content: center;
}

.content {
  background-color: #171717;
  padding: 6px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  position: relative;
}

.main {
  display: flex;
  justify-content: center;
  flex-direction: column;
}

.top {
  width: 97%;
  height: 210px;
}

.top-c {
  padding: 10px;
  width: 100%;
}

.km-ran {
  height: 125px;
}

.profile {
  height: 211.5px;
}

.center {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.profile-img {
  width: 60px;
  stroke: #d6d6d6;
  color: #d6d6d6;
  padding: 2px;
}

.margin {
  margin-top: 2px;
}

h3 {
  font-size: 16px;
}

.name {
  font-size: 20px;
  padding: 2px;
}

.shoe-profile {
  text-align: center;
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

.col {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: absolute;
  bottom: 18px;
}

.activity-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
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

/* .shoe-item button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.shoe-item button:hover {
  opacity: 0.8;
} */

.profile-container {
  border: 2px solid red;
}

.close-btn {
  top: 6px;
  margin-top: 22.8%;
  right: 12px;
  background: none;
  border: none;
  color: #d6d6d6;
  font-size: 16px;
  font-family: "Light", sans-serif;
}

.profile-settings {
  margin-top: 80px;
  height: 120px;
}

.search-container {
  position: relative;
  display: inline-block;
  width: 68%;
}

.search-bar {
  width: 100%;
  background-color: #171717;
  border-radius: 8px;
  border-style: none;
  padding: 8px;
  margin-top: 20px;
  font-size: 16px;
  box-sizing: border-box;
  color: #3f3f3f;
  font-family: "Text", sans-serif;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 45%;
  pointer-events: none;
}

.results-bg {
  margin-top: 12px;
  background-color: #171717;
  border-radius: 8px;
  overflow-y: auto; /* Maak de lijst scrollbaar */
  padding: 0 10px;
  box-sizing: border-box;
  max-height: 44vh; /* Zorgt dat er ruimte is */
}

.user-shoes-bg {
  margin-top: 12px;
  background-color: #171717;
  width: 100%;
  border-radius: 8px;
  overflow-y: auto; /* Maak de lijst scrollbaar */
  padding: 0;
  box-sizing: border-box;
  max-height: 44vh; /* Zorgt dat er ruimte is */
}

.activities-bg {
  margin-top: 12px;
  background-color: #171717;
  width: 90vw;
  border-radius: 8px;
  overflow-y: auto; /* Maak de lijst scrollbaar */
  padding: 12px;
  box-sizing: border-box;
  max-height: 44vh; /* Zorgt dat er ruimte is */
}

.results {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
}

.results li {
  margin-bottom: 10px;
  padding: 6px 0 0 0;
  border-radius: 5px;
}

.no-results {
  margin-top: 20px;
  font-size: 18px;
  color: #888;
}

img {
  width: 62px;
  height: 48px;
}

.shoe {
  border-bottom: 0.2px solid #3f3f3f;
  padding-left: 8px;
  padding-bottom: 16px;
  height: 58px;
  display: flex;
  align-items: center;
}

.row {
  display: flex;
  flex-direction: row;
  margin-top: 18px;
  gap: 6px;
}

.shoe-name {
  width: 100px;
  padding-left: 16px;
}

.col {
  display: flex;
  flex-direction: column;
}

.btn-activities {
  font-family: "text-b";
  font-size: 13px;
  background: linear-gradient(to right, #e02b07, #fc6e02);
  border-radius: 18px;
  padding: 6px 10px;
  color: white;
  border: none;
}

.btn-shoes-active {
  font-family: "text-b";
  font-size: 13px;
  background: #3f3f3f;
  border-radius: 18px;
  padding: 6px 10px;
  color: white;
  border: none;
}

.btn-shoes {
  font-family: "text-b";
  font-size: 13px;
  border-radius: 18px;
  padding: 6px 10px;
  color: white;
  border: none;
  background: linear-gradient(to right, #0b7b35 0%, #14e161 100%);
}

.btn-add {
  position: absolute;
  right: 0;
  font-family: "text-b";
  font-size: 13px;
  border-radius: 18px;
  padding: 6px 10px;
  color: white;
  border: none;
  background: linear-gradient(to right, #0b7b35 0%, #14e161 100%);
}

.btn-close {
  font-family: "text-b";
  font-size: 16px;
  background: none;
  border-radius: 18px;
  padding: 6px 10px;
  color: white;
  border: none;
  /* background-color: #e02b07; */
}
</style>
