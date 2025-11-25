########################################
# Instructions:
# 1) Select get_only_PF_res = True in main() to only read PF results without running experiments again.
# 2) Run experiments examples by uncommenting sys.argv in the __main__ function.
#  Alternatively, from cmd:

# Testing FX example (note: no --changes file)
# python3 ./src/run.py --csv "viking_previous_tests/input/experimentsfxLarge.csv" --model "viking_previous_tests/input/FX/fxLarge.pm" --properties "viking_previous_tests/input/FX/fxLarge.pctl" --output "outputDummy/fxlarge_test" --optimisation "viking_previous_tests/input/optimisationList_fxLarge.txt"

# Testing Agricultural example
# python3 ./src/run.py --csv "input/experimentsAgricultural_iter.csv" --model "input/evomodel/AG/agricultural-humanNonLinear.pm" --properties "input/evomodel/AG/agricultural.pctl" --output "outputDummy_ChangeInjectedBoth/agricultural" --optimisation "input/optimisationList_agricultural.txt" --changes "input/evomodel/AG/agricultural_changes_injected.txt"

########################################
from experiments.experimentSet import ExperimentSet
import experiments.aux as aux
import experiments.workflow as workflow
from readexperiments.readResultsExperiments import read_experiment_results_and_save_metrics
import sys
from experiments.experimentsResults import ExperimentResults



def main():
    #>>>>>> Select whether to run experiments and read PF results, or only read results
    get_only_PF_res = False  
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    # ===============================================================
    # 1) Initialise experiment set
    # a) initialise paths
    csv_def_file, model_file, properties_file,output_folder, noSeedingBackup_folder, optimisation_list_file, change_list_file = aux.initialise_paths()    
    
    # b) remove output folder (if previous result folder exists)
    if not get_only_PF_res: aux.delete_folder(output_folder)

    # c) initialise experiment set class
    experiments = ExperimentSet(csv_def_file, output_folder, noSeedingBackup_folder, model_file, properties_file, change_list_file)
    
    # ===============================================================
    # 2) Run experiments
    if not get_only_PF_res: workflow.run_experiments_workflow(experiments)
    
    # ===============================================================
    # 3) Read experiment results and save metrics (DONE in run_experiments.py if required to be tested separately)
    save_all_data_df(experiments,"|NONE|")      #>>>> NOTE: pass string in folder to ignore in PF metrics, e.g. "|NONE|"
    read_experiment_results_and_save_metrics(output_folder, optimisation_list_file)


def save_all_data_df(experiments, str_folder_to_ignore_in_PF_metrics):
        ex = ExperimentResults(experiments)
        
if __name__ == "__main__":
    # If no arguments provided, run examples
    if len(sys.argv) == 1:  # no arguments passed, run example
        
        # Run example for fxLarge
        sys.argv = [
            "run.py",  # usually the script name
            "--csv", "viking_previous_tests/input/experimentsfxLarge.csv",
            "--model", "viking_previous_tests/input/FX/fxLarge.pm",
            "--properties", "viking_previous_tests/input/FX/fxLarge.pctl",
            "--output", "outputDummy/fxlarge_test",
            "--optimisation", "viking_previous_tests/input/optimisationList_fxLarge.txt"
        ]

        # # Run example for agricultural
        # sys.argv = [
        #     "run.py",  # script name
        #     "--csv", "viking_previous_tests/input/experimentsfxLarge.csv",
        #     "--model", "viking_previous_tests/input/FX/fxLarge.pm",
        #     "--properties", "viking_previous_tests/input/FX/fxLarge.pctl",
        #     "--output", "outputDummy/fxlarge_test",
        #     "--optimisation", "viking_previous_tests/input/optimisationList_fxLarge.txt"
        # ]

    main()
