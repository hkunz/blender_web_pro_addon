import { setupScene } from './views/mainView.js'; // import the setupScene function from your main.js file
import WebGL from 'three/examples/jsm/capabilities/WebGL.js';

if (!WebGL.isWebGL2Available()) {
    const warning = WebGL.getWebGL2ErrorMessage();
    const warningContainer = document.createElement('div');
    warningContainer.textContent = "ERROR";
    warningContainer.className = 'warning-message';
    warningContainer.appendChild(warning);
    document.body.appendChild(warningContainer);
}

const canvas = document.createElement('canvas');
// set up your canvas here
document.body.appendChild(canvas);

// pass any necessary data to the setupScene function
setupScene(canvas);