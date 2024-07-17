from matplotlib import pyplot as plt

from acc.simulation import SimulationResult


def plot_results(results: SimulationResult,
                 include_speedometer: bool = False,
                 step_speed: float = 0.0):
    """Plot the results of the simulation."""
    time_label = 'Time (s)'

    plt.clf()
    plt.close()
    plt.figure(figsize=(25, 20))
    plt.subplot(4, 1, 1)

    # Plot the actual speed of the vehicle
    plt.plot(results.times, results.speeds, label='Actual Speed')
    if include_speedometer:
        plt.plot(results.times, results.speedometer, label='Speedometer Reading', linestyle='dashed')
    plt.axhline(y=step_speed + 4, color='greenyellow', linestyle='dotted', label='Speed Upper Limit')
    plt.axhline(y=step_speed, color='darkolivegreen', linestyle='--', label='Step Speed')
    plt.axhline(y=step_speed - 4, color='greenyellow', linestyle='dotted', label='Speed Lower Limit')
    plt.xlabel(time_label)
    plt.ylabel('Speed (km/h)')
    plt.title('Vehicle Speed Over Time')
    plt.legend()

    # Plot the error
    plt.subplot(4, 1, 2)
    plt.plot(results.times, results.errors, label='Error')
    plt.xlabel('Time (s)')
    plt.ylabel('Error (km/h)')
    plt.title('Error Over Time')
    plt.legend()

    # Plot the road inclination 
    plt.subplot(4, 1, 3)
    plt.plot(results.times, results.inclinations, label='Inclination')
    plt.xlabel(time_label)
    plt.ylabel('Inclination (degrees)')
    plt.title('Road Inclination Over Time')
    plt.legend()

    # Plot the throttle input
    plt.subplot(4, 1, 4)
    plt.plot(results.times, results.throttle, label='Throttle')
    plt.xlabel(time_label)
    plt.ylabel('Throttle (percentage)')
    plt.title('Throttle Change Over Time')
    plt.legend()
