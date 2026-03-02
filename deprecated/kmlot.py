# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:26:16 2022

@author: enado
"""

import camelot
import pandas as pd
lstClubesNeu=[]

url="C:\\Users\enado\Documents\coursera\Mod 1\Clubs-der-Bundesliga-2022-23-Geschaeftsjahresende-2021.pdf"

tables=camelot.read_pdf(url)

    
#clubesSalaries=pd.DataFrame(salary_values, lstClubesNeu, columns=['players salaries'])
#clubesSalaries.to_csv("report2022.csv", encoding='utf-8-sig')