from pymoo.indicators.gd import GD
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
import numpy as np
import pandas as pd

"""
Calculate IGD, GD, and Hypervolume metrics for a set of experiments.

Metrics Overview:
-----------------
| Metric | Meaning                   | Goal             |
|--------|---------------------------|------------------|
| IGD    | Distance from true Pareto | Lower is better  |
| GD     | Generational Distance     | Lower is better  |
| HV     | Hypervolume               | Higher is better |

This script assumes all objectives are minimization-based
(see readResultsExperiments.py for data preprocessing steps).
"""


# ------------------------------------------------------------------------------
# Metric Calculation Functions
# ------------------------------------------------------------------------------
def compute_igd(points, pareto_ref):
    return IGD(pareto_ref)(points)

def compute_gd(points, pareto_ref):
    return GD(pareto_ref)(points)

def compute_hypervolume(points, nadir_point):
    return HV(ref_point=nadir_point)(points)



# ------------------------------------------------------------------------------
# Main Metrics Evaluation Function
# ------------------------------------------------------------------------------
def evaluate_IGD_GD_HV(df, pareto_reference, nadir_point):
    # Get Pareto reference points, which should be a minimisation problem
    pareto_ref = pareto_reference.copy()
    pareto_ref = pareto_ref.iloc[:, :-1]  # Remove the 'experiment' column for metrics calculation
    pareto_ref_np = pareto_ref.to_numpy()  # Convert to numpy array for pymoo compatibility
    
    # Get unique experiments
    experiments = df['experiment'].unique()
    print("Experiments:", len(experiments), "experiments found.")
    print("Pareto reference points:", len(pareto_ref_np))
    
    # Create df with columns for IGD, GD, and Hypervolume and experiment name
    metrics_df = pd.DataFrame(columns=['IGD', 'GD', 'HV', 'pareto_front_size','experiment'])
    
    # Iterate through each experiment and compute metrics
    for experiment in experiments:
        exp_i = df[df['experiment'] == experiment].iloc[:, :-1]
        exp_i_np = exp_i.to_numpy()
        
        # compute IGD, GD, and Hypervolume
        igd_value = compute_igd(exp_i_np, pareto_ref_np)
        gd_value = compute_gd(exp_i_np, pareto_ref_np)
        hv_value = compute_hypervolume(exp_i_np, nadir_point)
        # size of exp_i_np
        pareto_front_i_size = exp_i_np.shape[0]
        
        # Store results in df
        new_row = pd.DataFrame([{
            'IGD': igd_value, 'GD': gd_value, 'HV': hv_value, 'pareto_front_size': pareto_front_i_size, 'experiment': experiment
        }])
        metrics_df = pd.concat([metrics_df, new_row], ignore_index=True)
    return metrics_df
