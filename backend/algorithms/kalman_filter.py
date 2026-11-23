class KalmanFilter1D:
    def __init__(self, process_variance: float = 1e-5, measurement_variance: float = 1e-3):
        self.q = process_variance
        self.r = measurement_variance
        self.x = 0.0  # estimate
        self.p = 1.0  # error covariance
        self.initialized = False

    def update(self, measurement: float) -> float:
        if not self.initialized:
            self.x = measurement
            self.initialized = True
            return self.x
            
        # Prediction
        self.p = self.p + self.q
        # Measurement update
        k = self.p / (self.p + self.r)
        self.x = self.x + k * (measurement - self.x)
        self.p = (1.0 - k) * self.p
        return self.x
