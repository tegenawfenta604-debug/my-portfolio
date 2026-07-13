// hero.js
// Orchestrates the hero: starts the Three.js particle scene and
// handles the smooth page entrance. (Tilt + AOS are initialised
// in main.js; ripple lives in animations.js.)

import { initHeroParticles } from './particles.js';

const canvas = document.getElementById('hero-canvas');
if (canvas) {
    initHeroParticles(canvas);
}
