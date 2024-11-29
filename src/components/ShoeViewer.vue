<template>
  <div id="shoe-viewer">
    <div class="bg"></div>
    <canvas ref="canvas"></canvas>
    <!-- <div style="background-color: white; position: fixed">
    <input type="range" id="colorSlider" min="0" max="8" v-model="colorIndex" @input="updateColor" />
      </div> -->
  </div>
</template>
<script>
import { onMounted, ref } from 'vue';
import { setupThreeJS, updateShoeColor } from '../threeSetup';

export default {
  name: 'ShoeViewer',
  setup() {
    const canvas = ref(null);
    const colorIndex = ref(0);

    onMounted(() => {
      setupThreeJS(canvas.value);
    });

    const updateColor = () => {
      updateShoeColor(colorIndex.value);
    };

    return {
      canvas,
      colorIndex,
      updateColor
    };
  }
};
</script>

<style scoped>
#shoe-viewer {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 100%;
  height: 100%;
}

canvas {

}

input[type="range"] {
  margin-top: 10px;
  width: 80%;
}

.bg {
  position: absolute;
  width: 320px;  /* Fixed width for consistent sizing */
  top: 25%; /* Adjust position as needed */
  background-color: rgb(23, 23, 23);
  border-radius: 8px;
  /*border: 3px solid rgb(33, 33, 33);*/
  z-index: -1;
}

</style>
