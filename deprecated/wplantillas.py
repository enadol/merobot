# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:40:12 2023

@author: enado
"""

import docx

# Abre el documento de Word existente
doc = docx.Document("plantilla_base.docx")

# Abre el archivo de texto
with open("documento.txt", "r") as file:
    text = file.read()

# Separa el texto en 16 campos
fields = text.split("\n")[:16]

# Reemplaza cada párrafo en el documento de Word con un campo
for i, field in enumerate(fields):
    doc.paragraphs[i].text = field

# Guarda el documento de Word
doc.save("plantilla_modificada.docx")
