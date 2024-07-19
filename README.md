# Analysis and Simulation of Cruise Control Systems in Automotive Applications

Tomas A. Sanchez, July 2024.

Cruise Control (CC) is a system that automatically controls the speed of a motor vehicle. The system takes over the
throttle of the car to maintain a steady speed as set by the driver.

## Overview

The CC system is a feedback control system that uses a controller to maintain the desired speed.
The controller adjusts the throttle of the car based on the difference between the desired speed and the actual speed
of the car. The CC system is widely used in modern cars to improve fuel efficiency and reduce driver fatigue.

![Block Diagram of Cruise Control System](notebooks/assets/block-diagram.png)

Read more about the Design and Analysis of Cruise Control Systems in the [Notebook](./notebooks/acc.ipynb).

## How to run the simulation

**IMPORTANT**: The simulation requires `Python 3.10` or later. You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

You can run the simulation by executing the following command:

```bash
python src/acc/main.py
```

You will be prompted to enter multiple values for the simulation. You can use the default values by pressing `Enter`.

Or you can run the simulation with the default values by executing the following command:

```bash
python src/acc/main.py --default
```

After the simulation is complete, a [`output/results.png`](./output/results.png) will be saved containing error, speed,
and throttle plots over time. Results are also provided as a `CSV` file in [`output/results.csv`](./output/results.csv).

## Project Structure

The project is structured as follows:

```
.
├── notebooks
│   └── acc.ipynb
├── output
│   ├── results.csv
│   └── results.png
└── src
    └── acc
        ├── simulation
        ├── model
        │   ├── control.py
        │   ├── feedback.py
        │   └── process.py
        └── cli.py
```

- `notebooks/`: Contains Jupyter notebooks for the analysis of the CC system.
- `output/`: Contains the simulation results in `CSV` and `PNG` formats.
- `src/acc/`: Source code for the CC system.
    - `simulation/`: Δt simulation logic.
    - `model/`: contains each control system component.
        - `control.py`: PID controller.
        - `feedback.py`: Feedback element (Speedometer).
        - `process.py`: Plant.
    - `cli.py`: Command-line interface for running the simulation.

## License

This project is licensed under the terms of the MIT license unless otherwise specified. See [`LICENSE`](LICENSE) for
more details or visit https://mit-license.org/.

## Acknowledgements

This project was designed and developed
by [Tomás Sánchez](https://tomsanchez.com.ar/about/) <[info@tomsanchez.com.ar](mailto:info@tomsanchez.com.ar)>.

If you find this project useful, please consider supporting its development by sponsoring it.

Special thanks to the [Python Control Systems Library](https://python-control.readthedocs.io/en/latest/cruise.html) for
providing knowledge and physics models for the simulation.
