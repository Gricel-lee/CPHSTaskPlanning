import os
from experiments.experimentSet import ExperimentSet
import experiments.aux as aux
import experiments.workflow as workflow
from readexperiments.readResultsExperiments import read_experiment_results_and_save_metrics


def initialise_paths():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # a) default paths examples (for quick testing)
    # FXLarge example paths
    csv_def = "viking_previous_tests/input/experimentsfxLarge.csv"
    model = "viking_previous_tests/input/FX/fxLarge.pm"
    properties = "viking_previous_tests/input/FX/fxLarge.pctl"
    output_folder = "output/fxlarge"
    optimisation_list_path = "viking_previous_tests/input/optimisationList_fxLarge.txt"
    change_list_file = None

    # Agricultural example paths
    csv_def = "input/experimentsAgricultural.csv"
    model = "input/evomodel/AG/agricultural-humanNonLinear.pm"
    properties = "input/evomodel/AG/agricultural.pctl"
    output_folder = "output/agricultural"
    optimisation_list_path = "input/optimisationList_agricultural.txt"
    change_list_file = "input/evomodel/AG/agricultural_changes_injected.txt"
    
    # b) override args from command line definitions
    directory, csv_def, output_folder, noSeedingBackup, optimisation_list_path, change_list_file = aux.read_args(directory, csv_def, output_folder, optimisation_list_path, model, properties, change_list_file)

    # check files exist
    aux.check_files_exist(csv_def, model, properties, optimisation_list_path, change_list_file)

    return directory, csv_def, model, properties, output_folder, noSeedingBackup, optimisation_list_path, change_list_file



def main():
    # ===============================================================
    # 1) Initialise experiment set
    # a) initialise paths
    directory, csv_def, model, properties, output_folder, noSeedingBackup, optimisation_list_path, change_list_file = initialise_paths()    
    # b) remove output folder (if previous result folder exists)
    aux.delete_folder(output_folder)
    # c) load experiments from CSV
    experiments = ExperimentSet(directory, csv_def, output_folder, noSeedingBackup, model, properties, change_list_file)
    
    # ===============================================================
    # 2) Run experiments
    workflow.run_experiments(experiments)
    
    # ===============================================================
    # 3) Read experiment results and save metrics
    read_experiment_results_and_save_metrics(directory, output_folder, optimisation_list_path)

if __name__ == "__main__":
    main()
