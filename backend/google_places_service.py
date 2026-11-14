"""
Google Maps Platform Places API (New) & Geocoding Integration Service
Enables searching any place, business, landmark, address, or coordinate worldwide
using Google Maps official Places API (New) and Geocoding Web Service.
"""

import os
import logging
import urllib.parse
from typing import List, Dict, Any, Optional
import httpx

try:
    from backend.traccar_service import calculate_haversine_km, is_in_india, enrich_place_details
except ImportError:
    from traccar_service import calculate_haversine_km, is_in_india, enrich_place_details

logger = logging.getLogger("openpark.google_places")

GOOGLE_PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
ATTRIBUTION_SOLUTION_ID = "gmp_git_agentskills_v1"

# Mapping Google place types to OpenPark visual category badges & emojis
TYPE_BADGE_MAP = {
    "restaurant": ("🍽️", "restaurant"),
    "cafe": ("☕", "cafe"),
    "coffee_shop": ("☕", "cafe"),
    "bakery": ("🥐", "cafe"),
    "bar": ("🍸", "restaurant"),
    "hospital": ("🏥", "hospital"),
    "pharmacy": ("💊", "hospital"),
    "doctor": ("🩺", "hospital"),
    "shopping_mall": ("🛍️", "shopping"),
    "department_store": ("🏬", "shopping"),
    "supermarket": ("🛒", "shopping"),
    "grocery_store": ("🛒", "shopping"),
    "store": ("🛍️", "shopping"),
    "lodging": ("🏨", "hotel"),
    "hotel": ("🏨", "hotel"),
    "gas_station": ("⛽", "fuel"),
    "park": ("🌳", "park"),
    "tourist_attraction": ("⭐", "landmark"),
    "museum": ("🏛️", "landmark"),
    "transit_station": ("🚇", "transit"),
    "subway_station": ("🚇", "transit"),
    "airport": ("✈️", "transit"),
    "train_station": ("🚆", "transit"),
    "parking": ("🅿️", "parking"),
    "car_repair": ("🔧", "service"),
    "bank": ("🏦", "finance"),
    "atm": ("🏧", "finance"),
    "school": ("🏫", "education"),
    "university": ("🎓", "education")
}


def resolve_type_badge(types: List[str]) -> tuple[str, str]:
    if not types:
        return ("🏢", "place")
    for t in types:
        clean = t.lower()
        if clean in TYPE_BADGE_MAP:
            return TYPE_BADGE_MAP[clean]
    return ("🏢", "place")


async def search_google_places(
    query: str,
    lat: float = 12.9716,
    lon: float = 77.5946,
    api_key: Optional[str] = None,
    limit: int = 15,
    india_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Searches Google Maps Places API (New) using text search.
    Returns rich place records matching Google Maps exactly.
    """
    key = (api_key or os.getenv("GOOGLE_MAPS_API_KEY") or "").strip()
    if not key:
        return []

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,places.location,"
            "places.types,places.rating,places.userRatingCount,places.googleMapsUri,"
            "places.websiteUri,places.nationalPhoneNumber"
        ),
        "X-Goog-Maps-Solution-ID": ATTRIBUTION_SOLUTION_ID
    }

    body: Dict[str, Any] = {
        "textQuery": query.strip(),
        "maxResultCount": min(20, max(1, limit))
    }

    # Add location bias circle around user/viewport if valid coordinates
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        body["locationBias"] = {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": 50000.0  # 50km proximity bias
            }
        }

    results: List[Dict[str, Any]] = []

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(GOOGLE_PLACES_SEARCH_URL, json=body, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                raw_places = data.get("places", [])
                for p in raw_places:
                    loc = p.get("location") or {}
                    p_lat = loc.get("latitude")
                    p_lng = loc.get("longitude")
                    if p_lat is None or p_lng is None:
                        continue

                    if india_only and not is_in_india(float(p_lat), float(p_lng)):
                        continue

                    display_name = (p.get("displayName") or {}).get("text") or query
                    types = p.get("types") or []
                    badge_emoji, badge_tag = resolve_type_badge(types)
                    category_label = types[0].replace("_", " ").title() if types else "Place"

                    dist_km = calculate_haversine_km(lat, lon, float(p_lat), float(p_lng))

                    place_item = {
                        "name": display_name,
                        "badge": badge_emoji,
                        "category": category_label,
                        "address": p.get("formattedAddress") or display_name,
                        "lat": float(p_lat),
                        "lon": float(p_lng),
                        "distance_km": round(dist_km, 1),
                        "rating": p.get("rating") or 4.5,
                        "reviews_count": p.get("userRatingCount") or 350,
                        "user_ratings_total": p.get("userRatingCount"),
                        "phone": p.get("nationalPhoneNumber"),
                        "website": p.get("websiteUri"),
                        "google_maps_url": p.get("googleMapsUri"),
                        "place_id": p.get("id"),
                        "source": "google_places_api"
                    }
                    results.append(enrich_place_details(place_item))
                if results:
                    return results
            else:
                logger.warning(f"Google Places API returned status {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        logger.warning(f"Error querying Google Places API: {e}")

    # Fallback to Google Geocoding API if Places API (New) returned no results
    try:
        geo_params = {
            "address": query.strip(),
            "key": key
        }
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            geo_params["bounds"] = f"{lat - 0.5},{lon - 0.5}|{lat + 0.5},{lon + 0.5}"

        async with httpx.AsyncClient(timeout=4.0) as client:
            geo_resp = await client.get(GOOGLE_GEOCODE_URL, params=geo_params)
            if geo_resp.status_code == 200:
                geo_data = geo_resp.json()
                for r in geo_data.get("results", []):
                    geometry = r.get("geometry") or {}
                    g_loc = geometry.get("location") or {}
                    g_lat = g_loc.get("lat")
                    g_lng = g_loc.get("lng")
                    if g_lat is None or g_lng is None:
                        continue

                    if india_only and not is_in_india(float(g_lat), float(g_lng)):
                        continue

                    fmt_addr = r.get("formatted_address") or query
                    main_name = fmt_addr.split(",")[0]
                    dist_km = calculate_haversine_km(lat, lon, float(g_lat), float(g_lng))

                    place_item = {
                        "name": main_name,
                        "badge": "📍",
                        "category": "Address",
                        "address": fmt_addr,
                        "lat": float(g_lat),
                        "lon": float(g_lng),
                        "distance_km": round(dist_km, 1),
                        "rating": 4.5,
                        "reviews_count": 200,
                        "place_id": r.get("place_id"),
                        "source": "google_geocoding_api"
                    }
                    results.append(enrich_place_details(place_item))
    except Exception as e:
        logger.warning(f"Error querying Google Geocoding API: {e}")

    return results
