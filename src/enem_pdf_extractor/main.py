
import pprint

class EnemPDFextractor():
    #-------constantes baseadas na nomeclatura do INEP dos arquivos do enem, ex: 2022_GB_impresso_D1_CD1.pdf------- 
    
    #utilizadas para identificar qual prova ou gabarito estamos lidando
    __YEAR_PATTERN__ = "20\d{2}"
    __DAY_ONE_SUBSTR__ = "D1"  #substr no nome do PDF que indica qual o dia da prova
    __TEST_IDENTIFIER__ = "PV"
    __ANSWER_PDF_IDENTIFIER__ = "GB"
    __NUM_PATTERN1__ = r"\*\w{9}\*"  #esses padrões vem de um código de barras presente no topo de toda página, ele vai ser removido
    __NUM_PATTERN2__ = r"\*\w{10}\*"
    __QUESTION_IDENTIFIER__ = "QUESTÃO"
    __TXT_QUESTION_TEMPLATE__= "(Enem/{test_year})  {question_text}\n(RESPOSTA CORRETA): {correct_answer}\n\n"
    __MD_QUESTION_TEMPLATE__ = "# Ano: (Enem/{test_year}) \n# texto da questão: \n {question_text} \n # (RESPOSTA CORRETA): {correct_answer}\n\n"
    __SUPPORTED_OUTPUT_FILES__:tuple = ("txt", "json", "markdown")
    __TEST_COLOR_PATTERN__ = "CD\d{1}"  #provas/cadernos e gabaritos  são separadas por cores, se as cores de ambos forem iguais, eles estão relacionados
 
    
    #-------variáveis específicas de cada classe-------
    test_pdf_path:str 
    answer_pdf_path:str
    extracted_data_path:str
    output_type:str 
    answer_pdf_text:str
    process_questions_with_images:bool 
    
    def __init__(self, output_type:str, process_questions_with_images:bool = True)-> None:
        """
        Construtor para a classe EnemPDFextractor.
        
        Argumentos:
            output_type (str) : Tipos de arquivo de output do texto, são suportados outputs .TXT e .JSON e Markdown.
            -OBS: arquivos JSON contem informações adicionais como lista de alternativas e lista de imagens associadas, caso imagens sejam extraídas.
            
            ignore_questions_with_images (bool) : Dita se textos e imagens de páginas com imagens serão processadas ou não.   
            -OBS: Caso a EXTRAÇÃO DE IMAGENS NÃO ESTEJA HABILITADA o código VAI PULAR PÁGINAS/QUESTÕES COM IMAGENS.
        """ 
        output_type = output_type.lower()
        if output_type not in self.__SUPPORTED_OUTPUT_FILES__:
            raise IOError("tipo de arquivo de output não suportado")

        self.output_type = output_type
        self.process_questions_with_images = process_questions_with_images
        
    #extrai o texto dos PDFs de um ano específico
    def extract_pdf(self, test_pdf_path: str, answers_pdf_path:str, extracted_data_path:str)-> None: 
        """
        Método público para extrair os conteúdos de um PDF do ENEM e escrever numa localização específica.

        Argumentos:
            test_pdf_path (str) : path para o PDF da prova do ENEM. 
            answers_pdf_path (str) : path para o gabarito da prova do ENEM.
            -OBS: ambos arquivos acima devem seguir a nomenclatura do PDF baixado do site do INEP.

            extracted_data_path (str) : path para o diretório onde os dados extraídos serão escritos.
        """
        pprint.pp({
            "test_pdf_path": test_pdf_path,
            "answers_pdf_path": answers_pdf_path,
            "extracted_data_path": extracted_data_path
        })