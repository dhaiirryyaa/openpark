from backend.algorithms.revenue_aggregator import aggregate_revenue

def test_revenue_aggregator():
    txs = [
        {'amount': 118.0, 'gst': 18.0, 'is_ev': False},
        {'amount': 236.0, 'gst': 36.0, 'is_ev': True}
    ]
    res = aggregate_revenue(txs)
    assert res['total_revenue'] == 354.0
    assert res['net_revenue'] == 300.0
    assert res['ev_charging_revenue'] == 236.0
