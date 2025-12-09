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

def calculate_summary_stats_latex(df: pd.DataFrame) -> pd.DataFrame:
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





def latex_table_metric(summary_df: pd.DataFrame, output_filename_ref: str):
    """
    Generates a LaTeX table for GD, HV, and IGD metrics for the first iteration only.
    Saves the .tex file in the same directory as the plot images.
    """
    # 1. Define output path based on the plot output path
    output_dir = os.path.dirname(output_filename_ref)
    table_path = os.path.join(output_dir, "table_first_iteration_metrics.tex")

    # 2. Filter data for the first iteration only (usually 0 or 1)
    if summary_df.empty:
        return
    
    first_iter = summary_df['iteration'].min()
    df_first = summary_df[summary_df['iteration'] == first_iter].copy()

    # 3. Sort the data using the existing 'experiment_key' logic
    # We apply the key to the experiment column to create a sortable index
    df_first['sort_idx'] = df_first['experiment'].apply(experiment_key)
    df_first = df_first.sort_values(by='sort_idx')

    # 4. Construct LaTeX content
    latex_lines = []
    latex_lines.append("\\begin{table}[ht]")
    latex_lines.append("\\centering")
    latex_lines.append(f"\\caption{{{output_filename_ref}Comparison of metrics at the first iteration (Iteration {first_iter}). Values are Mean $\\pm$ Std.}}")
    latex_lines.append("\\label{tab:init_metrics}")
    latex_lines.append("\\resizebox{\\textwidth}{!}{")
    latex_lines.append("\\begin{tabular}{l|ccc}")
    latex_lines.append("\\hline")
    latex_lines.append("\\textbf{Strategy} & \\textbf{GD} & \\textbf{HV} & \\textbf{IGD} \\\\")
    latex_lines.append("\\hline")

    for _, row in df_first.iterrows():
        # Escape special LaTeX characters in experiment names
        exp_name = str(row['experiment']).split("|")[1]  # Keep only the part after the first "|"
        exp_name = exp_name + str(row['experiment']).split("|")[2]  # Keep only the part after the first "|"
        exp_name = exp_name.replace("NONE2", "None")


        # Helper to safely format numbers
        def fmt(val, std):
            if pd.isna(val): return "N/A"
            s = 0.0 if pd.isna(std) else std
            return f"{val:.4f} $\\pm$ {s:.4f}"

        gd_str = fmt(row.get('GD_avr'), row.get('GD_std'))
        hv_str = fmt(row.get('HV_avr'), row.get('HV_std'))
        igd_str = fmt(row.get('IGD_avr'), row.get('IGD_std'))

        latex_lines.append(f"{exp_name} & {gd_str} & {hv_str} & {igd_str} \\\\")

    latex_lines.append("\\hline")
    latex_lines.append("\\end{tabular}")
    latex_lines.append("}")
    latex_lines.append("\\end{table}")
    
    latex_str = "\n".join(latex_lines)
    
    # Replace 

    # 5. Write to file
    try:
        with open(table_path, "w") as f:
            f.write(latex_str)
        print(f"   -> LaTeX table generated: {table_path}")
    except Exception as e:
        print(f"   -> Failed to write LaTeX table: {e}")





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
# removing 100 seeding for all-1
desired_order = [
        "NONE2|0",
        "Random|25",
        "KMeans|25",
        "FuzzyKMeans|25",
        "DBSCAN|25",
        "Random|100"
]
# Build a lookup index
order_index = {entry: i for i, entry in enumerate(desired_order)}

def experiment_key(exp):
    # Keep only the part after the first "|"
    parts = exp.split("|")
    algo_param = "|".join(parts[1:3])  # e.g., "DBSCAN|25"

    return order_index.get(algo_param, 9999)
########


# Define this once — a pattern per experiment
PATTERNS = [
    "",
    "////",      # diagonal
    "////",      # diagonal
    "...",      # dots
    "...",      # dots
    "xxx",      # cross hatch
    "xxx",      # cross hatch
    "\\\\",    # opposite diagonal
    "\\\\",    # opposite diagonal
]
PATTERNS = [
    "",
    "////",      # diagonal
    "////",      # diagonal
    "...",      # dots
    "...",      # dots
    "/",      # cross hatch
    "/",      # cross hatch
    "\\\\",    # opposite diagonal
    "\\\\",    # opposite diagonal
]
PATTERNS = [
    "",
    "",      # none
    "//",      # diagonal
    "",      # none
    "//",      # diagonal
    "",      # none
    "//",      # diagonal
    "",      # none
    "//",      # diagonal
]
# removing 100%
PATTERNS = [
    "",
    "",      # none
    "",      # none
    "",      # none
    "",      # none
    "",    # diagonal for 100%
]

GRAYS = ["#FFFFFF",
         "#FFFFFF","#666666",
         "#FFFFFF","#777777",
         "#FFFFFF","#777777",
         "#FFFFFF","#777777",
         "#FFFFFF","#777777"]
GRAYS = ["#ffffff",
           "#e9aae4","#e9aae4",
           "#97cc99","#97cc99",
           "#ffe119","#ffe119",
           "#8aa4ff","#8aa4ff"
           ]
# removing 100%
GRAYS = ["#ffffff",
           "#e9aae4",
           "#97cc99",
           "#ffe119",
           "#8aa4ff",
           "#ff9900"
           ]

import numpy as np

def plot_metric_boxplots(raw_df: pd.DataFrame, metric: str, y_label: str, output_filename: str):
    """
    Creates grouped boxplots:
        - X-axis = iterations
        - Each iteration group has N boxes (one per experiment)
        - Real quartile boxplots (no outliers)
        - Grayscale + hatching preserved per experiment
    """

    # ======= FILTER ITERATIONS =======
    # Filter to first two iterations AND iterations 5 and 10 only
    raw_df = raw_df[raw_df["iteration"].isin([1, 2, 5, 10])].copy()
    # raw_df = raw_df[raw_df["iteration"] <= 2].copy()
    
    # ======= FILTER DBSCAN|100, FuzzyKMeans|100, KMeans|100 =======
    # Filter columns where "experiment" contains |DBSCAN|100|
    raw_df = raw_df[~raw_df["experiment"].str.contains(r"\|DBSCAN\|100\|", regex=True, na=False)]
    # Filter columns where "experiment" contains |FuzzyKMeans|100|
    raw_df = raw_df[~raw_df["experiment"].str.contains(r"\|FuzzyKMeans\|100\|", regex=True, na=False)]
    # Filter columns where "experiment" contains |KMeans|100|
    raw_df = raw_df[~raw_df["experiment"].str.contains(r"\|KMeans\|100\|", regex=True, na=False)]
    
    
    if raw_df.empty:
        print(f"Cannot create boxplot for {metric.upper()}")
        return

    # Sort experiments with your ranking function
    raw_df["exp_sort"] = raw_df["experiment"].apply(experiment_key)
    experiments = sorted(raw_df["experiment"].unique(), key=experiment_key)
    iterations = sorted(raw_df["iteration"].unique())

    # Prepare color/hatch maps
    exp_to_color = {exp: GRAYS[i % len(GRAYS)] for i, exp in enumerate(experiments)}
    exp_to_hatch = {exp: PATTERNS[i % len(PATTERNS)] for i, exp in enumerate(experiments)}

    fig, ax = plt.subplots(figsize=(max(10, 1.2 * len(iterations)), 6))

    # Width settings
    group_width = 0.8                 # width each iteration group occupies
    box_width = group_width / len(experiments)

    # X positions for each iteration
    group_centers = np.arange(len(iterations))

    # Collect handles for legend
    legend_handles = []

    # For each experiment: place its boxes inside each iteration group
    for exp_idx, exp in enumerate(experiments):
        positions = group_centers - group_width/2 + exp_idx * box_width + box_width/2

        # box_data[i] = values for this experiment at iteration i
        box_data = []
        for it in iterations:
            values = raw_df[(raw_df["iteration"] == it) &
                            (raw_df["experiment"] == exp)][metric].dropna().values
            box_data.append(values if len(values) > 0 else [np.nan])

        # Draw boxplot for this experiment
        bp = ax.boxplot(
            box_data,
            positions=positions,
            widths=box_width * 0.9,
            patch_artist=True,
            showfliers=False
        )
        
        # Color medians red
        for median in bp['medians']:
            median.set_color("red")
            median.set_linewidth(1.5)


        # Style each box
        for patch in bp["boxes"]:
            patch.set_facecolor(exp_to_color[exp])
            patch.set_hatch(exp_to_hatch[exp])
            patch.set_edgecolor("black")
            patch.set_linewidth(1.1)

        # Store legend box
        legend_handles.append(
            Rectangle((0, 0), 1, 1, facecolor=exp_to_color[exp],
                      hatch=exp_to_hatch[exp], edgecolor='black')
        )
        

    
    
    # Axis formatting
    ax.set_xticks(group_centers)
    ax.set_xticklabels(iterations)
    # ax.set_xlabel("Iteration")
    # ax.set_title(y_label)
    # ax.set_ylabel(y_label)
    # ax.set_title(f"{metric.upper()} vs Iteration (Grouped Boxplot)")
    
    # Increase axis fonts
    ax.tick_params(axis='x', labelsize=12 + 5)
    ax.tick_params(axis='y', labelsize=12 + 5)
    ax.xaxis.label.set_size(14 + 8)
    ax.yaxis.label.set_size(14 + 8)
    # increase title font
    ax.title.set_size(16 + 10)

    # Legend
    plot_legend = False
    if plot_legend:
        ax.legend(legend_handles, experiments, title="Experiment",
                fontsize='x-small', title_fontsize='medium', loc='upper right')
    
    
    # Tighten x-limits in figure edges and box plot
    ax.set_xlim(-0.5, len(iterations) - 0.5)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()

    print(f"✔ Saved grouped boxplot {output_filename}")
    return output_filename



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
        
        summary_dataframe = calculate_summary_stats_latex(merged_df)

        if not summary_dataframe.empty:
            summary_csv_path = os.path.join(output_dir, "summary_statistics.csv")
            summary_dataframe.to_csv(summary_csv_path, index=False)
            print(f"✅ Saved the summary statistics to '{summary_csv_path}'")
            
            
            
            # [NEW] Generate the LaTeX table for the first iteration (will overwrite 4 times, ensuring it's up to date)
            latex_table_metric(summary_dataframe, output_dir)

            # --- Generate all four plots using the refactored function, saving to the new directory ---

            f1 = plot_metric_boxplots(merged_df, 
                        metric='HV', 
                        y_label='HV (Higher is Better)', 
                        output_filename=os.path.join(output_dir, 'HV_vs_Iteration.png'))
            f2 = plot_metric_boxplots(merged_df, 
                        metric='GD', 
                        y_label='GD (Lower is Better)', 
                        output_filename=os.path.join(output_dir, 'GD_vs_Iteration.png'))
            f3 = plot_metric_boxplots(merged_df, 
                        metric='IGD', 
                        y_label='IGD (Lower is Better)', 
                        output_filename=os.path.join(output_dir, 'IGD_vs_Iteration.png'))


            plot_metric_boxplots(merged_df, 
                        metric='time', 
                        y_label='Time (s)', 
                        output_filename=os.path.join(output_dir, 'Time_vs_Iteration.png'))


            # ---- Get images and joint them into one figure ----
            images = [f1, f2, f3]
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            for ax, img_path in zip(axes, images):
                img = plt.imread(img_path)
                ax.imshow(img)
                ax.axis('off')
            plt.tight_layout()
            # Reduce space between images
            plt.subplots_adjust(wspace=0.0, hspace=0)  
            combined_image_path = os.path.join(output_dir, 'Combined_Metrics_vs_Iteration.png')
            # plt.savefig(combined_image_path, dpi=300)
            plt.savefig(combined_image_path, dpi=300, bbox_inches='tight', pad_inches=0)

            plt.close()
            print(f"✔ Saved combined metrics image {combined_image_path}")


if __name__ == "__main__":

    # Run runIt() for each test case by setting sys.argv accordingly
    test_cases = [
        ('outputExpAgri_ChangeInjectedPropMin', 'plot_outputExpAgri_ChangeInjectedPropMin'),
        # ('outputAgri_ChangeInjectedProp', 'plot_outputAgri_ChangeInjectedProp'),
        # ('outputAgri_ChangeInjectedModel', 'plot_outputAgri_ChangeInjectedModel'),
        # ('outputAgri_ChangeInjectedBoth', 'plot_outputAgri_ChangeInjectedBoth'),
        ('outputExpAgri_ChangeInjectedProp', 'plot_outputExpAgri_ChangeInjectedProp'),
        ('outputExpAgri_ChangeInjectedBoth', 'plot_outputExpAgri_ChangeInjectedBoth'),
        ('outputExpAgri_ChangeInjectedModel', 'plot_outputExpAgri_ChangeInjectedModel'),
        ('outputSanity', 'plot_outputSanity')
    ]
    
    # Construction
    # test_cases = [
    #     ('outputExpCon_ChangInjPropMin', 'plot_outputExpCon_ChangInjPropMin')
    # ]
    test_cases = [
        ('outputExpCon_ChangInjPropLarge', 'plot_outputExpCon_ChangInjPropLarge')
    ]

    for inp_dir, out_dir in test_cases:
        sys.argv = ['process_summarize_plot.py', inp_dir, out_dir]
        runIt()