# lorenz63.py
"""Lorenz 1963 three-variable chaotic model."""
import numpy as np
import matplotlib.pyplot as plt 
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

    def __init__(self, sigma=10, rho=28, beta=(8 / 3)):
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
        # x, y, z = state # state must thus be [x, y, z]
        x, y, z = state
        return np.array([self.sigma*(y-x), self.rho*x - y - x*z, x*y - self.beta*z])

    def vectorized_tendency(self, state):
        # state = (n_members, 3)
        derivatives = np.zeros(state.shape)
        
        # x, y, z = state # state must thus be [x, y, z]
        # dx_dt = self.sigma*(y - x)
        # dy_dt = x*(self.rho - z) - y
        # dz_dt = x*y - self.beta * z
        xs = state[:,0]
        ys = state[:,1]
        zs = state[:,2]
        derivatives[:,0] = self.sigma*(ys-xs)
        derivatives[:,1] = xs*self.rho - xs*zs - ys
        derivatives[:,2] = xs * ys - self.beta * zs
        # print(f"{derivatives.shape}")
        return derivatives


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





        # trajectory = np.zeros([n_steps+1, len(state0)])
        # trajectory[0,:] = state0
        # for ii in range(0,n_steps):
        #     trajectory[ii+1,:] = trajectory[ii,:] + dt*self.tendency(trajectory[ii])
        # plt.plot(trajectory)
        # plt.savefig("run_internal_trajectory.png", bbox_inches='tight', dpi=150)
        # plt.show() #here too




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
        # ensemble_size = np.array([1,3])
        # print(f"{type(ensemble_size)}")
        # ensemble_members = ensemble_size[0]
        length = n_steps+1
        # print(f"{type(length)}") # debugging 

        # ensemble = np.zeros([ensemble_size[0], length, ensemble_size[1]])
        # for ii in range(0, ensemble_size[0]):
        #     individual_member = self.run(initial_conditions[ii,:], dt, n_steps)
        #     ensemble[ii, :, :] = individual_member
        # return ensemble


        ## METHOD 2:

        vector_ensemble = np.zeros([ensemble_size[0], length, ensemble_size[1]])
        # print(f"{vector_ensemble.shape}")
        vector_ensemble[:,0,:] = initial_conditions
        # print(f"Vector Initial: {vector_ensemble[:,0,:]}")
        for jj in range(0, n_steps):
            
            vector_ensemble[:,jj+1,:] = vector_ensemble[:,jj,:] + dt*self.vectorized_tendency(vector_ensemble[:,jj,:])
        return vector_ensemble

       



if __name__ == "__main__":
    # ── Test your code! ──────────────────────────────────────────────
    # Run this file directly:  python -m lorenz_project.lorenz63
    # If your implementations are correct, it should print
    # "lorenz63.py: all checks passed!" with no errors.

    model = Lorenz63()

    # Test 1: single trajectory
    traj = model.run(np.array([1.0, 1.0, 1.0]), dt=0.01, n_steps=1000)
    assert traj.shape == (1001, 3), f"Wrong shape: {traj.shape}, expected (1001, 3)"
    plt.plot(traj)
    plt.savefig("lorenz63_verification_graph.png", dpi = 200, bbox_inches='tight')
    plt.show()
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

    # # Test 3: What's goin on!
    # state_test = model.run(np.array([1.0, 1.0, 1.0]), dt = 0.01, n_steps = 500000)
    # plt.plot(state_test)
    # plt.savefig("State_test_run_IN_lorenz63.png", bbox_inches = 'tight', dpi = 150)
    # plt.show()
    # # oooooook so here too
