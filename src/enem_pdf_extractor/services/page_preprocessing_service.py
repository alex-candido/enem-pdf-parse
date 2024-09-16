import pymupdf
import re, os ,json 
import pprint

import enem_pdf_extractor.constants.enem_constants as enem_constants
from enem_pdf_extractor.services.yield_all_substrings_service import YieldAllSubstringsService 

#método para pre-processar o texto de uma página, retornando o texto processado, o num da primeira questão da página e pulando ela caso ela não tenha questões ou tenha imagens

class PagePreProcessingService():
    def __init__(self, pdf_reader: pymupdf.pymupdf.Document, page_index: int , total_question_number: int)-> dict:
        self.pdf_reader = pdf_reader
        self.page_index = page_index
        self.total_question_number = total_question_number
        
    def execute(self):    
        text_processing_dict: dict = {"text": "", "page_first_question": 0, "total_question_number": 0, "page_index": 0 }
        
        current_page: pymupdf.pymupdf.Page = self.pdf_reader[self.page_index]
        
        page_text: str = current_page.get_text()
        page_text = page_text.replace("Questão", "QUESTÃO")
        # acha a primeira questão da folha
        
        first_question_str_index: int = next(YieldAllSubstringsService(input_str = page_text, sub_str = enem_constants.__QUESTION_IDENTIFIER__).execute(), -1 ) 
        
        if first_question_str_index == -1:
            return {} # se não tiver questões na página (pagina de redação) pula a iteração
        
        #antes da primeira questão temos apenas um header inútil (ex: ENEM 2022, ENEM 2022....) do PDF
        page_text = page_text[first_question_str_index:]  
        
        #remove os padrões numéricos do QR codes
        page_text = re.sub(enem_constants.__NUM_PATTERN1__,"", page_text)  
        page_text = re.sub(enem_constants.__NUM_PATTERN2__,"",page_text)
        
        page_first_question: int = self.total_question_number + 1 #a primeira questão da prox página sera o numero total de questões processadas ate o momento + 1 (a primeira questão em si) 
        
        for _ in YieldAllSubstringsService(page_text, enem_constants.__QUESTION_IDENTIFIER__).execute():
            self.total_question_number += 1  #aumenta o numero de questoes ja processadas com todas daquela página
        
        image_list:list = current_page.get_images()
        
        if len(image_list):
            text_processing_dict.update({"text": page_text, "page_first_question": page_first_question, "total_question_number": self.total_question_number, "page_index": self.page_index})
            return text_processing_dict #retorna dict sem imagens
         
        
        #caso tenha imagens na página vamos pular ela, já que não podemos extrair a imagem   
        #não é possível fazer essa verificação no começo pois é preciso contar todas as questões da página para a variável total_question_number, já que ela dita qual matéria esta sendo processada

        page_text += f" {enem_constants.__QUESTION_IDENTIFIER__}" #coloca isso no final do texto para ajudar no processamento, já que teremos uma substr de parada do algoritmo
        
        text_processing_dict.update({"text": page_text, "page_first_question": page_first_question, "total_question_number": self.total_question_number, "page_index": self.page_index})
        
        return text_processing_dict
        
        