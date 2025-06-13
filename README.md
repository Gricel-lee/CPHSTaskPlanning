# CPHSTaskPlanning


Experiments to run EvoChecker with different seeding configurations.


### Inputs
- input folder with **experiments.csv**:
    - the first experiment must have 0% seeding, as the result of this run is used to seed the following experiments.
    - 
    - all experiments must belong to the same case name
- reported in config.properties.

### Output
- output folder is automatically generated with subfolders named:
    - **nameProblem and configuration params**: 
    - **previousPopulation**: a copy of the results obtained with no seeding, used for seeding other experiments.


# Troubleshooting

- In viking, it requires to install python libraries:
 ```pip3 install --user pandas```