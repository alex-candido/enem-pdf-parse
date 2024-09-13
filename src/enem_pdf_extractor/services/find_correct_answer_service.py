import pymupdf
import re, os ,json 

#acha a resposta correta dado o texto do gabarito (attbr de class) e o numero da questão, retorna a alternativa correta
class FindCorrectAnswerService():
    def __init__(self, question_number: int, day_one: bool, answer_pdf_text: str, is_spanish_question: bool = False)-> str:
        self.question_number = question_number
        self.day_one = day_one
        self.is_spanish_question = is_spanish_question
        self.answer_pdf_text = answer_pdf_text
        
    def execute(self): 
        # if self.day_one:
        if self.question_number > 5:
            self.question_number = self.question_number -5
            
        question_string = str(self.question_number)
        question_num_pattern = r'\b' + question_string + r'\b'
        
        num_match = re.search(question_num_pattern, self.answer_pdf_text)
        
        print(question_num_pattern, self.is_spanish_question)
