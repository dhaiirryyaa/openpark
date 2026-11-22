"""
OpenPark Supabase Integration Service
Provides seamless bidirectional sync between OpenPark and Supabase:
- PostgreSQL + PostGIS via direct database connection
- RESTful PostgREST API operations (httpx)
- Realtime table synchronization for parking lots, vehicle telemetry, reservations, and reports
- Resilient fallback to local state if Supabase is offline or unconfigured
"""

import os
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("openpark.supabase")

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
SUPABASE_KEY = SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY

DATABASE_URL = os.getenv("DATABASE_URL", "")


def is_supabase_configured() -> bool:
    """Returns True if Supabase REST API or Database connection is configured."""
    has_rest = bool(SUPABASE_URL and SUPABASE_KEY)
    has_db = "supabase" in DATABASE_URL.lower()
    return has_rest or has_db


def get_headers() -> Dict[str, str]:
    """Returns authenticated HTTP headers for Supabase PostgREST API."""
    key = SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }


async def check_supabase_health() -> Dict[str, Any]:
    """Tests connection to Supabase and returns diagnostic status."""
    if not is_supabase_configured():
        return {
            "status": "unconfigured",
            "connected": False,
            "message": "SUPABASE_URL and SUPABASE_ANON_KEY (or DATABASE_URL) are not set in environment.",
            "url": None
        }

    url_masked = None
    if SUPABASE_URL:
        # Mask project ref for privacy e.g. https://xyz****.supabase.co
        parts = SUPABASE_URL.split("//")
        if len(parts) == 2:
            host = parts[1]
            url_masked = f"{parts[0]}//{host[:4]}****.{host.split('.')[-2]}.{host.split('.')[-1]}" if '.' in host else SUPABASE_URL

    result = {
        "status": "ok",
        "connected": False,
        "url": url_masked,
        "rest_configured": bool(SUPABASE_URL and SUPABASE_KEY),
        "db_configured": "supabase" in DATABASE_URL.lower(),
        "tables": {}
    }

    if SUPABASE_URL and SUPABASE_KEY:
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                # Query parking_lots table count
                resp = await client.get(
                    f"{SUPABASE_URL}/rest/v1/parking_lots?select=id",
                    headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Range": "0-0", "Prefer": "count=exact"}
                )
                if resp.status_code in (200, 206):
                    content_range = resp.headers.get("content-range", "")
                    total = content_range.split("/")[-1] if "/" in content_range else "0"
                    result["connected"] = True
                    result["tables"]["parking_lots"] = {
                        "accessible": True,
                        "row_count": int(total) if total.isdigit() else 0
                    }
                else:
                    result["tables"]["parking_lots"] = {
                        "accessible": False,
                        "status_code": resp.status_code,
                        "detail": resp.text[:200]
                    }
        except Exception as e:
            logger.warning(f"[Supabase] Health check error: {e}")
            result["connected"] = False
            result["error"] = str(e)

    return result


async def fetch_lots_from_supabase(city: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """Fetches all parking lots from Supabase public.parking_lots table."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return None

    try:
        url = f"{SUPABASE_URL}/rest/v1/parking_lots?select=*"
        if city:
            url += f"&city=eq.{city}"
        url += "&order=id.asc"

        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url, headers=get_headers())
            if resp.status_code == 200:
                lots = resp.json()
                if isinstance(lots, list) and len(lots) > 0:
                    return lots
    except Exception as e:
        logger.warning(f"[Supabase] Failed to fetch lots: {e}")
    return None


async def sync_fallback_lots_to_supabase(fallback_lots: List[Dict[str, Any]]) -> bool:
    """Upserts fallback parking lots into Supabase parking_lots table on startup."""
    if not (SUPABASE_URL and SUPABASE_KEY and fallback_lots):
        return False

    records = []
    for lot in fallback_lots:
        rec = {
            "id": int(lot["id"]),
            "osm_ref": str(lot.get("osm_ref", f"lot_{lot['id']}")),
            "name": str(lot.get("name", "Parking Lot")),
            "address": str(lot.get("address") or f"{lot.get('name', 'Parking')}, Bengaluru"),
            "city": str(lot.get("city", "Bengaluru")),
            "lat": float(lot.get("lat") or 12.9716),
            "lon": float(lot.get("lon") or 77.5946),
            "capacity": int(lot.get("capacity") or 50),
            "free_spots": int(lot.get("free_spots") or 20),
            "price_car": str(lot.get("price_car") or "₹40"),
            "price_note": str(lot.get("price_note") or "₹40/hr"),
            "status": str(lot.get("status", "available")),
            "source": str(lot.get("source", "sensor")),
            "type": str(lot.get("type", "surface")),
            "has_ev": bool(lot.get("has_ev", False)),
            "is_covered": bool(lot.get("is_covered", False)),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        records.append(rec)

    try:
        headers = get_headers()
        headers["Prefer"] = "resolution=merge-duplicates"
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/parking_lots",
                headers=headers,
                json=records
            )
            if resp.status_code in (200, 201, 204):
                logger.info(f"[Supabase] Successfully synchronized {len(records)} parking lots.")
                return True
            else:
                logger.warning(f"[Supabase] Sync returned status {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        logger.warning(f"[Supabase] Error syncing parking lots: {e}")
    return False


async def update_lot_in_supabase(lot_id: int, free_spots: int, source: str = "sensor") -> bool:
    """Pushes a live vacancy update for a parking lot into Supabase."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return False

    try:
        now_iso = datetime.now(timezone.utc).isoformat()
        payload = {
            "free_spots": int(free_spots),
            "source": source,
            "status": "available" if free_spots > 0 else "full",
            "updated_at": now_iso
        }
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.patch(
                f"{SUPABASE_URL}/rest/v1/parking_lots?id=eq.{lot_id}",
                headers=get_headers(),
                json=payload
            )
            return resp.status_code in (200, 204)
    except Exception as e:
        logger.warning(f"[Supabase] Error updating lot {lot_id}: {e}")
        return False


async def save_vehicle_telemetry_to_supabase(
    device_id: str,
    lat: float,
    lon: float,
    speed: float = 0.0,
    heading: float = 0.0,
    altitude: float = 0.0,
    accuracy: float = 5.0,
    battery: float = 100.0
) -> bool:
    """Streams a vehicle GPS fix into Supabase vehicle_telemetry table."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return False

    try:
        payload = {
            "device_id": str(device_id),
            "lat": float(lat),
            "lon": float(lon),
            "speed": float(speed),
            "heading": float(heading),
            "altitude": float(altitude),
            "accuracy": float(accuracy),
            "battery": float(battery),
            "recorded_at": datetime.now(timezone.utc).isoformat()
        }
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/vehicle_telemetry",
                headers=get_headers(),
                json=payload
            )
            return resp.status_code in (200, 201, 204)
    except Exception as e:
        logger.debug(f"[Supabase] Telemetry save note: {e}")
        return False


async def save_reservation_to_supabase(
    reservation_id: str,
    lot_id: int,
    lot_name: str,
    pass_code: str,
    duration_mins: int,
    expires_at: datetime,
    user_id: Optional[str] = None,
    user_email: Optional[str] = None
) -> bool:
    """Records a new parking hold in Supabase reservations table."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return False

    try:
        payload = {
            "id": reservation_id,
            "lot_id": int(lot_id),
            "lot_name": lot_name,
            "pass_code": pass_code,
            "duration_mins": int(duration_mins),
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at.isoformat()
        }
        if user_id:
            payload["user_id"] = user_id
        if user_email:
            payload["user_email"] = user_email

        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/reservations",
                headers=get_headers(),
                json=payload
            )
            return resp.status_code in (200, 201, 204)
    except Exception as e:
        logger.warning(f"[Supabase] Reservation save error: {e}")
        return False


_TOKEN_CACHE: Dict[str, Dict[str, Any]] = {}


async def verify_supabase_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifies a Supabase Auth access token by calling GET /auth/v1/user.
    Returns user dict with id, email, role, user_metadata.
    Includes in-memory TTL caching for 60 seconds.
    """
    if not token or not SUPABASE_URL or not SUPABASE_KEY:
        return None

    now = datetime.now(timezone.utc)
    cached = _TOKEN_CACHE.get(token)
    if cached and cached["expires_at"] > now:
        return cached["user"]

    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {token}"
                }
            )
            if resp.status_code == 200:
                user_data = resp.json()
                _TOKEN_CACHE[token] = {
                    "user": user_data,
                    "expires_at": now + timedelta(seconds=60)
                }
                if len(_TOKEN_CACHE) > 1000:
                    oldest_k = next(iter(_TOKEN_CACHE))
                    _TOKEN_CACHE.pop(oldest_k, None)
                return user_data
    except Exception as e:
        logger.debug(f"[Supabase Auth] Token verify note: {e}")
    return None


async def fetch_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Fetches user profile row from public.user_profiles."""
    if not (SUPABASE_URL and SUPABASE_KEY and user_id):
        return None
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/user_profiles?id=eq.{user_id}",
                headers=get_headers()
            )
            if resp.status_code == 200:
                rows = resp.json()
                return rows[0] if rows else None
    except Exception as e:
        logger.debug(f"[Supabase] User profile fetch note: {e}")
    return None


async def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> bool:
    """Upserts user profile in public.user_profiles."""
    if not (SUPABASE_URL and SUPABASE_KEY and user_id):
        return False
    try:
        payload = {
            "id": user_id,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **profile_data
        }
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/user_profiles",
                headers={
                    **get_headers(),
                    "Prefer": "resolution=merge-duplicates"
                },
                json=payload
            )
            return resp.status_code in (200, 201, 204)
    except Exception as e:
        logger.warning(f"[Supabase] User profile update error: {e}")
        return False


async def fetch_user_reservations(user_id: str) -> List[Dict[str, Any]]:
    """Fetches active and recent reservations for an authenticated user."""
    if not (SUPABASE_URL and SUPABASE_KEY and user_id):
        return []
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(
                f"{SUPABASE_URL}/rest/v1/reservations?user_id=eq.{user_id}&order=created_at.desc&limit=20",
                headers=get_headers()
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        logger.debug(f"[Supabase] User reservations fetch note: {e}")
    return []


async def cancel_user_reservation(user_id: str, hold_id: str) -> bool:
    """Cancels a reservation owned by user."""
    if not (SUPABASE_URL and SUPABASE_KEY and user_id and hold_id):
        return False
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.patch(
                f"{SUPABASE_URL}/rest/v1/reservations?id=eq.{hold_id}&user_id=eq.{user_id}",
                headers=get_headers(),
                json={"status": "cancelled", "expires_at": datetime.now(timezone.utc).isoformat()}
            )
            return resp.status_code in (200, 204)
    except Exception as e:
        logger.warning(f"[Supabase] Cancel reservation error: {e}")
        return False


async def save_report_to_supabase(lot_id: int, kind: str, reporter_id: Optional[str] = None) -> bool:
    """Stores a crowd or sensor availability report in Supabase."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return False

    try:
        payload = {
            "lot_id": int(lot_id),
            "kind": kind,
            "reporter_id": reporter_id or "anonymous",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/reports",
                headers=get_headers(),
                json=payload
            )
            return resp.status_code in (200, 201, 204)
    except Exception as e:
        logger.warning(f"[Supabase] Report save error: {e}")
        return False


async def log_copilot_query_to_supabase(
    query: str,
    query_type: str,
    user_lat: Optional[float],
    user_lon: Optional[float],
    top_recommendation: Optional[str],
    results_count: int
) -> bool:
    """Logs an AI Copilot inquiry to Supabase copilot_queries table for analytics."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        return False

    try:
        payload = {
            "query": query[:500],
            "query_type": query_type,
            "user_lat": float(user_lat) if user_lat is not None else None,
            "user_lon": float(user_lon) if user_lon is not None else None,
            "top_recommendation": (top_recommendation or "")[:200],
            "results_count": int(results_count),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/copilot_queries",
                headers=get_headers(),
                json=payload
            )
            return resp.status_code in (200, 201, 204)
    except Exception as e:
        logger.debug(f"[Supabase] Copilot query log note: {e}")
        return False
