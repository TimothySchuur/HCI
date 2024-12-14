<template>
  <div class="width">
    <h1 class="title">SHOE COMPARISON</h1>

    <!-- Search Bar -->
    <div v-if="!selectedShoe" class="search-container">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search running shoe..." 
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

    <!-- Filters -->
    <div v-if="!selectedShoe" class="filters">
      <!-- Gender Filter -->
      <button
        v-for="(option, index) in genderOptions"
        :key="index"
        :class="{ active: selectedGender === option }"
        @click="setFilter('gender', option)"
      >
        {{ option }}
      </button>

      <button
        v-for="(option, index) in mileageOptions"
        :key="index"
        :class="{ active: selectedMileage === option }"
        @click="setFilter('mileage', option)"
      >
        {{ option }}
      </button>

      <button
        v-for="(option, index) in mainFocusOptions"
        :key="index"
        :class="{ active: selectedMainFocus === option }"
        @click="setFilter('main_focus', option)"
      >
        {{ option }}
      </button>

      <button
        v-for="(option, index) in ecoFriendlyOptions"
        :key="index"
        style="display: flex; flex-direction: row; "
        :class="{ active: selectedEcoFriendly === option }"
        @click="setFilter('eco_friendly', option)"
      >
        {{ option }} <img style="width: 100%; ; margin-left: 6px; height: 16px" src="../img/eco_24dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg">
      </button>
    </div>

    <!-- Main Content -->
    <div :style="mainContentStyle" class="main-content">
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
        <button @click="closeShoeInformation" class="close-btn"><u>Close</u></button>
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
import { ref, computed, onMounted, watch } from "vue";

export default {
  name: "ComparePage",
  setup() {
    const data = ref([]);
    const searchQuery = ref("");
    const selectedShoe = ref(null);

    const genderOptions = ref([
      "Male",
      "Female",
    ]);
    const mileageOptions = ref(["High distance coverage"]);
    const mainFocusOptions = ref([
      "Trail Running",
      "High cushioning",
      "Speed",
      "Stability",
      "Daily Training",
      "Long Distance",
    ]);
    const ecoFriendlyOptions = ref(["Eco friendly"]);

    const selectedGender = ref(null);
    const selectedMileage = ref(null);
    const selectedMainFocus = ref(null);
    const selectedEcoFriendly = ref(null);

    const setFilter = (filterType, option) => {
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
      if (filterType === "eco_friendly") {
        selectedEcoFriendly.value =
          selectedEcoFriendly.value === option ? null : option;
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
          .includes(query);
        
          const matchesGender = 
          !selectedGender.value || 
          (selectedGender.value === "Male" ? shoe.gender.includes("Men") || shoe.gender.includes("Unisex") : 
          selectedGender.value === "Female" ? shoe.gender.includes("Women")|| shoe.gender.includes("Unisex") : true);


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



        const matchesEcoFriendly =
          !selectedEcoFriendly.value || shoe.eco_friendly === true;

        return matchesSearch && matchesGender && matchesMileage && matchesMainFocus && matchesEcoFriendly;
      });
    });

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

    // Watcher to reset selectedShoe and filters when searchQuery changes
    watch(searchQuery, () => {
      if (searchQuery.value.trim() !== "") {
        selectedShoe.value = null;

        // Reset filters when typing in the search bar
        selectedMileage.value = null;
        selectedMainFocus.value = null;
        selectedEcoFriendly.value = null;
      }
    });

    onMounted(fetchData);

    return {
  data,
  searchQuery,
  filteredData,
  selectedShoe,
  genderOptions,
  mileageOptions,
  similarShoes,
  mainFocusOptions,
  ecoFriendlyOptions,
  selectedGender,
  selectedMileage,
  selectedMainFocus,
  selectedEcoFriendly,
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
  height: 100vh;
}

.title {
  width: 60%;
  text-align: left;
  margin-top: 80px;
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

</style>
