import sys
import pandas as pd
from readexperiments.aux.auxread import *
from readexperiments.aux.metrics import evaluate_IGD_GD_HV
from experiments.experimentSet import ExperimentSet

def read_experiment_results_and_save_metrics(output_dir,optimisation_list, str_folder_NONE_to_ignore="|NONE|", normalize=False):
    """
    Read experiment results from a CSV file "combined_experiment_data.csv"
    Compute Pareto reference points, Nadir point, and Pareto metrics.
    Save results to CSV output files.
    
    Input:
    - output_dir: Directory where the output files will be saved.
    - optimise: File with list indicating whether to maximise or minimise each objective (e.g., "max,min" s.t. optimise=["max", "min"]).
    - normalize: Flag to indicate whether to normalise data before computing metrics (if normalize the data from 0-100)
    """
    
    
    
    # --- Get data
    # read combined data from all Pareto Fronts saved in resPaths.csv
    df_original = pd.read_csv(f'{output_dir}/combined_experiment_data.csv')
    df = df_original.copy()
    
    # read optimisation list
    with open(optimisation_list, 'r') as f:
        optimise = f.readline().strip().split(",")
    print("Optimisation list:", optimise)
    
    # --- Transform data: remove duplicate rows (when same point appears more than once in a Pareto front)
    print(f"[PF-Indicators] Data points before removing duplicates: {len(df)} rows.")
    df = df.drop_duplicates()
    print(f"[PF-Indicators] Data points after removing duplicates: {len(df)} rows.")
    
    # --- Tranform data: remove |NONE| folder experiments (used for seeding)
    
    df = df[~df['experiment'].str.contains(r"\|NONE\|", regex=True, na=False)]
    
    # --- Transform data: remove rows with 0,0 in first two objectives (due to PRISM bug)
    df = df[~((df.iloc[:, 0] == 0) & (df.iloc[:, 1] == 0))]
    # save for reference
    df.to_csv(f'{output_dir}/combined_experiment_data_no0s.csv', index=False)
    

    # --- Transform data: make it a minimisation problem (pymoo assumes minimisation)
    for i in range(len(optimise)):
        if optimise[i] == "max":
            df.iloc[:, i] = - df.iloc[:, i]
    # if max in any objective, print a note
    if "max" in optimise:
        print("[PF-Indicators] Some objectives were converted from maximisation to minimisation for Pareto calculations.")
        # save for reference
        df.to_csv(f'{output_dir}/combined_experiment_data_minimised.csv', index=False)
    
    # --- Transform data: normalise data (optional) from 0 to 100
    if normalize:
        df.iloc[:, :-1] = normalize_data(df.iloc[:, :-1].to_numpy(), 0, 100)
        df.to_csv(f'{output_dir}/combined_experiment_data_minimised_normalised.csv', index=False)
        print(df.head())
    

    # --- Get Nadir point and Pareto reference points
    # get Nadir Point
    nadir_point = compute_nadir_point(df.iloc[:, :-1].to_numpy())
    print("Nadir Point:", nadir_point) # nadir point must be 100.0001 for all objectives after normalisation

    # get Pareto reference points
    pareto_ref = get_pareto_reference_and_plot(df, output_dir) # or print (if 2D)
    print("Length all data:", len(df))
    print("Length of pareto_ref:", len(pareto_ref))
    
    # --- Compute metrics
    # get IGD, GD and Hypervolume
    metrics = evaluate_IGD_GD_HV(df, pareto_ref, nadir_point)

    # save Pareto ref
    save_pareto_ref(f"{output_dir}/pareto_reference.csv", pareto_ref)

    # save Nadir point
    save_nadir_point(f"{output_dir}/nadir_point.csv", nadir_point, df)

    # save metrics
    save_metrics(f"{output_dir}/metrics_IGD_HV_IG.csv", metrics)
    



# ------------------------------------------------------------------------------
# Nadir Point Calculation
# ------------------------------------------------------------------------------
def compute_nadir_point(data: np.ndarray) -> np.ndarray:
    """
    Compute the nadir point from a dataset and optimisation directions.
    
    Parameters:
        data (np.ndarray): The dataset (N x M), where N is the number of points and M is the number of objectives.
        optimise (list[str]): List of "max" or "min" for each objective column.
        
    Returns:
        np.ndarray: The nadir point (1 x M)
    """
    # Compute nadir point: worst value among Pareto points per objective
    nadir = []
    for i in range(data.shape[1]): # worst = max for minimisation problem used in pymoo
        worst_value = np.max(data[:, i])
        epsilon = 1e-6 * abs(worst_value) if worst_value != 0 else 1e-6  # small offset
        nadir.append(worst_value + epsilon)
    print(f"Nadir Point: {np.array(nadir)}")
    return np.array(nadir)






def normalize_data(data: np.ndarray, new_min: float, new_max: float) -> np.ndarray:
    """
    Normalize the data to a new range [new_min, new_max].
    
    Parameters:
        data (np.ndarray): The dataset (N x M), where N is the number of points and M is the number of objectives.
        new_min (float): The new minimum value after normalization.
        new_max (float): The new maximum value after normalization.
        
    Returns:
        np.ndarray: The normalized dataset.
    """
    data_min = data.min(axis=0)
    data_max = data.max(axis=0)
    
    # Avoid division by zero
    denom = data_max - data_min
    denom[denom == 0] = 1e-8  # small value to prevent division by zero
    
    normalized_data = (data - data_min) / denom
    return normalized_data * (new_max - new_min) + new_min # scaled
