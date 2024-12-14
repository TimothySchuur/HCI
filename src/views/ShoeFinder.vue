<template>
   <div v-if="questionNum>0" class="pos-back">
      <div style="flex-direction: column;" @click="questionNum--">
        <p class="questionNum">{{ questionNum }} / 4</p>
        <img style="margin-top: 12px;" src="../img/arrow_back_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg">
      </div>
   </div>

  <div class="width">
    
    <h1  v-if="questionNum === 0" class="title">SHOE FINDER</h1>

    <!-- Filters -->
    <div v-if="!selectedShoe" :style="questionNum == 3 ? 'bottom: -11.4%' : 'bottom: 0'" class="content">


      <p class="question">{{ question[questionNum] }}</p>

      <div class="pos-btn" v-if="questionNum === 0">
        <button class="btn-gradient" @click="questionNum++">START</button>
      </div>

      <!-- Conditional rendering of gender options -->
      <div class="pos-btn" v-if="questionNum === 1">
        <button
          v-for="(option, index) in genderOptions"
          :key="index"
          class="btn-option"
          @click="setFilter('gender', option)"
        >
          {{ option }}
        </button>
      </div>

      <!-- Conditional rendering of main focus options -->
      <div v-if="questionNum === 2">
        <button
          v-for="(option, index) in mainFocusOptions"
          :key="index"
          class="btn-option"
          @click="setFilter('main_focus', option)"
        >
          {{ option }}
        </button>
      </div>

      <!-- Conditional rendering of eco-friendly options -->
      <div v-if="questionNum === 3">
        <button
          v-for="(option, index) in footTypeOptions"
          :key="index"
          class="btn-option"
          @click="setFilter('foot_type', option)"
        >
          {{ option }}
        </button>
      </div>

      <!-- Conditional rendering of mileage options -->
      <div v-if="questionNum === 4">
        <!-- Slider -->
      <div class="slider-container">
        <!-- Value Box Above the Slider -->
        <div 
          v-if="plannedMaxDistance" 
          class="value-box" 
          :style="{ 
            left: `${sliderPosition}%`, 
            transform: 'translateX(-50%)', /* Center the value box horizontally */
            bottom: '20px' /* Adjust to place it above the slider */
          }"
        >
          {{ plannedMaxDistance }}
        </div>

        <input 
          class="slider" 
          v-model="plannedMaxDistance" 
          min="0" 
          max="50" 
          step="5" 
          type="range"
          @input="updateSliderPosition"
        >
      </div>


        <button
          v-for="(option, index) in mileageOptions"
          :key="index"
          class="btn-gradient"
          @click="setFilter('mileage', option)"
        >
          {{ option }}
        </button>
      </div>
      
      <div v-if="questionNum > 4">
        <div class="results-bg">
        <ul v-if="filteredData.length > 0" class="results">
          <li v-for="(shoe, index) in filteredData" :key="index">
            <div @click="shoeInformation(shoe)" class="row shoe">
              <img src="../img/shoe.png" />
              <div class="shoe-name text-s">{{ shoe.shoe_brand }} {{ shoe.model_name }}</div>
              <div class="col">
                <div class="row ratings-s text-s">
                  <p>CUS</p>
                  <p>DUR</p>
                  <p>PAC</p>
                </div>
                <div style="margin-top: 8px;" class="row ratings-s text-b">
                  <p>{{ shoe.cushioning_rate }}</p>
                  <p>{{ shoe.durability_rate }}</p>
                  <p>{{ shoe.pace_rate }}</p>
                </div>
              </div>
            </div>
          </li>
        </ul>

        <h4 v-else class="no-results">No results found...</h4>
      </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";

export default {
  name: "ComparePage",
  setup() {
    const questionNum = ref(0);
    const question = ref([
      "Answer 4 quick questions to find the perfect running shoes for you!", 
      "What type of shoes are you looking for?", 
      "What is your main focus?", 
      "What describes your foot type best?", 
      "Wat is the longest distance you plan to run in this shoes?"
    ]);
    const data = ref([]);
    const searchQuery = ref("");
    const selectedShoe = ref(null);
    const plannedMaxDistance = ref(null);
    const sliderPosition = ref(50);

    const genderOptions = ref([
      "MALE",
      "FEMALE",
    ]);
    const mileageOptions = ref(["High distance coverage"]);
    const mainFocusOptions = ref([
      "DURABILITY",
      "SPEED",
      "TRAIL RUNNING",
      "ALL-ROUND",
    ]);
    const footTypeOptions = ref([
      "SMALL FEET",
      "NARROW FEET",
      "NEUTRAL",
      "HIGH ARCHES",
      "FLAT FEET",
      "WIDE FEET",
      // "OVER PRONATION"
    ]);

    const selectedGender = ref(null);
    const selectedMileage = ref(null);
    const selectedMainFocus = ref(null);
    const selectedFootType = ref(null);

    const setFilter = (filterType, option) => {
      questionNum.value += 1;
      if (filterType === "gender") {
        selectedGender.value = selectedGender.value === option ? null : option;
      }
      if (filterType === "mileage") {
        selectedMileage.value = selectedMileage.value === option ? null : option;
      }
      if (filterType === "main_focus") {
        selectedMainFocus.value =
          selectedMainFocus.value === option ? null : option;
      }
      if (filterType === "foot_type") {
        selectedFootType.value =
          selectedFootType.value === option ? null : option;
      }
    };

    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/compare-shoes");
        data.value = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const filteredData = computed(() => {
      const query = searchQuery.value.toLowerCase().trim();
      return data.value.filter((shoe) => {
        const matchesSearch = `${shoe.shoe_brand} ${shoe.model_name}`
          .toLowerCase()
          .includes(query);
        
          const matchesGender = 
          !selectedGender.value || 
          (selectedGender.value === "MALE" ? shoe.gender.includes("Men") || shoe.gender.includes("Unisex") : 
          selectedGender.value === "FEMALE" ? shoe.gender.includes("Women")|| shoe.gender.includes("Unisex") : true);


        const matchesMileage =
          !selectedMileage.value || shoe.mileage > 800;

         const matchesMainFocus =
            !selectedMainFocus.value ||
            shoe.main_focus.toLowerCase().includes(selectedMainFocus.value.toLowerCase()) ||
            (selectedMainFocus.value === "High cushioning" && shoe.main_focus.toLowerCase().includes("cushion")) ||
            (selectedMainFocus.value === "Speed" && 
              (shoe.main_focus.toLowerCase().includes("sprint") || 
              shoe.main_focus.toLowerCase().includes("race") || 
              shoe.main_focus.toLowerCase().includes("speed"))) ||
            (selectedMainFocus.value === "Stability" && shoe.main_focus.toLowerCase().includes("stability")) ||
            (selectedMainFocus.value === "Daily Training" && shoe.main_focus.toLowerCase().includes("training")) ||
            (selectedMainFocus.value === "Long Distance" && shoe.main_focus.toLowerCase().includes("distance"));


        const matchesFootType =
          !selectedFootType.value || shoe.foot_type.includes(selectedFootType.value.toLowerCase());

        return matchesSearch && matchesGender && matchesMileage && matchesMainFocus && matchesFootType;
      });
    });

    const updateSliderPosition = () => {
      sliderPosition.value = (plannedMaxDistance.value / 50) * 100;
    }
    const calculateSimilarity = (shoe) => {
      if (!selectedShoe.value) return 0;
      let score = 0;
      score += shoe.cushioning_rate === selectedShoe.value.cushioning_rate ? 1 : 0;
      score += shoe.durability_rate === selectedShoe.value.durability_rate ? 1 : 0;
      score += shoe.pace_rate === selectedShoe.value.pace_rate ? 1 : 0;
      return score / 3;
    };

    const similarShoes = computed(() => {
      if (!selectedShoe.value) return [];
      return data.value
        .map((shoe) => {
          const similarityScore = calculateSimilarity(shoe);
          return { ...shoe, similarityScore };
        })
        .filter((shoe) => shoe.similarityScore > 0.5)
        .sort((a, b) => b.similarityScore - a.similarityScore);
    });

    const mainContentStyle = computed(() =>
      selectedShoe.value ? "height: 78%;" : "height: 52%;"
    );


    onMounted(fetchData);

    return {
  data,
  question,
  questionNum,
  searchQuery,
  filteredData,
  selectedShoe,
  genderOptions,
  mileageOptions,
  similarShoes,
  mainFocusOptions,
  footTypeOptions,
  selectedGender,
  selectedMileage,
  selectedMainFocus,
  selectedFootType,
  plannedMaxDistance,
  sliderPosition,
  updateSliderPosition,
  setFilter,
  shoeInformation: (shoe) => {
    selectedShoe.value = shoe;
    searchQuery.value = ""; // Clear the search query
    console.log(shoe);
  },
  closeShoeInformation: () => (selectedShoe.value = null),
  mainContentStyle,
};

  },
};
</script>

<style scoped>
h3{
  font-family: 'Headers', sans-serif;
  font-size: 16px;
}
.width {
  width: 90%;
  height: 82vh;
  position: relative;
}

.title {
  width: 60%;
  text-align: left;
  margin-top: 132%;
}

.pos-back{
  width: 100%;
  text-align: center;
  position: absolute;
  top: 18%;
  z-index: 10;
  justify-content: center;
  align-content: center;
}

.questionNum{
  text-align: center;
  width: 100%;
  font-family: 'Light', sans-serif;
}

.content{
  display: flex;
  flex-direction: column;
  /* padding-top: 6px; */
  width: 100%;
  position: absolute;
  /* bottom: 0; */
  bottom: -12%;
}

.question{
  margin-top: 18px;
  width: 100%;
  text-align: left;
  font-family: 'Text', sans-serif;
}

.pos-btn{
  margin-top: 12px;
}

button{
  margin-top: 12px;
  width: 100%;
  box-sizing: border-box;
  padding: 16px;
  border-radius: 8px;
  color: #D6D6D6;
  font-size: 22px;
  font-family: 'Light', sans-serif;
  border: none;
}

.btn-gradient{
  background: linear-gradient(to right, #0B7B35, #14E161);
  font-family: 'Headers', sans-serif;
  padding: 22px;
}

.btn-option{
  background: #171717;
  border: solid #212121 3px;
}

.search-container {
  position: relative;
  display: inline-block;
  width: 100%;
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
  color: #3F3F3F;
  font-family: 'Text', sans-serif;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 45%;
  pointer-events: none;
}

.main-content {
  margin-top: 12px;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow-y: none; /* Zorgt dat scrollen mogelijk is */
}
.tags {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px;
  justify-content: flex-start; /* Tags worden nu links uitgelijnd */
  list-style-type: none;
  margin-bottom: 12px;
}


.tag {
  background-color: #2c2c2c;
  color: #D6D6D6;
  padding: 4px 8px;
  border-radius: 8px;
  font-family: 'Text', sans-serif;
  font-size: 13px;
}


.shoe-details {
  width: 100%;
  background-color: #171717;
  color: #D6D6D6;
  box-sizing: border-box;
  padding: 20px 0;
  border-radius: 8px;
  margin-top: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.close-btn {
  position: absolute;
  top: 6px;
  right: 12px;
  background: none;
  border: none;
  color: #D6D6D6;
  font-size: 16px;
  font-family: 'Light', sans-serif;
}

.ratings {
  display: flex;
  align-content: center;
  /* margin: 10px; */
}

.light {
  font-family: 'Light', sans-serif;
  font-size: 16px;
}

.container-rating{
  margin-top: 6px;
  height: 66px;
  width: 96px;
  position: relative;
  display: flex;
  align-items: center;
  background-color: #212121;
  border-radius: 8px;
  display: flex;
  justify-content: center;
}

.rating{
  position: absolute;
  height: 80%;
  width: 100%;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  bottom: 0;
  z-index: 0;
}

.spacing-ratings{
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  margin: 10px 24px 0 24px;
  text-align: center;
  width: 60px;
  font-family: 'SemiBold', sans-serif;
  font-size: 32px;
  z-index: 5;
}

img {
  width: 62px;
  height: 48px;
}

.shoe {
  border-bottom: .2px solid #3F3F3F;
  padding-left: 8px;
  padding-bottom: 16px;
  height: 58px;
  display: flex;
  align-items: center;
}

.row {
  display: flex;
  flex-direction: row;
}

.shoe-name {
  width: 100px;
  padding-left: 12px;
}

.col {
  display: flex;
  flex-direction: column;
}

.ratings-s {
  margin-left: 12px;
}

p {
  text-align: center;
  width: 44px;
}

.results-bg {
  margin-top: 12px;
  background-color: #171717;
  border-radius: 8px;
  overflow-y: auto; /* Maak de lijst scrollbaar */
  padding: 0 10px;
  box-sizing: border-box;
  max-height: calc(100vh - 150px); /* Zorgt dat er ruimte is */
}

.results {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
}

.results li {
  margin-bottom: 10px;
  padding: 6px;
  border-radius: 5px;
}

.no-results {
  margin-top: 20px;
  font-size: 18px;
  color: #888;
}
.filters {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 90%;
}

.filters button {
  padding: 6px 10px;
  background: #3F3F3F;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Light', sans-serif;
  white-space: nowrap;
}

.filters button.active {
  background: #D6D6D6;
  color: #000;
  font-family: 'SemiBold', sans-serif;
}

.slider-container {
  position: relative;
  width: 100%;
  background-color: #171717;
  height: 100px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
}

input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

input[type="range"]::-webkit-slider-runnable-track {
  background: #14DF61;
  height: 0.5rem;
  border-radius: 3px; /* Round the track */
  outline: none; /* Remove focus outline */
}

input[type="range"]::-webkit-slider-thumb {
   -webkit-appearance: none; /* Override default look */
   appearance: none;
   margin-top: -4px; /* Centers thumb on the track */
   background-color: #0B7C36;
   height: 1rem; /* Makes the thumb circular by matching height and width */
   width: 1rem; /* Same as height for a circle */
   border-radius: 50%; /* Ensures it is a circle */
}

.slider {
  width: 80%;
  color: #14E161;
}

.value-box {
  clip-path: polygon(0% 0%, 0% 75%, 50% 100%, 100% 75%, 100% 0%);
  position: absolute;
  bottom: 64px;
  transform: translateX(-50%);
  background-color: #D9D9D9;
  color: #171717;
  padding: 5px 8px 10px 8px;
  border-radius: 6px;
  font-weight: bold;
  white-space: nowrap;
  font-family: 'Light', sans-serif;
}

.slider:focus + .value-box {
  display: block;
}
</style>
