# lorenz63.py
"""Lorenz 1963 three-variable chaotic model."""
import numpy as np
from lorenz_project.integrators import integrate


class Lorenz63:
    """The Lorenz (1963) system: a 3-variable model of atmospheric convection.

    Equations
    ---------
    dx/dt = sigma * (y - x)
    dy/dt = rho * x - y - x * z
    dz/dt = x * y - beta * z

    Default parameters (sigma=10, rho=28, beta=8/3) produce chaotic behavior.
    """

    def __init__(self, sigma=10, rho=28, beta=8 / 3):
        """Store model parameters.

        Hint: just save sigma, rho, beta as self.sigma, etc.
        """
        # TODO: store parameters
        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def tendency(self, state):
        """Compute the time derivatives [dx/dt, dy/dt, dz/dt].

        Parameters
        ----------
        state : np.ndarray
            Current state [x, y, z], shape (3,).

        Returns
        -------
        np.ndarray
            Tendencies [dx/dt, dy/dt, dz/dt], shape (3,).

        Hint
        ----
        Unpack: x, y, z = state
        Return np.array([sigma*(y-x), rho*x - y - x*z, x*y - beta*z])
        """
        # TODO: implement Lorenz63 equations
        x, y, z = state # state must thus be [x, y, z]
        dx_dt = self.sigma*(y - x)
        dy_dt = x*(self.rho - z) - y
        dz_dt = x*y - self.beta * z
        return np.array([dx_dt, dy_dt, dz_dt])

    def run(self, state0, dt, n_steps):
        """Integrate the model forward from a single initial condition.

        Parameters
        ----------
        state0 : np.ndarray
            Initial condition [x0, y0, z0], shape (3,).
        dt : float
            Time step.
        n_steps : int
            Number of steps.

        Returns
        -------
        np.ndarray
            Trajectory, shape (n_steps + 1, 3).

        Hint
        ----
        Call the integrate() function from integrators.py,
        passing self.tendency as the tendency function.
        """
        # TODO: call integrate() with self.tendency
        trajectory = integrate(state0, self.tendency, dt, n_steps)
        return trajectory

    def run_ensemble(self, initial_conditions, dt, n_steps):
        """Run an ensemble of trajectories from multiple initial conditions.

        Parameters
        ----------
        initial_conditions : np.ndarray
            Array of initial conditions, shape (n_members, 3).
        dt : float
            Time step.
        n_steps : int
            Number of steps.

        Returns
        -------
        np.ndarray
            Ensemble trajectories, shape (n_members, n_steps + 1, 3).

        Instructions
        ------------
        Implement this TWO ways (keep both, comment one out):

        METHOD 1 — Nested for loop:
            Outer loop over ensemble members, inner call to self.run().
            Straightforward but slow for large ensembles.

        METHOD 2 — Single for loop with vectorized step:
            Instead of looping over members, advance ALL members at once.
            At each time step, compute tendency for ALL members simultaneously.

            Hint for Method 2:
            - states has shape (n_members, 3)
            - You need a vectorized_tendency that takes shape (n_members, 3)
              and returns shape (n_members, 3)
            - The Euler step is: states = states + vectorized_tendency(states) * dt
            - The loop is over TIME STEPS only, not members

        Start with Method 1. Once it works, do Method 2.
        """
        # TODO: implement ensemble integration
        
        ## METHOD 1:
        ensemble_size = initial_conditions.shape
        # print(f"{type(ensemble_size)}")
        # ensemble_members = ensemble_size[0]
        length = n_steps+1
        print(f"{type(length)}")

        ensemble = np.zeros([ensemble_size[0], length, ensemble_size[1]])
        for ii in range(0, ensemble_size[0]):
            individual_member = self.run(initial_conditions[ii,:], dt, n_steps)
            ensemble[ii, :, :] = individual_member
        return ensemble

        ## METHOD 2:




                
                



if __name__ == "__main__":
    # ── Test your code! ──────────────────────────────────────────────
    # Run this file directly:  python -m lorenz_project.lorenz63
    # If your implementations are correct, it should print
    # "lorenz63.py: all checks passed!" with no errors.

    model = Lorenz63()

    # Test 1: single trajectory
    traj = model.run(np.array([1.0, 1.0, 1.0]), dt=0.01, n_steps=1000)
    assert traj.shape == (1001, 3), f"Wrong shape: {traj.shape}, expected (1001, 3)"
    print(f"Single run: final state = [{traj[-1, 0]:.2f}, {traj[-1, 1]:.2f}, {traj[-1, 2]:.2f}]")
    print(f"  trajectory shape: {traj.shape}  ✓")

    # Test 2: ensemble of 5 members
    n_members = 5
    ics = np.array([[1.0, 1.0, 1.0]] * n_members) + np.random.randn(n_members, 3) * 0.01
    ensemble = model.run_ensemble(ics, dt=0.01, n_steps=1000)
    assert ensemble.shape == (n_members, 1001, 3), \
        f"Wrong shape: {ensemble.shape}, expected ({n_members}, 1001, 3)"
    print(f"Ensemble run: shape = {ensemble.shape}  ✓")

    print("lorenz63.py: all checks passed!")
