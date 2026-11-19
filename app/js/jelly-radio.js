/* OpenPark Smooth Pill & Segmented Control Interactions — Silky 120Hz Hardware Accelerated */
(function (global) {
  "use strict";

  function reducedMotion() {
    return Boolean(
      global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }

  function injectStyles() {
    if (document.getElementById("openpark-smooth-pill-styles")) return;
    const s = document.createElement("style");
    s.id = "openpark-smooth-pill-styles";
    s.textContent = `
      .chip-btn, .jelly-pill {
        will-change: transform;
        transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), 
                    background-color 0.2s ease, 
                    color 0.2s ease, 
                    border-color 0.2s ease, 
                    box-shadow 0.2s ease !important;
      }
      .chip-btn:hover, .jelly-pill:hover {
        transform: translateY(-1.5px) scale(1.02) !important;
      }
      .chip-btn:active, .jelly-pill:active {
        transform: scale(0.96) !important;
        transition-duration: 0.08s !important;
      }
    `;
    document.head.appendChild(s);
  }

  function enhanceBar(bar) {
    if (!bar || bar.dataset.smoothBound === "1") return;
    bar.dataset.smoothBound = "1";

    bar.addEventListener("click", (ev) => {
      const pill = ev.target && ev.target.closest ? ev.target.closest(".chip-btn, .jelly-pill, button") : null;
      if (!pill || pill.parentElement !== bar) return;
      if (reducedMotion() || !global.gsap) return;

      global.gsap.killTweensOf(pill);
      global.gsap.fromTo(
        pill,
        { scale: 0.95 },
        {
          scale: 1,
          duration: 0.28,
          ease: "back.out(2.2)",
          clearProps: "transform"
        }
      );
    });
  }

  function enhanceAllBars() {
    injectStyles();
    const selector = ".filter-chip-row, .segmented-control, .welcome-mode-row, #ai-filter-row, #explore-sort-bar, #map-style-switcher";
    document.querySelectorAll(selector).forEach(enhanceBar);
  }

  function boot() {
    enhanceAllBars();
    let timer = null;
    const obs = new MutationObserver(() => {
      if (timer) return;
      timer = requestAnimationFrame(() => {
        timer = null;
        enhanceAllBars();
      });
    });
    obs.observe(document.body, { childList: true, subtree: true });
  }

  global.OpenParkJellyRadio = { init: boot, enhanceAllBars };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(window);
