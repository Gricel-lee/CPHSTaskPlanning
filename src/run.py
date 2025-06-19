import os
from experiments.experimentSet import ExperimentSet
import experiments.aux as aux
import experiments.workflow as workflow
from readexperiments.readResultsExperiments import read_experiment_results_and_save_metrics

def main():
    # 1) Set up ---------------------------
    # a) default paths
    dirr = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # FXLarge example paths
    csv_def = "input/experimentsfxLarge.csv"
    model = "input/evomodel/FX/fxLarge.pm"
    properties = "input/evomodel/FX/fxLarge.pctl"
    output_folder = "output/fxlarge"
    optimisation_list = "input/optimisationList_fxLarge.txt"
    
    # Agricultural example paths
    csv_def = "input/experimentsAgricultural.csv"
    model = "input/evomodel/AG/agricultural.pm"
    properties = "input/evomodel/AG/agricultural.pctl"
    output_folder = "output/agricultural"
    optimisation_list = "input/optimisationList_agricultural.txt"
    
    
    # override args from command line
    dirr, csv_def, output_folder, noSeedingBackup, optimisation_list = aux.read_args(dirr, csv_def, output_folder, optimisation_list, model, properties)
    
    # check files exist
    aux.check_files_exist(csv_def, model, properties, optimisation_list)
    
    # b) remove previous initial seeding backup folder
    aux.delete_folder(output_folder)
    
    
    # 2) Load experiments from CSV---------------------------
    experiments = ExperimentSet(dirr, csv_def, output_folder, noSeedingBackup, model, properties)
    
    
    # ===============================================================
    # 3) Run experiments ---------------------------
    workflow.run_experiments(experiments)
    
    # 4) Read experiment results and save metrics ---------------------------
    read_experiment_results_and_save_metrics(dirr, output_folder, optimisation_list)

if __name__ == "__main__":
    main()
