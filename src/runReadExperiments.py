import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from readexperiments.auxread import *
from readexperiments.metrics import evaluate_IGD_GD_HV


import numpy as np

# --- Inputs
csv_file = '/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/output/experiments/combined_experiment_data.csv'
output_dir = '/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/output/experiments/'
# Define whether to maximise or minimise each objective. Example: ["max", "min"] means column 0 is to be maximized, column 1 minimized
optimise = ["max", "min"]  # Adjust this list for your case

# --- Get Pareto reference points and Nadir point
df = pd.read_csv(csv_file)

# get Nadir Point
nadir_point = compute_nadir_point(df.iloc[:, :-1].to_numpy(), optimise)
print("Nadir Point:", nadir_point)

# get Pareto reference points 
pareto_ref = get_pareto_reference(df,optimise)[0]
# pareto_ref = get_pareto_reference_and_plot(df, optimise) # or print (if 2D)
print("Lenght all data:", len(df))
print("Length of pareto_ref:", len(pareto_ref))

# get IGD, GD and Hypervolume
metrics = evaluate_IGD_GD_HV(df, pareto_ref, nadir_point, optimise)


# save Pareto ref
save_pareto_ref(f"{output_dir}pareto_reference.csv", pareto_ref)

# save Nadir point
save_nadir_point(f"{output_dir}nadir_point.csv", nadir_point, df)

# save metrics
save_metrics(f"{output_dir}metrics.csv", metrics)