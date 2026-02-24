# run_lorenz_ensemble.py
"""
Driver script: Lorenz63 Ensemble Predictability Experiment
==========================================================

This script produces a 3-panel figure showing how predictability
depends on where you start on the Lorenz attractor.

Each panel shows:
  - The full attractor (light blue background)
  - An ensemble of trajectories (red) started from a small cloud
    of initial conditions near a chosen point

The three starting regions are:
  (a) Deep left lobe  — ring barely grows (highly predictable)
  (b) High left lobe  — ring distorts into banana/boomerang (transition zone)
  (c) Saddle region   — ring explodes, members go left and right (no predictability)

Output: saves 'lorenz_ensemble_predictability.png'

Usage
-----
    python -m lorenz_project.run_lorenz_ensemble

Instructions
------------
1. Import Lorenz63 from lorenz63.py and plot functions from plotting.py
2. Create a Lorenz63 model with default parameters
3. Generate a long reference trajectory (spin up, then run ~10000 steps)
4. Pick 3 initial conditions from different regions of the attractor
   (Hint: use points from your reference trajectory at different times)
5. For each initial condition, create a cloud of ~30 nearby members
   by adding small random perturbations (e.g., np.random.randn * 0.5)
6. Run run_ensemble() for each cloud
7. Use plot_ensemble_panels() to make the 3-panel figure
8. Save the figure
"""
import numpy as np

# TODO: import Lorenz63 from lorenz_project.lorenz63
# TODO: import plotting functions from lorenz_project.plotting

# --- Configuration ---
DT = 0.01
SPINUP_STEPS = 500000       # let transients die out
REFERENCE_STEPS = 20000   # long trajectory for background attractor
ENSEMBLE_STEPS = 50     # how far to integrate each ensemble
N_MEMBERS = 30            # ensemble size
PERTURBATION_SCALE = 0.3  # std dev of initial perturbations
SAVE_PATH = "lorenz_ensemble_predictability.png"


def main():
    """Run the full ensemble experiment."""
    # TODO: Step 1 — Create model
    # model = Lorenz63()

    # TODO: Step 2 — Generate reference trajectory
    # Spin up from (1, 1, 1) for SPINUP_STEPS, then take the final state
    # and run for REFERENCE_STEPS more. The long run IS your reference.
    

    # TODO: Step 3 — Create initial condition clouds
    np.random.seed(42)  # reproducibility
    deep_left_state = np.array([-15,1,45])
    high_left_state = np.array([-8,-3,34])
    saddle_state = np.array([0,0,18])
    ics_deep = deep_left_state + np.random.randn(N_MEMBERS, 3) * PERTURBATION_SCALE
    ics_high = high_left_state + np.random.randn(N_MEMBERS, 3) * PERTURBATION_SCALE
    ics_saddle = saddle_state + np.random.randn(N_MEMBERS, 3) * PERTURBATION_SCALE

    # TODO: Step 4 — Run ensembles
    # ensemble_deep = model.run_ensemble(ics_deep, DT, ENSEMBLE_STEPS)
    # ensemble_high = model.run_ensemble(ics_high, DT, ENSEMBLE_STEPS)
    # ensemble_saddle = model.run_ensemble(ics_saddle, DT, ENSEMBLE_STEPS)

    # TODO: Step 5 — Plot
    # plot_ensemble_panels(
    #     [ensemble_deep, ensemble_high, ensemble_saddle],
    #     reference,
    #     ["(a) Deep left lobe", "(b) High left lobe", "(c) Saddle region"],
    #     save_path=SAVE_PATH,
    # )

    # print(f"Figure saved to {SAVE_PATH}")


if __name__ == "__main__":
    main()
