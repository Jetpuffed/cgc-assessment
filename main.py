import csv
import pprint
import pandas as pd

class SheetBuilder:
    def __init__(self, plo_file, clo_file):
        self.df = pd.DataFrame()
        self.plo_data = dict()
        self.clo_data = dict()
        self.plo_reader = csv.reader(plo_file)
        self.clo_reader = csv.reader(clo_file)
    
    def build_plo_data(self) -> None:
        for row in self.plo_reader:
            program_id = row[0][:4]
            if program_id not in self.plo_data:
                self.plo_data[program_id] = list()
            self.plo_data[program_id].append(row[2])
    
    def build_clo_data(self) -> None:
        for row in self.clo_reader:
            subject_id, course_id = row[0], row[1]
            full_id = "".join([subject_id, course_id])
            if full_id not in self.clo_data:
                self.clo_data[full_id] = list()
            self.clo_data[full_id].append(row[3])
    
    def run(self) -> None:
        self.build_plo_data()
        self.build_clo_data()
    
    # For debug purposes
    def get_debug_info(self) -> None:
        pprint.pp(self.plo_data)
        pprint.pp(self.clo_data)
    
    def get_plo_count(self, program_id: str) -> int:
        if program_id in self.plo_data.keys():
            count = 0
            for _ in self.plo_data[program_id]:
                count += 1
        return count
    
    def get_plo_info(self, program_id: str) -> None:
        if program_id in self.plo_data.keys():
            pprint.pp(self.plo_data[program_id])

    def get_clo_count(self, course_id: str) -> int:
        if course_id in self.clo_data.keys():
            count = 0
            for _ in self.clo_data[course_id]:
                count += 1
        return count
    
    def get_clo_info(self, course_id: str) -> None:
        if course_id in self.clo_data.keys():
            pprint.pp(self.clo_data[course_id])

    def write_plo_contents(self, program_id: str):
        plo_count = self.get_plo_count(program_id)
        plo_numbers = ["".join([program_id, ".", str(n)]) for n in range(1, plo_count + 1)]
        plo_descriptions = [desc for desc in self.plo_data.get(program_id)]
        self.df.insert(0, "PLO #", plo_numbers)
        self.df.insert(1, "PLO Description", plo_descriptions)
        print(self.df)
    
    def write_clo_contents(self, course_id: str):
        clo_count = self.get_clo_count(course_id)
        for i in range(1, clo_count + 1):
            self.df.insert(1+i, i, [None for _ in range(0, 11)])
        print(self.df)
    
    def export(self):
        self.df.to_excel("generated.xlsx")

if __name__ == "__main__":
    plo_file = open("cgc_plo.csv")
    clo_file = open("cgc_clo.csv")

    builder = SheetBuilder(plo_file, clo_file)
    builder.run()
    builder.write_plo_contents("3059") #TODO: Add a blank row so CLOs have a place in the header
    builder.write_clo_contents("EXS146") #TODO: Iterate over each course id in a given program
    builder.export()