import aux
import os

# def run_experiments(experiments):
    
    # Load initial population (first experiment)
    # load_init_pop(experiments)

    # # Run the experiment
    # experiment.run()

    # # Save the results
    # experiment.save_results()

    # # Print the results
    # experiment.print_results()




def run_experiments(experiments):
    """
    Run the experiment workflow.
    """
    
    for (i, experiment) in enumerate(experiments.experiment_list):    
        print(f"[EXP] Experiment {i}: {experiments.get(i)}")
        # a) create new folder and config.props file
        experiments.get(i).create_folder_and_files(experiments)
        
        # b) Create EvoChecker instance
        evo = os.path.join(experiments.dir, "EvoCheckerInJAR/target")
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
        import subprocess
        
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
        
        # g) delete temp folder
        # temp = experiments.get(i).temp_folder
        # aux.delete_folder(temp)
        