from sklearn.linear_model import LinearRegression

from xh_cpu_usage_simulator.MovingAvg import MovingAvg
import numpy as np


class LinearRegressionPredication:
    def __init__(self, size: int):
        self.x_mv = MovingAvg(size)
        self.y_mv = MovingAvg(size)
        self.model = LinearRegression()
        self.predication = None

    def insert(self, x: float, y: float):
        self.x_mv.insert(x)
        self.y_mv.insert(y)

        if not self.is_ready():
            return

        y = np.array(self.y_mv.data)
        x = np.array(self.x_mv.data).reshape((-1, 1))
        self.model.fit(x, y)

    def is_ready(self):
        return len(self.x_mv.data) >= 3

    def predict(self, target: float):
        return self.model.predict(np.asarray([target]).reshape((-1, 1)))[0]
