import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
// import * as THREE from "three";
// Step 1: Set up the scene, camera, and renderer.
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(window.innerWidth / - 2, window.innerWidth / 2, window.innerHeight / 2, window.innerHeight / - 2, 1, 1000);
const renderer = new THREE.WebGLRenderer();
const controls = new OrbitControls(camera, renderer.domElement);
controls.mouseButtons = {
	LEFT: THREE.MOUSE.PAN
};
controls.enableRotate = false; // Disabling rotation
controls.screenSpacePanning = true; // Enable different panning mode that might be more suitable for your case
const aspect = window.innerWidth / window.innerHeight;
camera.position.z = 500;

renderer.setSize(window.innerWidth, window.innerHeight);

// Append the renderer to the canvas div in HTML
document.getElementById('canvas').appendChild(renderer.domElement);

// Step 2: Load the floor plan image using TextureLoader
const loader = new THREE.TextureLoader();
const material = new THREE.MeshBasicMaterial({
    map: loader.load('floor1.png')
});

// Step 3: Create a plane geometry for the floor plan image
const geometry = new THREE.PlaneGeometry(4162, 2739);
const floorPlan = new THREE.Mesh(geometry, material);
scene.add(floorPlan);

// Step 4: Light blue circle with a grey boundary
const sphereGeometry = new THREE.SphereGeometry(20, 32, 32);
const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0x87CEEB });
// Step 5: Generate some mock data
const generateMockData = () => {
    const mockData = [];
    for (let i = 0; i < 10; i++) {
        const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
        sphere.position.x = (Math.random() - 0.5) * 50; // Random x-coordinate
        sphere.position.z = (Math.random() - 0.5) * 50; // Random z-coordinate
        sphere.material.transparent = true;

        // Create a new path with one point, the initial position
        const pathGeometry = new THREE.BufferGeometry().setFromPoints([ sphere.position.clone() ]);
        pathGeometry.vertices.push(sphere.position.clone());

        // Create a new path Line from the pathGeometry
        const pathMaterial = new THREE.LineBasicMaterial({color: 0xff0000});
        const path = new THREE.Line(pathGeometry, pathMaterial);

        scene.add(path);
        scene.add(sphere);

        // Store the sphere and path together
        mockData.push({sphere: sphere, path: path});
    }
    return mockData;
};

const people = generateMockData();

// Step 6: Set camera position
camera.position.z = 1000;
const vector = new THREE.Vector3(1, 0, 0); 

// Step 7: Animation and rendering
const animate = function () {
	requestAnimationFrame(animate);
	controls.update();
  
	for(let i = 0; i < people.length; i++) {
	  // Move the sphere
	  people[i].sphere.position.add(vector);
  
	  // Get the existing points
	  const points = people[i].path.geometry.attributes.position.array;
  
	  // Add a new point to the sphere's path at the new position
	  const newPoint = [
		...points,
		people[i].sphere.position.x,
		people[i].sphere.position.y,
		people[i].sphere.position.z
	  ];
  
	  // Update the geometry
	  people[i].path.geometry.setAttribute('position', new THREE.Float32BufferAttribute(newPoint, 3));
	}
  
	renderer.render(scene, camera);
  };
  
  animate();
  

animate();
