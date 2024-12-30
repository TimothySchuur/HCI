<template>
    <div class="pos-nav">
      <div @click="$router.push('/home')" class="pos-icon">
        <img :src="imageSource2" />
      </div>
      <div @click="$router.push('/compare')" class="pos-icon">
        <img :src="imageSource1" />
      </div>
      <div @click="$router.push('/shoes')" class="pos-icon">
        <img :src="imageSource3" />
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    name: 'NavBar',
  
    setup() {
      const route = useRoute(); // Access the current route
  
      // Reactive computed property to determine the image source
      const isCompareRoute = computed(() => route.path.includes('compare'));
      const isHomeRoute = computed(() => route.path === '/home' || route.path === '/login' );
      const isShoeFinderRoute = computed(() => route.path.includes('shoes'));
  
      const imageSource1 = computed(() =>
        isCompareRoute.value ? require('@/img/Compare-active.svg') : require('@/img/Compare.svg')
      );
      const imageSource2 = computed(() =>
        isHomeRoute.value ? require('@/img/Cushioning-state-active.svg') : require('@/img/Shoe.svg')
      );
      const imageSource3 = computed(() =>
        isShoeFinderRoute.value ? require('@/img/Shoe-finder-active.svg') : require('@/img/Shoe-finder.svg')
      );
  
      return {
        imageSource1,
        imageSource2,
        imageSource3,
        isCompareRoute,
        isHomeRoute,
        isShoeFinderRoute
      };
    },
  };
  </script>
  

 <style>
.pos-nav{
    width: 100%;
    height: 80px;
    position: absolute;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(to top, #0D0D0D, #0d0d0d00);
}

.pos-icon{
    padding:0 44px 0 44px;
}
</style>

