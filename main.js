import * as THREE from 'three';

// Crear la escena
const scene = new THREE.Scene();

// Crear la cámara
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Crear el renderizador
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Variables de control
let rotationSpeed = 0.01;
let vibrationIntensity = 0;
let originalPositions = null;

// Variables MIDI
let midiAccess = null;
let arduinoInput = null;

// Mapeo de canales CC a controles
const MIDI_CC_MAP = {
    70: 'size',        // CC 70 -> Size
    71: 'color',       // CC 71 -> Color
    72: 'segments',    // CC 72 -> Segments
    73: 'vibration',   // CC 73 -> Vibration
    74: 'opacity',     // CC 74 -> Opacity
    75: 'rotationSpeed' // CC 75 -> Rotation Speed
};

// Rangos de valores para cada control
const CONTROL_RANGES = {
    size: { min: 0.1, max: 3 },
    color: { min: 0, max: 360 },
    segments: { min: 4, max: 64 },
    vibration: { min: 0, max: 0.1 },
    opacity: { min: 0, max: 1 },
    rotationSpeed: { min: 0, max: 0.05 }
};

// Crear la geometría de la esfera
let geometry = new THREE.SphereGeometry(1, 32, 32);

// Crear el material
const material = new THREE.MeshBasicMaterial({
    color: 0x00ff00,
    wireframe: true,
    transparent: true,
    opacity: 1
});

// Crear la esfera
let sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Posicionar la cámara
camera.position.z = 5;

// Obtener referencias a los controles
const sizeSlider = document.getElementById('size');
const colorPicker = document.getElementById('color');
const segmentsSlider = document.getElementById('segments');
const vibrationSlider = document.getElementById('vibration');
const opacitySlider = document.getElementById('opacity');
const rotationSpeedSlider = document.getElementById('rotationSpeed');

// Guardar posiciones originales
function saveOriginalPositions() {
    const positions = sphere.geometry.attributes.position.array;
    originalPositions = new Float32Array(positions.length);
    for (let i = 0; i < positions.length; i++) {
        originalPositions[i] = positions[i];
    }
}

// Inicializar posiciones originales
saveOriginalPositions();

// Event listeners para los controles
sizeSlider.addEventListener('input', (e) => {
    const size = parseFloat(e.target.value);
    sphere.scale.setScalar(size);
    document.getElementById('sizeValue').textContent = size;
});

colorPicker.addEventListener('input', (e) => {
    const hue = parseInt(e.target.value);
    material.color.setHSL(hue / 360, 1, 0.5);
    document.getElementById('colorValue').textContent = hue;
});

segmentsSlider.addEventListener('input', (e) => {
    const segments = parseInt(e.target.value);
    sphere.geometry.dispose();
    sphere.geometry = new THREE.SphereGeometry(1, segments, segments);
    saveOriginalPositions(); // Actualizar posiciones originales
    document.getElementById('segmentsValue').textContent = segments;
});

vibrationSlider.addEventListener('input', (e) => {
    vibrationIntensity = parseFloat(e.target.value);
    document.getElementById('vibrationValue').textContent = vibrationIntensity;
});

opacitySlider.addEventListener('input', (e) => {
    material.opacity = parseFloat(e.target.value);
    document.getElementById('opacityValue').textContent = e.target.value;
});

rotationSpeedSlider.addEventListener('input', (e) => {
    rotationSpeed = parseFloat(e.target.value);
    document.getElementById('rotationSpeedValue').textContent = e.target.value;
});

// Inicializar MIDI
async function initMIDI() {
    try {
        midiAccess = await navigator.requestMIDIAccess();
        console.log('MIDI Access obtenido');

        // Buscar el Arduino Leonardo
        for (let input of midiAccess.inputs.values()) {
            if (input.name.includes('Arduino Leonardo') || input.name.includes('Arduino')) {
                arduinoInput = input;
                arduinoInput.onmidimessage = handleMIDIMessage;
                console.log('Arduino Leonardo conectado:', input.name);
                break;
            }
        }

        if (!arduinoInput) {
            console.warn('Arduino Leonardo no encontrado');
        }
    } catch (error) {
        console.error('Error al acceder a MIDI:', error);
    }
}

// Manejar mensajes MIDI
function handleMIDIMessage(message) {
    const [status, cc, value] = message.data;

    // Verificar que es un mensaje CC (Control Change)
    if ((status & 0xF0) === 0xB0) {
        const controlName = MIDI_CC_MAP[cc];
        if (controlName) {
            updateControlFromMIDI(controlName, value);
        }
    }
}

// Actualizar control desde MIDI
function updateControlFromMIDI(controlName, midiValue) {
    const range = CONTROL_RANGES[controlName];
    const normalizedValue = midiValue / 127;
    const scaledValue = range.min + (normalizedValue * (range.max - range.min));

    const slider = document.getElementById(controlName);
    const valueDisplay = document.getElementById(controlName + 'Value');

    if (slider) {
        slider.value = scaledValue;

        // Actualizar el valor mostrado
        if (valueDisplay) {
            if (controlName === 'segments' || controlName === 'color') {
                valueDisplay.textContent = Math.round(scaledValue);
            } else {
                valueDisplay.textContent = scaledValue.toFixed(controlName === 'size' ? 1 : 2);
            }
        }

        // Aplicar el cambio según el tipo de control
        switch (controlName) {
            case 'size':
                sphere.scale.setScalar(scaledValue);
                break;
            case 'color':
                material.color.setHSL(Math.round(scaledValue) / 360, 1, 0.5);
                break;
            case 'segments':
                const segments = Math.round(scaledValue);
                sphere.geometry.dispose();
                sphere.geometry = new THREE.SphereGeometry(1, segments, segments);
                saveOriginalPositions();
                break;
            case 'vibration':
                vibrationIntensity = scaledValue;
                break;
            case 'opacity':
                material.opacity = scaledValue;
                break;
            case 'rotationSpeed':
                rotationSpeed = scaledValue;
                break;
        }
    }
}

// Función de animación
function animate() {
    requestAnimationFrame(animate);

    // Aplicar vibración si está activa
    if (vibrationIntensity > 0 && originalPositions) {
        const positions = sphere.geometry.attributes.position.array;
        const time = Date.now() * 0.01;

        for (let i = 0; i < positions.length; i += 3) {
            positions[i] = originalPositions[i] + (Math.sin(time + i) * vibrationIntensity);
            positions[i + 1] = originalPositions[i + 1] + (Math.cos(time + i + 1) * vibrationIntensity);
            positions[i + 2] = originalPositions[i + 2] + (Math.sin(time + i + 2) * vibrationIntensity);
        }

        sphere.geometry.attributes.position.needsUpdate = true;
    }

    // Rotar la esfera
    sphere.rotation.x += rotationSpeed;
    sphere.rotation.y += rotationSpeed;

    // Renderizar la escena
    renderer.render(scene, camera);
}

// Manejar redimensionamiento de ventana
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Iniciar la animación
animate();

// Inicializar MIDI después de que todo esté cargado
initMIDI();
