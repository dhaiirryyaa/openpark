from backend.algorithms.lot_ranker import score_parking_lot

def test_lot_ranker():
    s1 = score_parking_lot(500, 40, 20, True)
    s2 = score_parking_lot(4500, 2, 80, False)
    assert s1 > s2
