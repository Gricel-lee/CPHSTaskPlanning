import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from matplotlib.patches import Rectangle

def process_metrics_files(main_directory: str) -> pd.DataFrame:
    """
    Reads all 'metrics_IGD_HV_IG.csv' files from subdirectories, adds new columns for
    experiment type, iteration number, and source folder, and combines them into a single DataFrame.
    """
    all_dataframes = []
    if not os.path.isdir(main_directory):
        print(f"Error: Directory '{main_directory}' not found.")
        return pd.DataFrame()
    print(f"Scanning subdirectories in '{main_directory}' for metrics files...")
    for folder_name in sorted(os.listdir(main_directory)):
        folder_path = os.path.join(main_directory, folder_name)
        if os.path.isdir(folder_path):
            metrics_file_path = os.path.join(folder_path, "metrics_IGD_HV_IG.csv")
            if os.path.exists(metrics_file_path):
                try:
                    print(f"  Reading metrics file: {metrics_file_path}")
                    df = pd.read_csv(metrics_file_path)
                    experiment_path_series = df['experiment']
                    df['iteration'] = experiment_path_series.str.split('_').str[-2].astype(int, errors='ignore')
                    df['experiment'] = experiment_path_series.str.split('/results/').str[0].str.split('/').str[-1]
                    df['source_folder'] = folder_name
                    all_dataframes.append(df)
                except Exception as e:
                    print(f"  Could not read or process metrics file {metrics_file_path}. Error: {e}")
    if not all_dataframes:
        return pd.DataFrame()
    return pd.concat(all_dataframes, ignore_index=True)

def process_time_files(main_directory: str) -> pd.DataFrame:
    """
    Scans all experiment subdirectories to read 'time.txt' files and compiles them into a single DataFrame.
    """
    all_time_data = []
    if not os.path.isdir(main_directory):
        return pd.DataFrame()
    print(f"\nScanning subdirectories in '{main_directory}' for time files...")
    for source_folder in sorted(os.listdir(main_directory)):
        source_folder_path = os.path.join(main_directory, source_folder)
        if not os.path.isdir(source_folder_path):
            continue
        for experiment_folder in sorted(os.listdir(source_folder_path)):
            experiment_folder_path = os.path.join(source_folder_path, experiment_folder)
            time_file_path = os.path.join(experiment_folder_path, 'results', 'time.txt')
            if os.path.isfile(time_file_path):
                try:
                    time_df = pd.read_csv(time_file_path, sep=r'\s+', header=None, names=['iteration_str', 'time'])
                    time_df['iteration_num_str'] = time_df['iteration_str'].str.extract(r'(\d+)')
                    time_df.dropna(subset=['iteration_num_str'], inplace=True)
                    time_df['iteration'] = time_df['iteration_num_str'].astype(int)
                    time_df['source_folder'] = source_folder
                    time_df['experiment'] = experiment_folder
                    all_time_data.append(time_df[['source_folder', 'experiment', 'iteration', 'time']])
                except Exception as e:
                    print(f"  Could not read or process time file {time_file_path}. Error: {e}")
    if not all_time_data:
        return pd.DataFrame()
    return pd.concat(all_time_data, ignore_index=True)

def calculate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the average and standard deviation for key metrics, grouped by 'experiment' and 'iteration'.
    """
    if 'iteration' not in df.columns or 'experiment' not in df.columns:
        return pd.DataFrame()
    print("\nCalculating summary statistics...")
    agg_columns = {
        'IGD': ['mean', 'std'], 'GD': ['mean', 'std'],
        'HV': ['mean', 'std'], 'pareto_front_size': ['mean', 'std'],
        'time': ['mean', 'std']
    }
    summary_df = df.groupby(['experiment', 'iteration']).agg(agg_columns)
    summary_df.columns = [
        'IGD_avr', 'IGD_std', 'GD_avr', 'GD_std',
        'HV_avr', 'HV_std', 'pareto_front_size_avr', 'pareto_front_size_std',
        'time_avr', 'time_std'
    ]
    return summary_df.reset_index()



##### Force order
desired_order = [
        "NONE2|0",
        "Random|25",
        "Random|100",
        "KMeans|25",
        "KMeans|100",
        "FuzzyKMeans|25",
        "FuzzyKMeans|100",
        "DBSCAN|25",
        "DBSCAN|100"
]
# Build a lookup index
order_index = {entry: i for i, entry in enumerate(desired_order)}

def experiment_key(exp):
    # Keep only the part after the first "|"
    parts = exp.split("|")
    algo_param = "|".join(parts[1:3])  # e.g., "DBSCAN|25"

    return order_index.get(algo_param, 9999)
########


def plot_metric(summary_df: pd.DataFrame, metric: str, y_label: str, output_filename: str):
    """
    Draw grouped 'box-like' plots: For each iteration on the x-axis,
    draw N adjacent boxes (one per experiment) representing mean ± std.
    """

    #>>>> Filter (you had iteration < 6 for debugging)
    summary_df = summary_df[summary_df['iteration'] < 11]
    
    print(summary_df.head())

    if summary_df.empty:
        print(f"Cannot create plot for {metric.upper()}: The summary DataFrame is empty.")
        return

    metric_avr = f"{metric}_avr"
    metric_std = f"{metric}_std"

    if metric_avr not in summary_df or metric_std not in summary_df:
        print(f"Missing columns {metric_avr} or {metric_std}")
        return

    print(f"\nGenerating grouped box plot for {metric.upper()} → {output_filename}")

    # Unique iterations and experiments
    iterations = sorted(summary_df["iteration"].unique())
    experiments = sorted(summary_df["experiment"].unique())
    
    #>>>>> FORCE order <<<<< (check function)
    experiments_sorted = sorted(summary_df["experiment"].unique(), key=experiment_key)
    experiments = experiments_sorted


    # Figure size – scale reasonably
    fig, ax = plt.subplots(figsize=(max(8, 1.2 * len(iterations)), 6))
    
    n_experiments = len(experiments)

    palette = sns.color_palette("husl", n_experiments)

    # ----- Spacing -----
    group_width = 0.8                      # width occupied by the entire group
    box_width = group_width / n_experiments  # width per experiment

    # Draw rectangular boxes
    for exp_index, exp_name in enumerate(experiments):
        sub = summary_df[summary_df["experiment"] == exp_name]

        for _, row in sub.iterrows():
            it = row["iteration"]
            avr = row[metric_avr]
            std = row[metric_std] if not pd.isna(row[metric_std]) else 0

            # X-position for this experiment inside the iteration group
            center = iterations.index(it)
            left = center - group_width / 2 + exp_index * box_width

            # Rectangle geometry
            bottom = avr - std
            height = 2 * std

            # Avoid invisible zero-height boxes
            if height <= 0:
                height = 0.01
                bottom = avr - height / 2

            rect = Rectangle(
                (left, bottom),
                box_width,
                height,
                facecolor=palette[exp_index],
                alpha=0.55,
                edgecolor="black",
                linewidth=0.7,
            )
            ax.add_patch(rect)

            # Mean marker
            ax.plot(left + box_width / 2, avr, "o", markersize=4,
                    color="white", markeredgecolor="black")

    # ----- Axes -----
    ax.set_xticks(range(len(iterations)))
    ax.set_xticklabels(iterations, rotation=45)
    ax.set_xlabel("Iteration")
    ax.set_ylabel(y_label)
    # ax.set_title(f"{metric.upper()} vs Iteration (Grouped Boxes)")

    # ----- Legend -----
    legend_patches = [
        Rectangle((0, 0), 1, 1, facecolor=palette[i], edgecolor="black", alpha=0.55)
        for i in range(n_experiments)
    ]
    # ax.legend(legend_patches, experiments, title="Experiment",
    #           bbox_to_anchor=(1.02, 1), loc="upper left")
    
    # add legend inside top right, size reduced
    ax.legend(legend_patches, experiments, title="Experiment",
              loc="upper right", fontsize='x-small', title_fontsize='medium')
    
    

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    
    # save legend as a separate image
    plt.legend(legend_patches, experiments, title="Experiment")
    plt.savefig(os.path.join(output_filename.split("/")[0], "legend.png"), dpi=300)
    plt.close()
    
    print(f"✔ Saved {output_filename}")



def create_dummy_data(base_path: str):
    # This function remains unchanged...
    """Creates a dummy folder structure and data for demonstration."""
    print(f"Creating a dummy data structure at '{base_path}' for demonstration...")
    # (Dummy data creation code is omitted for brevity but is identical to the previous version)




def runIt():

    # --- Argument Parsing ---
    if len(sys.argv) != 3:
        print("Usage: python process_summarize_plot.py <main_data_folder> <output_directory>")
        print("Example: python process_summarize_plot.py outputHumanNonL Plot_Pareto_metrics/output_outputHumanNonL")
        sys.exit(1) # Exit the script if arguments are incorrect

    main_folder_path = sys.argv[1]
    output_dir = sys.argv[2]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Input data folder: {main_folder_path}")
    print(f"Output will be saved to: {output_dir}")

    # Create dummy data if main folder doesn't exist
    if not os.path.isdir(main_folder_path):
        print(f"The specified directory '{main_folder_path}' does not exist.")
        # create_dummy_data(main_folder_path) # You can uncomment this to generate test data

    combined_df = process_metrics_files(main_folder_path)
    time_df = process_time_files(main_folder_path)

    if not combined_df.empty:
        if not time_df.empty:
            merged_df = pd.merge(combined_df, time_df, on=['source_folder', 'experiment', 'iteration'], how='left')
        else:
            merged_df = combined_df.copy()
            merged_df['time'] = None

        # Construct full paths for output files
        combined_csv_path = os.path.join(output_dir, "combined_metrics_results.csv")
        merged_df.to_csv(combined_csv_path, index=False)
        print(f"\n✅ Saved the combined raw data to '{combined_csv_path}'")
        
        summary_dataframe = calculate_summary_stats(merged_df)

        if not summary_dataframe.empty:
            summary_csv_path = os.path.join(output_dir, "summary_statistics.csv")
            summary_dataframe.to_csv(summary_csv_path, index=False)
            print(f"✅ Saved the summary statistics to '{summary_csv_path}'")
            
            # --- Generate all four plots using the refactored function, saving to the new directory ---
            plot_metric(summary_dataframe, 
                        metric='IGD', 
                        y_label='Average IGD (Lower is Better)', 
                        output_filename=os.path.join(output_dir, 'IGD_vs_Iteration.png'))

            plot_metric(summary_dataframe, 
                        metric='GD', 
                        y_label='Average GD (Lower is Better)', 
                        output_filename=os.path.join(output_dir, 'GD_vs_Iteration.png'))
            
            plot_metric(summary_dataframe, 
                        metric='HV', 
                        y_label='Average HV (Higher is Better)', 
                        output_filename=os.path.join(output_dir, 'HV_vs_Iteration.png'))

            plot_metric(summary_dataframe, 
                        metric='time', 
                        y_label='Average Time (s)', 
                        output_filename=os.path.join(output_dir, 'Time_vs_Iteration.png'))



if __name__ == "__main__":

    # Run runIt() for each test case by setting sys.argv accordingly
    test_cases = [
        ('outputAgri_ChangeInjectedProp', 'plot_outputAgri_ChangeInjectedProp'),
        ('outputAgri_ChangeInjectedModel', 'plot_outputAgri_ChangeInjectedModel'),
        ('outputAgri_ChangeInjectedBoth', 'plot_outputAgri_ChangeInjectedBoth'),
        ('outputExpAgri_ChangeInjectedBoth', 'plot_outputExpAgri_ChangeInjectedBoth'),
        ('outputExpAgri_ChangeInjectedProp', 'plot_outputExpAgri_ChangeInjectedProp'),
        ('outputExpAgri_ChangeInjectedBoth', 'plot_outputExpAgri_ChangeInjectedBoth'),
        ('outputSanity', 'plot_outputSanity')
    ]

    for inp_dir, out_dir in test_cases:
        sys.argv = ['process_summarize_plot.py', inp_dir, out_dir]
        try:
            runIt()
        except Exception as e:
            print(f"Error running for ({inp_dir}, {out_dir}): {e}")
        runIt()