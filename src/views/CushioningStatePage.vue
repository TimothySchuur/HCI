<template>
  <div class="width" v-if="!profileClicked">
      <!-- Page Content -->
      <h1 class="title">CUSHIONING STATE</h1>
      <div class="main">
        <div class="container top">
          <div class="content top-c">
            <!-- Pass the computed progressGradient as a prop to ShoeViewer -->
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
                <p style="color: #171717; font-family: 'SemiBold', sans-serif">122 KM</p>
                <p style="color: #171717; font-family: 'Light', sans-serif">REMAINING</p>
              </div>
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
  </div>
  <div v-else>
    <p>Profile page</p>
    <button @click="profilePage">Go back</button>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'; 
import ShoeViewer from '@/components/ShoeViewer.vue'; // Import the component
  
export default {
  name: 'CushioningStatePage', // Component name
  components: { ShoeViewer }, 
  setup() {
    // Reactive variables
    let kmRan = 12;
    let name = "TIMOTHY";
    let shoe = "Assics GEL-EXCITE 10";
    let profileClicked = ref(false);
    let cushioningPercentage = 99;

    // Methods
    const profilePage = () => {
      profileClicked.value = !profileClicked.value;
      console.log(profileClicked.value); // Check the value
    };

    // Computed property for dynamic gradient
    const progressGradient = computed(() => {
      const brightnessFactor = cushioningPercentage / 100; // Scale from 0.0 to 1.0
      const adjustedTopColor = `rgb(
        ${10 + (245 - 10) * (1 - brightnessFactor)}, 
        ${122 + (203 - 122) * (1 - brightnessFactor)}, 
        ${52 + (191 - 52) * (1 - brightnessFactor)})`;          
      return `linear-gradient(to top, #C5CBBF, ${adjustedTopColor})`; // Apply gradient
    });

    // Watch for changes to progressGradient
    watch(progressGradient, (newGradient) => {
      window.dispatchEvent(new CustomEvent('adjustedTopColorUpdated', { detail: newGradient }));
    });

    // Expose variables and methods
    return {
      kmRan,
      profilePage,
      name,
      shoe,
      profileClicked,
      cushioningPercentage,
      progressGradient,
      
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
  