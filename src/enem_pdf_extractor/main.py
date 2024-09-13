import re, os ,json 
import pprint
import pymupdf

from typing import Any  

from enem_pdf_extractor.services.handle_IO_errors_service import HandleIOErrorsService
from enem_pdf_extractor.services.handle_day_one_tests_service import HandleDayOneTestsService
from enem_pdf_extractor.services.handle_day_one_with_images_service import HandleDayOneWithImagesService
from enem_pdf_extractor.services.handle_day_two_tests_service import HandleDayTwoTestsService
from enem_pdf_extractor.services.handle_day_two_with_images_service import HandleDayTwoWithImagesService

import enem_pdf_extractor.constants.enem_constants as enem_constants

class EnemPDFextractor():
    
    #-------variáveis específicas de cada classe-------
    test_pdf_path: str 
    answer_pdf_path: str
    extracted_data_path: str
    output_type: str 
    answer_pdf_text: str
    process_questions_with_images: bool 
    
    def __init__(self, output_type: str, process_questions_with_images: bool = True)-> None:
        """
        Construtor para a classe EnemPDFextractor.
        
        Argumentos:
            output_type (str) : Tipos de arquivo de output do texto, são suportados outputs .TXT e .JSON e Markdown.
            -OBS: arquivos JSON contem informações adicionais como lista de alternativas e lista de imagens associadas, caso imagens sejam extraídas.
            
            ignore_questions_with_images (bool) : Dita se textos e imagens de páginas com imagens serão processadas ou não.   
            -OBS: Caso a EXTRAÇÃO DE IMAGENS NÃO ESTEJA HABILITADA o código VAI PULAR PÁGINAS/QUESTÕES COM IMAGENS.
        """ 
        
        output_type = output_type.lower()
        if output_type not in enem_constants.__SUPPORTED_OUTPUT_FILES__:
            raise IOError("tipo de arquivo de output não suportado")

        self.output_type = output_type
        self.process_questions_with_images = process_questions_with_images
        
    #extrai o texto dos PDFs de um ano específico
    def extract_pdf(self, test_pdf_path: str, answers_pdf_path: str, extracted_data_path: str)-> None: 
        """
        Método público para extrair os conteúdos de um PDF do ENEM e escrever numa localização específica.

        Argumentos:
            test_pdf_path (str) : path para o PDF da prova do ENEM. 
            answers_pdf_path (str) : path para o gabarito da prova do ENEM.
            -OBS: ambos arquivos acima devem seguir a nomenclatura do PDF baixado do site do INEP.

            extracted_data_path (str) : path para o diretório onde os dados extraídos serão escritos.
        """
        
        HandleIOErrorsService(test_pdf_path=test_pdf_path, answers_pdf_path=answers_pdf_path).execute()
        
        answer_pdf_reader: pymupdf.pymupdf.Document = pymupdf.open(answers_pdf_path)
        answer_page: pymupdf.pymupdf.Document.Page = answer_pdf_reader[0]
        raw_answer_text: str = answer_page.get_text()
        
        answers_pattern = "^.{4,}$" 
        #tira todas as linhas do gabarito com mais de 4 chars, ja que todas as respostas são formatadas com os números (max de 3 chars) em uma linha e a letra certa na prox
        
        modified_text = re.sub(answers_pattern, "", raw_answer_text, flags=re.MULTILINE)
        
        self.answer_pdf_text: str = modified_text 
        # texto do gabarito, usado para a função que pega a resposta oficial
        self.answer_pdf_path: str = answers_pdf_path
        self.test_pdf_path: str = test_pdf_path
        
        absolute_path: str = os.path.abspath(extracted_data_path)
        # cria path absoluto para o diretório de output com o argumento da função
        
        if not os.path.isdir(absolute_path):
            print("diretório não encontrado, criando um novo")
            os.makedirs(absolute_path)
            
        self.extracted_data_path: str = absolute_path
        
        test_pdf_reader: pymupdf.pymupdfHandleDayOneTests.Document = pymupdf.open(test_pdf_path) 
        
        regex_return: list = re.findall(enem_constants.__YEAR_PATTERN__, self.test_pdf_path)
        test_year: int = int(regex_return[0]) 
        
        if enem_constants.__DAY_ONE_SUBSTR__ in test_pdf_path:     
            if not self.process_questions_with_images:
                print("D1 - NOT WITH IMAGES")
                
                HandleDayOneTestsService(test_pdf_reader, test_year, output_type = self.output_type, answer_pdf_text = self.answer_pdf_text).execute()
                
        #     else:
        #         # pdf_reader = fitz.open(self.test_pdf_path)
        #         HandleDayOneWithImagesService(test_pdf_reader, test_year = test_year).execute()
        #         pprint.pp({
        #             "D1 - WITH IMAGES",
        #         })
        # else:
        #     if not self.process_questions_with_images:
        #         HandleDayTwoTestsService(test_pdf_reader, test_year).execute()
        #         pprint.pp({
        #             "D2 - NOT WITH IMAGES",
        #         })
        #     else:
        #         HandleDayTwoWithImagesService(test_pdf_reader, test_year).execute()
        #         pprint.pp({
        #             "D2 - WITH IMAGES",
        #         })

    
        
        
        