import re, os ,json 
import pprint

class MdParseAlternativesService():
    def __init__(self, question:str)->str:
        self.question = question
  
    def execute(self): 
        alternative_pattern = r"[A-E]\).*?"
        first_match = re.search(alternative_pattern, self.question)
        if first_match:
         start_index: int = first_match.start()
         self.question = self.question[:start_index] + "\n# alternativas: \n" + self.question[start_index:]
        
        return self.question 