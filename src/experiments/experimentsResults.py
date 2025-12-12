import os
import pandas as pd
from experiments.experimentSet import ExperimentSet

class ExperimentResults:
    file_with_all_Pareto_results_paths =  ""
    list_all_pareto_files_paths = []
    df_combined_data = pd.DataFrame()
    

    def __init__(self,  experiments: ExperimentSet):
        self.file_with_all_Pareto_results_paths  = experiments.file_with_all_Pareto_results_paths
        # Get list of paths to all Pareto front result files
        self.list_all_pareto_files_paths = self._read_experiment_paths()
        # Read and combine all experiment Pareto front data (except those to ignore)
        self.df_combined_data = self._read_raw_data_all_experiment_pareto_fronts()
        # Save combined data to CSV
        self.save_df("combined_experiment_data.csv")
        
    def _read_experiment_paths(self):
        if not os.path.exists(self.file_with_all_Pareto_results_paths):
            print(f"[ERROR] The file {self.file_with_all_Pareto_results_paths} does not exist.")
            exit(1)
        with open(self.file_with_all_Pareto_results_paths, 'r') as file:
            self.list_all_pareto_files_paths = [line.strip() for line in file if line.strip()]
        return self.list_all_pareto_files_paths
    
    def _read_raw_data_all_experiment_pareto_fronts(self):
        """
        Reads and concatenates all experiment files from the paths stored in self.files.
        Assumes each file has the same structure and tab-separated values.
        """
        all_experiment_data = []

        for file in self.list_all_pareto_files_paths:
            if os.path.exists(file):
                try:
                    data = pd.read_csv(file, sep='\t', header=0)
                    #data['source_file'] = os.path.basename(file)
                    data['experiment'] = file  # optional: add an experiment ID
                    all_experiment_data.append(data)
                except Exception as e:
                    print(f"[ERROR] Failed to read {file}: {e}")
            else:
                print(f"[ERROR] The file {file} does not exist.")

        if all_experiment_data:
            df_combined_data = pd.concat(all_experiment_data, ignore_index=True)
        else:
            df_combined_data = pd.DataFrame()
        
        return df_combined_data

    def save_df(self, file_name):
        """
        Saves the combined DataFrame to a CSV file.
        """
        if self.df_combined_data.empty:
            print("[ERROR] No data available to save.")
            return

        f = os.path.dirname(self.file_with_all_Pareto_results_paths)
        self.df_combined_data.to_csv(os.path.join(os.path.abspath(f), file_name), index=False)
        print(f"[INFO] Data saved to {file_name} in {f}")
        
    
# --- For tests  ---
# def _read_args(filePath):
#     """
#     Reads command line arguments for the file path.
#     """
#     import argparse
#     parser = argparse.ArgumentParser(description="Read experiments.")
#     parser.add_argument(
#         "--file", type=str, default=filePath, help="Path to the file containing experiment paths"
#     )

#     args = parser.parse_args()
#     # --file
#     if args.file is not None:
#         filePath = args.file
    
#     return filePath
    

# if __name__ == "__main__":
#     filePath="/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/output/experiments/resPaths.txt"
    
#     # read --file
#     filePath = _read_args(filePath)
    
#     exp = ExperimentResults(filePath)
# ----------------------