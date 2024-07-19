"""
Simulation module for the CC system.
"""
import pandas as pd
from pydantic import BaseModel

from acc.model.control import EngineControlUnit
from acc.model.feedback import speedometer
from acc.model.process import Vehicle, process, tcu
from acc.utils.rv import RoadInclinationGenerator


class SimulationResult(BaseModel):
    """
    Simulation Result

    Attributes:
        times: time vector
        errors: error vector
        speeds: speed vector
    """
    times: list[float] = []
    errors: list[float] = []
    speeds: list[float] = []
    inclinations: list[float] = []
    gears: list[int] = []
    throttle: list[float] = []
    speedometer: list[float] = []

    def df(self) -> pd.DataFrame:
        """
        Convert the simulation result to a pandas DataFrame.

        Returns:
            DataFrame: the simulation result as a DataFrame
        """
        return pd.DataFrame({
            'Error': self.errors,
            'Speed': self.speeds,
            'Throttle': self.throttle,
            'Speedometer': self.speedometer,
        })


def run_simulation(vehicle: Vehicle,
                   vi: float,
                   control: EngineControlUnit,
                   initial_speed: float = 0.0,
                   total_time: float = 3_600.0,
                   dt: float = 1.0,
                   inclination_generator: RoadInclinationGenerator | None = None,
                   ) -> SimulationResult:
    """
    Run the simulation of the CC system

    Args:
        vehicle: a dynamic model
        vi: step input speed
        control: ECU controller
        initial_speed: initial speed of the vehicle
        total_time: total simulation time
        dt: time step
        inclination_generator: road inclination generator
        
    Returns:
        Time series of the simulation
    """
    subject = vehicle.model_copy(update={'speed': initial_speed, 'position': 0})

    result = SimulationResult()

    for t in range(int(total_time)):
        # [Vo] - Output: plant velocity
        vo = subject.speed

        # [f(t)] - Feedback Element: Speedometer reading signal (f)
        f = speedometer(vo)

        # [e(t)] - Summing Point: Error signal
        error = vi - f

        # u(t) - Control Element: ECU control signal obtained from ETC actuator.
        u = control.etc(error, dt)

        # gear shifting
        subject.gear = tcu(subject, f)

        theta = inclination_generator.next_inclination(t) if inclination_generator else 0

        # vo(t) - Process: Vehicle Dynamics
        vo = process(subject, throttle=u, dt=dt, theta=theta)

        # save series
        result.times.append(t)
        result.errors.append(error * 3.6)
        result.speeds.append(vo * 3.6)
        result.gears.append(subject.gear)
        result.throttle.append(u)
        result.speedometer.append(f * 3.6)
        result.inclinations.append(theta)

    return result
