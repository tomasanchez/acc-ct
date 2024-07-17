"""
Control Elements

In Control Theory, the control elements are the components that allow the system to adjust its behavior based on the
input and feedback.
"""
import dataclasses

import numpy as np


@dataclasses.dataclass
class EngineControlUnit:
    """
    Engine Control Unit (ECU). Simplified as a Proportional-Integral-Derivative Controller

    Attributes:
        kp: proportional gain
        ki: integral gain
        kd: derivative gain
    """
    kp: float
    ki: float = 0.0
    kd: float = 0.0
    windup_protection: bool = False

    _integral: float = 0
    _previous_error: float = 0

    def etc(self, error: float, dt: float):
        """
        The Electronic Throttle Control (ETC) processes the error signal and returns a control signal.

        Args:
            error: the error signal
            dt: time step

        Returns:
            A value between [-1, 1] control signal
        """
        derivative = (error - self._previous_error) / dt

        # u(t) = Kp * e(t) + Ki * ∫e(t)dt + Kd * de(t)/dt
        output = self.kp * error + self.ki * self._integral + self.kd * derivative
        output = np.clip(output, -1, 1)

        if self.windup_protection:
            if not (output == -1 and error < 0) and not (output == 1 and error > 0):
                self._integral += error * dt
        else:
            self._integral += error * dt

        self._previous_error = error

        return output
