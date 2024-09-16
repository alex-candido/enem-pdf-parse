import pprint

class GetJsonFromQuestionService():
    def __init__(self, question:str, day_one: bool ,year: int, correct_answer:str, number:int, alternative_list:list[str] = [] , image_list = [None])-> dict:
        self.question = question
        self.day_one = day_one
        self.year = year
        self.correct_answer = correct_answer
        self.number = number
        self.alternative_list = alternative_list
        self.image_list = image_list
        
    def execute(self): 
        day_identifier = "D1" if self.day_one else "D2"
        
        if self.day_one:
            self.number = self.number if self.number < 6 else self.number -5 #subtrair as 5 questões contadas na matéria de espanhol
        else:
            self.number += 90
            
        if self.alternative_list:
            if len(self.image_list) == 0 or  self.image_list[0] != None:
                json_dict = {
                    "question_text": self.question,
                    "correct_answer": self.correct_answer ,
                    "alternatives": self.alternative_list,
                    "page_images": self.image_list,
                    "ID": f"{self.year}_{day_identifier}_N{self.number}",
                    "year": self.year,
                    "day": day_identifier,
                    "question_num": self.question
                }
            else:
                json_dict = {
                    "question_text": self.question,
                    "correct_answer": self.correct_answer ,
                    "alternatives": self.alternative_list,
                    "ID": f"{self.year}_{day_identifier}_N{self.number}",
                    "year": self.year,
                    "day": day_identifier,
                    "question_num": self.question
                }
        else:
            if image_list:
                json_dict = {
                    "question_text": self.question,
                    "correct_answer": self.correct_answer ,
                    "ID": f"{self.year}_{day_identifier}_N{self.number}",
                    "year": self.year,
                    "day": day_identifier,
                    "question_num": self.question
                }
            else:
                json_dict = {
                    "question_text": self.question,
                    "correct_answer": self.correct_answer ,
                    "page_images": self.image_list,
                    "ID": f"{self.year}_{day_identifier}_N{self.number}",
                    "year": self.year,
                    "day": day_identifier,
                    "question_num": self.question
                }
                
        return json_dict