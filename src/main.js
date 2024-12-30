import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { firebaseApp } from './firebase/firebase'; // Import Firebase config

// Controleer of Firebase goed is geïnitialiseerd
console.log('Firebase App:', firebaseApp);

createApp(App)
  .use(router)
  .mount('#app');
