(function () {
    'use strict';

    var root = document.documentElement;
    var toggle = document.getElementById('themeToggle');

    function applyTheme(theme) {
        root.setAttribute('data-bs-theme', theme);
        if (toggle) {
            toggle.innerHTML = theme === 'dark'
                ? '<i class="bi bi-sun"></i>'
                : '<i class="bi bi-moon-stars"></i>';
        }
        try { localStorage.setItem('theme', theme); } catch (e) {}
    }

    var stored = null;
    try { stored = localStorage.getItem('theme'); } catch (e) {}
    if (!stored) {
        stored = window.matchMedia &&
            window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    applyTheme(stored);

    if (toggle) {
        toggle.addEventListener('click', function () {
            var next = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
            applyTheme(next);
        });
    }

    // Typing effect (Typed.js with built-in fallback)
    var typedEl = document.getElementById('typed');
    if (typedEl) {
        var words = (typedEl.dataset.words || 'Developer,Designer,Freelancer').split(',');
        if (window.Typed) {
            new Typed('#typed', {
                strings: words,
                typeSpeed: 80,
                backSpeed: 40,
                backDelay: 1400,
                startDelay: 300,
                loop: true,
                smartBackspace: true,
            });
        } else {
            // Fallback typing effect if the CDN fails to load
            var wi = 0, ci = 0, deleting = false;
            function tick() {
                var word = words[wi];
                ci += deleting ? -1 : 1;
                typedEl.textContent = word.substring(0, ci);
                var delay = deleting ? 60 : 120;
                if (!deleting && ci === word.length) { deleting = true; delay = 1400; }
                else if (deleting && ci === 0) { deleting = false; wi = (wi + 1) % words.length; }
                setTimeout(tick, delay);
            }
            tick();
        }
    }

    // Initialize AOS (Animate On Scroll)
    if (window.AOS) {
        AOS.init({
            duration: 700,
            easing: 'ease-out-cubic',
            once: true,
            offset: 80,
        });
    }

    // Scroll reveal
    var reveals = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window && reveals.length) {
        var obs = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) {
                if (en.isIntersecting) { en.target.classList.add('visible'); obs.unobserve(en.target); }
            });
        }, { threshold: 0.15 });
        reveals.forEach(function (el) { obs.observe(el); });
    } else {
        reveals.forEach(function (el) { el.classList.add('visible'); });
    }

    // Animated counters
    function animateCount(el) {
        var target = parseInt(el.dataset.target, 10) || 0;
        var start = 0, dur = 1500, t0 = null;
        function step(ts) {
            if (!t0) t0 = ts;
            var p = Math.min((ts - t0) / dur, 1);
            el.textContent = Math.floor(p * (target - start) + start);
            if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }
    var counters = document.querySelectorAll('.count-up');
    if ('IntersectionObserver' in window && counters.length) {
        var cobs = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) {
                if (en.isIntersecting) { animateCount(en.target); cobs.unobserve(en.target); }
            });
        }, { threshold: 0.5 });
        counters.forEach(function (el) { cobs.observe(el); });
    }

    // Skill bar fill on view
    var bars = document.querySelectorAll('.skill-bar .fill');
    function fillBars() {
        bars.forEach(function (b) { b.style.width = (b.dataset.level || 0) + '%'; });
    }
    if ('IntersectionObserver' in window && bars.length) {
        var sobs = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) {
                if (en.isIntersecting) { fillBars(); sobs.disconnect(); }
            });
        }, { threshold: 0.2 });
        sobs.observe(bars[0].closest('section') || document.body);
    } else { fillBars(); }

    // Project filtering
    var filterWrap = document.getElementById('projectFilters');
    if (filterWrap) {
        var buttons = filterWrap.querySelectorAll('.filter-btn');
        var cards = document.querySelectorAll('[data-category]');
        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                buttons.forEach(function (b) { b.classList.remove('active'); });
                btn.classList.add('active');
                var cat = btn.dataset.filter;
                cards.forEach(function (card) {
                    card.style.display = (!cat || cat === 'all' || card.dataset.category === cat) ? '' : 'none';
                });
            });
        });
    }

    // 3D hover tilt on the hero profile image
    var tiltEl = document.getElementById('heroTilt');
    var tiltWrap = document.querySelector('.hero-image-wrap');
    if (tiltEl && tiltWrap) {
        tiltWrap.addEventListener('mousemove', function (e) {
            var r = tiltWrap.getBoundingClientRect();
            var px = (e.clientX - r.left) / r.width - 0.5;
            var py = (e.clientY - r.top) / r.height - 0.5;
            tiltEl.style.transform = 'rotateY(' + (px * 14) + 'deg) rotateX(' + (-py * 14) + 'deg)';
        });
        tiltWrap.addEventListener('mouseleave', function () {
            tiltEl.style.transform = 'rotateY(0deg) rotateX(0deg)';
        });
    }
})();
