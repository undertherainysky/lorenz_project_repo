# integrators.py
"""Numerical integration methods for ODE systems."""
import numpy as np
import matplotlib.pyplot as plt


def euler_step(state, tendency_fn, dt):
    """Advance one step using Forward Euler.

    Parameters
    ----------
    state : np.ndarray
        Current state vector (e.g., [x, y, z] for Lorenz63).
    tendency_fn : callable
        Function that takes state and returns dstate/dt.
    dt : float
        Time step size.

    Returns
    -------
    np.ndarray
        State at the next time step.

    Hint
    ----
    This is one line: y_{n+1} = y_n + f(y_n) * dt
    """
    # TODO: implement Forward Euler formula

    tend = tendency_fn(state)

    state_Stepped = state + tend*dt

    return state_Stepped


def integrate(state0, tendency_fn, dt, n_steps):
    """Integrate an ODE system forward in time using Forward Euler (or any time stepping method!).

    Parameters
    ----------
    state0 : np.ndarray
        Initial state vector, shape (n_vars,).
    tendency_fn : callable
        Function that takes state and returns tendency, shape (n_vars,).
    dt : float
        Time step size.
    n_steps : int
        Number of time steps to take.

    Returns
    -------
    np.ndarray
        Trajectory array, shape (n_steps + 1, n_vars).
        Row 0 is the initial condition, row -1 is the final state.

    Hint
    ----
    1. Pre-allocate: trajectory = np.zeros((n_steps + 1, len(state0)))
    2. Set trajectory[0] = state0
    3. Loop from 0 to n_steps-1, filling trajectory[i+1] using euler_step
    """
    # TODO: implement the integration loop
    trajectory = np.zeros((n_steps + 1, len(state0)))
    trajectory[0,:] = state0

    for ii in range(0, n_steps):
        trajectory[ii+1,:] = euler_step(trajectory[ii,:], tendency_fn, dt)
    plt.plot(trajectory)
    plt.savefig("integrate_internal_trajectory.png", dpi=150, bbox_inches='tight')
    plt.show()
    return trajectory




if __name__ == "__main__":
    # ── Test your code! ──────────────────────────────────────────────
    # Run this file directly:  python -m lorenz_project.integrators
    # If your implementations are correct, it should print
    # "integrators.py: all checks passed!" with no AssertionError.
    #
    # Test: exponential decay  dy/dt = -y,  y(0) = 1
    # Exact solution at t=1 is e^{-1} ≈ 0.3679
    # Forward Euler with dt=0.01, 100 steps should get close.s
    result = integrate(np.array([1.0]), lambda y: -y, dt=0.01, n_steps=100)
    final = result[-1, 0]
    exact = np.exp(-1.0)
    print(f"Euler result: {final:.10f}, Exact: {exact:.4f}, Error: {abs(final - exact):.4f}")
    assert abs(final - exact) < 0.01, f"Error too large: {abs(final - exact)}"
    print("integrators.py: all checks passed!")
    # plt.plot(result)
    # plt.savefig("Integrators_check.png", dpi = 150, bbox_inches='tight')
    # plt.show()
    # print(f"Mid-check: {result[50,0]}") # is correct?
    