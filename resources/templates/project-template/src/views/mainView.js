import * as THREE from 'three';
import { setSkySphere } from '../helpers/SkysphereHelper.js';
import { setupRenderer } from '../helpers/RendererHelper.js';
import { updateCameraAspect } from '../helpers/CameraHelper.js';
import { SetAmbientLighting } from '../helpers/LightingHelper.js';
import { loadModel } from '../helpers/ModelLoader.js'; // Import the new model loader

const imagePath = '/dist/src/textures/kloofendal_48d_partly_cloudy_puresky_1k.hdr';
const modelPath = '/dist/src/models/cube.glb'; // Update with the correct path to your model

console.log("Current script location:", window.location.href);
console.log("Resolved image path:", new URL(imagePath, window.location.href).href);

export async function setupScene(canvas) {
    const scene = new THREE.Scene();
    const renderer = setupRenderer();
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    updateCameraAspect(camera);
    scene.add(camera);

    // Set initial camera position and target
    const radius = 10;
    const cameraTarget = new THREE.Vector3(0, 0, 0); // Center of the scene, where the model is placed

    camera.position.set(radius, radius, radius);
    camera.lookAt(cameraTarget);

    SetAmbientLighting(scene);
    setSkySphere(scene, imagePath);

    // Load the model and store it for rotation
    const model = await loadModel(scene, modelPath);

    let angle = 0; // Angle for rotating the camera

    function animate() {
        requestAnimationFrame(animate);

        // Rotate the model
        if (model) {
            model.rotation.y += 0.01; // Adjust the rotation speed as needed
        }

        // Rotate the camera around the target
        angle -= 0.001; // Adjust the rotation speed as needed
        camera.position.x = radius * Math.cos(angle);
        camera.position.y = radius * Math.sin(angle);
        camera.lookAt(cameraTarget);

        renderer.render(scene, camera);
    }
    animate();
}
