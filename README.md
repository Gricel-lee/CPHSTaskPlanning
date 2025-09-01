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


## Install

#### In local laptop
To run the experiments, clone this repository and download dependencies:
```console
git clone https://github.com/Gricel-lee/CPHSTaskPlanning.git
cd CPHSTaskPlanning
git submodule update --init --recursive 
```

Note: In Viking, create virtual machine if no dependencies exists in python installation. First switch python and Java verisons (shown when running ```module spider Python``` or Java):
```
module load Python/3.10.4-GCCcore-11.3.0
module load Java/11.0.20
```
then do:
```
python3 -m venv my_project_env
source my_project_env/bin/activate
pip3 install --upgrade pip
pip3 install matplotlib
pip3 install pandas
```

## Run

From ```cd CPHSTaskPlanning```, run ```src/run.py``` as follows:
```console
python3 ./src/run.py --csv <csv_file> --model <evochecker_model_file> --properties <evochecker_props_file> --output <output_folder>
```

for example,
```console
python3 ./src/run.py --csv "input/experiments.csv" --model "input/evomodel/FX/fxLarge.pm" --properties "input/evomodel/FX/fxLarge.pctl" --output "output/fxlarge"
```

```console
python3 ./src/run.py --csv "input/experimentsAgricultural.csv" --model "input/evomodel/AG/agricultural-humanNonLinear.pm" --properties "input/evomodel/AG/agricultural.pctl" --output "output/agr-human-no-linear"
```



#### In UoY Viking server
Sign into viking and lauch the jobscript.job file:
```console
sbatch jobscript.job
```

# Troubleshooting

- If the EvoChecker file does not load normally after  ```git submodule update --init --recursive```, try:
```console
cd EvoChecker
git checkout -b seedResultsjar origin/seedResultsjar
```

- Change Java to Java 11 or later when (in Viking is possible by running```module load Java/11.0.20```)
```
Error: A JNI error has occurred, please check your installation and try again
Exception in thread "main" java.lang.UnsupportedClassVersionError: evochecker/EvoChecker has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0
	at java.lang.ClassLoader.defineClass1(Native Method)
	at java.lang.ClassLoader.defineClass(ClassLoader.java:756)
	at java.security.SecureClassLoader.defineClass(SecureClassLoader.java:142)
	at java.net.URLClassLoader.defineClass(URLClassLoader.java:473)
	at java.net.URLClassLoader.access$100(URLClassLoader.java:74)
	at java.net.URLClassLoader$1.run(URLClassLoader.java:369)
	at java.net.URLClassLoader$1.run(URLClassLoader.java:363)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.net.URLClassLoader.findClass(URLClassLoader.java:362)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:418)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:352)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:351)
	at sun.launcher.LauncherHelper.checkAndLoadMain(LauncherHelper.java:621)
```


 
 
 # Developers notes
 
Evochecker was uploaded as a github **submodule** (from the EvoChecker repository, _seedResultsjar_ branch by running ```git submodule add -b seedResultsjar https://github.com/gerasimou/EvoChecker.git```).
Hence, some useful commands to interact with this repo are:
| Task                                                                 | Command                                           |
|----------------------------------------------------------------------|---------------------------------------------------|
| Only after cloning, initialise submodules. This must download the files inside the EvoChecker folder.        | `git submodule update --init --recursive`         |
| Pull everything including submodules       | `git pull --recurse-submodules`                 |
| Update submodules to latest commits on their remote branches         | `git submodule update --remote --merge`           |
