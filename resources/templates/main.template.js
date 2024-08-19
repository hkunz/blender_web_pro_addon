/*
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const controls = new OrbitControls( camera, renderer.domElement );
const loader = new GLTFLoader();
*/

// Creating Scene: https://threejs.org/docs/#manual/en/introduction/Creating-a-scene
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 ); //FOV, Aspect Ratio, Near, Far (clipping)

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
// setSize(window.innerWidth/2, window.innerHeight/2, false) // will render your app at half resolution, given that your <canvas> has 100% width and height.
document.body.appendChild( renderer.domElement );
// renderer.setAnimationLoop( animate );

// Add Cube:
const geometry = new THREE.BoxGeometry( 1, 1, 1 );
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

camera.position.z = 5;

// This will create a loop that causes the renderer to draw the scene every time the screen is refreshed (on a typical screen this means 60 times per second).
function animate() {
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
	renderer.render( scene, camera );
}

window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
});

renderer.setAnimationLoop( animate );
animate();