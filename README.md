# Physics Simulation: Rolling and Sliding down an Inclined Plane

This project is an interactive physics simulation based on the paper **"Rolling and Sliding down an Inclined Plane" by Rod Cross (The Physics Teacher, 2023)**.

The simulation models the motion of a ball (rolling and sliding) as it moves down an incline, with a specific focus on the **offset distance ($D$)** of the normal reaction force and its impact on linear and angular accelerations.

## 🚀 Key Features

- **Interactive 3D Dashboard**: Built with VPython, allowing users to observe the ball's motion in a 3D environment with full camera controls (rotate/zoom).
- **Real-time Parameter Tuning**: Interactive sliders to adjust the incline angle ($\theta$), kinetic friction coefficient ($\mu_k$), and the normal force offset ratio ($D/R$) on the fly.
- **Live Graphing**: Real-time plots of linear velocity ($v$), angular velocity ($R\omega$), and the ratio ($v/R\omega$) to analyze the transition between sliding and pure rolling.
- **Automated Validation**: Includes a validation script to compare simulation results with the experimental data (Table I) provided in the original paper.

## 📚 Physics Background

The simulation strictly follows the mathematical model described in the paper:

- **Rolling Acceleration**: $a = \frac{5}{7}g(\sin\theta - \frac{D}{R}\cos\theta)$
- **Sliding Acceleration**: $a = g(\sin\theta - \mu_k\cos\theta)$
- **Angular Acceleration**: $\frac{d\omega}{dt} = \frac{5}{2}(\mu_k - \frac{D}{R})\frac{g\cos\theta}{R}$

Notably, the simulation captures the **backward spin phenomenon** that occurs when $\mu_k < D/R$, where the ball rotates backwards while sliding down the incline.

## 🛠 Installation & Usage

### Prerequisites
Python 3.13+ is required. Install the necessary libraries using pip:
```bash
pip install vpython numpy matplotlib
```

### Running the Simulation
Launch the interactive 3D dashboard:
```bash
python simulation.py
```

### Running the Validation
Verify the physics engine against the paper's experimental data:
```bash
python verify_results.py
```

## ✅ Validation Results
The `verify_results.py` script confirms high accuracy compared to the paper's Table I data:
- **Linear Acceleration ($a$)**: Error < 0.5%
- **Angular Acceleration ($\alpha$)**: Error < 5.0%

## 📄 License and Reference
This project is for educational and research purposes. For detailed theoretical background, please refer to the included paper: `4. Rolling and Sliding down an Inclined Plane.pdf`.
