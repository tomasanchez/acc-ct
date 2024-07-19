# Analysis and Simulation of Cruise Control Systems in Automotive Applications

Tomas A. Sanchez, July 2024.

Cruise Control (CC) is a system that automatically controls the speed of a motor vehicle. The system takes over the
throttle of the car to maintain a steady speed as set by the driver.

## Overview

The CC system is a feedback control system that uses a controller to maintain the desired speed.
The controller adjusts the throttle of the car based on the difference between the desired speed and the actual speed
of the car. The CC system is widely used in modern cars to improve fuel efficiency and reduce driver fatigue.

![Block Diagram of Cruise Control System](notebooks/assets/block-diagram.png)

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

After the simulation is complete, a [`output/results.png`](./output/results.png) will be saved containing error, speed,
and throttle plots over time. Results are also provided as a `CSV` file in [`output/results.csv`](./output/results.csv).
