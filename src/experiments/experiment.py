import os
from pathlib import Path
import csv
from typing import List, Optional
from aux import read_csv_file
import aux

# from experiment import Experiment

class Experiment:
    
    def __init__(self, output_folder, row, case,
                seeding: str, percentage: Optional[str],
                kMeanIterations: Optional[str], distance: Optional[str],
                fuzziness: Optional[str], epsilon: Optional[str],
                nMinPerCluster: Optional[str], dataPareto: str,
                population: int, evaluations: int, moga: str):
        self.id = self._get_experiment_id(row)
        self.case = case
        self.seeding = seeding
        self.percentage = percentage
        self.kMeanIterations = kMeanIterations
        self.distance = distance
        self.fuzziness = fuzziness
        self.epsilon = epsilon
        self.nMinPerCluster = nMinPerCluster
        self.dataPareto = dataPareto
        self.population = population
        self.evaluations = evaluations
        self.moga = moga
        self.output_experiment_folder = os.path.join(output_folder, self.id)
        self.temp_folder = os.path.join(self.output_experiment_folder, "temp/target") # used for temporary EvoChecker instance
        self.res_folder = os.path.join(self.output_experiment_folder, "results") # used for temporary EvoChecker instance
        self.configFile = ""
        
    def _get_experiment_id(self, row):
        rowString = "|".join(str(value) for value in row.values())
        return rowString
        
    def create_folder_and_files(self,experiments):
        # - create EvoChecker config file
        self.configFile = aux.create_config_props_file(self,experiments)
        
    
    def create_folder(self):
        # - create folder for the experiment output
        if not os.path.exists(self.output_experiment_folder):
            os.makedirs(self.output_experiment_folder)
        print(f"[EXP] Experiment output folder: {self.output_experiment_folder}")
        
    
    def get_id(self):
        return self.id
        
    def __repr__(self):
        return f"Experiment(case={self.case},seeding={self.seeding}, percentage={self.percentage}, kMeanIterations={self.kMeanIterations}, distance={self.distance}, fuzziness={self.fuzziness}, epsilon={self.epsilon}, nMinPerCluster={self.nMinPerCluster}, dataPareto={self.dataPareto}, population={self.population}, evaluations={self.evaluations}, moga={self.moga})"
    
    
    
    