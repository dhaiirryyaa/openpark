// map-engine.js – Clean MapLibre GL Integration for OpenPark
export class MapEngine {
  constructor({ containerId = 'map', onMarkerDragEnd, onLotClick, onMapClick }) {
    this.containerId = containerId;
    this.onMarkerDragEnd = onMarkerDragEnd;
    this.onLotClick = onLotClick;
    this.onMapClick = onMapClick;

    this.map = null;
    this.vehicleMarker = null;
    this.vehicleEl = null;
    this.destinationMarker = null;
    this.lotMarkers = new Map();

    this.styles = {
      'google-hybrid': {
        version: 8,
        sources: {
          'google-tiles': {
            type: 'raster',
            tiles: [
              'https://mt0.google.com/vt/lyrs=y&hl=en&gl=IN&scale=2&x={x}&y={y}&z={z}',
              'https://mt1.google.com/vt/lyrs=y&hl=en&gl=IN&scale=2&x={x}&y={y}&z={z}'
            ],
            tileSize: 256
          }
        },
        layers: [{ id: 'google-hybrid-base', type: 'raster', source: 'google-tiles' }]
      },
      'dark': 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
      'voyager': 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'
    };
    this.currentStyle = 'google-hybrid';
  }

  init() {
    this.map = new maplibregl.Map({
      container: this.containerId,
      style: this.styles[this.currentStyle],
      center: [77.5946, 12.9716], // Initial canvas center (stationary until fix)
      zoom: 14,
      pitch: 0,
      bearing: 0,
      antialias: true,
      attributionControl: false
    });

    this.map.on('load', () => {
      this._setupSources();
    });

    this.map.on('click', (e) => {
      if (this.onMapClick) this.onMapClick(e.lngLat);
    });

    window.addEventListener('resize', () => {
      if (this.map) this.map.resize();
    });
  }

  _setupSources() {
    if (!this.map) return;

    // Route polyline source
    if (!this.map.getSource('route')) {
      this.map.addSource('route', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
      this.map.addLayer({
        id: 'route-casing',
        type: 'line',
        source: 'route',
        layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: {
          'line-color': '#1d4ed8',
          'line-width': 9,
          'line-opacity': 0.75
        }
      });
      this.map.addLayer({
        id: 'route-line',
        type: 'line',
        source: 'route',
        layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: {
          'line-color': '#38bdf8',
          'line-width': 5,
          'line-opacity': 0.95
        }
      });
    }

    // Accuracy Circle Source
    if (!this.map.getSource('accuracy-circle')) {
      this.map.addSource('accuracy-circle', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
      this.map.addLayer({
        id: 'accuracy-fill',
        type: 'fill',
        source: 'accuracy-circle',
        paint: {
          'fill-color': '#0071e3',
          'fill-opacity': 0.12
        }
      });
      this.map.addLayer({
        id: 'accuracy-stroke',
        type: 'line',
        source: 'accuracy-circle',
        paint: {
          'line-color': '#0071e3',
          'line-width': 1.5,
          'line-opacity': 0.5
        }
      });
    }
  }

  switchStyle(styleKey) {
    if (!this.styles[styleKey] || this.currentStyle === styleKey) return;
    this.currentStyle = styleKey;
    this.map.setStyle(this.styles[styleKey]);
    this.map.once('style.load', () => {
      this._setupSources();
    });
  }

  // ---- Vehicle Marker (User Pin) ----
  updateVehicle({ lat, lng, heading = 0, speed = 0, accuracy = null, isManual = false }) {
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

    if (!this.vehicleMarker) {
      this.vehicleEl = document.createElement('div');
      this.vehicleEl.className = 'vehicle-marker-root';
      this.vehicleEl.innerHTML = `
        <div class="vehicle-chevron" id="v-rotator">
          <svg viewBox="0 0 48 48" width="44" height="44">
            <defs>
              <linearGradient id="vGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#ef4444"/>
                <stop offset="100%" stop-color="#b91c1c"/>
              </linearGradient>
              <filter id="vShadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="rgba(0,0,0,0.5)"/>
              </filter>
            </defs>
            <circle cx="24" cy="24" r="22" fill="rgba(239, 68, 68, 0.2)"/>
            <path d="M24 4 L42 40 L24 32 L6 40 Z" fill="#ffffff" filter="url(#vShadow)"/>
            <path d="M24 7 L38 37 L24 30 L10 37 Z" fill="url(#vGrad)"/>
            <circle cx="24" cy="24" r="3.5" fill="#ffffff"/>
          </svg>
        </div>
        <div class="vehicle-pill" id="v-pill">Device Location</div>
      `;

      this.vehicleMarker = new maplibregl.Marker({
        element: this.vehicleEl,
        anchor: 'center',
        draggable: true
      })
        .setLngLat([lng, lat])
        .addTo(this.map);

      this.vehicleMarker.on('dragstart', () => {
        this.vehicleEl.classList.add('dragging');
      });
      this.vehicleMarker.on('dragend', () => {
        this.vehicleEl.classList.remove('dragging');
        const pos = this.vehicleMarker.getLngLat();
        if (this.onMarkerDragEnd) this.onMarkerDragEnd(pos.lat, pos.lng);
      });
    } else {
      this.vehicleMarker.setLngLat([lng, lat]);
    }

    const rotator = this.vehicleEl?.querySelector('#v-rotator');
    if (rotator) {
      const mapBearing = this.map ? this.map.getBearing() : 0;
      rotator.style.transform = `rotate(${(heading - mapBearing + 360) % 360}deg)`;
    }

    const pill = this.vehicleEl?.querySelector('#v-pill');
    if (pill) {
      if (isManual) {
        pill.innerText = 'Pinned Spot (Exact)';
      } else if (accuracy && accuracy > 60) {
        pill.innerText = `±${Math.round(accuracy)}m • Drag to adjust`;
      } else {
        pill.innerText = `Device Location (±${Math.round(accuracy || 10)}m)`;
      }
    }

    // Update real-world accuracy circle
    this.updateAccuracyCircle(lng, lat, isManual ? 0 : accuracy);
  }

  updateAccuracyCircle(lng, lat, radiusMeters) {
    if (!this.map || !this.map.getSource('accuracy-circle')) return;
    const src = this.map.getSource('accuracy-circle');
    if (!Number.isFinite(lng) || !Number.isFinite(lat) || !radiusMeters || radiusMeters < 20) {
      src.setData({ type: 'FeatureCollection', features: [] });
      return;
    }
    const rad = Math.min(2000, radiusMeters);
    const coords = [];
    const points = 64;
    const distanceX = rad / (111320 * Math.cos((lat * Math.PI) / 180));
    const distanceY = rad / 110574;
    for (let i = 0; i < points; i++) {
      const theta = (i / points) * (2 * Math.PI);
      coords.push([lng + distanceX * Math.cos(theta), lat + distanceY * Math.sin(theta)]);
    }
    coords.push(coords[0]);
    src.setData({
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        geometry: { type: 'Polygon', coordinates: [coords] }
      }]
    });
  }

  // ---- Parking Lots Markers ----
  renderLots(lots = [], selectedLotId = null) {
    // Clean removed lots
    const activeIds = new Set(lots.map((l) => String(l.id)));
    for (const [id, marker] of this.lotMarkers.entries()) {
      if (!activeIds.has(id)) {
        marker.remove();
        this.lotMarkers.delete(id);
      }
    }

    lots.forEach((lot) => {
      const id = String(lot.id);
      const isSelected = selectedLotId && String(selectedLotId) === id;
      const lon = Number(lot.lon !== undefined ? lot.lon : lot.lng);
      const lat = Number(lot.lat);
      if (!Number.isFinite(lon) || !Number.isFinite(lat)) return;

      if (this.lotMarkers.has(id)) {
        const marker = this.lotMarkers.get(id);
        marker.getElement().classList.toggle('selected', isSelected);
        return;
      }

      const el = document.createElement('div');
      el.className = `openpark-lot-pin ${isSelected ? 'selected' : ''}`;
      const free = lot.free_spots !== undefined && lot.free_spots !== null ? lot.free_spots : (lot.capacity || 20);
      el.innerHTML = `
        <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#10b981;"></span>
        <span>${free} bays</span>
      `;

      el.addEventListener('click', (e) => {
        e.stopPropagation();
        if (this.onLotClick) this.onLotClick(lot);
      });

      const marker = new maplibregl.Marker({ element: el, anchor: 'center' })
        .setLngLat([lon, lat])
        .addTo(this.map);

      this.lotMarkers.set(id, marker);
    });
  }

  // ---- Destination Marker ----
  setDestination(place) {
    if (this.destinationMarker) {
      this.destinationMarker.remove();
      this.destinationMarker = null;
    }
    if (!place) return;
    const lon = Number(place.lon !== undefined ? place.lon : place.lng);
    const lat = Number(place.lat);
    if (!Number.isFinite(lon) || !Number.isFinite(lat)) return;

    const el = document.createElement('div');
    el.innerHTML = `
      <svg viewBox="0 0 32 40" width="32" height="40">
        <path d="M16 0 C7.16 0 0 7.16 0 16 C0 26 16 40 16 40 C16 40 32 26 32 16 C32 7.16 24.84 0 16 0 Z" fill="#ef4444" stroke="#ffffff" stroke-width="2"/>
        <circle cx="16" cy="15" r="5" fill="#ffffff"/>
      </svg>
    `;
    this.destinationMarker = new maplibregl.Marker({ element: el, anchor: 'bottom' })
      .setLngLat([lon, lat])
      .addTo(this.map);
  }

  clearDestination() {
    if (this.destinationMarker) {
      this.destinationMarker.remove();
      this.destinationMarker = null;
    }
  }

  // ---- Turn-by-Turn Route Polyline ----
  drawRoute(coordinates = []) {
    if (!this.map || !this.map.getSource('route')) return;
    const src = this.map.getSource('route');
    if (!coordinates.length) {
      src.setData({ type: 'FeatureCollection', features: [] });
      return;
    }
    src.setData({
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        geometry: { type: 'LineString', coordinates }
      }]
    });
  }

  clearRoute() {
    this.drawRoute([]);
  }

  flyTo(lng, lat, zoom = 16.5) {
    if (!this.map || !Number.isFinite(lng) || !Number.isFinite(lat)) return;
    this.map.flyTo({ center: [lng, lat], zoom, duration: 800 });
  }

  easeTo(lng, lat, zoom = 16.5) {
    if (!this.map || !Number.isFinite(lng) || !Number.isFinite(lat)) return;
    this.map.easeTo({ center: [lng, lat], zoom, duration: 400 });
  }
}
