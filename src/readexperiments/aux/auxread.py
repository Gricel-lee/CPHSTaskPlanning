import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# Utility Function to Normalise Objective Directions
# ------------------------------------------------------------------------------
def minimise_if_maximise(df, optimise):
    """
    Convert the DataFrame to a minimization problem if any column is set to 'max'.
    """
    for i, goal in enumerate(optimise):
        if goal == "max":
            df.iloc[:, i] = -df.iloc[:, i]  # Negate the column for minimization
        if goal not in ["min", "max"]:
            raise ValueError("Each entry in 'optimise' must be 'min' or 'max'")
    return df

# ------------------------------------------------------------------------------
# Pareto front calculation
# ------------------------------------------------------------------------------
def _is_pareto_reference(costs):
    """
    Find the Pareto-reference points efficiently by masking the rows.
    """
    is_ref = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_ref[i]:
            is_ref[is_ref] = np.any(costs[is_ref] < c, axis=1) | np.all(costs[is_ref] == c, axis=1)
            is_ref[i] = True  # Keep self
    return is_ref


def get_pareto_reference(df,optimise):
    """
    Get the Pareto reference points.
    """
    df.columns = df.columns.str.strip()  # Clean column names

    # Select all data columns except the last one (which is the 'experiment' string)
    data = df.iloc[:, :-1]
    
    # Convert to "costs" (for Pareto calculation, lower is better): if "max", we negate the column to turn it into a "min" problem
    optimised_data = minimise_if_maximise(data, optimise).values
    
    # Get Pareto reference points masked
    pareto_mask = _is_pareto_reference(optimised_data)
    
    # Get Pareto front
    pareto_df = df[pareto_mask]
    
    return pareto_df, data, pareto_mask

def get_pareto_reference_and_plot(df, optimise):
    """
    Get Pareto reference points and plot them if the data is 2D.
    """
    pareto_df, data, pareto_mask = get_pareto_reference(df, optimise)
    
    # Plot if 2D
    if data.shape[1] == 2:
        plt.figure(figsize=(8, 6))
        plt.scatter(data[:, 0], data[:, 1], color='red', label='All Points')
        plt.scatter(data[pareto_mask, 0], data[pareto_mask, 1], color='blue', label='Pareto Front')
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.title('Pareto Front Visualization')
        plt.legend()
        plt.grid(True)
        # plt.show()
    else:
        print(f"No plot: Data has {data.shape[1]} dimensions (only 2D is plotted).")

    # ordered by column
    # print(pareto_df.sort_values(by=df.columns[0]))
    
    return pareto_df


# ------------------------------------------------------------------------------
# Nadir Point Calculation
# ------------------------------------------------------------------------------
def compute_nadir_point(data: np.ndarray, optimise: list[str]) -> np.ndarray:
    """
    Compute the nadir point from a dataset and optimisation directions.
    
    Parameters:
        data (np.ndarray): The dataset (N x M), where N is the number of points and M is the number of objectives.
        optimise (list[str]): List of "max" or "min" for each objective column.
        
    Returns:
        np.ndarray: The nadir point (1 x M)
    """
    # Validate input dimensions
    if data.shape[1] != len(optimise):
        raise ValueError("Length of 'optimise' must match number of columns in 'data'")
    
    # Compute nadir point: worst value among Pareto points per objective
    nadir = []
    for i, goal in enumerate(optimise):
        if goal == "min":
            nadir.append(np.max(data[:, i]))  # worst = max for min
        elif goal == "max":
            nadir.append(np.min(data[:, i]))  # worst = min for max
        else:
            raise ValueError("Each entry in 'optimise' must be 'min' or 'max'")
    # print(f"Nadir Point: {np.array(nadir)}")
    return np.array(nadir)


# ------------------------------------------------------------------------------
# Output Utility
# ------------------------------------------------------------------------------
def save_pareto_ref(output_file, pareto_ref):
    pareto_ref.to_csv(output_file, index=False)


def save_nadir_point(output_dir, nadir_point, df):
    # save Nadir point
    np.savetxt(
        output_dir,
        nadir_point.reshape(1, -1),  # Ensures it's one row
        delimiter=',',
        header= ','.join(df.columns[:-1]),  # Use all but the last column as header
        fmt='%.3f',  #format for float values
        comments=''
    )
    
def save_metrics(output_file, metrics_df):
    # Save the metrics DataFrame to a CSV file
    metrics_df.to_csv(output_file, index=False)
    print(f"Metrics saved to {output_file}")
