import re, os ,json

import pymupdf
import pprint

import enem_pdf_extractor.constants.enem_constants as enem_constants

from typing import Any  

from enem_pdf_extractor.services.parse_alternatives_service import ParseAlternativesService
from enem_pdf_extractor.services.page_preprocessing_service import PagePreProcessingService
from enem_pdf_extractor.services.yield_all_substrings_service import YieldAllSubstringsService 
from enem_pdf_extractor.services.find_correct_answer_service import FindCorrectAnswerService
from enem_pdf_extractor.services.md_parse_alternatives_service import MdParseAlternativesService
from enem_pdf_extractor.services.get_json_from_question_service import GetJsonFromQuestionService

class HandleDayOneTestsService():
    question_json:dict = {}
    def __init__(self, pdf_reader: pymupdf.pymupdf.Document, test_year: int, output_type: str, answer_pdf_text: str, extracted_data_path: str)-> None:
        self.pdf_reader = pdf_reader
        self.test_year = test_year
        self.output_type = output_type
        self.answer_pdf_text = answer_pdf_text
        self.extracted_data_path = extracted_data_path
        
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
        topic_question_range: dict[str, tuple] = {"eng": (1,5), "spa":(6,10), "lang": (11,50), "huma":(51,95)} 
        
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
            
            #yield na posição da substring que identifica as questões
            for position in YieldAllSubstringsService(text, enem_constants.__QUESTION_IDENTIFIER__).execute():
                #se ele detectar a substr "QUESTÃO" no começo do texto, ele pula, caso contrário seria adicionado um string vazia
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
                
                unparsed_alternatives: str = text[question_start_index:position]
                
                parsed_question_vals: Any = ParseAlternativesService(unparsed_alternatives, output_type = self.output_type).execute()
                
                if isinstance(parsed_question_vals, tuple):
                    parsed_question:str = parsed_question_vals[0]
                    alternative_list = parsed_question_vals[1]
                elif isinstance(parsed_question_vals, str):
                    parsed_question:str = parsed_question_vals
                    
                if self.output_type == "markdown":
                    parsed_question: str = MdParseAlternativesService(parsed_question).execute()
                    
                if parsed_question == "non-standard alternatives": #caso a questão tenha alternativas de imagens (mas que o PDF não consegue detectar)     
                    question_start_index = position
                    answer_number += 1
                    continue

                #valor da questão depende do tipo de output
                if self.output_type == "txt":
                    parsed_question = enem_constants.__TXT_QUESTION_TEMPLATE__.format(test_year = self.test_year, question_text = parsed_question, correct_answer = correct_answer)
                elif self.output_type == "markdown":
                    parsed_question = enem_constants.__MD_QUESTION_TEMPLATE__.format(test_year = self.test_year, question_text = parsed_question, correct_answer = correct_answer)
                else:
                    question_json: dict = GetJsonFromQuestionService(
                        question= parsed_question,
                        day_one=True,
                        year= self.test_year,
                        correct_answer= correct_answer,
                        number= answer_number,
                        alternative_list= alternative_list
                    ).execute()
                
                #desempacotando a tuple de ranges de questões das matérias
                start_eng, end_eng = topic_question_range["eng"] 
                start_spa, end_spa = topic_question_range["spa"]
                start_lang, end_lang = topic_question_range["lang"]
                start_huma, end_huma = topic_question_range["huma"]
                
                if answer_number in range(start_eng, end_eng+1):
                    if self.output_type == "txt" or self.output_type == "markdown":
                        english_questions += parsed_question
                    else:
                        english_questions.append(question_json)

                elif answer_number in range(start_spa, end_spa+1):
                    if self.output_type == "txt" or self.output_type == "markdown":
                        spanish_questions += parsed_question
                    else:
                        spanish_questions.append(question_json)

                elif answer_number in range(start_lang, end_lang+1):
                    if self.output_type == "txt" or self.output_type == "markdown":
                        languages_arts_questions += parsed_question
                    else:
                        languages_arts_questions.append(question_json)

                elif answer_number in range(start_huma, end_huma+1):
                    if self.output_type == "txt" or self.output_type == "markdown":
                        humanities_questions += parsed_question
                    else:
                        humanities_questions.append(question_json)
                
                question_start_index = position
                answer_number += 1
        
        #escrever as strings extraidas nos seus arquivos respectivos
        if self.output_type == "txt"  or self.output_type == "markdown":   
            file_type_iden: str = ".txt" if self.output_type == "txt" else ".md"

            file_path:str = os.path.join(self.extracted_data_path,f"{self.test_year}_eng_questions{file_type_iden}" )
            with open(file_path, "w") as f_eng:
                f_eng.write(english_questions)
                
            file_path = os.path.join(self.extracted_data_path,f"{self.test_year}_spani_questions{file_type_iden}" )
            with open(file_path, "w") as f_spani:
                    f_spani.write(spanish_questions)

            file_path = os.path.join(self.extracted_data_path,f"{self.test_year}_lang_questions{file_type_iden}" )     
            with open(file_path, "w") as f_lang:
                f_lang.write(languages_arts_questions)
                
            file_path= os.path.join(self.extracted_data_path, f"{self.test_year}_huma_questions{file_type_iden}")
            with open(file_path, "w") as f_huma:
                f_huma.write(humanities_questions)
        else:
            file_path:str = os.path.join(self.extracted_data_path,f"{self.test_year}_eng_questions.json" )
            with open(file_path, "w") as f_eng:
                json.dump(english_questions,f_eng, indent=4,  ensure_ascii=False)
                
            file_path = os.path.join(self.extracted_data_path,f"{self.test_year}_spani_questions.json" )
            with open(file_path, "w") as f_spani:
                    json.dump(spanish_questions,f_spani,  indent=4,  ensure_ascii=False)

            file_path = os.path.join(self.extracted_data_path,f"{self.test_year}_lang_questions.json" )     
            with open(file_path, "w") as f_lang:
                json.dump(languages_arts_questions,f_lang, indent=4,  ensure_ascii=False)
                
            file_path= os.path.join(self.extracted_data_path, f"{self.test_year}_huma_questions.json" )
            with open(file_path, "w") as f_huma:
                json.dump(humanities_questions,f_huma, indent=4,  ensure_ascii=False)
                
            
