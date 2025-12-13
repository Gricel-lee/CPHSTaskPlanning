import sys
import os

s = '''#!/usr/bin/env bash
#SBATCH --job-name=<REPLACE FOR JOB NAME>               # Job name
#SBATCH --partition=nodes               # What partition the job should run on
#SBATCH --time=0-40:15:00               # Time limit (DD-HH:MM:SS)
#SBATCH --ntasks=1                      # Number of MPI tasks to request
#SBATCH --cpus-per-task=9               # Number of CPU cores per MPI task
#SBATCH --mem=40G                       # Total memory to request
#SBATCH --account=cs-ai4work-2025       # Project account to use
#SBATCH --mail-type=END,FAIL,ALL        # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=gricel.vazquez@york.ac.uk   # Where to send mail
#SBATCH --output=%x-%j.log              # Standard output log
#SBATCH --error=%x-%j.err               # Standard error log

# Abort if any command fails
set -e

# Purge any previously loaded modules
module purge

# Load modules
module load Python/3.11.3-GCCcore-12.3.0
module load Java/11.0.20
#module load compiler/GCC/8.2.0-2.31.1
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/users/gnvf500/scratch/CPHSTaskPlanning/EvoChecker/libs/runtime
export LD_LIBRARY_PATH
echo "$LD_LIBRARY_PATH"
#java -jar EvoChecker.jar config.properties


# Commands to run
pip3 install pandas
pip3 install pymoo

# 1 experiments for agricultural model
python3 ./src/run.py --csv "<REPLACE_CSV_FILE>" --model "<REPLACE_MODEL_FILE>" --properties "<REPLACE_PROPERTIES_FILE>" --output "<REPLACE_OUTPUT_FOLDER_AND_EXPERIMENT_SUBFOLDER>" --optimisation "<REPLACE_OPTIMISATION_FILE>" --changes "<REPLACE_CHANGES_FILE>"
'''





# ===========================================================================================

def create_job_files():
    numbering_experiments = [1,2,3,4,5,6,7,8,9,10]               #,11,12,13,14,15,16,17,18,19,20]

    # read from sys arguments
    csv_file = sys.argv[2]
    model_file = sys.argv[4]
    properties_file = sys.argv[6]
    output = sys.argv[8]
    optimisation_file= sys.argv[10]
    file_injected_change = sys.argv[12]


    for num in numbering_experiments:
        name = name_job_file  + str(num)
        # Create job script file
        with open("jobscript_" + name + ".job", "w") as f:
            # replace placeholders
            s_new = s.replace("<REPLACE FOR JOB NAME>", name)
            s_new = s_new.replace("<REPLACE_CSV_FILE>", csv_file) 
            s_new = s_new.replace("<REPLACE_MODEL_FILE>", model_file)
            s_new = s_new.replace("<REPLACE_PROPERTIES_FILE>", properties_file)
            s_new = s_new.replace("<REPLACE_OUTPUT_FOLDER_AND_EXPERIMENT_SUBFOLDER>", f"{output}{num}")
            s_new = s_new.replace("<REPLACE_OPTIMISATION_FILE>", optimisation_file)
            s_new = s_new.replace("<REPLACE_CHANGES_FILE>", file_injected_change)
            
            # write to file
            f.write(s_new)
            
    # Create single .sh to launch all jobs
    with open("launch_all_jobs_" + name_job_file + ".sh", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        for num in numbering_experiments:
            name = name_job_file  + str(num)
            f.write(f"echo 'Submitting jobscript_{name}.job'\n")
            f.write(f"sbatch jobscript_{name}.job\n")

    # make it executable (chmod +x submit_10.sh)

    os.chmod("launch_all_jobs_" + name_job_file + ".sh", 0o755)
    


# ===================== Set experiments to create job files ===========================

#======================== Agricultural model experiments ========================
# Input:
name_job_file = "ExpDummy"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ1/Agricultural/experiment_files/dummy.csv",
            "--model", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural-humanNonLinear.pm",
            "--properties", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural.pctl",
            "--output", f"outputDummy/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ1/Agricultural/experiment_files/optimisationList_agricultural.txt",
            "--changes", "assets/RQ1/Agricultural/experiment_files/changes_injected/agricultural_changes_injected_in_prop_minimum.txt"#<<<
        ]
# create_job_files()

# Input:
name_job_file = "ExpAgricultural_None"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ1/Agricultural/experiment_files/experimentsAgricultural_iter_25_100.csv",
            "--model", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural-humanNonLinear.pm",
            "--properties", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural.pctl",
            "--output", f"outputExpAgricultural_None/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ1/Agricultural/experiment_files/optimisationList_agricultural.txt",
            "--changes", "assets/RQ1/Agricultural/experiment_files/changes_injected/agricultural_changes_injected_NONE.txt"#<<<
        ]
# create_job_files()

# Input:
name_job_file = "ExpAgricultural_PropMin"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ1/Agricultural/experiment_files/experimentsAgricultural_iter_25_100.csv",
            "--model", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural-humanNonLinear.pm",
            "--properties", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural.pctl",
            "--output", f"outputExpAgricultural_PropMin/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ1/Agricultural/experiment_files/optimisationList_agricultural.txt",
            "--changes", "assets/RQ1/Agricultural/experiment_files/changes_injected/agricultural_changes_injected_in_prop_minimum.txt"#<<<
        ]
# create_job_files()

# Input:
name_job_file = "ExpAgricultural_PropLarge"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ1/Agricultural/experiment_files/experimentsAgricultural_iter_25_100.csv",
            "--model", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural-humanNonLinear.pm",
            "--properties", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural.pctl",
            "--output", f"outputExpAgricultural_PropLarge/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ1/Agricultural/experiment_files/optimisationList_agricultural.txt",
            "--changes", "assets/RQ1/Agricultural/experiment_files/changes_injected/agricultural_changes_injected_in_prop.txt"#<<<
        ]
# create_job_files()

# Input:
name_job_file = "ExpAgricultural_Model"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ1/Agricultural/experiment_files/experimentsAgricultural_iter_25_100.csv",
            "--model", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural-humanNonLinear.pm",
            "--properties", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural.pctl",
            "--output", f"outputExpAgricultural_Model/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ1/Agricultural/experiment_files/optimisationList_agricultural.txt",
            "--changes", "assets/RQ1/Agricultural/experiment_files/changes_injected/agricultural_changes_injected_in_model.txt"#<<<
        ]
# create_job_files()


# Input:
name_job_file = "ExpAgricultural_Both"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ1/Agricultural/experiment_files/experimentsAgricultural_iter_25_100.csv",
            "--model", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural-humanNonLinear.pm",
            "--properties", "assets/RQ1/Agricultural/ARCH_input/evomodel/agricultural.pctl",
            "--output", f"outputExpAgricultural_Both/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ1/Agricultural/experiment_files/optimisationList_agricultural.txt",
            "--changes", "assets/RQ1/Agricultural/experiment_files/changes_injected/agricultural_changes_injected_both.txt"#<<<
        ]
# create_job_files()



#======================== Construction model experiments ========================
name_job_file = "ExpConstruction_None"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ3/Construction/experiment_files/experiments_iter_25_50.csv",
            "--model", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.prism",
            "--properties", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.props",
            "--output", f"output_Construct_None/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ3/Construction/experiment_files/optimisationList_construction.txt",
            "--changes", "assets/RQ3/Construction/experiment_files/changes_injected_NONE.txt"#<<<
        ]
create_job_files()

name_job_file = "ExpConstruction_PropMin"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ3/Construction/experiment_files/experiments_iter_25_50.csv",
            "--model", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.prism",
            "--properties", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.props",
            "--output", f"output_Construct_PropMin/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ3/Construction/experiment_files/optimisationList_construction.txt",
            "--changes", "assets/RQ3/Construction/experiment_files/change_injected_in_propMin.txt"#<<<
        ]
create_job_files()

name_job_file = "ExpConstruction_PropLarge"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ3/Construction/experiment_files/experiments_iter_25_50.csv",
            "--model", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.prism",
            "--properties", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.props",
            "--output", f"output_Construct_PropLarge/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ3/Construction/experiment_files/optimisationList_construction.txt",
            "--changes", "assets/RQ3/Construction/experiment_files/changes_injected_in_propLarge.txt"#<<<
        ]
create_job_files()


name_job_file = "ExpConstruction_Model"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ3/Construction/experiment_files/experiments_iter_25_50.csv",
            "--model", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.prism",
            "--properties", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.props",
            "--output", f"output_Construct_Model/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ3/Construction/experiment_files/optimisationList_construction.txt",
            "--changes", "assets/RQ3/Construction/experiment_files/changes_injected_in_model.txt"#<<<
        ]
create_job_files()

name_job_file = "ExpConstruction_Both"
sys.argv = [
            "run.py",  # script name
            "--csv", "assets/RQ3/Construction/experiment_files/experiments_iter_25_50.csv",
            "--model", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.prism",
            "--properties", "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.props",
            "--output", f"output_Construct_Both/exp",   #---->>>> ***Select output folder name (without experiment number)***
            "--optimisation", "assets/RQ3/Construction/experiment_files/optimisationList_construction.txt",
            "--changes", "assets/RQ3/Construction/experiment_files/changes_injected_both.txt"#<<<
        ]
create_job_files()
