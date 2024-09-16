from enem_pdf_extractor.app import CreateApp

image_extraction:list = [True,False]
#tupla para acessar as provas e gabaritos do primeiro e segundo dia (caderno azul)
day_color_identifier:list[tuple] = [(1,1),(2,7)] 

# years:list[int] = [23,22,21,20]
years:list[int] = [23]
output_file:list[str] = ["txt", "json"]
pdf_folder_path:str = "pdfs_enem"
test_pdf_path: str = "src/pdfs_enem"
extracted_data_path: str = "src/test_output"

app = CreateApp(
    image_extraction=image_extraction, 
    day_color_identifier=day_color_identifier, 
    years=years, 
    output_file=output_file, 
    pdf_folder_path=pdf_folder_path,
    test_pdf_path=test_pdf_path,
    extracted_data_path=extracted_data_path
    )

app.run()