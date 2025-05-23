
import csv
import os
from experiments.experiment import Experiment
from typing import List, Optional


class ExperimentSet:
    """
    Class to manage a set of experiments loaded from a CSV file.
    Each experiment is represented as an instance of the Experiment class.
    """
    
    def __init__(self, dir:str, csv_file_abs: str, output_folder: str, noSeedingBackup: str, model:str, properties:str):
        # paths info
        self.dir = dir
        self.csv_file_abs = csv_file_abs
        # create output folders
        self.output_folder = output_folder
        self.noSeedingBackup = noSeedingBackup
        print(f"[EXP] CSV file: {self.csv_file_abs}")
        print(f"[EXP] Output folder: {self.output_folder}")
        # load the experiments from the csv file
        self.experiment_list:List[Experiment] = self.load_experiments()
        # evochecker files names
        self.evocheckerModel = model.split("/")[-1]
        self.evocheckerProps = properties.split("/")[-1]
        # input evo files
        self.model = os.path.join(dir, model)
        self.properties = os.path.join(dir, properties)
    
    def get(self, index: int) -> Experiment:
        """
        Get the experiment at the given index.
        """
        if index < 0 or index >= len(self.experiment_list):
            raise IndexError("Index out of range")
        return self.experiment_list[index]    
    
            
    def load_experiments(self):
        all_experiments = []
        with open(self.csv_file_abs, newline='', encoding='cp1252') as csvfile:
            #read the csv file abs 
            # csvfile = open(self.csv_file_abs, newline='', encoding='utf-8')
            # for line in csvfile:
            #     print(line)
            
            with open(self.csv_file_abs, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # - get experiment instance
                    exp = Experiment(
                    output_folder = self.output_folder,
                    row = row,
                    case=row["case"],
                    seeding=row["seeding"],
                    percentage=self._none_if_dash(row["percentage"]),
                    kMeanIterations=self._none_if_dash(row["kMeanIterations"]),
                    distance=self._none_if_dash(row["Distance"]),
                    fuzziness=self._none_if_dash(row["fuzziness"]),
                    epsilon=self._none_if_dash(row["epsilon"]),
                    nMinPerCluster=self._none_if_dash(row["nMinPerCluster"]),
                    dataPareto=row["dataPareto"],
                    population=int(row["population"]),
                    evaluations=int(row["Evaluations"]),
                    moga=row["MOGA"]
                    )
                    if False:
                        print(f"[EXPSET] Loaded {exp}.\n ID: {exp.id}")
                    all_experiments.append(exp)
        print(f"[EXP] Loaded {len(all_experiments)} experiments from {self.csv_file_abs}.")
        return all_experiments
    
    
    @staticmethod
    def _none_if_dash(value: str) -> Optional[str]:
        return None if value.strip() == '-' else value.strip()
