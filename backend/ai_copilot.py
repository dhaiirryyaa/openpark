"""
OpenPark - AI Parking Copilot & Predictive Vacancy Engine
=========================================================
Orchestrates natural-language parking requests, temporal rush curves,
and driver-specific recommendations with clear explainable justifications.

Key capabilities:
1. Natural language intent understanding (vehicle size, EV, budget, walk distance, urgency).
2. Probabilistic temporal vacancy prediction based on time-of-day and day-of-week traffic.
3. Plain-English driver reasoning ("Why this spot was selected").
4. Audio speech synthesis text for hands-free driving assistance.
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


def calculate_temporal_vacancy(category: str, distance_km: float) -> Dict[str, Any]:
    """
    Computes real-time probabilistic vacancy chance and rush level using
    temporal turnover curves for Indian metros.
    """
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0=Monday, 6=Sunday
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
    else:  # 21-24
        base_vacancy = 74
        rush = "Evening Ebb (Moderate Turnover)"

    # Category adjustments
    if category == "mall_parking":
        # Malls are busier on weekends and evenings
        if is_weekend and 14 <= hour <= 21:
            base_vacancy = max(20, base_vacancy - 25)
        else:
            base_vacancy = min(95, base_vacancy + 10)
    elif category == "empty_ground":
        # Grounds have high availability
        base_vacancy = min(96, base_vacancy + 15)
    else:  # roadside bays
        # Roadside bays turn over quickly
        if 9 <= hour <= 19:
            base_vacancy = max(25, base_vacancy - 15)

    # Slight distance penalty for farther spots (closer spots are preferred)
    vacancy_pct = max(15, min(98, int(base_vacancy - (distance_km * 5))))

    return {
        "vacancy_probability_pct": vacancy_pct,
        "rush_status": rush,
        "turnover_index": "High" if category == "legal_bay" else "Steady",
        "predicted_free_bays": max(2, int(vacancy_pct / 5))
    }


def parse_driver_intent(query: str) -> Dict[str, Any]:
    """
    Extracts structured constraints from natural language queries.
    """
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
    """
    Ranks candidates against driver intent and constructs plain-English justifications.
    """
    intent = parse_driver_intent(query)
    scored = []

    for s in spots:
        score = 100
        dist_km = float(s.get("distance_km", 0.5))
        score -= dist_km * 35  # distance is high priority

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
        scored.append((score, s_copy))

    scored.sort(key=lambda x: x[0], reverse=True)
    ranked = [x[1] for x in scored]
    best = ranked[0] if ranked else None

    # Audio synthesis text
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
        "total_evaluated": len(spots),
        "best_spot": best,
        "ranked_spots": ranked,
        "audio_speech_text": audio_text,
        "copilot_summary": (
            f"Evaluated {len(spots)} spots for '{intent['vehicle_type'].upper()}'. "
            f"Top match: {best.get('name', 'Spot')} ({best.get('copilot_score', 0)} pts)."
            if best else "No matching spots."
        )
    }


async def run_copilot_assistant(
    query: str,
    spots: List[Dict[str, Any]],
    gemini_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main Copilot entrypoint: analyzes driver query, ranks spots, and
    enriches with Gemini natural language response when available.
    """
    result = rank_and_justify_spots(query, spots)
    key = gemini_key if isinstance(gemini_key, str) else os.getenv("GEMINI_API_KEY", "")
    key = key.strip() if key else ""

    if not key or not result.get("best_spot"):
        return result

    # Augment with Gemini if key is provided
    try:
        best = result["best_spot"]
        prompt = (
            f"You are OpenPark AI, an intelligent in-car driving parking copilot. "
            f"Driver asked: \"{query}\". "
            f"Best spot chosen: \"{best.get('name')}\" ({best.get('distance_km')}km away, "
            f"{best.get('temporal', {}).get('vacancy_probability_pct')}% vacancy chance, fee: {best.get('fee')}). "
            f"In 2 sentences, give a crisp, friendly navigation instruction to the driver explaining why this spot was picked."
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
