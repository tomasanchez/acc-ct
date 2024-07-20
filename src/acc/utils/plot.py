import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from rich import print
from rich.table import Table

from acc.simulation import SimulationResult


def plot_results(results: SimulationResult,
                 include_speedometer: bool = False,
                 step_speed: float = 0.0,
                 save: bool = False):
    """Plot the results of the simulation."""
    time_label = 'Time (s)'

    plt.clf()
    plt.close()
    plt.figure(figsize=(25, 20))

    plots = 4 if len(results.inclinations) > 0 else 3
    plt.subplot(plots, 1, 1)

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
    plt.subplot(plots, 1, 2)
    plt.plot(results.times, results.errors, label='Error')
    plt.xlabel('Time (s)')
    plt.ylabel('Error (km/h)')
    plt.title('Error Over Time')
    plt.legend()

    # Plot the road inclination
    if results.inclinations:
        plt.subplot(plots, 1, plots - 1)
        plt.plot(results.times, results.inclinations, label='Inclination')
        plt.xlabel(time_label)
        plt.ylabel('Inclination (degrees)')
        plt.title('Road Inclination Over Time')
        plt.legend()

    # Plot the throttle input
    plt.subplot(plots, 1, plots)
    plt.plot(results.times, results.throttle, label='Throttle')
    plt.xlabel(time_label)
    plt.ylabel('Throttle (percentage)')
    plt.title('Throttle Change Over Time')
    plt.legend()

    if save:
        root_folder = Path(__file__).resolve().parents[3]
        output_directory = Path(root_folder, 'output')

        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        output_folder = Path(output_directory, 'results.png')

        print(f"Plotting in [blue bold]{output_folder}[/blue bold]")
        plt.savefig(output_folder)

        csv_output = Path(output_directory, 'results.csv')
        print(f"Saving series in [blue bold]{csv_output}[/blue bold]")
        results.df().to_csv(csv_output)


def to_rich_table(
        pandas_dataframe: pd.DataFrame,
        rich_table: Table,
        show_index: bool = True,
        index_name: str | None = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.

    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.

    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values.
    """

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table
