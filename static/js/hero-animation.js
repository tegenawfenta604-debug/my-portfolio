// hero-animation.js
// Premium 3D glowing particle hero for Tegenaw Fenta's portfolio.
// Uses Three.js (ES module) + GSAP. No jQuery.
// Particles: BufferGeometry + Points + AdditiveBlending (GPU friendly).
// Neural-network connecting lines for a "digital universe" feel.

import * as THREE from 'three';

(function () {
    'use strict';

    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    let renderer;
    try {
        renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    } catch (err) {
        // WebGL unavailable -> dark CSS background remains.
        return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
    camera.position.set(0, 0, 60);

    const group = new THREE.Group();
    scene.add(group);

    // --- Soft circular glow sprite (simulates bloom) ---
    function makeGlowTexture() {
        const c = document.createElement('canvas');
        c.width = c.height = 64;
        const ctx = c.getContext('2d');
        const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
        g.addColorStop(0.0, 'rgba(255,255,255,1)');
        g.addColorStop(0.25, 'rgba(255,255,255,0.85)');
        g.addColorStop(1.0, 'rgba(255,255,255,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, 64, 64);
        return new THREE.CanvasTexture(c);
    }
    const glowTex = makeGlowTexture();

    // Neon palette: deep purple, electric blue, neon pink, soft violet
    const palette = [0x7c4dff, 0x00e5ff, 0xff4fd8, 0xb388ff];

    // --- Particle field ---
    const COUNT = 3500;
    const positions = new Float32Array(COUNT * 3);
    const colors = new Float32Array(COUNT * 3);
    const base = new Float32Array(COUNT * 3);
    const col = new THREE.Color();

    for (let i = 0; i < COUNT; i++) {
        // Distribute inside a sphere for an "energy object" shape
        const r = 16 + Math.random() * 24;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);
        const ix = i * 3;
        positions[ix] = base[ix] = x;
        positions[ix + 1] = base[ix + 1] = y;
        positions[ix + 2] = base[ix + 2] = z;
        col.setHex(palette[(Math.random() * palette.length) | 0]);
        colors[ix] = col.r;
        colors[ix + 1] = col.g;
        colors[ix + 2] = col.b;
    }

    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    pGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const pMat = new THREE.PointsMaterial({
        size: 1.5,
        map: glowTex,
        vertexColors: true,
        transparent: true,
        opacity: 0.9,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true,
    });
    const points = new THREE.Points(pGeo, pMat);
    group.add(points);

    // --- Neural-network connecting lines (subset of nodes) ---
    const NODES = 140;
    const nodeIdx = [];
    for (let i = 0; i < NODES; i++) nodeIdx.push((Math.random() * COUNT) | 0);
    const linePos = [];
    const lineCol = [];
    const maxDist = 13;
    for (let i = 0; i < NODES; i++) {
        for (let j = i + 1; j < NODES; j++) {
            const a = nodeIdx[i], b = nodeIdx[j];
            const dx = base[a * 3] - base[b * 3];
            const dy = base[a * 3 + 1] - base[b * 3 + 1];
            const dz = base[a * 3 + 2] - base[b * 3 + 2];
            if (Math.sqrt(dx * dx + dy * dy + dz * dz) < maxDist) {
                linePos.push(base[a * 3], base[a * 3 + 1], base[a * 3 + 2],
                             base[b * 3], base[b * 3 + 1], base[b * 3 + 2]);
                lineCol.push(colors[a * 3], colors[a * 3 + 1], colors[a * 3 + 2],
                             colors[b * 3], colors[b * 3 + 1], colors[b * 3 + 2]);
            }
        }
    }
    const lGeo = new THREE.BufferGeometry();
    lGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePos, 3));
    lGeo.setAttribute('color', new THREE.Float32BufferAttribute(lineCol, 3));
    const lMat = new THREE.LineBasicMaterial({
        vertexColors: true, transparent: true, opacity: 0.18,
        depthWrite: false, blending: THREE.AdditiveBlending,
    });
    const lines = new THREE.LineSegments(lGeo, lMat);
    group.add(lines);

    // --- Mouse interaction (parallax + rotation) ---
    const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
    window.addEventListener('mousemove', function (e) {
        mouse.tx = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.ty = (e.clientY / window.innerHeight) * 2 - 1;
    }, { passive: true });

    // --- Resize ---
    function resize() {
        const w = canvas.clientWidth || window.innerWidth;
        const h = canvas.clientHeight || window.innerHeight;
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
    }
    window.addEventListener('resize', resize);
    window.addEventListener('load', resize);

    // --- Intro animation (GSAP) ---
    const container = document.querySelector('.hero-3d .container');
    if (window.gsap) {
        group.scale.set(0.01, 0.01, 0.01);
        pMat.opacity = 0;
        lMat.opacity = 0;
        const tl = window.gsap.timeline();
        tl.to(group.scale, { x: 1, y: 1, z: 1, duration: 3.2, ease: 'power2.out' }, 0);
        tl.to(pMat, { opacity: 0.9, duration: 2.6 }, 0.6);
        tl.to(lMat, { opacity: 0.18, duration: 2.6 }, 1.0);
        tl.fromTo(camera.position, { z: 150 }, { z: 60, duration: 3.6, ease: 'power2.inOut' }, 0);
        if (container) {
            tl.fromTo(container, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.2 }, 2.6);
        }
    } else if (container) {
        container.style.opacity = 1;
    }

    // --- Render loop ---
    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();

        // Gentle floating motion
        const pos = pGeo.attributes.position.array;
        for (let i = 0; i < COUNT; i++) {
            const ix = i * 3;
            pos[ix] = base[ix] + Math.sin(t * 0.6 + i) * 0.6;
            pos[ix + 1] = base[ix + 1] + Math.cos(t * 0.5 + i * 1.3) * 0.6;
            pos[ix + 2] = base[ix + 2] + Math.sin(t * 0.4 + i * 0.7) * 0.6;
        }
        pGeo.attributes.position.needsUpdate = true;

        // Smooth mouse follow -> rotation + camera parallax
        mouse.x += (mouse.tx - mouse.x) * 0.05;
        mouse.y += (mouse.ty - mouse.y) * 0.05;
        group.rotation.y = t * 0.05 + mouse.x * 0.6;
        group.rotation.x = mouse.y * 0.4;
        camera.position.x += (mouse.x * 6 - camera.position.x) * 0.05;
        camera.position.y += (-mouse.y * 4 - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    resize();
    animate();
})();
