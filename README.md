# CPHSTaskPlanning
This repository runs experiments in EvoChecker with different seeding configurations.

### Inputs
An **input** folder must exist with the following content:
- file **experiments.csv**, containing the set of experiments to run. The csv file follows the rows as in the figure below, with rows:
    - first row with 0% seeding experiment. The result of this experiment is used to seed the following ones.
    - n following rows with different configurations of seedings. Each with their respective parameters (example, 
![image](https://github.com/user-attachments/assets/320a0654-b930-4a45-9907-5854240a948a)
Note: all experiments must belong to the same case name. The name is used to create an output folder
- a **.pm** file with the EvoChecker model
- a **.prop** file with the EvoChecker objectives

### Output
An output folder is automatically generated with the following content:
    - **nameProblem and configuration params**: 
    - **previousPopulation**: a copy of the results obtained with no seeding, used for seeding other experiments.


## Run

#### In local laptop
To run the experiments, clone this repository and dependencies:
```
git clone https://github.com/Gricel-lee/CPHSTaskPlanning.git
cd CPHSTaskPlanning
git submodule update --init --recursive 
```

Go the project's folder and from there run src/run.py with inputs and folder to save the output, for example, to save the output in output/fxlarge: 
```
cd CPHSTaskPlanning
python3 ./src/run.py --csv "input/experiments.csv" --model "input/evomodel/FX/fxLarge.pm" --properties "input/evomodel/FX/fxLarge.pctl" --output "output/fxlarge"
```

#### In UoY Viking server
Sign into viking and lauch the jobscript.job file:
```
sbatch jobscript.job
```

# Troubleshooting

- If the EvoChecker file does not load normally after  ```git submodule update --init --recursive```, try:
```
cd EvoChecker
git checkout -b seedResultsjar origin/seedResultsjar
```

 
 
 # Developers notes
 
Evochecker was uploaded as a github **submodule** (from the EvoChecker repository, _seedResultsjar_ branch by running ```git submodule add -b seedResultsjar https://github.com/gerasimou/EvoChecker.git```).
Hence, some useful commands to interact with this repo are:
| Task                                                                 | Command                                           |
|----------------------------------------------------------------------|---------------------------------------------------|
| Only after cloning, initialise submodules. This must download the files inside the EvoChecker folder.        | `git submodule update --init --recursive`         |
| Pull everything including submodules       | `git pull --recurse-submodules`                 |
| Update submodules to latest commits on their remote branches         | `git submodule update --remote --merge`           |
