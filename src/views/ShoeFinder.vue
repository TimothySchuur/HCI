<template>
    <div v-if="questionNum > 0 && questionNum <= 4 " class="pos-back">
      <div style="flex-direction: column;" @click="questionNum--">
        <p class="questionNum">{{ questionNum }} / 4</p>
        <img style="margin-top: 12px;" src="../img/arrow_back_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg">
      </div>
   </div>
   <div v-if="questionNum > 4" class="pos-restart">
      <div style="flex-direction: row;">
        <img @click="questionNum--" style="height: 32px;" src="../img/arrow_back_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg">
        <img @click="questionNum = 0" style="height: 32px; margin-left: -14px" src="../img/replay_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg">
      </div>
   </div>

  <div class="width">
    <div v-if="questionNum <= 4">
      <h1  v-if="questionNum === 0" class="title">SHOE FINDER</h1>

      <!-- Filters -->
      <div :style="questionNum == 3 ? 'bottom: -11.4%' : 'bottom: 0'" class="content">

        <p :style="questionNum == 4 ? 'margin-bottom: 12px' : ''"  class="question">{{ question[questionNum] }}</p>

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

        <!-- Conditional rendering of  focus options -->
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
            <div style="position: absolute; width: 77%; left: 50%; transform: translateX(-50%);">
              <div 
                v-if="plannedMaxDistance" 
                class="value-box" 
                :style="{ left: `${sliderPosition}%`, transform: 'translateX(-50%)' }"
              >
                {{ plannedMaxDistance }}
              </div>
            </div>

            <input 
              class="slider" 
              v-model="plannedMaxDistance" 
              min="0" 
              max="50" 
              step="5" 
              type="range"
              @input="updateSliderPosition"
              :style="sliderBackgroundStyle"
            >
            <div class="planned-distances">
              <p class="dist" style="left: 0">0</p>
              <p class="dist" style="left: 20%">10</p>
              <p class="dist" style="left: 40%">20</p>
              <p class="dist" style="left: 60%">30</p>
              <p class="dist" style="left: 80%">40</p>
              <p class="dist" style="left: 100%">50</p>
            </div>
          </div>

          <button
            class="btn-gradient"
            @click="setFilter('mileage', plannedMaxDistance)"
            :disabled="!plannedMaxDistance"
            style="z-index: 10;"
          >
            CONTINUE
          </button>
        </div>
      </div>
    </div>
      
      <div v-else class="main-content"> 
        <h1 class="title-end">SHOE MATCH</h1>   
      <!-- Shoe Details -->
      <h1 style="margin-top: 6px; font-size: 18px; width: 80%;"  v-if="selectedShoe">{{ selectedShoe.shoe_brand }} {{ selectedShoe.model_name }}</h1>
      <div v-if="selectedShoe" class="shoe-details col">
        <ul class="tags">
          <!-- Eco Friendly -->
          <li style="white-space: nowrap; display: flex; flex-direction: row; " v-if="selectedShoe.eco_friendly" class="tag">
            Eco-Friendly
            <img 
              style="width: 100%; margin-left: 6px; height: 16px;" 
              src="../img/eco_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg" 
              alt="Eco-Friendly Icon"
            />
          </li>

          <!-- Main Focus -->
          <li class="tag">Main focus: {{ selectedShoe.main_focus }}</li>
          <!-- Mileage -->
          <li class="tag">Mileage: {{ selectedShoe.mileage }}</li>
          <!-- Foot Type -->
          <li v-if="selectedShoe.foot_type" class="tag">Foot Type: {{ selectedShoe.foot_type }}</li>
          <!-- Price -->
          <li v-if="selectedShoe.price" class="tag">Price: €{{ selectedShoe.price }}</li>
        </ul>
  
        <img style="width: 260px; height: 100%" src="../img/shoe-big.png" alt="Shoe Image">
        <div class="ratings row">

          <div class="col spacing-ratings">
            <p class="center light">Cushioning</p> 
            <div class="container-rating">
              <p style="z-index: 2" class="center">{{ selectedShoe.cushioning_rate }}</p>
              <div :style="{ 
                height: selectedShoe ? selectedShoe.cushioning_rate * 10 + '%' : 'auto', 
                borderRadius: selectedShoe && selectedShoe.cushioning_rate === 10 ? '8px' : '',
                background: selectedShoe && selectedShoe.cushioning_rate > 5 ? 'linear-gradient(to top, #6DBB84, #067631)' : 'linear-gradient(to top, #C9432F, #C3210F)'
              }"
              class="rating"></div>
            </div>
          </div>
          <div class="col spacing-ratings">
            <p class="center light">Durability</p> 
            <div class="container-rating">
              <p style="z-index: 2" class="center">{{ selectedShoe.durability_rate }}</p>
              <div :style="{ 
                height: selectedShoe ? selectedShoe.durability_rate * 10 + '%' : 'auto', 
                borderRadius: selectedShoe && selectedShoe.durability_rate === 10 ? '8px' : '',
                background: selectedShoe && selectedShoe.durability_rate > 5 ? 'linear-gradient(to top, #6DBB84, #067631)' : 'linear-gradient(to top, #C9432F, #C3210F)'
              }"
              class="rating"></div>
            </div>
          </div>
          <div class="col spacing-ratings">
            <p class="center light">Pace</p> 
            <div class="container-rating">
              <p style="z-index: 2" class="center">{{ selectedShoe.pace_rate }}</p>
              <div :style="{ 
                height: selectedShoe ? selectedShoe.pace_rate * 10 + '%' : 'auto', 
                borderRadius: selectedShoe && selectedShoe.pace_rate === 10 ? '8px' : '',
                background: selectedShoe && selectedShoe.pace_rate > 5 ? 'linear-gradient(to top, #6DBB84, #067631)' : 'linear-gradient(to top, #C9432F, #C3210F)'
              }"
              class="rating"></div>
            </div>
          </div>
        </div>
      </div>

        <!-- Similar Shoes Section -->
      <h4 style="margin-top: 18px;" v-if="selectedShoe">Similar Shoes</h4>
      <div v-if="selectedShoe" class="results-bg">
        <ul class="results">
          <li v-for="(shoe, index) in similarShoes" :key="index">
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
      </div>

 

      <!-- Search Results -->
      <div v-if="!selectedShoe" class="results-bg">
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

</template>


<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";

export default {
  name: "ComparePage",
  setup() {
  
    const questionNum = ref(0 );
    const question = ref([
      "Answer 4 quick questions to find the perfect running shoes for you!", 
      "What type of shoes are you looking for?", 
      "What is your main focus?", 
      "What describes your foot type best?", 
      "Wat is the longest distance you plan to run in this shoes?"
    ]);
    const sliderBackgroundStyle = ref({
      background: "linear-gradient(to right, #14DF61 50%, #D9D9D9 50%)" // initial background
    });
    const data = ref([]);
    const searchQuery = ref("");
    const selectedShoe = ref(null);
    const plannedMaxDistance = ref(null);
    const sliderPosition = ref(50);

    const genderOptions = ref([
      "MALE",
      "FEMALE",
    ]);

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

    const selectRandomShoe = () => {
      const results = filteredData.value || []; // Default to an empty array
      console.log("Filtered Results:", results); // Debug filtered results
      if (results.length > 0) {
        selectedShoe.value = results[Math.floor(Math.random() * results.length)];
        console.log("Selected Shoe:", selectedShoe.value); // Debug selected shoe
      } else {
        console.warn("No shoes match the selected criteria.");
        selectedShoe.value = null; // Or show a default message
      }
    };



    const setFilter = (filterType, option) => {
      questionNum.value += 1;
      if (filterType === "gender") {
        selectedGender.value = selectedGender.value === option ? null : option;
      }
      if (filterType === "mileage") {
        selectedMileage.value = selectedMileage.value === plannedMaxDistance.value ? null : plannedMaxDistance.value;
      }
      if (filterType === "main_focus") {
        selectedMainFocus.value =
          selectedMainFocus.value === option ? null : option;
      }
      if (filterType === "foot_type") {
        selectedFootType.value =
          selectedFootType.value === option ? null : option;
      }

      if (questionNum.value > 4) {
        if (filteredData.value.length > 0) {
          selectRandomShoe();
        } else {
          console.warn("No shoes match the selected criteria.");
          selectedShoe.value = null; // Or show a default message
        }
      }


    };

    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/compare");
        data.value = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
  
    const filteredDataWithoutMileage = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  return data.value.filter((shoe) => {
    const matchesSearch = `${shoe.shoe_brand} ${shoe.model_name}`
      .toLowerCase()
      .includes(query);

    const matchesGender =
      !selectedGender.value ||
      (selectedGender.value === "MALE"
        ? shoe.gender.includes("Men") || shoe.gender.includes("Unisex")
        : selectedGender.value === "FEMALE"
        ? shoe.gender.includes("Women") || shoe.gender.includes("Unisex")
        : true);

    const matchesMainFocus =
      !selectedMainFocus.value ||
      shoe.main_focus.toLowerCase().includes(selectedMainFocus.value.toLowerCase());

    const matchesFootType =
      !selectedFootType.value ||
      (Array.isArray(shoe.foot_type)
        ? shoe.foot_type.some((type) =>
            type.toLowerCase().includes(selectedFootType.value.toLowerCase())
          )
        : shoe.foot_type?.toLowerCase().includes(selectedFootType.value.toLowerCase()));

    return matchesSearch && matchesGender && matchesMainFocus && matchesFootType;
  });
});


  const filteredData = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  const results = data.value.filter((shoe) => {
    const matchesSearch = `${shoe.shoe_brand} ${shoe.model_name}`
      .toLowerCase()
      .includes(query);

    const matchesGender =
      !selectedGender.value ||
      (selectedGender.value === "MALE"
        ? shoe.gender.includes("Men") || shoe.gender.includes("Unisex")
        : selectedGender.value === "FEMALE"
        ? shoe.gender.includes("Women") || shoe.gender.includes("Unisex")
        : true);

    const matchesMainFocus =
      !selectedMainFocus.value ||
      shoe.main_focus.toLowerCase().includes(selectedMainFocus.value.toLowerCase()) ||
      (selectedMainFocus.value === "DURABILITY" &&
        (shoe.main_focus.toLowerCase().includes("long distance") || shoe.main_focus.toLowerCase().includes("cushioned"))) ||
      (selectedMainFocus.value === "SPEED" &&
        (shoe.main_focus.toLowerCase().includes("sprint") || shoe.main_focus.toLowerCase().includes("race") || shoe.main_focus.toLowerCase().includes("speed"))) ||
      (selectedMainFocus.value === "TRAIL RUNNING" &&
        shoe.main_focus.toLowerCase().includes("trail")) ||
      (selectedMainFocus.value === "ALL-ROUND" &&
        (shoe.main_focus.toLowerCase().includes("daily training") ||
          shoe.main_focus.toLowerCase().includes("neutral") ||
          shoe.main_focus.toLowerCase().includes("stability")));

    const matchesFootType =
      !selectedFootType.value ||
      (Array.isArray(shoe.foot_type)
        ? shoe.foot_type.some((type) =>
            type.toLowerCase().includes(selectedFootType.value.toLowerCase())
          )
        : shoe.foot_type?.toLowerCase().includes(selectedFootType.value.toLowerCase()));

    const matchesMileage =
      !plannedMaxDistance.value ||
      (plannedMaxDistance.value <= 10 && shoe.mileage < 522 + 133.6) ||
      (plannedMaxDistance.value > 10 && plannedMaxDistance.value <= 20 && shoe.mileage < 522 + 2 * 133.6) ||
      (plannedMaxDistance.value > 20 && plannedMaxDistance.value <= 30 && shoe.mileage < 522 + 3 * 133.6) ||
      (plannedMaxDistance.value > 30 && plannedMaxDistance.value <= 40 && shoe.mileage < 522 + 4 * 133.6) ||
      (plannedMaxDistance.value > 40 && plannedMaxDistance.value <= 50 && shoe.mileage <= 522 + 5 * 133.6);

    return matchesSearch && matchesGender && matchesMainFocus && matchesFootType && matchesMileage;
  });

  // Return the results if any match, else fall back
  if (results.length > 0) {
    return results;
  } else {
    // Fallback to data without mileage filter
    return filteredDataWithoutMileage.value || [];
  }
});





    const updateSliderPosition = () => {
      sliderPosition.value = (plannedMaxDistance.value / 50) * 100;

      // Update slider background color based on the slider position
      sliderBackgroundStyle.value = {
        background: `linear-gradient(to right, #14DF61 ${sliderPosition.value}%, #D9D9D9 ${sliderPosition.value}%)`
      };
    };


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


    onMounted(fetchData);

    return {
      data,
      question,
      questionNum,
      searchQuery,
      filteredData,
      selectedShoe,
      genderOptions,
      similarShoes,
      mainFocusOptions,
      footTypeOptions,
      selectedGender,
      selectedMileage,
      sliderBackgroundStyle,
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
    };
    }
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

.title-end {
  width: 60%;
  text-align: left;
  z-index: 12;
  /* margin-top: 12%; */
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

.pos-restart{
  /* width: 90vw;  */
  position: absolute;
  top: 15%;
  z-index: 10;
  justify-content: left;
  right: 3%;
  /* align-content: center; */
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

.btn-gradient:disabled {
  background-color: #ccc; /* Light gray background */
  cursor: not-allowed;    /* Show not-allowed cursor */
  opacity: 0.3;           /* Slightly transparent */
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
  margin-top: 20.5%;
  width: 90%;
  position: fixed;
  display: flex;
  flex-direction: column;
  overflow-y: none; /* Zorgt dat scrollen mogelijk is */
  height: 84%;
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
  margin-bottom: 12px;
}

.value-box {
  clip-path: polygon(0% 0%, 0% 75%, 50% 100%, 100% 75%, 100% 0%);
  position: absolute;
  top: 0px;
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

.slider {
  width: 80%;
  top: 50%;
  transform: translateY(-50%);
  position: absolute;
  height: 8px;
  background: linear-gradient(to right, #0B7B35 0%, #14E161 100%); /* Default color */
  border-radius: 10px;
  outline: none;
  appearance: none;
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

input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

input[type="range"]::-webkit-slider-runnable-track {
  /* background: #14DF61; */
  height: 0.5rem;
  border-radius: 3px; /* Round the track */
  outline: none; /* Remove focus outline */
}

.planned-distances{
  width: 75%;
  position: relative;
  left: -2%;
  margin-top: 66px;
  /* transform: translateX(-50%); */
}

.dist{
  width: 10px;
  box-sizing: border-box;
  position: absolute;
  text-align: left;
  font-family: 'Light', sans-serif;
  font-size: 14px;
}

</style>
