import * as THREE from 'three';
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';

export function setSkySphere(scene, imagePath) {
    new RGBELoader().load(imagePath, (hdrTexture) => {
        hdrTexture.mapping = THREE.EquirectangularReflectionMapping;

        // Set HDR as environment map
        scene.environment = hdrTexture;
        scene.background = hdrTexture;

        // Create sky sphere
        const skySphereGeometry = new THREE.SphereGeometry(300, 60, 60);
        const skySphereMaterial = new THREE.MeshBasicMaterial({
            map: hdrTexture,
            side: THREE.BackSide
        });
        const skySphereMesh = new THREE.Mesh(skySphereGeometry, skySphereMaterial);
        scene.add(skySphereMesh);
    });
}
