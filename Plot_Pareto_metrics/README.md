# Plot statistical analysis of Pareto front metrics

This assumes that the GitHub repository is cloned into Viking.

In order to generate a new set of statistical plot for an experiment:

1. First, run an experiment in Viking for the job desired (e.g., sbatch job_X.job)

2. Wait for the job to be completed, make sure all results are available in the output file set in the .job file.

3. Push into Github all output folder or *at least* the following results:

a) the Pareto front metrics summary
```
git add {name output file}/{name_problem}*/metrics_IGD_HV_GD.csv
```
for example ```git add outputHumanNonL/agricultural*/metrics_IGD_HV_GD.csv```

b) the completion times after each iteration
```
git add {name_output_file}/{name_problem}*/{name_problem}*/results/time.txt
```

for example ```git add outputHumanNonL/agricultural*/agricultural*/results/time.txt```


4. In the local device, ```git pull``` the new results.

5. From the CPHSTaskPlanning folder, first set ``{viking_output_folder} {folder_to_save_results}" in ```Plot_Pareto_metrics/plot-avr-std-results.py ```, for example ```outputExpAgri_None``` and ```plot_output_outputHumanNonL```.

6. Run
```
python3 Plot_Pareto_metrics/plot-avr-std-results.py 
```

7. The plots and statistics summary will be saved.