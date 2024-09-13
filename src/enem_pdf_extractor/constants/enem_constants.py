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
__TEST_COLOR_PATTERN__ = "CD\d{1}"