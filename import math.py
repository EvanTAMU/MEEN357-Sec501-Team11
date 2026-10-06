import math


def analyze_stress_case(sx, sy, txy, S_y):
    """Calculates principal stresses and safety factors for DE and MSS theories."""
    # 1. In-plane Principal Stresses
    center = (sx + sy) / 2.0
    radius = math.sqrt(((sx - sy) / 2.0) ** 2 + txy**2)

    sigma_1 = center + radius
    sigma_2 = center - radius

    # 2. 3D Principal Stresses (incorporating σ3 = 0 for plane stress)
    stresses = sorted([sigma_1, sigma_2, 0.0], reverse=True)
    sigma_A, sigma_B, sigma_C = stresses[0], stresses[1], stresses[2]

    # 3. Distortion-Energy (DE / von Mises) Theory
    sigma_von_mises = math.sqrt(sx**2 - sx * sy + sy**2 + 3 * (txy**2))
    n_DE = S_y / sigma_von_mises if sigma_von_mises != 0 else float("inf")

    # 4. Maximum-Shear-Stress (MSS / Tresca) Theory
    tau_max = (sigma_A - sigma_C) / 2.0
    n_MSS = S_y / (2.0 * tau_max) if tau_max != 0 else float("inf")

    return {
        "sigma_A": sigma_A,
        "sigma_B": sigma_B,
        "sigma_vm": sigma_von_mises,
        "tau_max": tau_max,
        "n_DE": n_DE,
        "n_MSS": n_MSS,
    }


def main():
    # Given material yield strength
    S_y = 350.0  # MPa

    # Given stress values for Problem 1(a): sigma_x = 100 MPa, sigma_y = 100 MPa, tau_xy = 0 MPa
    sx, sy, txy = 100.0, 100.0, 0.0

    # Compute results
    results = analyze_stress_case(sx, sy, txy, S_y)

    # Print results
    print("=" * 45)
    print("          PROBLEM 1(a) RESULTS          ")
    print("=" * 45)
    print(f"Yield Strength (S_y)      : {S_y:.2f} MPa")
    print(f"Principal Stress σ_A      : {results['sigma_A']:.2f} MPa")
    print(f"Principal Stress σ_B      : {results['sigma_B']:.2f} MPa")
    print(f"von Mises Stress (σ')     : {results['sigma_vm']:.2f} MPa")
    print(f"Max Shear Stress (τ_max)  : {results['tau_max']:.2f} MPa")
    print("-" * 45)
    print(f"DE Factor of Safety (n_DE): {results['n_DE']:.3f}")
    print(f"MSS Factor of Safety (n_MSS): {results['n_MSS']:.3f}")
    print("=" * 45)


if __name__ == "__main__":
    main()