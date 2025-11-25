import experiments.aux as aux
import os
import subprocess
from experiments.experimentSet import ExperimentSet


def run_experiments_workflow(experiments: ExperimentSet):
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
        
        # c) copy evochecker model and props
        tempM = os.path.join(experiments.get(i).temp_folder, "models/"+experiments.evocheckerModel)
        tempP = os.path.join(experiments.get(i).temp_folder, "models/"+experiments.evocheckerProps)
        print(f"[CP] Copying EvoChecker model {experiments.model} to {tempM}")
        print(f"[CP] Copying EvoChecker properties {experiments.properties} to {tempP}")
        aux.copy_file(experiments.model, tempM)
        aux.copy_file(experiments.properties, tempP)
        
        # d) inject changes modifying the model or properties file from change_list
        for (s_original, (s_changed, injected_change)) in experiments.change_list.items():
            if (i != 0) and injected_change!="none":
                # determine which file to modify
                if (i != 0) and injected_change=="properties":
                    temp_file = tempP
                elif (i != 0) and injected_change=="model":
                    temp_file = tempM
                # read, replace and save file
                s = aux.read_file_as_string(temp_file)
                s = s.replace(s_original, s_changed)
                with open(temp_file, "w") as f:
                    f.write(s)
                print(f"[INJ_CHANGE] Injected change into {temp_file} file: {s_original} -> {s_changed}")
        
        
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
        print(f"[CP] Copying EvoChecker config {conf} to {tempC}") # only make a copy into temp/target folder (to excecute EvoChecker.jar)

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
        aux.copy_folder_recursive_ignoreSome(tempResults, results) # ignore if start with "prev_" as this are the previous population files
        
        # ------ comment out to keep all EvoChecker temp data ------
        # delete unnecesary folders from the EvoChecker run
        folders = ["classes/", "libs/", "maven-archiver/", "maven-status/", "scripts/", "surefire-reports/", "test-classes/"]
        for folder in folders:
            tempOtherData = os.path.join(experiments.get(i).temp_folder, folder)
            aux.delete_folder(tempOtherData)
        tempOtherData = os.path.join(experiments.get(i).temp_folder, "EvoChecker-1.1.1.jar")
        aux.delete_file(tempOtherData)
        tempOtherData = os.path.join(experiments.get(i).temp_folder, "EvoChecker-1.1.1.zip")
        aux.delete_file(tempOtherData)
        # ------------------------------------------------------------
        

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
        for f in files_pareto_fronts:
            aux.append_to_file(experiments.file_with_all_Pareto_results_paths,f+"\n")
    return 



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


