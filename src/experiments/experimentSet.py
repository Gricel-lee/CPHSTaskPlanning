
import ast
import csv
import os
from experiments.experiment import Experiment
from typing import List, Optional
import experiments.aux as aux

class ExperimentSet:
    """
    Class to manage a set of experiments loaded from a CSV file.
    Each experiment is represented as an instance of the Experiment class.
    """
    
    def __init__(self, csv_file: str, output_folder: str, noSeedingBackup_folder: str, model_file:str, properties_file:str, change_list_file:Optional[str]=None):
        # paths info
        self.dir = aux.get_directory()
        self.csv_file = csv_file
        # create output folders
        self.output_folder = output_folder
        self.noSeedingBackup = noSeedingBackup_folder
        print(f"[EXP] CSV file: {self.csv_file}")
        print(f"[EXP] Output folder: {self.output_folder}")
        # load the experiments from the csv file
        self.experiment_list:List[Experiment] = self.load_experiments()
        # evochecker files names
        self.evocheckerModel = model_file.split("/")[-1]
        self.evocheckerProps = properties_file.split("/")[-1]
        # input evo files
        self.model = os.path.join(self.dir, model_file)
        self.properties = os.path.join(self.dir, properties_file)

        # load injected changes. Injected changes; follow the format {original_string: [changed_string, "model"/"properties"/"none"]}
        self.change_list = self.import_changes(change_list_file)

        # file with all Pareto front results paths (across all experiments and iterations)
        self.file_with_all_Pareto_results_paths = os.path.join(self.output_folder, "resPaths.txt")

    def import_changes(self, change_list_file:Optional[str]=None):
        if change_list_file is None:
            return {}
        print(f"[EXP] Loading injected changes from {change_list_file}")
        # Read the change list file content
        file_content = aux.read_file_as_string(change_list_file)
        # ast.literal_eval() safely parse the string into a Python dictionary
        try:
            change_list = ast.literal_eval(file_content)  # This converts the string to a Python dictionary
            print(change_list)  # You can now use 'change_list' as a normal dictionary
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing content: {e}")
        return change_list

    def get(self, index: int) -> Experiment:
        """
        Get the experiment at the given index.
        """
        if index < 0 or index >= len(self.experiment_list):
            raise IndexError("Index out of range")
        return self.experiment_list[index]    
    
            
    def load_experiments(self):
        all_experiments = []
        with open(self.csv_file, newline='', encoding='cp1252') as csvfile:
            #read the csv file abs 
            # csvfile = open(self.csv_file_abs, newline='', encoding='utf-8')
            # for line in csvfile:
            #     print(line)
            
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
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
        print(f"[EXP] Loaded {len(all_experiments)} experiments from {self.csv_file}.")
        return all_experiments
    
    
    @staticmethod
    def _none_if_dash(value: str) -> Optional[str]:
        return None if value.strip() == '-' else value.strip()
