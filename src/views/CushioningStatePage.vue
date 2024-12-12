<template>
  <div class="width" v-if="!profileClicked">
    <!-- Page Content -->
    <h1 class="title">CUSHIONING STATE</h1>

    <div class="main">
      <div class="container top">
        <div class="content top-c">
          <ShoeViewer />
        </div>
      </div>
      <div style="display: flex; flex-direction: row;">
        <div class="container">
          <div class="content progress-bar">
            <div class="progress" :style="{ height: cushioningPercentage + '%' }"></div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column">
          <div class="container">
            <div class="content km-ran">
              <div class="center"> 
                <h1>{{ kmRan }} KM</h1>
                <h4>RAN</h4>
              </div>
            </div>
          </div>
          <div class="container">
            <div @click="profilePage" class="content profile">
              <div class="center">
                <img class="profile-img" src="../img/profile-circle.svg">
                <h3 class="margin name">{{ name }}</h3>
                <h4 class="margin shoe">{{ shoe }}</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Overview Section -->
    <div class="profile-overview">
      <h2>Profile Overview</h2>
      <p><strong>ID:</strong> {{ athleteData.id }}</p>
      <p><strong>First Name:</strong> {{ athleteData.firstname }}</p>
      <p><strong>Last Name:</strong> {{ athleteData.lastname }}</p>
    </div>

    <!-- Activities Section -->
    <div class="activities">
      <h2>Recent Activities</h2>
      <ul>
        <li v-for="activity in activities" :key="activity.id">
          <p><strong>Name:</strong> {{ activity.name }}</p>
          <p><strong>Distance:</strong> {{ (activity.distance / 1000).toFixed(2) }} km</p>
          <p><strong>Date:</strong> {{ new Date(activity.start_date).toLocaleDateString() }}</p>
        </li>
      </ul>
    </div>
  </div>
  <div v-else>
    <p>Profile page</p>
    <button @click="profilePage">Go back</button>
  </div>
</template>


  
<script>
import { ref } from 'vue';
import axios from 'axios';
import ShoeViewer from '@/components/ShoeViewer.vue';

export default {
  name: 'CushioningStatePage',
  components: { ShoeViewer },
  setup() {
    // Reactive variables
    const kmRan = 12;
    const name = "TIMOTHY";
    const shoe = "Assics GEL-EXCITE 10";
    const profileClicked = ref(false);
    const cushioningPercentage = 80;
    const athleteData = ref({});
    const activities = ref([]); // Store activities

    // Fetch Profile Data
    const fetchProfileData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/profile');
        athleteData.value = response.data;
      } catch (error) {
        console.error('Error fetching profile data:', error);
      }
    };

    // Fetch Activities
    const fetchActivities = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/activities'); // Replace with your backend activities endpoint
        activities.value = response.data;
      } catch (error) {
        console.error('Error fetching activities:', error);
      }
    };

    // Fetch data on component mount
    fetchProfileData();
    fetchActivities();

    // Methods
    const profilePage = () => {
      profileClicked.value = !profileClicked.value;
    };

    // Expose variables and methods to the template
    return {
      kmRan,
      profilePage,
      name,
      shoe,
      profileClicked,
      cushioningPercentage,
      athleteData,
      activities, // Expose activities
    };
  },
};

  </script>
  
  <style scoped>
  .width{
    width: 90%;
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
    margin-top: 80px;
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

  .progress-bar{
    height: 360px
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

.progress{
  width: 100%;
  position: absolute; /* Anchor it to the bottom */
  bottom: 0;
  border-radius: 0 0 8px 8px;
  background: linear-gradient(to top, #C5CBBF, #0A7A34);
  transition: height 0.3s ease; /* Smooth height transitions */
}
.profile-overview {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.profile-overview h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.profile-overview p {
  margin: 5px 0;
}


  </style>
  