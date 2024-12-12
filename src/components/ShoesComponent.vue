<template>
  <div id="shoes">
    <div class="bg"></div>
    <div style="background-color: white; position: fixed;">
      <table>
        <thead>
          <tr>
            <th>Brand</th>
            <th>Model</th>
            <th>Price ($)</th>
            <th>Mileage (km)</th>
            <th>Main Focus</th>
            <th>Eco-Friendly</th>
            <th>Foot Type</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="shoe in shoes" :key="shoe.id">
            <td>{{ shoe.shoe_brand }}</td>
            <td>{{ shoe.model_name }}</td>
            <td>{{ shoe.price }}</td>
            <td>{{ shoe.mileage }}</td>
            <td>{{ shoe.main_focus }}</td>
            <td>{{ shoe.eco_friendly ? "Yes" : "No" }}</td>
            <td>{{ shoe.foot_type }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import axios from 'axios';

export default {
  name: 'ShoesComponent',
  setup() {
    const shoes = ref([]);

    onMounted(() => {
      // Fetch data from the backend API
      axios
        .get('http://127.0.0.1:5000/api/shoes')
        .then((response) => {
          if (response.data && response.data.shoes) {
            shoes.value = response.data.shoes;
          } else {
            console.error('Invalid API response:', response);
          }
        })
        .catch((error) => {
          console.error('Error fetching data from API:', error);
        });
    });

    return {
      shoes,
    };
  },
};
</script>

<style scoped>
#running-shoes {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 100%;
  height: auto;
}

.bg {
  position: absolute;
  width: 90%; /* Adjust to fit the table */
  height: auto; /* Adapt to content */
  top: 10%; /* Adjust as needed */
  background-color: rgb(23, 23, 23);
  border-radius: 8px;
  z-index: -1;
}

table {
  width: 90%;
  border-collapse: collapse;
  margin-top: 20px;
  z-index: 1;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}
</style>
