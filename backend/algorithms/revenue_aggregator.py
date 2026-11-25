"""Parking revenue analytics time-series aggregator."""

def aggregate_revenue(transactions: list) -> dict:
    total = sum(t.get('amount', 0.0) for t in transactions)
    gst = sum(t.get('gst', 0.0) for t in transactions)
    ev_rev = sum(t.get('amount', 0.0) for t in transactions if t.get('is_ev'))
    return {
        "total_revenue": round(total, 2),
        "total_gst": round(gst, 2),
        "net_revenue": round(total - gst, 2),
        "ev_charging_revenue": round(ev_rev, 2),
        "count": len(transactions)
    }
