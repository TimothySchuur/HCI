<template>
  <div id="shoe-viewer">
    <div class="bg"></div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { onMounted, ref, reactive, watch } from 'vue';
import { setupThreeJS } from '../threeSetup';

export default {
  name: 'ShoeViewer',
  props: {
    progressGradient: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const canvas = ref(null);
    const rgbVue = reactive({ r: 20, g: 224, b: 97 }); // Reactive RGB object

    // Function to dispatch the custom event with RGB values
    const updateRgbVue = () => {
      const rgbString = `rgb(${rgbVue.r}, ${rgbVue.g}, ${rgbVue.b})`;
      const event = new CustomEvent('adjustedTopColorUpdated', {
        detail: rgbString
      });
      window.dispatchEvent(event);
    };

    // Function to extract RGB values from progressGradient prop
    const extractRgbFromGradient = () => {
      const regex = /linear-gradient\([^)]+,\s*(rgb\([^)]+\))\)/;
      const match = props.progressGradient.trim().match(regex);

      if (match && match[1]) {
        const rgb = match[1];
        const rgbValues = rgb.match(/\d+(\.\d+)?/g).map(Number); // Extract and parse RGB values
        rgbVue.r = Math.round(rgbValues[0]);
        rgbVue.g = Math.round(rgbValues[1]);
        rgbVue.b = Math.round(rgbValues[2]);

        // Dispatch custom event with updated RGB
        updateRgbVue();
      } else {
        console.log('No match found for the regex');
      }
    };

    onMounted(() => {
      // Set timeout of 200ms (you can adjust as needed)
      setTimeout(() => {

        extractRgbFromGradient();
      }, 500);

      // Watch rgbVue for updates
      watch(rgbVue, () => {

        if (canvas.value) {
          setupThreeJS(canvas.value, rgbVue); // Pass updated rgbVue to Three.js
        }
      }, { deep: true, immediate: true });
    });

    return { canvas, rgbVue, updateRgbVue };
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
  height: 100%; /* Ensure the container has full height */
}

canvas {
  position: absolute;
  z-index: 10; /* Adjust the z-index of the canvas to avoid covering .bg */
}

.bg {
  position: absolute;
  width: 100%;
  top: 25%;
  background-color: rgb(23, 23, 23);
  border-radius: 8px;
  z-index: -1;
}
</style>
