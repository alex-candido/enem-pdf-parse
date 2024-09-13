import pymupdf
import pprint

import enem_pdf_extractor.constants.enem_constants as enem_constants

from enem_pdf_extractor.services.page_preprocessing_service import PagePreProcessingService
from enem_pdf_extractor.services.yield_all_substrings_service import YieldAllSubstringsService 
from enem_pdf_extractor.services.find_correct_answer_service import FindCorrectAnswerService

class HandleDayOneTestsService():
    def __init__(self, pdf_reader: pymupdf.pymupdf.Document, test_year: int, output_type: str, answer_pdf_text: str)-> None:
        self.pdf_reader = pdf_reader
        self.test_year = test_year
        self.output_type = output_type
        self.answer_pdf_text = answer_pdf_text
        
    def execute(self): 
        total_question_number: int = 0 
        
        if self.output_type == "txt" or self.output_type == "markdown" :
            english_questions: str = ""
            spanish_questions: str = ""
            humanities_questions: str = ""
            languages_arts_questions: str = ""
        else:
            english_questions: list[dict] = []
            spanish_questions: list[dict] = []
            humanities_questions: list[dict] = []
            languages_arts_questions: list[dict] = []
        
        num_pages: int = len(self.pdf_reader)
        
        #ultima questão de humanas é a 96 pq tbm são contadas as de ingles e espanhol, ambas entre 1-6
        topic_question_range: dict[str,tuple] = {"eng": (1,5), "spa":(6,10), "lang": (11,50), "huma":(51,95)} 
        
        #começamos da página numero um para não processar a capa 
        for i in range(1, num_pages):
            #função que realiza o pre-processamento do texto da página, incluindo decidindo se pula a página ou não (e de que forma pular)
            page_attributes: dict = PagePreProcessingService(
                    pdf_reader = self.pdf_reader,
                    page_index = i, 
                    total_question_number = total_question_number
            ).execute()
            
            if not page_attributes: #dict vazio, pagina não tem questões
                 continue  
            
            page_first_question: int = page_attributes.get("page_first_question")
            total_question_number = page_attributes.get("total_question_number")
            text:str = page_attributes.get("text") 
            #dict com texto vazio (imagens na pagina), mas atualizando page_first question e total_question_number
            if not text: 
                continue
            
            question_start_index: int = 0
            answer_number: int = page_first_question
            in_spanish_question: bool = False
            
            if self.output_type == "json": alternative_list:list[str] = []
            
            #yield na posição da substring que identifica as questoes
            for position in YieldAllSubstringsService(text, enem_constants.__QUESTION_IDENTIFIER__).execute():
                if position == 0:
                    continue
                
                if answer_number > 5 and answer_number < 11:
                    in_spanish_question = True  #verifica se a questão é de espanhol
                else:
                    in_spanish_question = False
                    
                # se a questão for de espanhol é necessário uma pequena mudança na parte de pegar a resposta
                correct_answer: str = FindCorrectAnswerService(
                    question_number = answer_number, 
                    is_spanish_question = in_spanish_question, 
                    day_one = True,
                    answer_pdf_text = self.answer_pdf_text
                ).execute()
                # unparsed_alternatives: str = text[question_start_index:position]
