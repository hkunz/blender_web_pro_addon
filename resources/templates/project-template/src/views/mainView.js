import * as THREE from 'three';
import { setSkySphere } from '../helpers/SkysphereHelper.js';
import { setupRenderer } from '../helpers/RendererHelper.js';
import { updateCameraAspect } from '../helpers/CameraHelper.js';
import { SetAmbientLighting } from '../helpers/LightingHelper.js';
import { loadModel } from '../helpers/ModelLoader.js';

const imagePath = '/dist/src/textures/kloofendal_48d_partly_cloudy_puresky_1k.hdr';
const modelPath = '/dist/src/models/metal-cube.glb';

export async function setupScene(canvas) {
    const scene = new THREE.Scene();
    const renderer = setupRenderer();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    updateCameraAspect(camera, renderer);
    scene.add(camera);

    const radius = 3;
    const cameraTarget = new THREE.Vector3(0, 0, 0); // Center of the scene

    camera.position.set(radius, radius, radius);
    camera.lookAt(cameraTarget);

    SetAmbientLighting(scene);
    setSkySphere(scene, imagePath);

    const axesHelper = new THREE.AxesHelper(5); // Change the size as needed
    scene.add(axesHelper);

    const model = await loadModel(scene, modelPath);

    if (model) {
        const boxHelper = new THREE.BoxHelper(model, 0xffff00); // Yellow color for the bounding box
        scene.add(boxHelper);
    }

    let angle = 0;

    function animate() {
        requestAnimationFrame(animate);

        if (model) {
            model.rotation.y += 0.005;
            model.rotation.z += 0.001;
        }

        angle -= 0.001;
        camera.position.x = radius * Math.cos(angle);
        camera.position.y = radius * Math.sin(angle);
        camera.lookAt(cameraTarget);

        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        updateCameraAspect(camera, renderer);
    });
}
