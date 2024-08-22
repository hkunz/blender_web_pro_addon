import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function loadModel(scene, modelPath) {
    const loader = new GLTFLoader();
    return new Promise((resolve, reject) => {
        loader.load(
            modelPath,
            (gltf) => {
                // Set metallic properties on the loaded model
                gltf.scene.traverse((child) => {
                    if (child.isMesh) {
                        //child.material.metalness = 1.0; // Fully metallic
                        //child.material.roughness = 0.0; // No roughness
                        child.material.envMap = scene.environment; // Set environment map for reflections
                        child.material.envMapIntensity = 1.0; // Adjust environment map intensity
                        child.material.needsUpdate = true; // Ensure material updates
                    }
                });
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
