import pymupdf

#generator que itera sobre todas as substrings e retorna o index dela na string principal

class YieldAllSubstringsService():
    def __init__(self, input_str: str, sub_str:str)-> int:
        self.input_str = input_str
        self.sub_str = sub_str
        
    def execute(self): 
        self.sub_str = self.sub_str or "*" 
        start = 0  
        
        while True:
            start:int = self.input_str.find(self.sub_str, start)
            if start == -1: return  
            yield start
            start += len(self.sub_str) 
        