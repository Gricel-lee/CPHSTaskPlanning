import subprocess
import time


# ==== Run ARCH (./src/run.py) for scalability experiments ======
def run_experiments(exp, XT_YA):
    commands = [
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_1/datamodelEvo_1.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_1/datamodelEvo_1.props" --output "assets/RQ4/evo_output_{XT_YA}/plan1/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_2/datamodelEvo_2.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_2/datamodelEvo_2.props" --output "assets/RQ4/evo_output_{XT_YA}/plan2/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_3/datamodelEvo_3.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_3/datamodelEvo_3.props" --output "assets/RQ4/evo_output_{XT_YA}/plan3/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_4/datamodelEvo_4.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_4/datamodelEvo_4.props" --output "assets/RQ4/evo_output_{XT_YA}/plan4/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_5/datamodelEvo_5.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_5/datamodelEvo_5.props" --output "assets/RQ4/evo_output_{XT_YA}/plan5/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_6/datamodelEvo_6.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_6/datamodelEvo_6.props" --output "assets/RQ4/evo_output_{XT_YA}/plan6/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_7/datamodelEvo_7.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_7/datamodelEvo_7.props" --output "assets/RQ4/evo_output_{XT_YA}/plan7/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_8/datamodelEvo_8.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_8/datamodelEvo_8.props" --output "assets/RQ4/evo_output_{XT_YA}/plan8/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_9/datamodelEvo_9.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_9/datamodelEvo_9.props" --output "assets/RQ4/evo_output_{XT_YA}/plan9/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_10/datamodelEvo_10.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_10/datamodelEvo_10.props" --output "assets/RQ4/evo_output_{XT_YA}/plan10/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_11/datamodelEvo_11.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_11/datamodelEvo_11.props" --output "assets/RQ4/evo_output_{XT_YA}/plan11/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_12/datamodelEvo_12.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_12/datamodelEvo_12.props" --output "assets/RQ4/evo_output_{XT_YA}/plan12/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_13/datamodelEvo_13.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_13/datamodelEvo_13.props" --output "assets/RQ4/evo_output_{XT_YA}/plan13/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_14/datamodelEvo_14.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_14/datamodelEvo_14.props" --output "assets/RQ4/evo_output_{XT_YA}/plan14/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_15/datamodelEvo_15.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_15/datamodelEvo_15.props" --output "assets/RQ4/evo_output_{XT_YA}/plan15/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_16/datamodelEvo_16.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_16/datamodelEvo_16.props" --output "assets/RQ4/evo_output_{XT_YA}/plan16/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_17/datamodelEvo_17.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_17/datamodelEvo_17.props" --output "assets/RQ4/evo_output_{XT_YA}/plan17/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_18/datamodelEvo_18.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_18/datamodelEvo_18.props" --output "assets/RQ4/evo_output_{XT_YA}/plan18/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_19/datamodelEvo_19.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_19/datamodelEvo_19.props" --output "assets/RQ4/evo_output_{XT_YA}/plan19/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"',
        f'python3 ./src/run.py --csv "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/experiment_files/experimentsAgri_iter_25_100.csv" --model "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_20/datamodelEvo_20.pm" --properties "assets/RQ4/AgentsTasks_Variants_Plans/output_data_agri_{XT_YA}/output_plan_20/datamodelEvo_20.props" --output "assets/RQ4/evo_output_{XT_YA}/plan20/{exp}" --optimisation "assets/RQ4/experiment_files/optimisationList_agricultural.txt" --changes "assets/RQ4/experiment_files/changes_injected/agricultural_change_propmin.txt"'
    ]

    # File to store durations
    output_file = f"/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/evo_output_{XT_YA}/{exp}_execution_times.txt"

    for idx, cmd in enumerate(commands, start=1):
        start_time = time.time()
        print(f"Running command {idx}...")
        try:
            subprocess.run(cmd, shell=True, check=True)
            status = "SUCCESS"
        except subprocess.CalledProcessError as e:
            print(f"Command {idx} failed with error: {e}")
            status = "NA plan not saved from TEMpest as was repeated"
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Command {idx} finished in {duration:.2f} seconds ({status})")
        
        # Save duration to file after each run
        with open(output_file, "a") as f:
            f.write(f"Command {idx}: {duration:.2f} seconds ({status})\n")


# ==== Read all "_execution_times.txt" files and compile a summary ======
import os
import math

def time_avr_std(exp_list, XT_YA_list, summary_file="execution_times_summary.txt"):
    print("Compiling summary of execution times...")
    
    with open(summary_file, "w") as summary:
        summary.write("Variant\tPlan (COMMAND)\tAverage Time (s)\tStd Dev (s)\n")
        
        for XT_YA in XT_YA_list:
            for cmd_idx in range(1, 21):  # 20 commands/plans
                times = []
                for exp in exp_list:
                    exec_time_file = f"/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/evo_output_{XT_YA}/{exp}_execution_times.txt"
                    if not os.path.exists(exec_time_file):
                        print(f"Execution time file not found: {exec_time_file}")
                        continue
                    
                    with open(exec_time_file, "r") as f:
                        for line in f:
                            if line.startswith(f"Command {cmd_idx}:"):
                                parts = line.split(":")[1].strip().split(" ")[0]
                                if "NA" not in parts:
                                    try:
                                        times.append(float(parts))
                                    except ValueError:
                                        pass
                
                if times:
                    avg_time = sum(times) / len(times)
                    if len(times) > 1:
                        std_dev = math.sqrt(sum((x - avg_time) ** 2 for x in times) / (len(times) - 1))
                    else:
                        std_dev = 0.0  # or NA if you prefer
                    summary.write(f"{XT_YA}\tPlan {cmd_idx}\t{avg_time:.4f} $\pm$ {std_dev:.4f}\n")
                else:
                    summary.write(f"{XT_YA}\tPlan {cmd_idx}\tNA\tNA\n")
    
    print("Summary compilation completed. Saved to", summary_file)





# === Set parameters and run experiments ===
# 1) Number of experiment
exp_list = ["exp4"] #"exp1","exp2"]
# 2) Change scalability variant (T=number of tasks, A=number of agents): 5T_3A 10T_A 15T_3A 15T_4A 15T_5A
XT_YA_list = ["4T_2A","5T_3A","10T_3A","10T_4A_case_study"] #"4T_2A", "5T_3A", "10T_3A", "10T_4A_case_study", "15T_3A","15T_4A","15T_5A"]


# 1) Number of experiment
# exp_list = ["exp1","exp2"]
# # 2) Change scalability variant (T=number of tasks, A=number of agents): 5T_3A 10T_A 15T_3A 15T_4A 15T_5A
# XT_YA_list = ["4T_2A", "5T_3A", "10T_3A", "10T_4A_case_study"]    # can't run in EvoChecker: , "15T_3A","15T_4A","15T_5A"



# === Run experiments for all variants and compile summary ====
for exp in exp_list:
    for XT_YA in XT_YA_list:
        run_experiments(exp, XT_YA)


# ==== Get summary of times (after running all experiments) ======
# summary_file = "/home/gnvf500/Gricel-Documents/GithubGris/CPHSTaskPlanning/assets/RQ4/evo_output_summary_times.txt"
# time_avr_std(exp_list, XT_YA_list, summary_file)

