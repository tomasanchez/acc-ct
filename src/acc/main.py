from acc.model.control import EngineControlUnit
from acc.model.process import Vehicle
from acc.simulation import run_simulation, SimulationResult
from acc.utils.plot import plot_results


def main_simulation(kp: float = 0.5,
                    ki: float = 0.2,
                    kd: float = 1.0,
                    windup_protection: bool = False,
                    ) -> SimulationResult:
    camry_xse_2025 = Vehicle(mass=1_604,
                             drag_coefficient=0.28,
                             frontal_area=1.94,
                             torque_max=221,
                             omega_max=545.3,
                             gear_speed_ranges=[(0, 10), (10, 30), (30, 50), (50, 70), (70, 100), (100, 130),
                                                (130, 160),
                                                (160, 200)])

    ecu = EngineControlUnit(kp=kp, ki=ki, kd=kd, windup_protection=windup_protection)
    return run_simulation(vehicle=camry_xse_2025, vi=30, control=ecu, road_inclinations=[], initial_speed=0)


if __name__ == "__main__":
    results = main_simulation()
    plot_results(results, step_speed=30 * 3.6)
