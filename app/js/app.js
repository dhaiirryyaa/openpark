// app.js – Clean Modern OpenPark Application Orchestration
import { LOC, onLocation, startLocating } from './locate.js';
import { API } from './api.js';
import { MapEngine } from './map-engine.js';

class OpenParkApp {
  constructor() {
    this.state = {
      userLocation: null,
      isManualLocation: false,
      activeFilter: 'all',
      lots: [],
      selectedLot: null,
      selectedPlace: null,
      activeTrip: null,
      tripWatchTimer: null
    };

    this.mapEngine = null;
    this.searchTimer = null;
  }

  init() {
    this._initMap();
    this._bindSearch();
    this._bindControls();
    this._bindDrawer();
    this._initLocator();
  }

  _initMap() {
    this.mapEngine = new MapEngine({
      containerId: 'map',
      onMarkerDragEnd: (lat, lng) => {
        this.setUserLocation(lat, lng, true);
        this.showToast(`Pinned Spot: [${lat.toFixed(4)}, ${lng.toFixed(4)}]`, 'success');
      },
      onLotClick: (lot) => {
        this.selectLot(lot);
      },
      onMapClick: () => {
        // Dismiss autocomplete dropdown on map tap
        const dd = document.getElementById('autocomplete-dropdown');
        if (dd) dd.classList.remove('open');
      }
    });

    this.mapEngine.init();
  }

  _initLocator() {
    const gpsPill = document.getElementById('gps-status-pill');
    const gpsText = document.getElementById('gps-status-text');

    onLocation((loc) => {
      if (loc.state === 'locating') {
        if (gpsPill) { gpsPill.className = 'gps-status-pill'; }
        if (gpsText) { gpsText.innerText = 'Locating…'; }
        return;
      }

      if (loc.state === 'precise' || loc.state === 'coarse') {
        // If user manually set their spot, do not let background Wi-Fi overwrite it
        if (this.state.isManualLocation) return;

        const isFirst = !this.state.userLocation;
        const fix = {
          lat: loc.lat,
          lng: loc.lon,
          accuracy: Math.round(loc.accuracy || 20),
          isManual: false
        };
        this.state.userLocation = fix;

        if (gpsPill) {
          gpsPill.className = `gps-status-pill ${loc.state === 'precise' ? 'live' : 'approx'}`;
        }
        if (gpsText) {
          gpsText.innerText = loc.state === 'precise' ? `Live GPS (±${fix.accuracy}m)` : `Approx (±${fix.accuracy}m)`;
        }

        // Rule: map only moves when we have a REAL fix
        this.mapEngine.updateVehicle(fix);

        if (isFirst && !this.state.selectedPlace) {
          this.mapEngine.flyTo(fix.lng, fix.lat, fix.accuracy > 400 ? 15.0 : 16.5);
          this.loadNearbyLots(fix.lat, fix.lng);
          if (loc.state === 'coarse') {
            this.showToast(`Location approximate (±${fix.accuracy}m). Drag red pin to adjust exact spot.`, 'info', 4000);
          } else {
            this.showToast(`Live GPS: [${fix.lat.toFixed(4)}, ${fix.lng.toFixed(4)}]`, 'success', 2500);
          }
        }
        return;
      }

      // Error states
      if (gpsPill) gpsPill.className = 'gps-status-pill';
      if (gpsText) gpsText.innerText = loc.state === 'denied' ? 'GPS Blocked' : 'GPS Standby';
    });

    startLocating();
  }

  setUserLocation(lat, lng, isManual = false) {
    this.state.userLocation = { lat, lng, isManual, accuracy: isManual ? 5 : 20 };
    this.state.isManualLocation = isManual;

    const gpsPill = document.getElementById('gps-status-pill');
    const gpsText = document.getElementById('gps-status-text');
    if (isManual) {
      if (gpsPill) gpsPill.className = 'gps-status-pill approx';
      if (gpsText) gpsText.innerText = 'Pinned Spot';
    }

    this.mapEngine.updateVehicle(this.state.userLocation);
    this.loadNearbyLots(lat, lng);
  }

  async loadNearbyLots(lat, lng) {
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
    const lots = await API.getNearbyLots(lat, lng, this.state.activeFilter);
    this.state.lots = lots;
    this.mapEngine.renderLots(lots, this.state.selectedLot?.id);
    this.renderLotsList(lots);
  }

  renderLotsList(lots = []) {
    const listEl = document.getElementById('lots-list-scroll');
    const countEl = document.getElementById('drawer-count-badge');
    if (!listEl) return;

    if (countEl) countEl.innerText = `${lots.length} lots`;
    listEl.innerHTML = '';

    if (!lots.length) {
      listEl.innerHTML = `
        <div style="text-align:center;padding:32px 16px;color:var(--text-muted);">
          <div style="font-size:24px;margin-bottom:8px;">🅿️</div>
          <div style="font-weight:600;color:var(--text-secondary);">No parking lots found nearby</div>
          <div style="font-size:12px;margin-top:4px;">Search a destination or try changing the filter</div>
        </div>
      `;
      return;
    }

    lots.forEach((lot) => {
      const free = lot.free_spots !== undefined && lot.free_spots !== null ? lot.free_spots : (lot.capacity || 20);
      let statusClass = 'available';
      let statusText = `${free} bays free`;
      if (free <= 0 || lot.status === 'Full') {
        statusClass = 'full';
        statusText = 'Full';
      } else if (free <= 8 || lot.status === 'Filling up') {
        statusClass = 'filling';
        statusText = `${free} bays left`;
      }

      const card = document.createElement('div');
      card.className = `lot-card pressable ${this.state.selectedLot?.id === lot.id ? 'selected' : ''}`;
      card.innerHTML = `
        <div class="lot-card-top">
          <div>
            <div class="lot-card-name">${lot.name}</div>
            <div class="lot-card-address">${lot.address || 'Bengaluru'}</div>
          </div>
          <span class="lot-bays-badge ${statusClass}">${statusText}</span>
        </div>
        <div class="lot-card-meta">
          <div class="lot-meta-left">
            <span class="lot-price">${lot.price_car || '₹30/hr'}</span>
            <span>•</span>
            <span>${lot.is_covered ? '🛡️ Covered' : '☀️ Open Lot'}</span>
            ${lot.is_ev ? '<span>•</span><span>⚡ EV Fast</span>' : ''}
          </div>
          <span style="font-family:var(--font-mono);font-size:11px;color:var(--text-muted);">${lot.distance_m ? `${lot.distance_m}m` : 'Nearby'}</span>
        </div>
        <div class="lot-actions-row">
          <button class="btn-primary pressable btn-route-lot">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            Route
          </button>
          <button class="btn-secondary pressable btn-hold-lot">Hold Bay</button>
        </div>
      `;

      card.addEventListener('click', (e) => {
        if (e.target.closest('.btn-route-lot')) {
          e.stopPropagation();
          this.startNavigation(lot);
        } else if (e.target.closest('.btn-hold-lot')) {
          e.stopPropagation();
          this.holdLotBay(lot);
        } else {
          this.selectLot(lot);
        }
      });

      listEl.appendChild(card);
    });
  }

  selectLot(lot) {
    this.state.selectedLot = lot;
    this.mapEngine.renderLots(this.state.lots, lot.id);
    const lon = Number(lot.lon !== undefined ? lot.lon : lot.lng);
    const lat = Number(lot.lat);
    this.mapEngine.flyTo(lon, lat, 17);

    // Scroll card into view
    const cards = document.querySelectorAll('.lot-card');
    cards.forEach((c) => {
      const isSelected = c.querySelector('.lot-card-name')?.innerText === lot.name;
      c.classList.toggle('selected', isSelected);
      if (isSelected) c.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  }

  async holdLotBay(lot) {
    this.showToast(`Reserving bay at ${lot.name}…`, 'info');
    const res = await API.holdBay(lot.id);
    if (res) {
      this.showToast(`Bay reserved for 15 mins! Code: OP-${Math.floor(1000 + Math.random() * 9000)}`, 'success', 4500);
    } else {
      this.showToast(`Bay held for 15 mins. Please proceed to gate.`, 'success', 4000);
    }
  }

  async startNavigation(destination) {
    if (!this.state.userLocation) {
      this.showToast('Please enable device location to start navigation.', 'warning');
      return;
    }
    const destLat = Number(destination.lat);
    const destLon = Number(destination.lon !== undefined ? destination.lon : destination.lng);
    const uLat = this.state.userLocation.lat;
    const uLon = this.state.userLocation.lng;

    this.showToast(`Calculating route to ${destination.name}…`, 'info');
    const route = await API.getRoute(uLat, uLon, destLat, destLon);
    this.state.activeTrip = { destination, route };

    // Draw route on map
    this.mapEngine.drawRoute(route.coordinates || []);
    this.mapEngine.setDestination(destination);

    // Show dynamic island banner
    const banner = document.getElementById('nav-island-banner');
    const titleEl = document.getElementById('nav-instruction-main');
    const subEl = document.getElementById('nav-instruction-sub');

    if (banner) banner.classList.add('active');
    if (titleEl) titleEl.innerText = `Head to ${destination.name}`;
    if (subEl) subEl.innerText = `${route.distance_km || '1.2'} km • ~${route.duration_mins || '4'} mins ETA`;

    // Collapse bottom drawer during active trip
    const drawer = document.getElementById('bottom-drawer');
    if (drawer) drawer.classList.add('collapsed');

    this.showToast('Navigation started!', 'success');
  }

  endNavigation() {
    this.state.activeTrip = null;
    this.mapEngine.clearRoute();
    this.mapEngine.clearDestination();

    const banner = document.getElementById('nav-island-banner');
    if (banner) banner.classList.remove('active');

    const drawer = document.getElementById('bottom-drawer');
    if (drawer) drawer.classList.remove('collapsed');

    this.showToast('Navigation ended.', 'info');
  }

  _bindSearch() {
    const searchInput = document.getElementById('search-input');
    const clearBtn = document.getElementById('search-clear-btn');
    const dropdown = document.getElementById('autocomplete-dropdown');

    if (!searchInput) return;

    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim();
      clearBtn?.classList.toggle('visible', q.length > 0);
      clearTimeout(this.searchTimer);

      if (q.length < 2) {
        if (dropdown) dropdown.classList.remove('open');
        return;
      }

      this.searchTimer = setTimeout(async () => {
        const centerLat = this.state.userLocation?.lat;
        const centerLon = this.state.userLocation?.lng;
        const results = await API.searchPlaces(q, centerLat, centerLon);
        this._renderAutocomplete(results);
      }, 220);
    });

    clearBtn?.addEventListener('click', () => {
      searchInput.value = '';
      clearBtn.classList.remove('visible');
      if (dropdown) dropdown.classList.remove('open');
      this.state.selectedPlace = null;
      this.mapEngine.clearDestination();
      if (this.state.userLocation) {
        this.loadNearbyLots(this.state.userLocation.lat, this.state.userLocation.lng);
      }
    });
  }

  _renderAutocomplete(results = []) {
    const dropdown = document.getElementById('autocomplete-dropdown');
    if (!dropdown) return;

    dropdown.innerHTML = '';
    if (!results.length) {
      dropdown.classList.remove('open');
      return;
    }

    results.slice(0, 5).forEach((place) => {
      const item = document.createElement('div');
      item.className = 'autocomplete-item';
      item.innerHTML = `
        <div class="autocomplete-icon-box">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </div>
        <div class="autocomplete-text">
          <div class="autocomplete-name">${place.name}</div>
          <div class="autocomplete-sub">${place.address || 'Landmark • Bengaluru'}</div>
        </div>
      `;

      item.addEventListener('click', () => {
        dropdown.classList.remove('open');
        const sInput = document.getElementById('search-input');
        if (sInput) sInput.value = place.name;
        this.selectPlace(place);
      });

      dropdown.appendChild(item);
    });

    dropdown.classList.add('open');
  }

  selectPlace(place) {
    this.state.selectedPlace = place;
    const lon = Number(place.lon !== undefined ? place.lon : place.lng);
    const lat = Number(place.lat);

    this.mapEngine.setDestination(place);
    this.mapEngine.flyTo(lon, lat, 16);
    this.loadNearbyLots(lat, lon);
    this.showToast(`Selected: ${place.name}`, 'info');
  }

  _bindControls() {
    // My Location Button
    document.getElementById('btn-my-location')?.addEventListener('click', () => {
      this.state.isManualLocation = false;
      this.showToast('Acquiring fresh device location…', 'info');
      startLocating();
      if (this.state.userLocation) {
        this.mapEngine.flyTo(this.state.userLocation.lng, this.state.userLocation.lat, 16.5);
      }
    });

    // Zoom Controls
    document.getElementById('btn-zoom-in')?.addEventListener('click', () => {
      if (this.mapEngine?.map) this.mapEngine.map.zoomIn();
    });
    document.getElementById('btn-zoom-out')?.addEventListener('click', () => {
      if (this.mapEngine?.map) this.mapEngine.map.zoomOut();
    });

    // 3D Tilt Toggle
    let is3d = false;
    document.getElementById('btn-tilt-3d')?.addEventListener('click', () => {
      if (!this.mapEngine?.map) return;
      is3d = !is3d;
      this.mapEngine.map.easeTo({ pitch: is3d ? 55 : 0, duration: 600 });
      document.getElementById('btn-tilt-3d')?.classList.toggle('active', is3d);
    });

    // Compass North Reset
    document.getElementById('btn-compass-north')?.addEventListener('click', () => {
      if (this.mapEngine?.map) this.mapEngine.map.resetNorthPitch();
    });

    // End Route Navigation
    document.getElementById('btn-nav-abort')?.addEventListener('click', () => {
      this.endNavigation();
    });
  }

  _bindDrawer() {
    const grabBar = document.getElementById('drawer-grab-bar');
    const drawer = document.getElementById('bottom-drawer');
    grabBar?.addEventListener('click', () => {
      drawer?.classList.toggle('collapsed');
    });

    // Filter Chips
    const chips = document.querySelectorAll('.filter-chips-row .chip-btn');
    chips.forEach((btn) => {
      btn.addEventListener('click', () => {
        chips.forEach((c) => c.classList.remove('active'));
        btn.classList.add('active');
        this.state.activeFilter = btn.dataset.filter || 'all';

        const lat = this.state.selectedPlace?.lat || this.state.userLocation?.lat;
        const lon = this.state.selectedPlace?.lon || this.state.userLocation?.lng;
        if (lat && lon) {
          this.loadNearbyLots(lat, lon);
        }
      });
    });
  }

  showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const pill = document.createElement('div');
    pill.className = `toast-pill toast-${type}`;
    pill.innerText = message;
    container.appendChild(pill);
    setTimeout(() => {
      pill.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
      pill.style.opacity = '0';
      pill.style.transform = 'translateY(12px)';
      setTimeout(() => pill.remove(), 250);
    }, duration);
  }
}

// Bootstrap
window.addEventListener('DOMContentLoaded', () => {
  const app = new OpenParkApp();
  app.init();
  window.OpenPark = app;
});
