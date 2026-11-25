"""Smart EV charging slot scheduling allocator."""

def allocate_ev_slot(battery_capacity_kwh: float, current_soc_pct: float, target_soc_pct: float, charger_kw: float = 22.0) -> dict:
    needed_kwh = max(0.0, (target_soc_pct - current_soc_pct) / 100.0 * battery_capacity_kwh)
    charge_hours = needed_kwh / max(1.0, charger_kw)
    return {
        "needed_kwh": round(needed_kwh, 2),
        "charge_minutes": int(round(charge_hours * 60)),
        "charger_kw": charger_kw,
        "can_complete": target_soc_pct > current_soc_pct
    }
