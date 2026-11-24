/* OpenPark Fable Motion Animation Engine v1.0
   Brings rich vector micro-animations, living pin levitation, ambient sonar radars,
   glowing route particle trails, and interactive map shockwaves to MapLibre GL.
*/
(() => {
  'use strict';

  const FableMotion = {
    initialized: false,
    routeAnimFrameId: null,
    routeProgress: 0,
    routeOrbMarker: null,

    init(ctx) {
      if (this.initialized) return;
      this.initialized = true;

      const mapEngine = ctx.MapEngine || window.MapEngine;
      if (!mapEngine) {
        console.warn('[FableMotion] MapEngine not ready, retrying on event...');
        window.addEventListener('openpark:ready', (e) => this.init(e.detail));
        return;
      }

      this.setupMapClickShockwaves(mapEngine);
      this.patchLotMarkers(mapEngine);
      this.patchDestinationMarker(mapEngine);
      this.patchVehicleMarker(mapEngine);
      this.patchRouteMotion(mapEngine, ctx.NavigationEngine || window.NavigationEngine);

      console.log('[FableMotion] High-End Motion & Living Map Animations active.');
    },

    // 1. Interactive Map Tap / Click Liquid Shockwave
    setupMapClickShockwaves(mapEngine) {
      const attachListener = () => {
        if (!mapEngine.map) return;
        mapEngine.map.on('click', (e) => {
          if (!e || !e.point) return;
          const container = mapEngine.map.getContainer();
          if (!container) return;

          const shockwave = document.createElement('div');
          shockwave.className = 'fable-map-shockwave';
          shockwave.style.left = `${e.point.x}px`;
          shockwave.style.top = `${e.point.y}px`;

          const innerEcho = document.createElement('div');
          innerEcho.className = 'fable-map-echo';
          shockwave.appendChild(innerEcho);

          container.appendChild(shockwave);
          setTimeout(() => {
            if (shockwave.parentNode) shockwave.parentNode.removeChild(shockwave);
          }, 850);
        });
      };

      if (mapEngine.map && mapEngine.map.loaded()) {
        attachListener();
      } else if (mapEngine.map) {
        mapEngine.map.once('load', attachListener);
      }
    },

    // 2. Fable Living Map Pins with Organic Staggered Levitation & Sonar Pings
    patchLotMarkers(mapEngine) {
      const origRender = mapEngine.renderLotMarkers;
      if (!origRender || origRender._fablePatched) return;

      const self = this;
      mapEngine.renderLotMarkers = function(lots) {
        origRender.call(this, lots);

        let idx = 0;
        this.markers.forEach((item) => {
          if (!item || !item.element) return;
          const el = item.element;
          el.classList.add('fable-pin');

          // Stagger levitation phases so pins bob rhythmically across the map
          const delay = -((idx % 6) * 0.55).toFixed(2);
          el.style.setProperty('--fable-delay', `${delay}s`);

          // Add dual sonar beacon ring to status pulse if missing
          const pulse = el.querySelector('.status-pulse');
          if (pulse && !pulse.querySelector('.fable-sonar-ring')) {
            const r1 = document.createElement('span');
            r1.className = 'fable-sonar-ring r1';
            const r2 = document.createElement('span');
            r2.className = 'fable-sonar-ring r2';
            pulse.appendChild(r1);
            pulse.appendChild(r2);
          }

          idx++;
        });
      };
      mapEngine.renderLotMarkers._fablePatched = true;
    },

    // 3. Fable Destination Beacon with 3D Ground Target Radar
    patchDestinationMarker(mapEngine) {
      const origSetDest = mapEngine.setDestinationMarker;
      if (!origSetDest || origSetDest._fablePatched) return;

      mapEngine.setDestinationMarker = function(place) {
        origSetDest.call(this, place);

        if (this.destinationMarker) {
          const el = this.destinationMarker.getElement();
          if (el && !el.querySelector('.fable-ground-target')) {
            el.classList.add('fable-dest-root');

            const groundTarget = document.createElement('div');
            groundTarget.className = 'fable-ground-target';
            groundTarget.innerHTML = `
              <span class="fable-target-ring tr1"></span>
              <span class="fable-target-ring tr2"></span>
              <span class="fable-target-ring tr3"></span>
              <span class="fable-target-core"></span>
            `;
            el.prepend(groundTarget);

            const svg = el.querySelector('.destination-pin-svg');
            if (svg) svg.classList.add('fable-pin-bob');
          }
        }
      };
      mapEngine.setDestinationMarker._fablePatched = true;
    },

    // 4. Fable Vehicle Sonar Radar & Dynamic Aura
    patchVehicleMarker(mapEngine) {
      const origCreateVehicle = mapEngine.createVehicleMarker;
      if (!origCreateVehicle || origCreateVehicle._fablePatched) return;

      mapEngine.createVehicleMarker = function() {
        origCreateVehicle.call(this);

        if (this.vehicleEl && !this.vehicleEl.querySelector('.fable-vehicle-sonar')) {
          this.vehicleEl.classList.add('fable-vehicle-root');

          const sonar = document.createElement('div');
          sonar.className = 'fable-vehicle-sonar';
          sonar.innerHTML = `
            <span class="fable-v-wave w1"></span>
            <span class="fable-v-wave w2"></span>
            <div class="fable-v-radar-sweep"></div>
          `;
          this.vehicleEl.prepend(sonar);
        }
      };
      mapEngine.createVehicleMarker._fablePatched = true;
    },

    // 5. Fable Route Energy Stream & Flowing Light Photon
    patchRouteMotion(mapEngine, navEngine) {
      if (!navEngine) return;
      const self = this;

      const origLoadRoute = navEngine.loadRoute;
      if (!origLoadRoute || origLoadRoute._fablePatched) return;

      navEngine.loadRoute = async function(origin, destination) {
        const res = await origLoadRoute.call(this, origin, destination);

        // Start Fable gliding energy photon along the route line
        if (this.routePoints && this.routePoints.length > 2 && mapEngine.map) {
          self.startRouteEnergyStream(mapEngine.map, this.routePoints);
        } else {
          self.stopRouteEnergyStream();
        }

        return res;
      };
      navEngine.loadRoute._fablePatched = true;
    },

    startRouteEnergyStream(map, points) {
      this.stopRouteEnergyStream();
      if (!map || !points || points.length < 2) return;

      // Create glowing photon DOM marker
      const orbEl = document.createElement('div');
      orbEl.className = 'fable-route-orb';
      orbEl.innerHTML = `<span class="fable-orb-glow"></span><span class="fable-orb-core"></span>`;

      this.routeOrbMarker = new maplibregl.Marker({
        element: orbEl,
        anchor: 'center'
      })
        .setLngLat(points[0])
        .addTo(map);

      // Precalculate cumulative lengths for smooth constant-speed gliding
      const cumulativeDists = [0];
      for (let i = 1; i < points.length; i++) {
        const p1 = points[i - 1];
        const p2 = points[i];
        const dx = p2[0] - p1[0];
        const dy = p2[1] - p1[1];
        const segDist = Math.sqrt(dx * dx + dy * dy);
        cumulativeDists.push(cumulativeDists[i - 1] + segDist);
      }
      const totalDist = cumulativeDists[cumulativeDists.length - 1];
      if (totalDist <= 0) return;

      let startTime = performance.now();
      const loopDurationMs = Math.min(8000, Math.max(3200, points.length * 60));

      const animate = (now) => {
        const elapsed = (now - startTime) % loopDurationMs;
        const progress = elapsed / loopDurationMs;
        const targetDist = progress * totalDist;

        // Find segment
        let segIdx = 0;
        while (segIdx < cumulativeDists.length - 1 && cumulativeDists[segIdx + 1] < targetDist) {
          segIdx++;
        }

        const segStartDist = cumulativeDists[segIdx];
        const segEndDist = cumulativeDists[segIdx + 1];
        const segLen = segEndDist - segStartDist;
        const segT = segLen > 0 ? (targetDist - segStartDist) / segLen : 0;

        const p1 = points[segIdx];
        const p2 = points[segIdx + 1] || p1;
        const currentLng = p1[0] + (p2[0] - p1[0]) * segT;
        const currentLat = p1[1] + (p2[1] - p1[1]) * segT;

        if (this.routeOrbMarker) {
          this.routeOrbMarker.setLngLat([currentLng, currentLat]);
        }

        this.routeAnimFrameId = requestAnimationFrame(animate);
      };

      this.routeAnimFrameId = requestAnimationFrame(animate);
    },

    stopRouteEnergyStream() {
      if (this.routeAnimFrameId) {
        cancelAnimationFrame(this.routeAnimFrameId);
        this.routeAnimFrameId = null;
      }
      if (this.routeOrbMarker) {
        try { this.routeOrbMarker.remove(); } catch (e) {}
        this.routeOrbMarker = null;
      }
    }
  };

  window.FableMotionEngine = FableMotion;

  // Boot on ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      FableMotion.init(window.__openpark || {});
    });
  } else {
    FableMotion.init(window.__openpark || {});
  }
  window.addEventListener('openpark:ready', (e) => FableMotion.init(e.detail || {}));
})();
