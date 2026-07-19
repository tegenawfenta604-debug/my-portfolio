// animations.js
// Premium micro-interactions for the hero buttons:
// a material-style ripple effect on every .btn-hero click.
// (Scroll reveals use AOS; the 3D tilt is in main.js.)

(function () {
    'use strict';

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('.btn-hero');
        if (!btn) return;

        var rect = btn.getBoundingClientRect();
        var size = Math.max(rect.width, rect.height);
        var ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
        ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
        btn.appendChild(ripple);
        setTimeout(function () { ripple.remove(); }, 600);
    });
})();
