import time

import typer
from rich import print
from rich.progress import track

from acc.model.control import EngineControlUnit
from acc.model.process import Vehicle
from acc.simulation import run_simulation, SimulationResult
from acc.utils.constants import CONSOLE_BANNER
from acc.utils.plot import plot_results
from acc.utils.rv import RoadInclinationGenerator


def main_simulation(kp: float = 0.5,
                    ki: float = 0.2,
                    kd: float = 1.0,
                    windup_protection: bool = False,
                    vi: float = 30.0,
                    road_inclinations: bool = False
                    ) -> SimulationResult:
    print("\n[cyan]Running simulation with the following parameters[/cyan]:")
    print(f"  - Kp: {kp}")
    print(f"  - Ki: {ki}")
    print(f"  - Kd: {kd}")
    print(f"  - Step Speed: {round(vi, 2)} m/s ({vi * 3.6} km/h)")
    print(f"  - Windup Protection: {windup_protection}")
    print(f"  - Road Inclinations: {road_inclinations}")

    camry_xse_2025 = Vehicle(mass=1_604,
                             drag_coefficient=0.28,
                             frontal_area=1.94,
                             torque_max=221,
                             omega_max=545.3,
                             gear_speed_ranges=[(0, 10), (10, 30), (30, 50), (50, 70), (70, 100), (100, 130),
                                                (130, 160),
                                                (160, 200)])
    print("\nDynamic Model:")
    print(camry_xse_2025)

    ecu = EngineControlUnit(kp=kp, ki=ki, kd=kd, windup_protection=windup_protection)
    return run_simulation(vehicle=camry_xse_2025,
                          vi=vi,
                          control=ecu,
                          inclination_generator=RoadInclinationGenerator() if road_inclinations else None,
                          initial_speed=0)


def main():
    print(CONSOLE_BANNER)
    print("Cruise Control System Simulation")
    print("By Tomas A. Sanchez")
    print(CONSOLE_BANNER)

    print("\nThis simulation models the behavior of a vehicle equipped with a cruise control system.")
    print("Simulation is using [bold yellow]TOYOTA CAMRY XSE 2025[/bold yellow] specs.\n")
    vi: float = typer.prompt("Set step speed (km/h)", default=108)

    print("\n[blue]PID Controller Parameters[/blue]:")
    kp: float = typer.prompt("Enter the proportional gain", default=0.5)
    ki: float = typer.prompt("Enter the integral gain", default=0.25)
    kd: float = typer.prompt("Enter the derivative gain", default=1.0)
    use_windup: bool = typer.confirm("Use Integral Windup?", default=False)

    print("\n[blue]Disturbance Options[/blue]:")
    generate_road_inclinations: bool = typer.confirm("Generate Road Inclinations?", default=False)

    result = main_simulation(vi=vi / 3.6,
                             kp=kp, ki=ki, kd=kd, windup_protection=use_windup,
                             road_inclinations=generate_road_inclinations)

    for value in track(range(100), description="Simulating..."):
        time.sleep(0.5 if value >= 90 else 0.01)

    print("\n[magenta]Variables over time[/magenta]:")
    print(result.df().describe())
    print(CONSOLE_BANNER)
    plot_results(result, step_speed=vi, save=True)
    print("Simulation Results plotted: check the 'output' folder for the plots.")
    print("[bold green]Simulation finished successfully[/bold green]")
    print(CONSOLE_BANNER)


if __name__ == "__main__":
    typer.run(main)
