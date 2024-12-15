import { reactive } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let scene, camera, renderer, controls, shoeModel, customMaterial;
const rgbVue = reactive({ r: 0, g: 0, b: 0 });


function setupThreeJS(canvas) {
    const shoeViewer = document.getElementById('shoe-viewer');

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(shoeViewer.clientWidth, shoeViewer.clientHeight);
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Scene
    scene = new THREE.Scene();

    // Camera
    const aspectRatio = shoeViewer.clientWidth / shoeViewer.clientHeight;
    camera = new THREE.PerspectiveCamera(25, aspectRatio, 1, 1000);
    camera.position.set(4, 5, 12);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.enablePan = false;
    controls.minDistance = 8;
    controls.maxDistance = 12;
    controls.minPolarAngle = 0.6;
    controls.maxPolarAngle = Math.PI * 0.6;
    controls.target.set(0, 0, 0);
    controls.update();

    // Lights
    const lights = [
        new THREE.DirectionalLight(0xffffff, 20),
        new THREE.DirectionalLight(0xffffff, 20),
        new THREE.DirectionalLight(0xffffff, 10),
        new THREE.DirectionalLight(0xffffff, 10),
        new THREE.AmbientLight(0xffffff, 10),
    ];
    lights[0].position.set(0, 10, 0);
    lights[1].position.set(0, -10, 0);
    lights[2].position.set(-10, 0, 0);
    lights[3].position.set(10, 0, 0);
    lights[4].position.set(0, 0, 0);
    lights.forEach(light => scene.add(light));

    // Listen for the custom event dispatched from Vue
    window.addEventListener('adjustedTopColorUpdated', (event) => {
        const newColor = event.detail; // Extract the color passed from Vue
        const rgbValues = newColor.match(/\d+/g).map(Number); // Extract RGB values as an array of numbers
    
        if (rgbValues.length === 3) {
            // Round and clamp the RGB values to integers between 0 and 255
            rgbValues.forEach((value, index) => {
                rgbValues[index] = Math.min(255, Math.max(0, Math.round(value)));
            });
    
            // Update the rgbVue to reflect the new values
            rgbVue.r = rgbValues[0];
            rgbVue.g = rgbValues[1];
            rgbVue.b = rgbValues[2];
    
            // Update the material uniforms for the color change
            if (customMaterial) {
                customMaterial.uniforms.r.value = rgbValues[0] / 255.0;
                customMaterial.uniforms.g.value = rgbValues[1] / 255.0;
                customMaterial.uniforms.b.value = rgbValues[2] / 255.0;
            }
    
            // Reload the shoe color with the updated state
            reloadShoeColor();
        } else {
            console.error('Invalid color format received:', newColor);
        }
    });
    
    
    
    // Shoe Group
    const shoeGroup = new THREE.Group();
    scene.add(shoeGroup);

    // Load Shoe Model
    const loader = new GLTFLoader();
    loader.load('Shoes-Make.gltf', (gltf) => {
        shoeModel = gltf.scene;
        const boundingBox = new THREE.Box3().setFromObject(shoeModel);
        const center = boundingBox.getCenter(new THREE.Vector3());
        shoeModel.position.sub(center);
        shoeGroup.add(shoeModel); // Add the model to the group
        reloadShoeColor(); // Now it's safe to call
    });
    

    // Initial Custom Material setup after color is received
    customMaterial = createCustomMaterial();

    // Animation Loop
    const clock = new THREE.Clock();
    function mainLoop() {
        const elapsedTime = clock.getElapsedTime();
        if (customMaterial) {
            customMaterial.uniforms.time.value = elapsedTime;
        }
        renderer.render(scene, camera);
        controls.update();
        requestAnimationFrame(mainLoop);
    }
    mainLoop();
}

function createCustomMaterial() {
    console.log("Creating material with rgbVue:", rgbVue); // Log before creating the material

    return new THREE.ShaderMaterial({
        uniforms: {
            time: { value: 0.0 },
            lightDirection: { value: new THREE.Vector3(1, 1, 1).normalize() },
            r: { value: rgbVue.r / 255.0 },
            g: { value: rgbVue.g / 255.0 },
            b: { value: rgbVue.b / 255.0 },
        },
        vertexShader: `
            varying vec3 vNormal;
            varying vec3 vViewPosition;
            void main() {
                vNormal = normalize(normalMatrix * normal);
                vec4 viewPosition = modelViewMatrix * vec4(position, 1.0);
                vViewPosition = -viewPosition.xyz;
                gl_Position = projectionMatrix * viewPosition;
            }
        `,
        fragmentShader: `
            uniform vec3 lightDirection;
            uniform float r, g, b;
            varying vec3 vNormal;
            varying vec3 vViewPosition;
            void main() {
                vec3 color = vec3(r, g, b);
                vec3 normal = normalize(vNormal);
                vec3 lightDir = normalize(lightDirection);
                vec3 viewDir = normalize(vViewPosition);
                float diff = max(dot(normal, lightDir), 0.0);
                vec3 reflectDir = reflect(-lightDir, normal);
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), 12.0) * 0.8;
                vec3 finalColor = (color * diff) + vec3(1.0) * spec * 0.5;
                gl_FragColor = vec4(finalColor, 1.0);
            }
        `,
    });
}

function reloadShoeColor() {
    if (!shoeModel) {
        console.warn("Shoe model is not loaded yet.");
        return;
    }

    shoeModel.traverse((child) => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            child.material =
                child.name === "Plane" || child.name === "Plane_1"
                    ? customMaterial
                    : new THREE.MeshPhongMaterial({ color: new THREE.Color(0, 0, 0), shininess: 10 });
        }
    });
}



export { setupThreeJS };

// import { reactive  } from 'vue'; // onMounted, watch, ref
// import * as THREE from 'three';
// import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
// import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// let scene, camera, renderer, controls, shoeModel, customMaterial;
// const rgbVue = reactive({ r: 0, g: 0, b: 0 });


// function setupThreeJS(canvas) {
//     const shoeViewer = document.getElementById('shoe-viewer');

//     // Renderer
//     renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
//     renderer.setSize(shoeViewer.clientWidth, shoeViewer.clientHeight);
//     renderer.setClearColor(0x000000, 0);
//     renderer.setPixelRatio(window.devicePixelRatio);
//     renderer.shadowMap.enabled = true;
//     renderer.shadowMap.type = THREE.PCFSoftShadowMap;

//     // Scene
//     scene = new THREE.Scene();

//     // Camera
//     const aspectRatio = shoeViewer.clientWidth / shoeViewer.clientHeight;
//     camera = new THREE.PerspectiveCamera(25, aspectRatio, 1, 1000);
//     camera.position.set(4, 5, 12);

//     // Controls
//     controls = new OrbitControls(camera, renderer.domElement);
//     controls.enableDamping = true;
//     controls.enablePan = false;
//     controls.minDistance = 8;
//     controls.maxDistance = 12;
//     controls.minPolarAngle = 0.6;
//     controls.maxPolarAngle = Math.PI * 0.6;
//     controls.target.set(0, 0, 0);
//     controls.update();

//     // Lights
//     const lights = [
//         new THREE.DirectionalLight(0xffffff, 20),
//         new THREE.DirectionalLight(0xffffff, 20),
//         new THREE.DirectionalLight(0xffffff, 10),
//         new THREE.DirectionalLight(0xffffff, 10),
//         new THREE.AmbientLight(0xffffff, 10),
//     ];
//     lights[0].position.set(0, 10, 0);
//     lights[1].position.set(0, -10, 0);
//     lights[2].position.set(-10, 0, 0);
//     lights[3].position.set(10, 0, 0);
//     lights[4].position.set(0, 0, 0);
//     lights.forEach(light => scene.add(light));

//     // Listen for the custom event dispatched from Vue
//     window.addEventListener('adjustedTopColorUpdated', (event) => {
//         const newColor = event.detail;
//         const rgbValues = newColor.match(/\d+/g).map(Number);
    
//         if (rgbValues.length === 3) {
//             rgbVue.r = rgbValues[0];
//             rgbVue.g = rgbValues[1];
//             rgbVue.b = rgbValues[2];
    
//             // if (shoeModel) { // Only call if shoeModel is loaded
//             //     reloadShoeColor();
//             // } else {
//             //     console.warn('Shoe model is not loaded yet; color change will be applied later.');
//             // }
//         }
//     });
    
    
    
    
//     // Shoe Group
//     const shoeGroup = new THREE.Group();
//     scene.add(shoeGroup);

//     // Load Shoe Model
//     const loader = new GLTFLoader();
//     // let isShoeModelLoaded = false;

//     loader.load('Shoes-Make.gltf', (gltf) => {
//         shoeModel = gltf.scene;
//         // isShoeModelLoaded = true;
//         const boundingBox = new THREE.Box3().setFromObject(shoeModel);
//         const center = boundingBox.getCenter(new THREE.Vector3());
//         shoeModel.position.sub(center);
//         shoeGroup.add(shoeModel);
//         // reloadShoeColor(); // Process pending updates
//     });

    

//     // Initial Custom Material setup after color is received
//     customMaterial = createCustomMaterial();

//     // Animation Loop
//     const clock = new THREE.Clock();
//     function mainLoop() {
//         const elapsedTime = clock.getElapsedTime();
//         if (customMaterial) {
//             customMaterial.uniforms.time.value = elapsedTime;
//         }
//         renderer.render(scene, camera);
//         controls.update();
//         requestAnimationFrame(mainLoop);
//     }
//     mainLoop();
// }

// function createCustomMaterial() {
//     console.log("Creating material with rgbVue:", rgbVue); // Log before creating the material

//     return new THREE.ShaderMaterial({
//         uniforms: {
//             time: { value: 0.0 },
//             lightDirection: { value: new THREE.Vector3(1, 1, 1).normalize() },
//             r: { value: rgbVue.r / 255.0 },
//             g: { value: rgbVue.g / 255.0 },
//             b: { value: rgbVue.b / 255.0 },
//         },
//         vertexShader: `
//             varying vec3 vNormal;
//             varying vec3 vViewPosition;
//             void main() {
//                 vNormal = normalize(normalMatrix * normal);
//                 vec4 viewPosition = modelViewMatrix * vec4(position, 1.0);
//                 vViewPosition = -viewPosition.xyz;
//                 gl_Position = projectionMatrix * viewPosition;
//             }
//         `,
//         fragmentShader: `
//             uniform vec3 lightDirection;
//             uniform float r, g, b;
//             varying vec3 vNormal;
//             varying vec3 vViewPosition;
//             void main() {
//                 vec3 color = vec3(r, g, b);
//                 vec3 normal = normalize(vNormal);
//                 vec3 lightDir = normalize(lightDirection);
//                 vec3 viewDir = normalize(vViewPosition);
//                 float diff = max(dot(normal, lightDir), 0.0);
//                 vec3 reflectDir = reflect(-lightDir, normal);
//                 float spec = pow(max(dot(viewDir, reflectDir), 0.0), 12.0) * 0.8;
//                 vec3 finalColor = (color * diff) + vec3(1.0) * spec * 0.5;
//                 gl_FragColor = vec4(finalColor, 1.0);
//             }
//         `,
//     });
// }

// // function reloadShoeColor() {
// //     if (!isShoeModelLoaded) {
// //         console.warn("Shoe model is not loaded yet.");
// //         return;
// //     }

// //     shoeModel.traverse((child) => {
// //         if (child.isMesh) {
// //             child.castShadow = true;
// //             child.receiveShadow = true;
// //             child.material =
// //                 child.name === "Plane" || child.name === "Plane_1"
// //                     ? customMaterial
// //                     : new THREE.MeshPhongMaterial({ color: new THREE.Color(0, 0, 0), shininess: 10 });
// //         }
// //     });
// // }




// export { setupThreeJS };