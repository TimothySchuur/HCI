import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let scene, camera, renderer, controls, shoeModel, customMaterial;
let stateIndex = 0;

const cushioningState = [
    { r: 20, g: 224, b: 97 },
    { r: 128, g: 255, b: 0 },   // Light Green - Moderate UV
    { r: 255, g: 255, b: 0 },   // Yellow - Elevated UV
    { r: 255, g: 200, b: 0 },   // Orange-Yellow - High UV
    { r: 255, g: 165, b: 0 },   // Orange - Very High UV
    { r: 255, g: 100, b: 0 },   // Red-Orange - Extreme UV
    { r: 255, g: 0, b: 0 },     // Red - Severe UV
    { r: 200, g: 0, b: 0 },     // Dark Red - Very Severe UV
    { r: 255, g: 0, b: 125 },   // Magenta - Critical UV
    // { r: 255, g: 0, b: 255 }    // Purple - Ultra Critical UV
]

// bright purple:  // { r: 100, g: 90, b: 255 },

const cushioningStateShoeColor = [
    { r: 20, g: 224, b: 97 },
    { r: 245, g: 245, b: 255 },// Light Green - Moderate UV
    { r: 255, g: 255, b: 0 },   // Yellow - Elevated UV
    { r: 255, g: 200, b: 0 },   // Orange-Yellow - High UV
    { r: 255, g: 165, b: 0 },   // Orange - Very High UV
    { r: 255, g: 100, b: 0 },   // Red-Orange - Extreme UV
    { r: 255, g: 0, b: 0 },     // Red - Severe UV
    { r: 200, g: 0, b: 0 },     // Dark Red - Very Severe UV
    { r: 255, g: 0, b: 125 },   // Magenta - Critical UV
    { r: 255, g: 0, b: 255 }    // Purple - Ultra Critical UV
]


function setupThreeJS(canvas) {
    const shoeViewer = document.getElementById('shoe-viewer'); // Get #shoe-viewer element

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(shoeViewer.clientWidth, shoeViewer.clientHeight);
    renderer.setClearColor(0x000000, 0); // Set background transparent
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Scene
    scene = new THREE.Scene();

    // Camera
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(4, 5, 12);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.enablePan = false;
    controls.minDistance = 8;
    controls.maxDistance = 13;
    controls.minPolarAngle = 0.6;
    controls.maxPolarAngle = Math.PI * 0.6;
    controls.target.set(0, 0, 0);
    controls.update();

    const lights = [
        new THREE.DirectionalLight(0xffffff, 20),
        new THREE.DirectionalLight(0xffffff, 20),
        new THREE.DirectionalLight(0xffffff, 10),
        new THREE.DirectionalLight(0xffffff, 10),
        new THREE.AmbientLight(0xffffff, 10),
    ];

// Set the position of directional lights
    lights[0].position.set(0, 10, 0);
    lights[1].position.set(0, -10, 0);
    lights[2].position.set(-10, 0, 0);
    lights[3].position.set(10, 0, 0);
    lights[4].position.set(0, 0, 0); // This won't affect ambient light position


// Add lights to the scene
    lights.forEach(light => scene.add(light));

    // Shoe Group
    const shoeGroup = new THREE.Group();
    scene.add(shoeGroup);

    // Load Shoe Model
    const loader = new GLTFLoader()
    loader.load('Shoes-Make.gltf', (gltf) => {
        shoeModel = gltf.scene;
        const boundingBox = new THREE.Box3().setFromObject(shoeModel);
        const center = boundingBox.getCenter(new THREE.Vector3());
        shoeModel.position.sub(center);
        reloadShoeColor();
        shoeGroup.add(shoeModel);
    });

    // Custom Material
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
    return new THREE.ShaderMaterial({
        uniforms: {
            time: { value: 0.0 },
            lightDirection: { value: new THREE.Vector3(1, 1, 1).normalize() },
            rw: { value: cushioningStateShoeColor[stateIndex + 1].r / 255.0 },
            gw: { value: cushioningStateShoeColor[stateIndex + 1].g / 255.0 },
            bw: { value: cushioningStateShoeColor[stateIndex + 1].b / 255.0 },
            r: { value: cushioningState[stateIndex].r / 255.0 },
            g: { value: cushioningState[stateIndex].g / 255.0 },
            b: { value: cushioningState[stateIndex].b / 255.0 },
        },
        vertexShader: `
            varying vec3 vNormal;
            varying vec3 vViewPosition;
            
            void main() {
                // Compute normal and view position in the vertex shader for later use
                vNormal = normalize(normalMatrix * normal);
                vec4 viewPosition = modelViewMatrix * vec4(position, 1.0);
                vViewPosition = -viewPosition.xyz;

                // Final position of vertex
                gl_Position = projectionMatrix * viewPosition;
            }
        `,
        fragmentShader: `
            uniform float time;
            uniform vec3 lightDirection;
            uniform float rw, gw, bw, r, g, b;
            
            varying vec3 vNormal;
            varying vec3 vViewPosition;

            // Function for color cycling between two colors over time
            vec3 getColorCycle(float t) {
                vec3 bright = vec3(r, g, b);
                vec3 white = vec3(rw, gw, bw);
                
                // Normalize time for a consistent cycle duration
                t = mod(t, 1.25); 
                
                // Smooth transitions using easing functions
                float easedT = smoothstep(0.0, 0.25, t); 
                float easedReverseT = pow(smoothstep(0.5, 1.0, t), 3.0);

                // Transition to white and back to bright
                if (t < 0.5) {
                    return mix(bright, white, easedT); 
                } else {
                    return mix(white, bright, easedReverseT); 
                }
            }

            void main() {
                // Set cycle time for slower color cycling
                float cycleTime = mod(time * 0.6, 1.25);
                vec3 colorCycle = getColorCycle(cycleTime);
                
                // Lighting calculations
                vec3 normal = normalize(vNormal);
                vec3 lightDir = normalize(lightDirection);
                vec3 viewDir = normalize(vViewPosition);

                // Diffuse component based on the angle to the light source
                float diff = max(dot(normal, lightDir), 0.0);

                // Specular reflection for added shininess
                vec3 reflectDir = reflect(-lightDir, normal);
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), 12.0) * 0.8;

                // Combine diffuse and specular lighting with color cycle
                vec3 finalColor = (colorCycle * (diff * 0.8)) + vec3(1.0) * spec * 0.5;

                // Output the final fragment color
                gl_FragColor = vec4(finalColor, 1.0);
            }
        `,
        // Uncomment this line for wireframe mode (for testing)
        // wireframe: true,
    });
}



function reloadShoeColor() {
    shoeModel.traverse((child) => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            child.material = (child.name === "Plane" || child.name === "Plane_1")
                ? customMaterial
                : new THREE.MeshPhongMaterial({
                    color: new THREE.Color(0,0,0),
                    shininess: 10,
                })

        }
    });
}

function updateShoeColor(value) {
    // Log the incoming value and its type for debugging
    console.log("Incoming value:", value, "Type:", typeof value);

    // Convert value to a number
    const numericValue = Number(value);

    // Ensure value is a number
    if (isNaN(numericValue)) {
        console.warn("Provided value is not a number:", value);
        return; // Exit if value is not a number
    }

    // Set stateIndex and ensure it's within bounds
    stateIndex = Math.max(0, Math.min(cushioningState.length - 1, numericValue));

    if (customMaterial) {
        // Check if the next state index is within bounds
        if (stateIndex + 1 < cushioningStateShoeColor.length) {
            customMaterial.uniforms.rw.value = cushioningStateShoeColor[stateIndex + 1].r / 255.0;
            customMaterial.uniforms.gw.value = cushioningStateShoeColor[stateIndex + 1].g / 255.0;
            customMaterial.uniforms.bw.value = cushioningStateShoeColor[stateIndex + 1].b / 255.0;
        } else {
            console.warn("cushioningStateShoeColor index out of bounds for stateIndex + 1:", stateIndex + 1);
        }

        // Ensure stateIndex is valid for current color
        customMaterial.uniforms.r.value = cushioningStateShoeColor[stateIndex].r / 255.0;
        customMaterial.uniforms.g.value = cushioningStateShoeColor[stateIndex].g / 255.0;
        customMaterial.uniforms.b.value = cushioningStateShoeColor[stateIndex].b / 255.0;
    }

    reloadShoeColor();
}

export { setupThreeJS, updateShoeColor };