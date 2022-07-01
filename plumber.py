# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:26:16 2022

@author: enado
"""

import pdfplumber
import pandas as pd
lstClubesNeu=[]

url="C:\\Users\enado\Documents\coursera\Mod 1\Clubs-der-Bundesliga-2022-23-Geschaeftsjahresende-2021.pdf"


with pdfplumber.open(url) as pdf:
    first_page=pdf.pages[0]
    tables=first_page.extract_table()
    #print(tables)
    #forclubs=tables[0][1].split('\n')
    #split1=forclubs[1].split('  ')
    clubes=tables[1][1:]
    salary_values=tables[5][1:]
    #teams_truncated=tables[0][1].split(' ')
    
        
for club in clubes:
    if '\n' in club:
        uno=club.split('\n')[0]
        dos=club.split('\n')[1]
        club=f'{uno}{dos}'
    #club.replace('\n ', ' ')
    #club.replace('  ', ' ')
    lstClubesNeu.append(club)    
    
clubesSalaries=pd.DataFrame(salary_values, lstClubesNeu, columns=['players salaries'])
clubesSalaries.to_csv("report2022.csv", encoding='utf-8-sig')