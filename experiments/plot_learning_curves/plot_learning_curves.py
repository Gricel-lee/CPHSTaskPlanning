import numpy as np
import matplotlib.pyplot as plt

# Tried functions to model probability of success with a task as a function of the number of attempts: power law, log power law, and S-shape.
# The S-shape (plot_s_shape_learning_curve) is selected as it converges on 1. The modified version varies between the initial probability "p" of an agent succeeding with a task, and 1.
# The S-shape function is parametrised by the steepness of the curve.


def plot_power_law(a, b, N_min=1, N_max=10, num_points=100):
    """
    Plots the function a * N^(-b) for N in the range [N_min, N_max].

    Parameters:
    a (float): Coefficient of the power law.
    b (float): Exponent of the power law.
    N_min (int): Minimum value of N.
    N_max (int): Maximum value of N.
    num_points (int): Number of points to plot.
    """
    N = np.linspace(N_min, N_max, num_points)
    y = a * N ** (-b)

    plt.figure(figsize=(10, 6))
    plt.plot(N, y, label=f'{a} * N^(-{b})', color='blue')
    plt.title('Power Law Plot')
    plt.xlabel('N')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_log_power_law(a, c, N_min=1, N_max=10, num_points=100):
    """
    Plots the function a * log(N) + c for N in the range [N_min, N_max].

    Parameters:
    a (float): Coefficient of the logarithmic term.
    c (float): Constant term.
    N_min (int): Minimum value of N (must be > 0).
    N_max (int): Maximum value of N.
    num_points (int): Number of points to plot.
    """
    # Ensure N_min > 0 to avoid log(0) or log(negative)
    if N_min <= 0:
        raise ValueError("N_min must be greater than 0.")

    N = np.linspace(N_min, N_max, num_points) # N = np.array(range(1, 1001))
    y =  np.log(N) 
    
    # plt.figure(figsize=(10, 6))
    plt.plot(N, y, label=f'{a} * log(N) + {c}', color='green')
    plt.title('Logarithmic Power Law Plot')
    plt.xlabel('N')
    plt.ylabel('y')
    # plt.xscale('log')  # Logarithmic x-axis
    # plt.grid(True, which='both', linestyle='--')
    plt.legend()
    plt.show()


def plot_s_shape_learning_curve_steepness(N_min=0, N_max=10, num_points=200):
    """
    Plots multiple S-shaped (sigmoid) learning curves using different steepness values.
    """
    N = np.linspace(N_min, N_max, num_points)
    p = 0.8
    steepness_values = [0,0.1,0.3, 0.5, 1, 1.5,3]

    plt.figure(figsize=(5, 3))
    for s in steepness_values:
        y = 2 * (1 - p) * (1 / (1 + np.exp(-(N * s)))) + (2 * p - 1)
        label = f"steepness = {s}"
        plt.plot(N, y, label=label)
    plt.title('S-Shaped Learning Curves for Different Steepness Values')
    plt.xlabel('Number of Attempts (N)')
    plt.ylabel('Performance')
    plt.grid(True)
    plt.legend()
    plt.show()
    


# Example usage
if __name__ == "__main__":
    a = 1.0  # Coefficient
    b = 2.0  # Exponent
    # plot_power_law(a, b)
        
    a_log = 1  # Coefficient for logarithmic term
    c = 0.0     # Constant term
    # plot_log_power_law(a_log, c)
    
    plot_s_shape_learning_curve_steepness()