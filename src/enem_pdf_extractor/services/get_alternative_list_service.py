import re, os ,json 
import pprint

#essa função retorna uma string caso o output é TXT e uma tuple (str,lista) caso o output seja JSON
class GetAlternativeListService():
    def __init__(self, question:str)->list[str]:
        self.question = question
        
    def execute(self): 
        regex_pattern = r"[A-E]\)"
        alternatives_list: list[str] = []
        matches_list: list[int] = [match.start() for match in re.finditer(pattern=regex_pattern, string=self.question)]
       
        for i in range(len(matches_list)):
            if i < len(matches_list)-1:
              alternative_text:str = self.question[matches_list[i]: matches_list[i+1]]
              alternatives_list.append(alternative_text)
            else:
              alternative_text:str = self.question[matches_list[i]: len(self.question)]
              alternatives_list.append(alternative_text)

        return alternatives_list