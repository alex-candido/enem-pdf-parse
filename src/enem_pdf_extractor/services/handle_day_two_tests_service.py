import pymupdf

class HandleDayTwoTestsService():
    def __init__(self, pdf_reader: pymupdf.pymupdf.Document, test_year: int)-> None:
        self.pdf_reader = pdf_reader
        self.test_year = test_year
        
    def execute(self): 
        print("Executing HandleDayTwoTestsService")
        