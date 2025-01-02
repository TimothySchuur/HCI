// Import Firebase SDK
import { initializeApp } from 'firebase/app';

// Je Firebase-configuratie
const firebaseConfig = {
  apiKey: "AIzaSyByh_sGgAydZA6ihF6bOrSWWgBZdLHCGBg",
  authDomain: "runw-dc68c.firebaseapp.com",
  projectId: "runw-dc68c",
  storageBucket: "runw-dc68c.appspot.com",
  messagingSenderId: "945557284271",
  appId: "1:945557284271:web:c94ad07831884155f97b5a"
};

// Initialiseer Firebase
const firebaseApp = initializeApp(firebaseConfig);

// Exporteer de app om deze elders te kunnen gebruiken
export { firebaseApp };
