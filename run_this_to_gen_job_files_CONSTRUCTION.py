s = '''#!/usr/bin/env bash
#SBATCH --job-name=<REPLACE FOR JOB NAME>               # Job name
#SBATCH --partition=nodes               # What partition the job should run on
#SBATCH --time=0-40:15:00               # Time limit (DD-HH:MM:SS)
#SBATCH --ntasks=1                      # Number of MPI tasks to request
#SBATCH --cpus-per-task=9               # Number of CPU cores per MPI task
#SBATCH --mem=30G                       # Total memory to request
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
python3 ./src/run.py --csv "assets/RQ3/Construction/experiment_files/experiments_iter_25_50.csv" --model "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.prism" --properties "assets/RQ3/Construction/ARCH_input/evomodel/datamodelEvo.props" --output "<REPLACE_OUTPUT_FOLDER_AND_EXPERIMENT_SUBFOLDER>" --optimisation "assets/RQ3/Construction/experiment_files/optimisationList_construction.txt" --changes "<REPLACE_CHANGES_FILE>"
'''

# lists of names and files
# names_all = ["ExpAgri_ChangeInjectedBoth", "ExpAgri_ChangeInjectedModel", "ExpAgri_ChangeInjectedProp"]
# files_all = ["input/evomodel/AG/agricultural_changes_injected.txt","input/evomodel/AG/agricultural_changes_injected_in_model.txt","input/evomodel/AG/agricultural_changes_injected_in_prop.txt"]

# lists of names and files
names_all = ["ExpCon_ChangInjModel"]
files_all = ["assets/RQ3/Construction/experiment_files/changes_injected_in_model.txt"]

names_all = ["ExpCon_ChangInjBoth"]
files_all = ["assets/RQ3/Construction/experiment_files/changes_injected_both.txt"]


# ========= Select the name for the job file (also use for the output folder name) ==========
i = 0   #---->>>> Select 0,1 or 2= ["Agri_ChangeInjectedBoth", "Agri_ChangeInjectedModel", "Agri_ChangeInjectedProp"]
# Set numbering for experiments
numbering_experiments = [1,2,3,4,5,6,7,8,9,10]               #,11,12,13,14,15,16,17,18,19,20]
# ===========================================================================================

# create job files
name_job_file = names_all[i]
file_injected_change = files_all[i]

for num in numbering_experiments:
    name = name_job_file + "_exp" + str(num)
    # Create job script file
    with open("jobscript_" + name + ".job", "w") as f:
        # replace placeholders
        s_new = s.replace("<REPLACE FOR JOB NAME>", name)
        s_new = s_new.replace("<REPLACE_OUTPUT_FOLDER_AND_EXPERIMENT_SUBFOLDER>", f"output{name_job_file}/construction{num}")
        s_new = s_new.replace("<REPLACE_CHANGES_FILE>", file_injected_change)
        # write to file
        f.write(s_new)
        
# Create single .sh to launch all jobs
with open("launch_all_jobs_" + name_job_file + ".sh", "w") as f:
    f.write("#!/usr/bin/env bash\n\n")
    for num in numbering_experiments:
        name = name_job_file + "_exp" + str(num)
        f.write(f"echo 'Submitting jobscript_{name}.job'\n")
        f.write(f"sbatch jobscript_{name}.job\n")

# make it executable (chmod +x submit_10.sh)
import os
os.chmod("launch_all_jobs_" + name_job_file + ".sh", 0o755)