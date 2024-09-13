import pprint
import re, os ,json 

import enem_pdf_extractor.constants.enem_constants as enem_constants

#lida com erros de input/output, alertando sobre nomes não baseados na nomeclatura do INEP, assim como alerta sobre gabaritos e provas de cores diferentes

class HandleIOErrorsService():
    
    def __init__(self, test_pdf_path: str, answers_pdf_path: str)-> None:
        self.test_pdf_path = test_pdf_path
        self.answers_pdf_path = answers_pdf_path
        
    def execute(self):   
        if enem_constants.__TEST_IDENTIFIER__ not in self.test_pdf_path:
            raise IOError("nome do arquivo da prova não segue o padrão do INEP")
        
        if enem_constants.__ANSWER_PDF_IDENTIFIER__ not in self.answers_pdf_path:
            raise IOError("nome do arquivo do gabarito não segue o padrão do INEP")
        
        test_color_identifier = re.findall(enem_constants.__TEST_COLOR_PATTERN__, self.test_pdf_path)
        if not test_color_identifier:
            raise IOError("especificação da cor do caderno da prova não segue o padrão do INEP")
        
        answers_color_identifier = re.findall(enem_constants.__TEST_COLOR_PATTERN__, self.answers_pdf_path)
        if not answers_color_identifier:
            raise IOError("especificação da cor do gabarito não segue o padrão do INEP")
        
        test_color_identifier:str = test_color_identifier[0]
        answers_color_identifier:str = answers_color_identifier[0]
        
        if test_color_identifier[2] != answers_color_identifier[2]:  #terceiro char desse padrão é o numero referente à cor do caderno
            raise IOError("prova e gabarito são de cores diferentes") 