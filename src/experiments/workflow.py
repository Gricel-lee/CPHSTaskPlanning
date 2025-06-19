import experiments.aux as aux
import os
import subprocess
from experiments.experimentsResults import ExperimentResults


def run_experiments(experiments):
    f = run_exp_workflow(experiments)
    save_all_data_df(f)

def save_all_data_df(f):
        ex = ExperimentResults(f)


def run_exp_workflow(experiments):
    """
    Run the experiment workflow.
    """    
    for (i, experiment) in enumerate(experiments.experiment_list):    
        print(f"[EXP] Experiment {i}: {experiments.get(i)}")
        
        # a) create config.props file and output folder
        experiments.get(i).create_folder_and_config_file(experiments)
        
        # b) Create EvoChecker instance
        evo = os.path.join(experiments.dir, "EvoChecker/target")
        temp = experiments.get(i).temp_folder
        print(f"[CP] Copying EvoChecker {evo} folder to {temp}")
        aux.copy_folder_recursive(evo,temp)  
        
        # copy evochecker model and props
        tempM = os.path.join(experiments.get(i).temp_folder, "models/"+experiments.evocheckerModel)
        tempP = os.path.join(experiments.get(i).temp_folder, "models/"+experiments.evocheckerProps)
        print(f"[CP] Copying EvoChecker model {experiments.model} to {tempM}")
        print(f"[CP] Copying EvoChecker properties {experiments.properties} to {tempP}")
        aux.copy_file(experiments.model, tempM)
        aux.copy_file(experiments.properties, tempP)
        
        # copy initial population
        if (i != 0):
            # copy files from backup
            backup = experiments.noSeedingBackup
            tempResults = os.path.join(experiments.get(i).temp_folder, "data/"+experiments.get(i).case+"/"+experiments.get(i).moga+"/")
            print(f"[CP] Copying EvoChecker results {backup} to {tempResults}")
            aux.copy_folder_recursive(backup, tempResults)
        
        # d) copy config and properties
        conf = experiments.get(i).configFile
        tempC = os.path.join(experiments.get(i).output_experiment_folder, "temp/target/config.properties")
        aux.copy_file(conf , tempC)
        print(f"[CP] Copying EvoChecker config {conf} to {tempC}")
        
        # e) run EvoChecker
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "libs/runtime"
        # Run the Java JAR and wait for it to complete
        process = subprocess.run(
            ["java", "-jar", "EvoChecker-1.1.1.jar"],
            env=env,
            cwd=experiments.get(i).temp_folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Print the output
        print(process.stdout.decode())
        print(process.stderr.decode())
        
        # Check the result code
        if process.returncode == 0:
            print("EvoChecker finished successfully.")
        else:
            print(f"EvoChecker exited with code {process.returncode}.")
        
        # f) Copy results to experiment folder 
        tempResults = os.path.join(experiments.get(i).temp_folder, "data/"+experiments.get(i).case+"/"+experiments.get(i).moga+"/")
        results = experiments.get(i).res_folder
        print(f"[CP] Copying EvoChecker results {tempResults} to {results}")
        aux.copy_folder_recursive_ignoreSome(tempResults, results)
        
        # g) backup results from No seeding (and rename to distinguish)
        if (i == 0):
            backup = experiments.noSeedingBackup
            aux.copy_folder_recursive(results, backup)
            aux.rename_files_with_prefix(backup, "prev_")
        
        # h) delete temp folder (or some large files)
        # temp = experiments.get(i).temp_folder
        # aux.delete_folder(temp)
        
        # i) Save all result file paths as a single file
        files_pareto_fronts = get_sorted_front_files(results)
        file_res_paths = os.path.join(experiments.output_folder, "resPaths.txt")
        for f in files_pareto_fronts:
            aux.append_to_file(file_res_paths,f+"\n")
        
    return file_res_paths



def get_sorted_front_files(folder_path):
    """
    Reads all files ending in 'Front' in the given folder,
    and returns them sorted by creation time (oldest to newest).
    """
    files = aux.get_files_in_folder(folder_path)
    files_front_ordered = []
    exists = True;
    i = 1;
    while exists:
        file_i = ""
        for f in files:
            if f.endswith(f"_{i}_Front"):
                file_i = f
        if file_i=="":
            exists=False
            break
        else:
            files_front_ordered.append(file_i)
            i+=1
    return files_front_ordered


