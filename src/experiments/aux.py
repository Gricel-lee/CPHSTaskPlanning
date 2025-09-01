import os
import sys
import argparse
import pandas as pd
# import config
import shutil
import os
import sys

def read_csv_file(file_path):
    """
    Read a CSV file and return its contents as a Pandas DataFrame.
    """
    data = pd.read_csv(file_path)
    return data


def check_files_exist(csv_def, model, properties, optimisation_list):
    # check that files exists csv_def, model, properties, optimisation_list
    if not os.path.isfile(csv_def):
        print(f"[ARGS] CSV file {csv_def} does not exist. Exiting.")
        exit(1)
    if not os.path.isfile(model):
        print(f"[ARGS] EvoChecker model file {model} does not exist. Exiting.")
        exit(1)
    if not os.path.isfile(properties):
        print(f"[ARGS] EvoChecker properties file {properties} does not exist. Exiting.")
        exit(1)
    if not os.path.isfile(optimisation_list):
        print(f"[ARGS] Optimisation list file {optimisation_list} does not exist. Exiting.")
        exit(1)


def create_config_props_file(experiment:'Experiment',experiments:'ExperimentSet'):
    s = ""
    s += f"PROBLEM = {experiment.case}\n"
    s += f"MODEL_TEMPLATE_FILE = models/{experiments.evocheckerModel}\n"
    
    s += f"PROPERTIES_FILE = models/{experiments.evocheckerProps}\n"
    s += f"ALGORITHM = {experiment.moga}\n"
    s += f"POPULATION_SIZE = {experiment.population}\n"
    s += f"MAX_EVALUATIONS = {experiment.evaluations}\n"
    s += f"PROCESSORS = 1\n"
    s += f"INIT_PORT = 8860\n"
    s += f"MODEL_CHECKING_ENGINE_LIBS_DIRECTORY = libs/runtime\n"
    s += f"PLOT_PARETO_FRONT = FALSE\n"
    s += f"PYTHON3_DIRECTORY = /usr/bin/python3\n"
    s += f"VERBOSE = FALSE\n"
    s += f"EVOCHECKER_TYPE = NORMAL\n"
    s += f"EVOCHECKER_ENGINE = PRISM\n"
    
    s += f"# Select percentage of previous population to re-use\n"
    s += f"SEED_PERCENTAGE = {experiment.percentage}\n"
    s += f"# Type of reload: RANDOM | KMEANS |  FUZZYKMEANS | DBSCAN\n"
    if experiment.seeding == "NONE":
        s += f"# SEED_TYPE = NONE\n"
    else:
        s += f"SEED_TYPE = {experiment.seeding}\n"
    s += f"# Seed cluster strategy using the previous Pareto front or set or both: FRONT | SET | BOTH\n"
    s += f"SEED_CLUSTER_FROM_PARETO = {experiment.dataPareto}\n"
    s += f"# If KMEANS\n"
    s += f"SEED_KMEANS_ITERATIONS = {experiment.kMeanIterations}\n"
    s += f"# If FUZZYKMEANS\n"
    s += f"SEED_FUZZINESS = {experiment.fuzziness}\n"
    s += f"# If DBSCAN\n"
    s += f"SEED_DBSCAN_EPS = {experiment.epsilon}\n"
    s += f"SEED_DBSCAN_MINPTS = {experiment.nMinPerCluster}\n"
    s += f"# Save Pareto set/front every N>1 iterations (total iterations = evaluations/population)\n"
    s += f"SAVE_PARETO_EVERY_N_ITERATIONS = 1\n"
    
    # NOTE: Deletes the output folder if it already exists
    if os.path.exists(experiment.output_experiment_folder):
        shutil.rmtree(experiment.output_experiment_folder)
        
    # create the output folder if it doesn't exist
    if not os.path.exists(experiment.output_experiment_folder):
        os.makedirs(experiment.output_experiment_folder)
        
    # save the config file
    cf = f"{experiment.output_experiment_folder}/config.properties"
    print(f"[CONFIG] Config file: {cf}")
    with open(f"{cf}", "w") as f:
        f.write(s)
    return cf






def read_args(directory, csv_def, output_folder, optimisation_list, model, properties):    
    # Read command line arguments
    parser = argparse.ArgumentParser(description="Run experiment.")
    parser.add_argument(
        "--dir", type=str, default=directory, help="Path to directory"
    )
    parser.add_argument(
        "--csv", type=str, default=csv_def, help="Path to the experiments CSV file"
    )
    parser.add_argument(
        "--model", type=str, default=model, help="Path to the EvoChecker model file"
    )
    parser.add_argument(
        "--properties", type=str, default=properties, help="Path to the EvoChecker properties file"
    )
    parser.add_argument(
        "--output", type=str, default=output_folder, help="Path to the output folder"
    )
    parser.add_argument(
        "--optimisation", type=str, default=optimisation_list, help="Path to the optimisation list file"
    )
    
    # Save the arguments
    args = parser.parse_args()
    # --dir
    if args.dir is not None:
        directory = args.dir
    # -- csv file
    if args.csv is not None:
        csv_def = args.csv
    # -- out folder
    if args.output is not None:
        output_folder = args.output
    # -- evo files
    if args.model is not None:
        model = args.model
    if args.properties is not None:
        properties = args.properties
    if args.optimisation is not None:
        optimisation_list = args.optimisation
    
    # Get paths
    # -- csv file
    csv_def = os.path.join(directory, csv_def)
    # check if the file exists
    if not os.path.isfile(csv_def):
        print(f"[ARGS] CSV file {csv_def} does not exist. Exiting.")
        sys.exit(1)
    # -- output folder
    output_folder = os.path.join(directory, output_folder)
    make_folder(output_folder)
    # -- no seeding backup folder
    noSeedingBackup = os.path.join(directory, output_folder+"/previousPopulation")
    make_folder(noSeedingBackup)

    if True:
        print(f"[ARGS] Directory: {directory}")
        print(f"[ARGS] CSV default file: {csv_def}")
        print(f"[ARGS] Output folder: {output_folder}")
        print(f"[ARGS] Seeding folder: {noSeedingBackup}")
        
    return directory, csv_def, output_folder, noSeedingBackup, optimisation_list


def delete_folder(folder):
    """
    Recursively delete a folder and all its contents.
    """
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Deleted folder: {folder}")
    else:
        print(f"Folder does not exist: {folder}")


def copy_folder_recursive(src, dst):
    if not os.path.exists(src):
        print(f"Source folder does not exist: {src}")
        return

    if not os.path.isdir(src):
        print(f"Source is not a directory: {src}")
        return

    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dst, item)
        # print(f"Copying {s_item} to {d_item}")
        if os.path.isdir(s_item):
            copy_folder_recursive(s_item, d_item)  # recurse
        else:
            shutil.copy2(s_item, d_item)  # copy file with metadata

    # print(f"Copied all contents from {src} to {dst}")

def copy_folder_recursive_ignoreSome(src, dst, ignore_files_with_prefix="prev_"):
    if not os.path.exists(src):
        print(f"Source folder does not exist: {src}")
        return

    if not os.path.isdir(src):
        print(f"Source is not a directory: {src}")
        return

    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        # print(f"Item>>: {item}")
        if not item.startswith(ignore_files_with_prefix):
            # print(f"yes >>: {item}")
            s_item = os.path.join(src, item)
            d_item = os.path.join(dst, item)
            # print(f"Copying {s_item} to {d_item}")
            if os.path.isdir(s_item):
                copy_folder_recursive(s_item, d_item)  # recurse
            else:
                shutil.copy2(s_item, d_item)  # copy file with metadata



def rename_files_with_prefix(folder_path, prefix):
    """
    Renames all files in the specified folder by adding 'prev_' to the beginning of each filename.

    Args:
        folder_path (str): The path to the folder containing the files to rename.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            new_filename = f"{prefix}{filename}"
            new_file_path = os.path.join(folder_path, new_filename)

            os.rename(file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

# Example usage:
# rename_files_with_prev("/path/to/your/folder")




def make_folder(folder):
    """
    Create a folder if it doesn't exist.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        print(f"Folder already exists: {folder}")



def copy_file(src, dst):
    if not os.path.isfile(src):
        print(f"Source file does not exist: {src}")
        sys.exit(1)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
    shutil.copy2(src, dst)  # copy file with metadata
    # print(f"Copied {src} to {dst}")
    

def append_to_file(filePath, appendString):
    '''Append to file or create it if missing'''
    print("filePath", filePath)
    with open(filePath, 'a') as f:
        f.write(appendString)
        
        
        
def get_files_in_folder(folderPath):
    front_files = []
    for filename in os.listdir(folderPath):
        full_path = os.path.join(folderPath, filename)
        if os.path.isfile(full_path):  # optional: only include files
            front_files.append(full_path)
    return front_files
