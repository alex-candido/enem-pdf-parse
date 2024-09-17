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
        if self.day_one:
            if self.question_number > 5:
                # -5 pois a partir do questão 5, inicia o intervalo 1
                self.question_number = self.question_number -5
                
            question_string = str(self.question_number)
            question_num_pattern = r'\b' + question_string + r'\b'
            
            num_match = re.search(question_num_pattern, self.answer_pdf_text)
            
            # se achamos o número da questão isolado (não como parte de outro número)
            if num_match: 
                if self.question_number < 10 :
                    if self.is_spanish_question:
                        answer_index:int = (num_match.start() +4) #se o numero da questão de for de 1 digito, e ela for de espanhol, a resposta está a 4 espaços na direita
                    else:
                        answer_index = (num_match.start() +2) #se o numero da questão de for de 1 digito, e ela for de inglês, a resposta está a 2 espaços na direita
                
                else:  answer_index = (num_match.start() +3) #se tiver 2 dígitos, a resposta está a 3 espaços na direita
                
            else: 
                return "não achou a questão"
            
            return self.answer_pdf_text[answer_index]
        # else:
        #     question_number += 90  #gabarito do segundo dia começa da questão 91, mas a lógica do código conta as questões do 0 independente do dia, entao para achar é preciso somar +90

        #     question_string = str(question_number)
        #     question_num_pattern = r'\b' + question_string + r'\b'
        #     num_match =  re.search(question_num_pattern, self.answer_pdf_text)

        #     if num_match:
        #         if question_number < 100 :
        #             answer_index = (num_match.start() +3) #se o numero da questao de for de 2 digitos (antes de subtrai 90), a resposta está a 3 espaços na direita
        #         else:  
        #             answer_index = (num_match.start() +4) #se tiver 3 digitos, a resposta está a 4 espaços na direita

        #         return self.answer_pdf_text[answer_index]
        #     else:
        #         return "não achou a questão"