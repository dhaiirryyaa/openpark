from backend.algorithms.maneuver_generator import generate_maneuver

def test_maneuver_generator():
    assert generate_maneuver(0.0, 5.0) == 'Continue straight'
    assert generate_maneuver(0.0, 90.0) == 'Turn right'
    assert generate_maneuver(90.0, 0.0) == 'Turn left'
