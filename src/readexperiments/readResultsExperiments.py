import sys
import pandas as pd
from readexperiments.aux.auxread import *
from readexperiments.aux.metrics import evaluate_IGD_GD_HV
from experiments.experimentSet import ExperimentSet

def read_experiment_results_and_save_metrics(output_dir,optimisation_list):
    """
    Read experiment results from a CSV file, compute Pareto reference points, Nadir point, and Pareto metrics.
    Save results to CSV output files.
    
    Input:
    - output_dir: Directory where the output files will be saved.
    - optimise: File with list indicating whether to maximise or minimise each objective (e.g., "max,min" s.t. optimise=["max", "min"]).
    """
    # --- Get Pareto reference points and Nadir point
    # read combined data from all Pareto Fronts saved in resPaths.csv
    df = pd.read_csv(f'{output_dir}/combined_experiment_data.csv')

    # --- Read optimisation list
    with open(optimisation_list, 'r') as f:
        optimise = f.readline().strip().split(",")
    print("Optimisation list:", optimise)
    
    
    # --- Get Nadir point and Pareto reference points
    # get Nadir Point
    nadir_point = compute_nadir_point(df.iloc[:, :-1].to_numpy(), optimise)
    print("Nadir Point:", nadir_point)

    # get Pareto reference points
    pareto_ref = get_pareto_reference(df, optimise)[0]
    # pareto_ref = get_pareto_reference_and_plot(df, optimise) # or print (if 2D)
    print("Lenght all data:", len(df))
    print("Length of pareto_ref:", len(pareto_ref))
    
    # --- Compute metrics
    # get IGD, GD and Hypervolume
    metrics = evaluate_IGD_GD_HV(df, pareto_ref, nadir_point, optimise)
    
    # save Pareto ref
    save_pareto_ref(f"{output_dir}/pareto_reference.csv", pareto_ref)

    # save Nadir point
    save_nadir_point(f"{output_dir}/nadir_point.csv", nadir_point, df)

    # save metrics
    save_metrics(f"{output_dir}/metrics_IGD_HV_IG.csv", metrics)
    
