import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# @Deprecated: changed to minimise in readResultsExperiments.py
# def minimise_if_maximise(df, optimise):
#     """
#     Convert the DataFrame to a minimization problem if any column is set to 'max'.
#     """
#     for i, goal in enumerate(optimise):
#         if goal == "max":
#             df.iloc[:, i] = -df.iloc[:, i]  # Negate the column for minimization
#         if goal not in ["min", "max"]:
#             raise ValueError("Each entry in 'optimise' must be 'min' or 'max'")
#     return df

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

def pareto_mask_2d(costs):
    """
    Efficient 2D Pareto front mask for minimization.
    costs: np.array of shape (n_points, 2)
    Returns: boolean mask of Pareto-optimal points
    """
    # Sort by the first objective
    sorted_idx = np.argsort(costs[:, 0])
    costs_sorted = costs[sorted_idx]

    pareto_mask_sorted = np.ones(costs_sorted.shape[0], dtype=bool)
    min_second_obj = np.inf

    for i, (_, second) in enumerate(costs_sorted):
        if second < min_second_obj:
            min_second_obj = second
        else:
            pareto_mask_sorted[i] = False

    # Return mask in original order
    mask = np.zeros(costs.shape[0], dtype=bool)
    mask[sorted_idx] = pareto_mask_sorted
    return mask


def get_pareto_reference(df):
    """
    Get the Pareto reference points.
    """
    df.columns = df.columns.str.strip()  # Clean column names

    # Select all data columns except the last one (which is the 'experiment' string)
    data = df.iloc[:, :-1]

    # Get Pareto reference points masked
    pareto_mask = _is_pareto_reference(data.values)

    # Get Pareto front
    pareto_df = df[pareto_mask]
    
    return pareto_df, data, pareto_mask

def get_pareto_reference_and_plot(df, output_dir):
    """
    Get Pareto reference points and plot them if the data is 2D.
    """
    pareto_df, data, pareto_mask = get_pareto_reference(df)
    
    # Plot if 2D
    if data.shape[1] == 2:
        plt.figure(figsize=(8, 6))
        # Use the DataFrame values for numeric indexing and keep the DataFrame for labels
        data_vals = data.values
        # debug print of first few x values
        print(data.iloc[:, 0].head())
        plt.scatter(data_vals[:, 0], data_vals[:, 1], color='red', label='All Points')
        plt.scatter(data_vals[pareto_mask, 0], data_vals[pareto_mask, 1], color='blue', label='Pareto Front')
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.title('Pareto Front Visualization')
        plt.legend()
        plt.grid(True)
        # plt.show()
        
        # Save plot
        plt.savefig(f'{output_dir}/pareto_front_plot.png')
        plt.close()
        print("Pareto front plot saved as 'pareto_front_plot.png'.")
        
    else:
        print(f"No plot: Data has {data.shape[1]} dimensions (only 2D is plotted).")

    # ordered by column
    # print(pareto_df.sort_values(by=df.columns[0]))
    
    return pareto_df



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
