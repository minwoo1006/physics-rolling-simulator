# Rolling and Sliding down an Inclined Plane: Simulation & Verification

This project implements a Python-based simulation to reproduce and verify the experimental findings from the paper **"Rolling and Sliding down an Inclined Plane"**. It focuses on the motion of a ball on an incline, accounting for both sliding and rolling behaviors.

## 1. Introduction
While standard physics textbooks often assume that the normal force acts through the center of a rolling object, real-world conditions involve a small offset distance (D) due to surface deformation or friction. This project simulates how this offset D affects the ball's linear acceleration and angular velocity.

## 2. Physical Model

### Key Equations
Let R be the radius, M the mass, theta the incline angle, and mu the friction coefficient.

1.  **Sliding State (v > R * omega)**:
    - Linear Acceleration: a = g * (sin(theta) - mu_k * cos(theta))
    - Angular Acceleration: alpha = (5/2) * (mu_k - D/R) * g * cos(theta) / R

2.  **Rolling State (v = R * omega)**:
    - Linear Acceleration: a = (5/7) * g * (sin(theta) - (D/R) * cos(theta))
    - Angular Acceleration: alpha = a / R

### Transition Condition
Sliding occurs if the required friction ratio exceeds the static friction coefficient (mu_s):
- Condition: (2/7) * tan(theta) + (5/7) * (D/R) > mu_s

## 3. Implementation Details
- **Language**: Python 3.13+
- **Physics Engine**: Numerical calculation using the derived physics formulas within a time-stepping loop.
- **Visualization**: 3D simulation and real-time graphing using the `vpython` library.
- **Interactive UI**: A dashboard allowing users to adjust theta, mu, and the D/R ratio in real-time.

## 4. Verification Results
The table below compares the experimental values (Exp) from Table I of the paper with the results calculated by our simulation (Sim).

| Case Name | Sim a (m/s^2) | Exp a (m/s^2) | Error a (%) | Sim alpha (rad/s^2) | Exp alpha (rad/s^2) | Error alpha (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Billiard Smooth (Slide) | 6.08 | 6.05 | **0.5%** | 114.2 | 116.7 | **2.2%** |
| Rubber Smooth (Roll) | 5.08 | 5.07 | **0.2%** | 161.3 | 164.2 | **1.8%** |
| Billiard Rough (Roll) | 5.00 | 4.99 | **0.2%** | 196.9 | 199.2 | **1.2%** |
| Rubber Rough (Roll) | 4.88 | 4.88 | **0.1%** | 155.0 | 162.6 | **4.7%** |

*The results show high accuracy, confirming that the model including the offset D/R accurately describes real-world dynamics.*

## 5. Instructions

### Prerequisites
Install the required libraries:
```bash
pip install numpy vpython
```

### Running the Simulation
Execute the main script to see the 3D visualization:
```bash
python3 simulation.py
```

### Running the Verification
Execute the verification script to see the data comparison:
```bash
python3 verify_results.py
```

## 6. Conclusion
The simulation successfully demonstrates that the normal force offset (D) is a critical factor in determining both the transition from sliding to rolling and the overall acceleration of the object. This model provides a more realistic representation than simplified textbook examples.
