import * as THREE from 'three';
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import WebGL from 'three/examples/jsm/capabilities/WebGL.js';

if (!WebGL.isWebGL2Available()) {
    const warning = WebGL.getWebGL2ErrorMessage();
    const warningContainer = document.createElement('div');
    warningContainer.textContent = "ERROR";
    warningContainer.className = 'warning-message';
    warningContainer.appendChild(warning);
    document.body.appendChild(warningContainer);
}

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
camera.position.z = 5;

window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

const hdrLoader = new RGBELoader();
hdrLoader.load('sky2k.hdr', (hdrTexture) => {
    hdrTexture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = hdrTexture;
    scene.environment = hdrTexture;

    // Load GLTF model
    const gltfLoader = new GLTFLoader();
    gltfLoader.load('burger.glb', (gltf) => {
        scene.add(gltf.scene);
        render();
    }, undefined, (error) => {
        console.error('An error occurred loading the GLTF model:', error);
    });
}, undefined, (error) => {
    console.error('An error occurred loading the HDR texture:', error);
});

// Add lights
const ambientLight = new THREE.AmbientLight(0x404040); // Soft white light
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(1, 1, 1).normalize();
scene.add(directionalLight);

// Render function
function render() {
    requestAnimationFrame(render);
    renderer.render(scene, camera);
}

render();
