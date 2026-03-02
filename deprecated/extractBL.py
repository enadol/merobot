# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tabula


url="C:\\Users\enado\Documents\coursera\Mod 1\Clubs-der-2.-Bundesliga-2022-23-Geschaeftsjahresende-2021.pdf"

#df=tabula.read_pdf(url, encoding="utf-8", pages=1)
#df.to_csv('out.csv')


# PDF Tables Extraction
# pip install tabula-py
# save to CSV
tabula.convert_into("C:\\Users\enado\Documents\coursera\Mod 1\Clubs-der-2.-Bundesliga-2022-23-Geschaeftsjahresende-2021.pdf", "2BLFinanz21.csv", output_format="csv", pages=1)
# save to Excel
#tabula.convert_into("test.pdf", "output.pdf", output_format="xlsx", pages="all")
# save to JSON
#tabula.convert_into("test.pdf", "output.pdf", output_format="json", pages="all")
# Extract Multiple Tables
#tabula.read_pdf("test.pdf", pages="all", multiple_tables=True, output_format="csv")
# Extract Tables from Multiple PDF
#tabula.convert_into_by_batch("pdfs", "output.pdf", output_format="csv", pages="all")

