// =========================================================
// hero-premium.js  (ES module)
// - Three.js neon particle + network background
// - Cursor glow, mouse parallax (shapes + avatar stage)
// - Hero fade-upward on scroll
// Typing effect + counters live in main.js.
// =========================================================

import * as THREE from 'three';

const reduce = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------------------------------------------------------
   1. Cursor glow
--------------------------------------------------------- */
(function cursorGlow() {
    const glow = document.getElementById('phCursorGlow');
    if (!glow) return;
    let raf = null;
    const s = { x: innerWidth / 2, y: innerHeight / 2, tx: innerWidth / 2, ty: innerHeight / 2 };
    addEventListener('mousemove', (e) => {
        s.tx = e.clientX; s.ty = e.clientY; glow.style.opacity = '1';
        if (!raf) raf = requestAnimationFrame(follow);
    }, { passive: true });
    document.addEventListener('mouseleave', () => { glow.style.opacity = '0'; });
    function follow() {
        s.x += (s.tx - s.x) * 0.15; s.y += (s.ty - s.y) * 0.15;
        glow.style.transform = `translate(${s.x}px, ${s.y}px) translate(-50%, -50%)`;
        if (Math.abs(s.tx - s.x) > 0.5 || Math.abs(s.ty - s.y) > 0.5) raf = requestAnimationFrame(follow);
        else raf = null;
    }
})();

/* ---------------------------------------------------------
   2. Mouse parallax (geometric shapes + avatar stage)
--------------------------------------------------------- */
(function parallax() {
    const shapes = Array.from(document.querySelectorAll('#phShapes .ph-shape'));
    const stage = document.getElementById('phStage');
    if (!shapes.length && !stage) return;
    let mx = 0, my = 0, cx = 0, cy = 0, ticking = false;
    addEventListener('mousemove', (e) => {
        mx = (e.clientX / innerWidth) - 0.5;
        my = (e.clientY / innerHeight) - 0.5;
        if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    function update() {
        cx += (mx - cx) * 0.08; cy += (my - cy) * 0.08;
        shapes.forEach((el) => {
            const d = parseFloat(el.dataset.depth || '2');
            el.style.transform = `translate(${cx * d * 16}px, ${cy * d * 16}px)`;
        });
        if (stage) stage.style.transform = `translate(${cx * 22}px, ${cy * 22}px)`;
        if (Math.abs(mx - cx) > 0.001 || Math.abs(my - cy) > 0.001) requestAnimationFrame(update);
        else ticking = false;
    }
})();

/* ---------------------------------------------------------
   3. Hero fades upward on scroll
--------------------------------------------------------- */
(function heroScrollFade() {
    const inner = document.getElementById('phHeroInner');
    const hero = document.querySelector('.ph-hero');
    if (!inner || !hero || reduce) return;
    let ticking = false;
    function onScroll() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
            const y = window.scrollY;
            const h = hero.offsetHeight;
            if (y < h) {
                const p = Math.min(y / h, 1);
                inner.style.transform = `translateY(${-y * 0.25}px)`;
                inner.style.opacity = String(1 - p * 1.1);
            }
            ticking = false;
        });
    }
    addEventListener('scroll', onScroll, { passive: true });
})();

/* ---------------------------------------------------------
   4. Three.js neon particle + network background
--------------------------------------------------------- */
(function background() {
    const canvas = document.getElementById('ph-bg-canvas');
    if (!canvas || reduce) return;

    let renderer;
    try {
        renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    } catch (err) { return; }
    renderer.setClearColor(0x000000, 0);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
    camera.position.set(0, 0, 60);
    const group = new THREE.Group();
    scene.add(group);

    function makeGlow() {
        const c = document.createElement('canvas');
        c.width = c.height = 64;
        const ctx = c.getContext('2d');
        const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
        g.addColorStop(0, 'rgba(255,255,255,1)');
        g.addColorStop(0.35, 'rgba(255,255,255,0.75)');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = g; ctx.fillRect(0, 0, 64, 64);
        return new THREE.CanvasTexture(c);
    }
    const glowTex = makeGlow();
    const palette = [0x4F46E5, 0x06B6D4, 0xFFD43B, 0x3776AB];

    const COUNT = 1700;
    const positions = new Float32Array(COUNT * 3);
    const colors = new Float32Array(COUNT * 3);
    const base = new Float32Array(COUNT * 3);
    const col = new THREE.Color();
    for (let i = 0; i < COUNT; i++) {
        const r = 18 + Math.random() * 42;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const ix = i * 3;
        positions[ix] = base[ix] = r * Math.sin(phi) * Math.cos(theta);
        positions[ix + 1] = base[ix + 1] = r * Math.sin(phi) * Math.sin(theta);
        positions[ix + 2] = base[ix + 2] = (r * Math.cos(phi)) * 0.6;
        col.setHex(palette[(Math.random() * palette.length) | 0]);
        colors[ix] = col.r; colors[ix + 1] = col.g; colors[ix + 2] = col.b;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const mat = new THREE.PointsMaterial({
        size: 1.6, map: glowTex, vertexColors: true, transparent: true,
        opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true,
    });
    group.add(new THREE.Points(geo, mat));

    // network lines
    const NODES = 90, idx = [];
    for (let i = 0; i < NODES; i++) idx.push((Math.random() * COUNT) | 0);
    const lp = [], lc = [], maxDist = 16;
    for (let i = 0; i < NODES; i++) {
        for (let j = i + 1; j < NODES; j++) {
            const a = idx[i], b = idx[j];
            const dx = base[a * 3] - base[b * 3], dy = base[a * 3 + 1] - base[b * 3 + 1], dz = base[a * 3 + 2] - base[b * 3 + 2];
            if (Math.sqrt(dx * dx + dy * dy + dz * dz) < maxDist) {
                lp.push(base[a * 3], base[a * 3 + 1], base[a * 3 + 2], base[b * 3], base[b * 3 + 1], base[b * 3 + 2]);
                lc.push(colors[a * 3], colors[a * 3 + 1], colors[a * 3 + 2], colors[b * 3], colors[b * 3 + 1], colors[b * 3 + 2]);
            }
        }
    }
    const lGeo = new THREE.BufferGeometry();
    lGeo.setAttribute('position', new THREE.Float32BufferAttribute(lp, 3));
    lGeo.setAttribute('color', new THREE.Float32BufferAttribute(lc, 3));
    const lMat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.16, depthWrite: false, blending: THREE.AdditiveBlending });
    group.add(new THREE.LineSegments(lGeo, lMat));

    const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
    addEventListener('mousemove', (e) => {
        mouse.tx = (e.clientX / innerWidth) * 2 - 1;
        mouse.ty = (e.clientY / innerHeight) * 2 - 1;
    }, { passive: true });

    function resize() {
        const w = canvas.clientWidth || innerWidth, h = canvas.clientHeight || innerHeight;
        renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
        renderer.setSize(w, h, false);
        camera.aspect = w / h; camera.updateProjectionMatrix();
    }
    addEventListener('resize', resize);

    if (window.gsap) {
        group.scale.set(0.2, 0.2, 0.2); mat.opacity = 0; lMat.opacity = 0;
        const tl = window.gsap.timeline();
        tl.to(group.scale, { x: 1, y: 1, z: 1, duration: 2.6, ease: 'power2.out' }, 0);
        tl.to(mat, { opacity: 0.9, duration: 2.2 }, 0.4);
        tl.to(lMat, { opacity: 0.16, duration: 2.2 }, 0.8);
        tl.fromTo(camera.position, { z: 130 }, { z: 60, duration: 3, ease: 'power2.inOut' }, 0);
    }

    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        const pos = geo.attributes.position.array;
        for (let i = 0; i < COUNT; i++) {
            const ix = i * 3;
            pos[ix + 1] = base[ix + 1] + Math.sin(t * 0.4 + i) * 0.5;
            pos[ix] = base[ix] + Math.cos(t * 0.3 + i * 1.2) * 0.4;
        }
        geo.attributes.position.needsUpdate = true;
        mouse.x += (mouse.tx - mouse.x) * 0.04; mouse.y += (mouse.ty - mouse.y) * 0.04;
        group.rotation.y = t * 0.03 + mouse.x * 0.35;
        group.rotation.x = mouse.y * 0.25;
        camera.position.x += (mouse.x * 8 - camera.position.x) * 0.04;
        camera.position.y += (-mouse.y * 5 - camera.position.y) * 0.04;
        camera.lookAt(scene.position);
        renderer.render(scene, camera);
    }
    resize(); animate();
})();
