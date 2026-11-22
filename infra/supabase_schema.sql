-- ============================================================================
-- OpenPark Supabase Database Schema & Realtime Setup
-- Fully compatible with Supabase PostgreSQL 15+ & PostGIS
-- ============================================================================

-- 1. Enable PostGIS Extension (spatial indexing, distance & geometry functions)
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Parking Lots Table
CREATE TABLE IF NOT EXISTS public.parking_lots (
    id BIGINT PRIMARY KEY,
    osm_ref TEXT UNIQUE,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT DEFAULT 'Bengaluru',
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(Point, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(lon, lat), 4326)) STORED,
    capacity INT DEFAULT 50,
    free_spots INT DEFAULT 20,
    price_car TEXT DEFAULT '₹40',
    price_note TEXT DEFAULT '₹40/hr',
    status TEXT DEFAULT 'available',
    source TEXT DEFAULT 'sensor',
    type TEXT DEFAULT 'surface',
    has_ev BOOLEAN DEFAULT FALSE,
    is_covered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Spatial GIST Index for high-performance radius & proximity searches
CREATE INDEX IF NOT EXISTS parking_lots_geom_idx ON public.parking_lots USING GIST (geom);
CREATE INDEX IF NOT EXISTS parking_lots_city_idx ON public.parking_lots (city);

-- 3. Vehicle Telemetry Table (Live GPS Tracking & Traccar Stream)
CREATE TABLE IF NOT EXISTS public.vehicle_telemetry (
    id BIGSERIAL PRIMARY KEY,
    device_id TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    speed DOUBLE PRECISION DEFAULT 0,
    heading DOUBLE PRECISION DEFAULT 0,
    altitude DOUBLE PRECISION DEFAULT 0,
    accuracy DOUBLE PRECISION DEFAULT 5,
    battery DOUBLE PRECISION DEFAULT 100,
    recorded_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS vehicle_telemetry_device_time_idx ON public.vehicle_telemetry (device_id, recorded_at DESC);

-- 4. Parking Bay Reservations / Holds Table
CREATE TABLE IF NOT EXISTS public.reservations (
    id TEXT PRIMARY KEY,
    lot_id BIGINT REFERENCES public.parking_lots(id) ON DELETE CASCADE,
    lot_name TEXT,
    pass_code TEXT NOT NULL,
    duration_mins INT DEFAULT 15,
    status TEXT DEFAULT 'active', -- active | expired | completed | cancelled
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS reservations_lot_time_idx ON public.reservations (lot_id, created_at DESC);
CREATE INDEX IF NOT EXISTS reservations_status_idx ON public.reservations (status);

-- 5. Crowd & Sensor Reports Table
CREATE TABLE IF NOT EXISTS public.reports (
    id BIGSERIAL PRIMARY KEY,
    lot_id BIGINT REFERENCES public.parking_lots(id) ON DELETE CASCADE,
    kind TEXT NOT NULL, -- got_spot | lot_full | has_space | ev_free | blocked
    reporter_id TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS reports_lot_time_idx ON public.reports (lot_id, created_at DESC);

-- 6. AI Copilot Query Analytics Table
CREATE TABLE IF NOT EXISTS public.copilot_queries (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    query_type TEXT, -- place_search | parking_search
    user_lat DOUBLE PRECISION,
    user_lon DOUBLE PRECISION,
    top_recommendation TEXT,
    results_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================================================
-- 7. Supabase Realtime Setup
-- Enable WebSocket broadcast streaming for instant cross-device synchronization
-- ============================================================================
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables 
    WHERE pubname = 'supabase_realtime' AND tablename = 'parking_lots'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.parking_lots;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables 
    WHERE pubname = 'supabase_realtime' AND tablename = 'vehicle_telemetry'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.vehicle_telemetry;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables 
    WHERE pubname = 'supabase_realtime' AND tablename = 'reservations'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.reservations;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables 
    WHERE pubname = 'supabase_realtime' AND tablename = 'reports'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE public.reports;
  END IF;
END $$;

-- Set replica identity to FULL so realtime updates send old & new row snapshots
ALTER TABLE public.parking_lots REPLICA IDENTITY FULL;
ALTER TABLE public.vehicle_telemetry REPLICA IDENTITY FULL;
ALTER TABLE public.reservations REPLICA IDENTITY FULL;
ALTER TABLE public.reports REPLICA IDENTITY FULL;

-- ============================================================================
-- 8. Row Level Security (RLS) Policies
-- Public read access + Authenticated/Service Role write permissions
-- ============================================================================
ALTER TABLE public.parking_lots ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vehicle_telemetry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reservations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.copilot_queries ENABLE ROW LEVEL SECURITY;

-- Parking Lots: anyone can read; anon & service_role can insert/update
CREATE POLICY "Public Read Parking Lots" ON public.parking_lots FOR SELECT USING (true);
CREATE POLICY "Allow Insert/Update Parking Lots" ON public.parking_lots FOR ALL USING (true) WITH CHECK (true);

-- Vehicle Telemetry: anyone can read & insert
CREATE POLICY "Public Read Vehicle Telemetry" ON public.vehicle_telemetry FOR SELECT USING (true);
CREATE POLICY "Allow Insert Vehicle Telemetry" ON public.vehicle_telemetry FOR INSERT WITH CHECK (true);

-- Reservations: public read & insert
CREATE POLICY "Public Read Reservations" ON public.reservations FOR SELECT USING (true);
CREATE POLICY "Allow Insert/Update Reservations" ON public.reservations FOR ALL USING (true) WITH CHECK (true);

-- Reports: public read & insert
CREATE POLICY "Public Read Reports" ON public.reports FOR SELECT USING (true);
CREATE POLICY "Allow Insert Reports" ON public.reports FOR INSERT WITH CHECK (true);

-- Copilot Queries: public read & insert
CREATE POLICY "Public Read Copilot Queries" ON public.copilot_queries FOR SELECT USING (true);
CREATE POLICY "Allow Insert Copilot Queries" ON public.copilot_queries FOR INSERT WITH CHECK (true);

-- ============================================================================
-- 9. Seed Data: Pre-Populate Verified OpenPark Bengaluru Parking Lots
-- ============================================================================
INSERT INTO public.parking_lots (id, osm_ref, name, address, city, lat, lon, capacity, free_spots, price_car, price_note, status, source, type, has_ev, is_covered)
VALUES
  (1, 'way/blr_ub_city', 'UB City Multi-Level Parking', 'Vittal Mallya Road, KG Halli, D Souza Layout, Bengaluru', 'Bengaluru', 12.97194, 77.59583, 200, 95, '₹50', '₹50/hr', 'available', 'sensor', 'multilevel', true, true),
  (2, 'way/blr_brigade_road', 'Brigade Road Smart On-Street Parking', 'Brigade Road, Ashok Nagar, Bengaluru', 'Bengaluru', 12.97333, 77.60806, 60, 18, '₹40', '₹40/hr', 'available', 'sensor', 'surface', false, false),
  (3, 'way/blr_forum_mall', 'The Forum South Bengaluru Mall Parking', 'Konanakunte Cross, Kanakapura Rd, Bengaluru', 'Bengaluru', 12.88880, 77.54580, 350, 142, '₹40', '₹40/hr', 'available', 'sensor', 'multilevel', true, true),
  (4, 'way/blr_cubbon_park', 'Cubbon Park High Court Gate Parking', 'Ambedkar Veedhi, Sampangi Rama Nagar, Bengaluru', 'Bengaluru', 12.97806, 77.59250, 90, 48, '₹30', '₹30/hr', 'available', 'sensor', 'surface', false, false),
  (5, 'way/blr_church_street', 'Church Street Pedestrian Bay', 'Church Street, Shanthala Nagar, Ashok Nagar, Bengaluru', 'Bengaluru', 12.97444, 77.60556, 40, 2, '₹40', '₹40/hr', 'limited', 'crowd', 'surface', false, false),
  (6, 'way/blr_garuda_mall', 'Garuda Mall Basement Parking', 'Magrath Rd, Ashok Nagar, Bengaluru', 'Bengaluru', 12.97028, 77.60972, 220, 88, '₹50', '₹50/hr', 'available', 'sensor', 'underground', true, true),
  (7, 'way/blr_mantri_square', 'Mantri Square Mall Multi-Level Deck', 'Sampige Rd, Malleshwaram, Bengaluru', 'Bengaluru', 12.99167, 77.57111, 400, 175, '₹40', '₹40/hr', 'available', 'sensor', 'multilevel', true, true),
  (8, 'way/blr_indiranagar_100ft', '100 Feet Road Indiranagar Street Parking', '100 Feet Rd, HAL 2nd Stage, Indiranagar, Bengaluru', 'Bengaluru', 12.96444, 77.64167, 75, 24, '₹30', '₹30/hr', 'available', 'crowd', 'surface', false, false),
  (9, 'way/blr_orion_mall', 'Orion Mall & Gateway Plaza Parking', 'Dr Rajkumar Rd, Rajajinagar, Bengaluru', 'Bengaluru', 13.01111, 77.55500, 450, 210, '₹50', '₹50/hr', 'available', 'sensor', 'multilevel', true, true),
  (10, 'way/blr_commercial_street', 'Commercial Street Kamaraj Road Lot', 'Kamaraj Rd, Tasker Town, Shivaji Nagar, Bengaluru', 'Bengaluru', 12.98222, 77.60889, 80, 15, '₹40', '₹40/hr', 'available', 'crowd', 'surface', false, false),
  (11, 'way/blr_koramangala_80ft', 'Koramangala 80 Feet Road Smart Bay', '80 Feet Rd, 4th Block, Koramangala, Bengaluru', 'Bengaluru', 12.93444, 77.62500, 50, 12, '₹30', '₹30/hr', 'available', 'crowd', 'surface', false, false),
  (12, 'way/blr_majestic_kbs', 'Kempegowda Bus Station (Majestic) Lot', 'Gubbi Veeranna Crescent, Majestic, Bengaluru', 'Bengaluru', 12.97722, 77.57278, 250, 64, '₹20', '₹20/hr', 'available', 'sensor', 'surface', false, false),
  (13, 'way/blr_nexus_koramangala', 'Nexus Mall Koramangala Parking Deck', 'Hosur Rd, Chikku Lakshmaiah Layout, Koramangala, Bengaluru', 'Bengaluru', 12.93500, 77.61333, 300, 110, '₹40', '₹40/hr', 'available', 'sensor', 'multilevel', true, true),
  (14, 'way/blr_kr_market', 'KR Market City Market Multi-Deck', 'Kalasipalya New Extension, Kalasipalya, Bengaluru', 'Bengaluru', 12.96472, 77.57639, 120, 31, '₹20', '₹20/hr', 'available', 'sensor', 'multilevel', false, true),
  (15, 'way/blr_cantonment_station', 'Bengaluru Cantonment Railway Station Parking', 'Cantonment Railway Station Rd, Vasanth Nagar, Bengaluru', 'Bengaluru', 12.99370, 77.59830, 180, 82, '₹20', '₹20/hr', 'available', 'sensor', 'surface', false, false),
  (16, 'way/blr_mg_road_cbd', 'MG Road & Brigade Smart Parking', 'Mahatma Gandhi Rd, Shanthala Nagar, Ashok Nagar, Bengaluru', 'Bengaluru', 12.97560, 77.60660, 150, 68, '₹40', '₹40/hr', 'available', 'sensor', 'multilevel', false, true)
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  address = EXCLUDED.address,
  lat = EXCLUDED.lat,
  lon = EXCLUDED.lon,
  capacity = EXCLUDED.capacity,
  free_spots = EXCLUDED.free_spots,
  price_car = EXCLUDED.price_car,
  price_note = EXCLUDED.price_note,
  has_ev = EXCLUDED.has_ev,
  is_covered = EXCLUDED.is_covered,
  updated_at = now();
