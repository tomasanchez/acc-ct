"""
Feedback Elements

In Control Theory, the feedback elemnts are the components that allow the system to adjust its behavior based on the
 output.
"""

import numpy as np

from acc.utils.constants import SPEEDOMETER_BIAS, SPEEDOMETER_STD, SPEEDOMETER_MAX_READING, SPEEDOMETER_MIN_READING


def speedometer(vo: float) -> float:
    """
    Simulate the speedometer sensor.

    Args:
        vo: the plant output, the speed of the vehicle in m/s

    Returns:
        f: the speedometer reading in m/s
    """

    # The speedometer sensor is not perfect.
    error = np.random.normal(SPEEDOMETER_BIAS, SPEEDOMETER_STD)
    factor = np.random.choice([1, -1])
    return np.clip(vo + factor * error, SPEEDOMETER_MIN_READING, SPEEDOMETER_MAX_READING)
