"""Multi-zone sensor health watchdog."""

def evaluate_sensor_health(last_heartbeat_s_ago: float, threshold_s: float = 60.0) -> str:
    if last_heartbeat_s_ago < threshold_s:
        return "HEALTHY"
    elif last_heartbeat_s_ago < threshold_s * 3.0:
        return "DEGRADED"
    else:
        return "OFFLINE"
