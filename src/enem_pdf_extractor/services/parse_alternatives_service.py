import re, os ,json 
import pprint

from enem_pdf_extractor.services.get_alternative_list_service import GetAlternativeListService

#essa função retorna uma string caso o output é TXT e uma tuple (str,lista) caso o output seja JSON
class ParseAlternativesService():
    def __init__(self, question:str, output_type: str )-> str | tuple[str,list[str]]:
        self.question = question
        self.output_type = output_type
        
    def execute(self): 
        if self.output_type == "txt":
            return_val: str = "non-standard alternatives"
        else:
            return_val: tuple[str,list[str]] = "non-standard alternatives" , []
        pattern = r"([A-E])\s*\n\1\s*"
        
        single_letter_pattern = r"([A-E])\s{2}" #padrão de uma letra maiúscula com 2 espaços, pq o ENEM 2020 não repete as alternativas 2 vezes
        
        def replace_match(match):
            return f"{match.group(1)})"
        
        number_substi: int 
        question, number_substi = re.subn(pattern, replace_match, self.question)
        if number_substi < 5:
           question , num = re.subn(single_letter_pattern,replace_match, question)
           if num < 5: #menos que 5 substituições no novo padrão
             return return_val
        #caso nos tenhamos realizado menos que 5 substituições (num de alternativas) então a estrutura da questão estava quebrada
        #provavelmente uma questão com imagem de alternativa
        
        alternative_pattern = r"([A-E])\)"
        alternatives = {}
        #vamos ver se as alternativas contem texto vazio (então são imagens) e se for vamos pular a questão
        matches = list(re.finditer(alternative_pattern, question))
        for i, match in enumerate(matches):
            letter = match.group(1)
            start_pos = match.end()     
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(question)
            
            alternative_text = question[start_pos:end_pos]
            if not alternative_text:
                return return_val

            alternatives[letter] = alternative_text
        
        if isinstance(return_val,str):  #return_val depende do tipo de output, se for .txt retorna uma string, se for .json retorna uma tuple
            return_val = question
        elif isinstance(return_val,tuple):
            return_val = (question, GetAlternativeListService(question).execute())
            
        return return_val

    