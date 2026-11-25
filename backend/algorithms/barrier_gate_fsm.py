"""Parking garage barrier gate finite state machine."""

class BarrierGateState:
    CLOSED = "CLOSED"
    OPENING = "OPENING"
    OPEN = "OPEN"
    CLOSING = "CLOSING"
    FAULT = "FAULT"

class BarrierGateFSM:
    def __init__(self):
        self.state = BarrierGateState.CLOSED

    def on_vehicle_approached(self):
        if self.state in (BarrierGateState.CLOSED, BarrierGateState.CLOSING):
            self.state = BarrierGateState.OPENING
            return True
        return False

    def on_fully_opened(self):
        if self.state == BarrierGateState.OPENING:
            self.state = BarrierGateState.OPEN

    def on_vehicle_passed(self):
        if self.state == BarrierGateState.OPEN:
            self.state = BarrierGateState.CLOSING
            return True
        return False

    def on_fully_closed(self):
        if self.state == BarrierGateState.CLOSING:
            self.state = BarrierGateState.CLOSED
