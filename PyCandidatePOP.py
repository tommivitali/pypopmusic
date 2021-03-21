from ctypes import *
import numpy as np
import os
import tempfile


class PyCandidatePOP:
    so_file = "LKH-2.0.9/LKH_lib.so"

    def __init__(self,
                 parameter_file_name="parameters.txt",
                 problem_file_name="problem.tsp",
                 candidate_file_name="candidate.csv",
                 number_of_solutions=None,
                 max_candidates=None,
                 original_write_candidate=False):
        self.parameterFileName = parameter_file_name
        self.problemFileName = problem_file_name
        self.candidateFileName = candidate_file_name
        self.numberOfSolutions = number_of_solutions
        self.maxCandidates = max_candidates
        self.originalWriteCandidate = original_write_candidate

    def write_parameter_file(self, number_cities):
        with open(self.parameterFileName, "w") as parameter_file:
            parameter_file.write(f"PROBLEM_FILE = {self.problemFileName}\n")
            parameter_file.write(f"CANDIDATE_SET_TYPE = POPMUSIC\n")
            if self.originalWriteCandidate:
                parameter_file.write(f"CANDIDATE_FILE = {self.candidateFileName}\n")
            else:
                parameter_file.write(f"CANDIDATE_OUTPUT_FILE = {self.candidateFileName}\n")
            if self.numberOfSolutions is not None:
                parameter_file.write(f"POPMUSIC_SOLUTIONS = {self.numberOfSolutions}\n")
            if self.maxCandidates is None:
                parameter_file.write(f"MAX_CANDIDATES = {2 * number_cities}\n")
            else:
                parameter_file.write(f"MAX_CANDIDATES = {self.maxCandidates}\n")

    def write_problem_file(self, positions, precision=100000):
        pos = np.round(positions * precision).astype(int)
        number_cities = pos.shape[0]

        with open(self.problemFileName, "w") as file:
            file.write(f"NAME : inst{number_cities}\n")
            file.write(f"COMMENT : TSP instance generated\n")
            file.write(f"TYPE : TSP\n")
            file.write(f"DIMENSION : {number_cities}\n")
            file.write(f"EDGE_WEIGHT_TYPE : EUC_2D\n")
            file.write(f"NODE_COORD_SECTION\n")
            for num, [pos_x, pos_y] in enumerate(pos[:], start=1):
                file.write(f"{num} {pos_x} {pos_y}\n")
            file.write(f"EOF\n")

    def __call__(self, positions):
        if not os.path.isfile(self.so_file):
            print("Library not found. Have you 'make' the LKH?")
            return None

        number_cities = positions.shape[0]
        candidate = [[]] * number_cities

        old_directory = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_path:
            os.chdir(temp_path)

            self.write_parameter_file(number_cities)
            self.write_problem_file(positions)

            LKH_library = CDLL(f"{old_directory}/{self.so_file}")
            LKH_library.LKH_POPMUSIC(f"{self.parameterFileName}".encode())

            if self.originalWriteCandidate:
                with open(self.candidateFileName, "r") as candidate_file:
                    for line in candidate_file.readlines()[1:-2]:
                        line = line.split(" ")
                        candidate[int(line[0]) - 1] = [int(x)-1 for x in line[3:-1:2]]
            else:
                with open(self.candidateFileName, "r") as candidate_file:
                    for line in candidate_file.readlines():
                        line = line.split(":")
                        candidate[int(line[0])-1] = [int(x)-1 for x in line[1].split(";")[:-1]]

        os.chdir(old_directory)
        return candidate
