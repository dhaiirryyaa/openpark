def classify_turn_maneuver(initial_bearing: float, final_bearing: float) -> str:
    diff = (final_bearing - initial_bearing + 360.0) % 360.0
    if diff > 180.0:
        diff -= 360.0
        
    if -20.0 <= diff <= 20.0:
        return "straight"
    elif 20.0 < diff <= 65.0:
        return "slight_right"
    elif 65.0 < diff <= 120.0:
        return "turn_right"
    elif diff > 120.0:
        return "sharp_right"
    elif -65.0 <= diff < -20.0:
        return "slight_left"
    elif -120.0 <= diff < -65.0:
        return "turn_left"
    else:
        return "sharp_left"
