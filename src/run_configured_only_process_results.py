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
    get_only_PF_res = True  
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
    #>>>> NOTE: the combined_experiment_data.csv file is created in Viking!!
    # 3) Read experiment results (save all PF data points into single CSV "combined_experiment_data.csv"
    save_all_data_df(experiments)      
    
    # 4) Read experiment results and save metrics (DONE in run_experiments.py if required to be tested separately) , exclude |NONE| results
    read_experiment_results_and_save_metrics(output_folder, optimisation_list_file, "|NONE|")


def save_all_data_df(experiments):
    # Save all data points from all experiments into a single CSV file combined_experiment_data.csv
    # ignores |NONE| folder experiments (used for seeding)
    ex = ExperimentResults(experiments)



def get_immediate_subdirectories(a_dir):
    import os
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
    
            
if __name__ == "__main__":
    ''' Run to obtain PF indicators from Viking generated data folders '''
    
    # If no arguments provided, run examples
    if len(sys.argv) == 1:  # no arguments passed, run example
        
        # # Run example
        # sys.argv = [
        #     "run.py",  # script name
        #     "--csv", "viking_previous_tests/input/experimentsfxLarge.csv",
        #     "--model", "viking_previous_tests/input/FX/fxLarge.pm",
        #     "--properties", "viking_previous_tests/input/FX/fxLarge.pctl",
        #     "--output", "outputDummy/fxlarge_test",
        #     "--optimisation", "viking_previous_tests/input/optimisationList_fxLarge.txt"
        # ]
        
        # Construction example
        sys.argv = [
            "run.py",  # script name
            "--csv", "RQ1/Construction/experiment_files/experiments_iter_25_50.csv",
            "--model", "RQ1/Construction/ARCH_input/evomodel/datamodelEvo.prism",
            "--properties", "RQ1/Construction/ARCH_input/evomodel/datamodelEvo.props",
            "--output", "outputExpCon_ChangInjPropMin/construction3",
            "--optimisation", "RQ1/Construction/experiment_files/optimisationList_construction.txt",
            "--changes", "RQ1/Construction/experiment_files/change_injected_in_prop_minimum.txt"
        ]
        main()
        
        
        # for select in [0,1,2]: # [0, 1, 2]: # 0: both changes injected, 1: only properties changes injected, 2: only model changes injected
            
        #     # >>>>>> Select batch <<<<
        #     # Second batch "ExpAgri"
        #     experiment_folder = ["outputExpAgri_ChangeInjectedBoth",
        #                         "outputExpAgri_ChangeInjectedProp",
        #                         "outputExpAgri_ChangeInjectedModel"][select]
            
            
        #     # First batch "Agri" (sanity tests) -- note: only run it for select in [0], or leave it as it is (three times the same experiment)
        #     experiment_folder = ["outputExpAgri_ChangeInjectedPropMin",
        #                         "outputSanity",
        #                         "outputSanity"][select]
            
            
            
            
        #     # Shared files
        #     change_file = ["input/evomodel/AG/agricultural_changes_injected.txt",
        #                 "input/evomodel/AG/agricultural_changes_injected_in_prop.txt",
        #                 "input/evomodel/AG/agricultural_changes_injected_in_model.txt"][select]
            
        #     print(experiment_folder)
        #     print(change_file)
            
        #     # get subfolders in experiment folder
        #     subfolders = get_immediate_subdirectories(experiment_folder)
        #     print("Subfolders found:", subfolders)

        #     # Run for each agricultural change experiment, 
        #     for i in subfolders:
        #         print(f"{experiment_folder}/{i}")
        #         sys.argv = [
        #             "run.py",  # script name
        #             "--csv", "input/experimentsAgricultural_iter.csv",
        #             "--model", "input/evomodel/AG/agricultural-humanNonLinear.pm",
        #             "--properties", "input/evomodel/AG/agricultural.pctl",
        #             "--output", f"{experiment_folder}/{i}", # e.g.: outputExpAgri_ChangeInjectedBoth/agricultural1
        #             "--optimisation", "input/optimisationList_agricultural.txt",
        #             "--changes", change_file
        #         ]
        #         main()


