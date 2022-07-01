# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# PDF Tables Extraction
# pip install tabula-py
import tabula
# save to CSV
tabula.convert_into("test.pdf", "output.pdf", output_format="csv", pages="all")
# save to Excel
tabula.convert_into("test.pdf", "output.pdf", output_format="xlsx", pages="all")
# save to JSON
tabula.convert_into("test.pdf", "output.pdf", output_format="json", pages="all")
# Extract Multiple Tables
tabula.read_pdf("test.pdf", pages="all", multiple_tables=True, output_format="csv")
# Extract Tables from Multiple PDF
tabula.convert_into_by_batch("pdfs", "output.pdf", output_format="csv", pages="all")

