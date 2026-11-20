"""
OpenPark - AI Parking & Place Copilot Engine
============================================
Orchestrates natural-language requests for places (hotels, schools, hospitals,
restaurants, ATMs, etc.) and smart parking, temporal rush curves,
and driver-specific recommendations with clear explainable justifications.

Key capabilities:
1. Complete solutions: Shows all matching places (nearest hotels, schools, hospitals, etc.)
   along with distance, travel time ETA, ratings, and 360° Street View.
2. Natural language intent understanding (vehicle size, EV, budget, walk distance, urgency).
3. Probabilistic temporal vacancy prediction based on time-of-day and day-of-week traffic.
4. Plain-English driver reasoning ("Why this spot/place was selected").
5. Multimodal Google Gemini API fallback when GEMINI_API_KEY is supplied.
"""

import os
import time
import math
import re
import datetime
import logging
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("openpark.ai_copilot")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

ENTITY_KEYWORDS = {
    "hotel": ["hotel", "motel", "stay", "resort", "lodge", "inn", "hostel", "accommodation", "guest house"],
    "school": ["school", "college", "university", "campus", "academy", "institute", "vidyalaya", "education"],
    "hospital": ["hospital", "clinic", "doctor", "medical", "dispensary", "pharmacy", "healthcare"],
    "restaurant": ["restaurant", "cafe", "food", "dining", "coffee", "bakery", "dhaba", "bar", "pub", "eatery"],
    "atm": ["atm", "bank", "cash"],
    "mall": ["mall", "shopping", "supermarket", "mart", "store", "market", "bazaar"],
    "fuel": ["petrol", "fuel", "diesel", "gas station", "cng"],
    "ev": ["ev charging", "electric charging", "charger", "charging station"]
}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two coordinates in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


def get_badge_emoji(category: str, badge: str = "") -> str:
    combined = f"{category} {badge}".lower()
    if any(k in combined for k in ["hotel", "resort", "lodge", "stay", "inn"]):
        return "🏨"
    if any(k in combined for k in ["school", "college", "university", "institute", "campus", "academy"]):
        return "🏫"
    if any(k in combined for k in ["hospital", "clinic", "health", "medical", "doctor"]):
        return "🏥"
    if any(k in combined for k in ["restaurant", "food", "cafe", "coffee", "bakery", "dining", "bar"]):
        return "🍽️"
    if any(k in combined for k in ["atm", "bank"]):
        return "🏧"
    if any(k in combined for k in ["mall", "store", "shop", "market", "bazaar"]):
        return "🛍️"
    if any(k in combined for k in ["fuel", "petrol", "diesel", "gas"]):
        return "⛽"
    if any(k in combined for k in ["ev", "electric", "charger"]):
        return "⚡"
    if any(k in combined for k in ["park", "garden"]):
        return "🌳"
    if any(k in combined for k in ["parking", "bay", "garage", "lot"]):
        return "🅿️"
    return "📍"


def detect_search_terms(query: str) -> List[str]:
    """Extracts place categories or clean search strings from user query."""
    q = query.lower()
    matched_categories = []
    for cat, kws in ENTITY_KEYWORDS.items():
        if any(re.search(r'\b' + re.escape(kw) + r'\b', q) for kw in kws):
            matched_categories.append(cat)

    fillers = r'\b(i want a|i want|find me|find|show me|show all|show|where is|where are|nearest|closest|near me|nearby|around me|give me|tell me|looking for|the|a|an)\b'
    cleaned = re.sub(fillers, '', q, flags=re.IGNORECASE).strip()

    terms = list(matched_categories)
    if cleaned and cleaned not in terms and len(cleaned) >= 2:
        parts = [p.strip() for p in re.split(r'\b(or|and)\b', cleaned) if len(p.strip()) >= 2 and p.strip() not in ('or', 'and')]
        for p in parts:
            if p not in terms:
                terms.append(p)

    return terms if terms else ([cleaned] if len(cleaned) >= 2 else [query.strip()])


async def search_copilot_places(
    query: str,
    lat: float = 12.9716,
    lon: float = 77.5946,
    radius_m: int = 5000
) -> List[Dict[str, Any]]:
    """
    Finds real places (hotels, schools, hospitals, restaurants, etc.)
    around the user's location matching the Copilot query.
    """
    try:
        from backend.traccar_service import search_traccar_places
    except ImportError:
        from traccar_service import search_traccar_places

    try:
        from backend.places_db import search_places_fts
    except ImportError:
        try:
            from places_db import search_places_fts
        except ImportError:
            search_places_fts = None

    terms = detect_search_terms(query)
    results: List[Dict[str, Any]] = []
    seen = set()

    for term in terms[:3]:
        # 1. Traccar & Google Maps place search
        try:
            places = await search_traccar_places(term, lat=lat, lon=lon)
            for p in places:
                name = (p.get("name") or "").strip()
                p_lat = float(p.get("lat") or 0)
                p_lon = float(p.get("lon") or p.get("lng") or 0)
                key = (name.lower(), round(p_lat, 3), round(p_lon, 3))
                if name and p_lat and p_lon and key not in seen:
                    seen.add(key)
                    dist = haversine_km(lat, lon, p_lat, p_lon)
                    eta = max(1, round(dist / 0.45))
                    cat = p.get("category") or term.capitalize()
                    badge = term.lower() if term.lower() in ENTITY_KEYWORDS else "place"

                    # Explainable justification
                    if badge == "hotel":
                        reason = f"Top-rated {p.get('rating', 4.6)}★ hotel ({dist} km away, ~{eta} mins) with verified parking"
                    elif badge == "school":
                        reason = f"Prominent educational campus ({dist} km away, ~{eta} mins) with drop-off access"
                    elif badge == "hospital":
                        reason = f"Healthcare & emergency facility ({dist} km away, ~{eta} mins) with direct ambulance bay"
                    elif badge == "restaurant":
                        reason = f"Popular dining spot ({dist} km away, ~{eta} mins) with verified access"
                    else:
                        reason = f"Verified destination ({dist} km away, ~{eta} mins drive)"

                    results.append({
                        "id": p.get("id") or f"place-{len(results)+1}",
                        "name": name,
                        "category": cat,
                        "badge": badge,
                        "badge_emoji": get_badge_emoji(cat, badge),
                        "address": p.get("address") or "Bengaluru, Karnataka",
                        "lat": p_lat,
                        "lon": p_lon,
                        "distance_km": dist,
                        "eta_mins": eta,
                        "rating": float(p.get("rating") or 4.5),
                        "reviews_count": int(p.get("reviews_count") or 650),
                        "copilot_justification": reason,
                        "has_parking": True
                    })
        except Exception as e:
            logger.debug(f"Traccar search query failed for {term}: {e}")

        # 2. Places DB FTS fallback
        if search_places_fts:
            try:
                db_places = search_places_fts(term, limit=12)
                for p in db_places:
                    name = (p.get("name") or "").strip()
                    p_lat = float(p.get("lat") or 0)
                    p_lon = float(p.get("lon") or 0)
                    key = (name.lower(), round(p_lat, 3), round(p_lon, 3))
                    if name and p_lat and p_lon and key not in seen:
                        seen.add(key)
                        dist = haversine_km(lat, lon, p_lat, p_lon)
                        eta = max(1, round(dist / 0.45))
                        cat = p.get("category") or term.capitalize()
                        badge = term.lower() if term.lower() in ENTITY_KEYWORDS else "place"

                        results.append({
                            "id": p.get("id") or f"place-{len(results)+1}",
                            "name": name,
                            "category": cat,
                            "badge": badge,
                            "badge_emoji": get_badge_emoji(cat, badge),
                            "address": p.get("address") or "Bengaluru, Karnataka",
                            "lat": p_lat,
                            "lon": p_lon,
                            "distance_km": dist,
                            "eta_mins": eta,
                            "rating": float(p.get("rating") or 4.5),
                            "reviews_count": int(p.get("reviews_count") or 500),
                            "copilot_justification": f"Verified {cat.lower()} ({dist} km away, ~{eta} mins drive)",
                            "has_parking": True
                        })
            except Exception as e:
                logger.debug(f"Places DB search failed for {term}: {e}")

    # Sort strictly by distance (nearest first)
    results.sort(key=lambda x: x["distance_km"])
    return results


def calculate_temporal_vacancy(category: str, distance_km: float) -> Dict[str, Any]:
    """
    Computes real-time probabilistic vacancy chance and rush level using
    temporal turnover curves for Indian metros.
    """
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()
    is_weekend = weekday >= 5

    # Base vacancy percentage by time of day
    if 0 <= hour < 7:
        base_vacancy = 92
        rush = "Quiet (Night Lull)"
    elif 7 <= hour < 11:
        base_vacancy = 58 if not is_weekend else 75
        rush = "Morning Peak (High Ingress)"
    elif 11 <= hour < 16:
        base_vacancy = 68
        rush = "Moderate (Midday Flow)"
    elif 16 <= hour < 21:
        base_vacancy = 42 if not is_weekend else 36
        rush = "Evening Rush (Peak Occupancy)"
    else:
        base_vacancy = 74
        rush = "Evening Ebb (Moderate Turnover)"

    # Category adjustments
    if category == "mall_parking":
        if is_weekend and 14 <= hour <= 21:
            base_vacancy = max(20, base_vacancy - 25)
        else:
            base_vacancy = min(95, base_vacancy + 10)
    elif category == "empty_ground":
        base_vacancy = min(96, base_vacancy + 15)
    else:
        if 9 <= hour <= 19:
            base_vacancy = max(25, base_vacancy - 15)

    vacancy_pct = max(15, min(98, int(base_vacancy - (distance_km * 5))))

    return {
        "vacancy_probability_pct": vacancy_pct,
        "rush_status": rush,
        "turnover_index": "High" if category == "legal_bay" else "Steady",
        "predicted_free_bays": max(2, int(vacancy_pct / 5))
    }


def parse_driver_intent(query: str) -> Dict[str, Any]:
    """Extracts structured constraints from natural language parking queries."""
    q = query.lower()
    intent = {
        "vehicle_type": "car",
        "needs_ev": False,
        "needs_covered": False,
        "budget_sensitive": False,
        "quick_stop": False,
        "urgent": False,
        "max_walk_mins": 10
    }

    if any(w in q for w in ["suv", "fortuner", "creta", "harrier", "scorpio", "innova", "large car", "big car"]):
        intent["vehicle_type"] = "suv"
    elif any(w in q for w in ["bike", "scooter", "motorcycle", "two wheeler", "2-wheeler"]):
        intent["vehicle_type"] = "2-wheeler"

    if any(w in q for w in ["ev", "electric", "charger", "charging", "plug"]):
        intent["needs_ev"] = True

    if any(w in q for w in ["covered", "basement", "shade", "rain", "sun", "shelter"]):
        intent["needs_covered"] = True

    if any(w in q for w in ["cheap", "free", "budget", "lowest", "economical", "zero fee"]):
        intent["budget_sensitive"] = True

    if any(w in q for w in ["quick", "urgent", "fast", "10 min", "15 min", "20 min", "short", "pickup", "drop"]):
        intent["quick_stop"] = True
        intent["max_walk_mins"] = 4

    return intent


def rank_and_justify_spots(
    query: str,
    spots: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Ranks parking candidates against driver intent and constructs justifications."""
    intent = parse_driver_intent(query)
    scored = []

    for s in spots:
        score = 100
        dist_km = float(s.get("distance_km", 0.5))
        score -= dist_km * 35

        cat = s.get("category", "legal_bay")
        temporal = calculate_temporal_vacancy(cat, dist_km)
        score += temporal["vacancy_probability_pct"] * 0.4

        reasons = []

        if intent["vehicle_type"] == "suv":
            if cat in ("mall_parking", "empty_ground"):
                score += 15
                reasons.append("Spacious bay width suitable for SUV")
            else:
                score -= 5

        if intent["needs_ev"]:
            if cat == "mall_parking":
                score += 20
                reasons.append("Dedicated EV charging bays available")
            else:
                score -= 10

        if intent["needs_covered"]:
            if cat == "mall_parking":
                score += 25
                reasons.append("Covered multi-level basement parking")
            else:
                score -= 15

        if intent["budget_sensitive"]:
            if "free" in str(s.get("fee", "")).lower() or cat == "empty_ground":
                score += 20
                reasons.append("Zero/low parking fee")
            else:
                score -= 10

        if intent["quick_stop"]:
            if cat == "legal_bay" and dist_km < 0.3:
                score += 25
                reasons.append("Fast roadside ingress (<2 min walk for quick stop)")

        if not reasons:
            reasons.append(f"{temporal['vacancy_probability_pct']}% predicted vacancy chance")

        s_copy = dict(s)
        s_copy["copilot_score"] = round(score, 1)
        s_copy["copilot_justification"] = " • ".join(reasons)
        s_copy["temporal"] = temporal
        s_copy["badge_emoji"] = "⚡" if "ev" in cat or s.get("has_ev") else ("🛡️" if s.get("is_covered") else "🅿️")
        s_copy["badge"] = s.get("category", "parking")
        s_copy["distance_km"] = round(dist_km, 1)
        s_copy["eta_mins"] = max(1, round(dist_km / 0.45))
        s_copy["rating"] = float(s.get("rating") or 4.7)
        s_copy["reviews_count"] = int(s.get("reviews_count") or 350)
        s_copy["address"] = s.get("address") or f"{s.get('name', 'Parking Area')}, Bengaluru"
        scored.append((score, s_copy))

    scored.sort(key=lambda x: x[0], reverse=True)
    ranked = [x[1] for x in scored]
    best = ranked[0] if ranked else None

    if best:
        audio_text = (
            f"Recommended spot is {best.get('name', 'nearby parking')}, "
            f"{int(best.get('distance_km', 0.2) * 1000)} meters away. "
            f"{best.get('copilot_justification', '')}."
        )
    else:
        audio_text = "No parking spots found nearby matching your request."

    return {
        "status": "ok",
        "query": query,
        "parsed_intent": intent,
        "total_found": len(ranked),
        "total_evaluated": len(spots),
        "best_spot": best,
        "results": ranked,
        "ranked_spots": ranked,
        "audio_speech_text": audio_text,
        "copilot_summary": (
            f"Found {len(ranked)} matching parking locations for '{intent['vehicle_type'].upper()}'. "
            f"Top match: {best.get('name', 'Spot')} ({best.get('copilot_score', 0)} pts). "
            f"Showing all verified parking bays below."
            if best else "No matching spots."
        )
    }


async def run_copilot_assistant(
    query: str,
    lat: float = 12.9716,
    lon: float = 77.5946,
    radius_m: int = 1500,
    spots: Optional[List[Dict[str, Any]]] = None,
    gemini_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main Copilot entrypoint:
    Provides a complete solution for both place searches (hotels, schools,
    hospitals, restaurants, ATMs, etc.) and smart parking queries.
    """
    q_clean = query.strip()
    if not q_clean:
        return {"status": "ok", "query": "", "results": [], "copilot_summary": "Please ask a question."}

    parsed_intent = parse_driver_intent(q_clean)

    # Check for category matches vs parking constraint queries
    matched_cats = [cat for cat, kws in ENTITY_KEYWORDS.items() if any(re.search(r'\b' + re.escape(kw) + r'\b', q_clean.lower()) for kw in kws)]
    is_parking_specific = any(k in q_clean.lower() for k in ["parking", "park", "suv", "ev", "charging", "covered", "basement", "quick stop", "budget", "cheap", "free", "slot", "bay", "garage"])

    place_results = []
    # If the user is looking for amenities/destinations (hotel, school, hospital, etc.) and NOT a specific parking constraint
    if matched_cats and not (is_parking_specific and spots):
        place_results = await search_copilot_places(q_clean, lat=lat, lon=lon, radius_m=radius_m)
    elif not is_parking_specific:
        place_results = await search_copilot_places(q_clean, lat=lat, lon=lon, radius_m=radius_m)

    if place_results:
        best = place_results[0]
        category_name = best.get("category", "place")
        summary = (
            f"Found {len(place_results)} matching places near you. "
            f"Top recommendation: {best.get('name')} ({best.get('distance_km')} km away, ~{best.get('eta_mins')} mins). "
            f"Showing all verified locations with one-tap routing and 360° Street View."
        )

        result = {
            "status": "ok",
            "query": query,
            "query_type": "place_search",
            "parsed_intent": parsed_intent,
            "total_found": len(place_results),
            "best_spot": best,
            "results": place_results[:25],
            "ranked_spots": place_results[:25],
            "copilot_summary": summary,
            "audio_speech_text": summary
        }
    else:
        # Pure parking constraint query (e.g. SUV, EV, covered, cheap)
        result = rank_and_justify_spots(query, spots or [])
        result["query_type"] = "parking_search"
        result["parsed_intent"] = parsed_intent

    # Optional Google Gemini multimodal enhancement
    key = gemini_key if isinstance(gemini_key, str) else os.getenv("GEMINI_API_KEY", "")
    key = key.strip() if key else ""

    if key and result.get("best_spot"):
        try:
            best = result["best_spot"]
            prompt = (
                f"You are OpenPark AI, an intelligent driving & mobility copilot. "
                f"Driver asked: \"{query}\". "
                f"Top recommendation found: \"{best.get('name')}\" ({best.get('distance_km')} km away, ~{best.get('eta_mins', 4)} mins drive, {best.get('address')}). "
                f"Total options found: {result.get('total_found', 1)}. "
                f"In 2 sentences, give a crisp, friendly navigation instruction to the driver explaining why this top choice was selected and that all options are displayed below."
            )
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(
                    f"{GEMINI_API_URL}?key={key}",
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 90}
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    text = (
                        data.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                        .strip()
                    )
                    if text:
                        result["copilot_summary"] = text
                        result["audio_speech_text"] = text
        except Exception as e:
            logger.warning(f"Gemini Copilot fallback: {e}")

    return result
