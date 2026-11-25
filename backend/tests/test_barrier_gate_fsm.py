from backend.algorithms.barrier_gate_fsm import BarrierGateFSM, BarrierGateState

def test_barrier_gate_fsm():
    fsm = BarrierGateFSM()
    assert fsm.state == BarrierGateState.CLOSED
    fsm.on_vehicle_approached()
    assert fsm.state == BarrierGateState.OPENING
    fsm.on_fully_opened()
    assert fsm.state == BarrierGateState.OPEN
    fsm.on_vehicle_passed()
    assert fsm.state == BarrierGateState.CLOSING
    fsm.on_fully_closed()
    assert fsm.state == BarrierGateState.CLOSED
