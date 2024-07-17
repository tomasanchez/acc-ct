"""
Model representing the Vehicle Dynamics.

In Control Theory, it represents the "Plant" of the system.
"""
import random
from math import sin, copysign, radians

from pydantic import BaseModel

from acc.utils.constants import g, air_density, p_sua

# Since we are using the math module, we can use the sin function directly
sign = lambda x: copysign(1, x)


class Vehicle(BaseModel):
    """
    Vehicle Dynamics Model

    Attributes:
        position: current position of the vehicle (m)
        speed: current speed of the vehicle (m/s)
        mass: mass of the vehicle (Kg)
        drag_coefficient: drag coefficient (dimensionless)
        frontal_area: frontal area of the vehicle (m^2)
        torque_max: maximum torque of the motor (Nm)
        omega_max: maximum angular velocity of the motor (rad/s)
        gear_speed_ranges: speed ranges for each gear (km/h)
        gear_ratio: gear ratios (dimensionless)
        wheel_radius: radius of the wheel (m)
        gear: current gear of the vehicle (dimensionless)
    """
    position: float = 0  # m
    speed: float = 0  # m/s
    mass: float  # Kg
    drag_coefficient: float  # dimensionless
    frontal_area: float  # m^2
    torque_max: float  # Nm
    omega_max: float  # rad/s
    gear_speed_ranges: list[tuple[float, float]]  # km/h
    gear_ratio: list[float] = [5.25, 3.03, 1.95, 1.46, 1.22, 1.0, 0.81, 0.67]  # dimensionless
    wheel_radius: float = 0.3355  # m
    gear: int = 1  # dimensionless


def process(vehicle: Vehicle, throttle: float, dt: float, theta: float = 0.0, mu: float = 0.01) -> float:
    """
    Simulate vehicle dynamics updating its position and speed.

    Args:
        vehicle: a dynamic model
        throttle: percentage of throttle input
        dt: time step
        theta: inclination angle of the road
        mu: coefficient of rolling friction

    Returns:
        Vo, the new speed of the vehicle in m/s
    """
    m = vehicle.mass  # Kg
    v = vehicle.speed  # m/s
    area = vehicle.frontal_area  # m^2
    alpha = vehicle.gear_ratio[vehicle.gear - 1] / vehicle.wheel_radius  # m^-1

    # Force generated by the throttle input
    omega = v * alpha  # s^-1
    f = alpha * motor_torque(vehicle, omega) * throttle  # N

    # force Fg = m g sin \theta.
    fg = m * g * sin(radians(theta))

    # A simple model of rolling friction is Fr = m g Cr sgn(v), where Cr is
    # the coefficient of rolling friction and sgn(v) is the sign of v (±1) or
    # zero if v = 0.
    fr = m * g * mu * sign(v)

    # from: Fa = 1/2 * Cd * A * rho * |v| * v
    fa = 0.5 * vehicle.drag_coefficient * area * air_density * abs(v) * v

    # Total disturbance force
    fd = fg + fr + fa

    # from: a = F/m
    a = (f - fd) / m

    # Sudden Unintended Acceleration (SUA) disturbance
    sua = sudden_unintended_acceleration(a)
    a += sua

    # Update vehicle position and speed
    # v = v0 + a * t
    vo = v + a * dt
    vehicle.position += v * dt
    vehicle.speed = vo

    return vo


def motor_torque(vehicle: Vehicle, omega: float) -> float:
    """
    Calculate the motor torque based on the current angular velocity.

    Args:
        vehicle: a dynamic model
        omega: current angular velocity of the motor (rad/s)

    Returns:
        the torque generated by the motor in Nm
    """
    tm = vehicle.torque_max
    omega_m = vehicle.omega_max
    beta = 0.4

    # Tm * (1 - beta * (ω / ωm - 1)^2)
    return max(tm * (1 - beta * (omega / omega_m - 1) ** 2), 0)


def sudden_unintended_acceleration(a: float) -> float:
    """
    Simulates an unintended increment in acceleration.

    Args:
        a: acceleration in m/s^2

    Returns:
        Either an increase of 25% to 45% using a uniform distribution. Or 0.
    """
    r = random.uniform(0, 1)
    increment = random.uniform(0.25, 0.45)

    return a * increment if r <= p_sua else 0


def tcu(vehicle: Vehicle, v: float) -> int:
    """
    Simulates the Transmission Control Unit (TCU) of the vehicle.

    Args:
        vehicle: a dynamic model
        v: current speed of the vehicle in m/s

    Returns:
        The next gear of the vehicle
    """

    # Convert the speed ranges from km/h to m/s
    ranges = [(low / 3.6, high / 3.6) for low, high in vehicle.gear_speed_ranges]

    # Check if the speed is within the range of the current gear
    if ranges[vehicle.gear - 1][0] < v < ranges[vehicle.gear - 1][1]:
        return vehicle.gear

    # Check if the speed is within the range of the next gear
    if vehicle.gear < len(ranges) and v > ranges[vehicle.gear][0]:
        return vehicle.gear + 1

    # Check if the speed is within the range of the previous gear
    if vehicle.gear > 1 and v < ranges[vehicle.gear - 2][1]:
        return vehicle.gear - 1

    return vehicle.gear