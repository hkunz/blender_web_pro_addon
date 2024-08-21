import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function loadModel(scene, modelPath) {
    const loader = new GLTFLoader();
    return new Promise((resolve, reject) => {
        loader.load(
            modelPath,
            (gltf) => {
                scene.add(gltf.scene);
                resolve(gltf.scene); // Return the loaded model
            },
            undefined,
            (error) => {
                console.error('An error occurred loading the GLTF model:', error);
                reject(error);
            }
        );
    });
}
