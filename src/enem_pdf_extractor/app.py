import time
from enem_pdf_extractor.main import EnemPDFextractor

class CreateApp():
    no_images_timer:float = 0.0
    images_timer:float = 0.0
    execution_counter:int = 0 
    
    def __init__(self, image_extraction: list, day_color_identifier: list[tuple], years: list[int], output_file: list[str], pdf_folder_path: str, test_pdf_path: str, extracted_data_path: str):
        self.image_extraction = image_extraction
        self.day_color_identifier = day_color_identifier
        self.years = years
        self.output_file = output_file
        self.pdf_folder_path = pdf_folder_path
        self.test_pdf_path = test_pdf_path
        self.extracted_data_path = extracted_data_path
        
    def run(self):
        for image in self.image_extraction:
            for output in self.output_file:
                text_extractor = EnemPDFextractor(output_type=output, process_questions_with_images=image)
                image_identifier = "img" if image else ""  
                
                for i, j in self.day_color_identifier:
                    for year in self.years: 
                        time_before: float = time.time()

                        text_extractor.extract_pdf(
                            test_pdf_path=f"{self.test_pdf_path}/20{year}/20{year}_PV_impresso_D{i}_CD{j}.pdf",
                            answers_pdf_path=f"{self.test_pdf_path}/20{year}/20{year}_GB_impresso_D{i}_CD{j}.pdf", 
                            extracted_data_path=f"{self.extracted_data_path}/20{year}_D{i}_{image_identifier}"
                        )
                    
                        time_passed = time.time() - time_before
                        self.execution_counter += 1
                        if image:
                            self.images_timer += time_passed
                        else:
                            self.no_images_timer += time_passed

        #metades das execuções são extraindo imagens, metade não
        self.execution_counter /= 2  

        print(f"tempo médio extrair PDFs sem imagens {self.no_images_timer/self.execution_counter}, tempo médio para extrair os pdfs com as images {self.images_timer/self.execution_counter}")