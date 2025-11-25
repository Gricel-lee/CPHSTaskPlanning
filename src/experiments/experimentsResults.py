import os
import pandas as pd
from experiments.experimentSet import ExperimentSet

class ExperimentResults:
    file_with_all_Pareto_results_paths =  ""
    files = []
    df_combined_data = pd.DataFrame()
    

    def __init__(self,  experiments: ExperimentSet, str_folder_to_ignore_in_PF_metrics: str = "|NONE|"):
        self.file_with_all_Pareto_results_paths  = experiments.file_with_all_Pareto_results_paths
        self.files = self._read_experiment_paths()
        self.str_folder_to_ignore_in_PF_metrics = str_folder_to_ignore_in_PF_metrics
        self.df_combined_data = self._read_all_experiment_pareto_front_data()
        self.save_df("combined_experiment_data.csv")
        
    def _read_experiment_paths(self):
        if not os.path.exists(self.file_with_all_Pareto_results_paths):
            print(f"[ERROR] The file {self.file_with_all_Pareto_results_paths} does not exist.")
            exit(1)
        with open(self.file_with_all_Pareto_results_paths, 'r') as file:
            self.files = [line.strip() for line in file if line.strip()]
        return self.files
    
    def _read_all_experiment_pareto_front_data(self):
        """
        Reads and concatenates all experiment files from the paths stored in self.files.
        Assumes each file has the same structure and tab-separated values.
        """
        all_experiment_data = []

        for file in self.files:
            if self.str_folder_to_ignore_in_PF_metrics in file:
                continue
            elif os.path.exists(file):
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