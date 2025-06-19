import os
from experiments.experimentSet import ExperimentSet
import experiments.aux as aux
import experiments.workflow as workflow
from readexperiments.readResultsExperiments import read_experiment_results_and_save_metrics

def main():
    # 1) Set up ---------------------------
    # a) set up paths
    # default paths
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_def = "input/experiments.csv"
    model = "input/evomodel/FX/fxLarge.pm"
    properties = "input/evomodel/FX/fxLarge.pctl"
    output_folder = "output/experiments"
    optimisation_list = "input/optimisationList.txt"
    
    # override args from command line
    dir, csv_def, output_folder, noSeedingBackup = aux.read_args(dir, csv_def, output_folder, model, properties)
    
    
    # b) remove previous initial seeding backup folder
    aux.delete_folder(output_folder)
    
    
    # 2) Load experiments from CSV---------------------------
    experiments = ExperimentSet(dir, csv_def, output_folder, noSeedingBackup, model, properties)
    
    
    # ===============================================================
    # 3) Run experiments ---------------------------
    workflow.run_experiments(experiments)
    
    # 4) Read experiment results and save metrics ---------------------------
    read_experiment_results_and_save_metrics(dir, output_folder, optimisation_list)

if __name__ == "__main__":
    main()
