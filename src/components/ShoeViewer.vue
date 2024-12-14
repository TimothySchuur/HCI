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
    const rgbVue = reactive({ r: 20, g: 224, b: 97 });

    // Function to dispatch the custom event with RGB values
    const updateRgbVue = () => {
      const event = new CustomEvent('adjustedTopColorUpdated', {
        detail: `rgb(${rgbVue.r}, ${rgbVue.g}, ${rgbVue.b})`
      });
      window.dispatchEvent(event);
    };

    // Watch rgbVue for changes, dispatching an event each time
    watch(rgbVue, updateRgbVue, { deep: true });

    onMounted(() => {
      setupThreeJS(canvas.value);

      // Log the original progressGradient to see its value
      console.log('Original progressGradient:', props.progressGradient);

      // Update the regex to handle spaces and line breaks inside the rgb() value
      const regex = /linear-gradient\([^)]+,\s*(rgb\([^)]+\))\)/;
      const match = props.progressGradient.trim().match(regex);

      if (match && match[1]) {
        const rgb = match[1]; // Extracted RGB value
        console.log('Extracted RGB:', rgb);

        // Extract the numeric RGB values from the string and round them
        const rgbValues = rgb.match(/\d+(\.\d+)?/g).map(Number); // This also handles decimals
        const roundedRgbValues = rgbValues.map(value => Math.round(value));

        // Construct the rounded RGB string
        const roundedRgbString = `rgb(${roundedRgbValues.join(', ')})`;

        // Dispatch custom event with the rounded RGB value
        const event = new CustomEvent('adjustedTopColorUpdated', { detail: roundedRgbString });
        window.dispatchEvent(event);
      } else {
        console.log('No match found for the regex');
      }
    });

    // Return the necessary bindings to the template
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
