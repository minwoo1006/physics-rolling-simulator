import numpy as np
from simulation import calculate_physics

# Data from Table I in the paper
test_cases = [
    {
        "name": "Billiard Smooth (Slide)",
        "theta": 47.8,
        "mu_k": 0.18,
        "mu_s": 0.20,
        "D_R": 0.004,
        "R": 0.0254,
        "v": 0.1, # Initial slight velocity to ensure slide state if needed
        "omega": 0,
        "expected_a": 6.05,
        "expected_alpha": 116.7
    },
    {
        "name": "Rubber Smooth (Roll)",
        "theta": 47.6,
        "mu_k": 0.31, 
        "mu_s": 0.40,
        "D_R": 0.020,
        "R": 0.0315,
        "v": 0,
        "omega": 0,
        "expected_a": 5.07,
        "expected_alpha": 164.2
    },
    {
        "name": "Billiard Rough (Roll)",
        "theta": 48.1,
        "mu_k": 0.32,
        "mu_s": 0.40,
        "D_R": 0.046,
        "R": 0.0254,
        "v": 0,
        "omega": 0,
        "expected_a": 4.99,
        "expected_alpha": 199.2
    },
    {
        "name": "Rubber Rough (Roll)",
        "theta": 48.1,
        "mu_k": 0.32,
        "mu_s": 0.45,
        "D_R": 0.071,
        "R": 0.0315,
        "v": 0,
        "omega": 0,
        "expected_a": 4.88,
        "expected_alpha": 162.6
    }
]

print(f"{'Case Name':<25} | {'Sim a':<7} | {'Exp a':<7} | {'Err a%':<7} | {'Sim alpha':<10} | {'Exp alpha':<10} | {'Err alpha%':<7}")
print("-" * 105)

for case in test_cases:
    # Directly use the function from simulation.py
    sim_a, sim_alpha, is_sliding = calculate_physics(
        case["v"], case["omega"], case["R"], np.radians(case["theta"]), 
        case["mu_k"], case["mu_s"], case["D_R"]
    )
    
    err_a = abs(sim_a - case["expected_a"]) / case["expected_a"] * 100
    err_alpha = abs(sim_alpha - case["expected_alpha"]) / case["expected_alpha"] * 100
    
    print(f"{case['name']:<25} | {sim_a:<7.2f} | {case['expected_a']:<7.2f} | {err_a:<7.1f} | {sim_alpha:<10.1f} | {case['expected_alpha']:<10.1f} | {err_alpha:<7.1f}")
