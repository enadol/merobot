# -*- coding: utf-8 -*-
"""
Created on Mon May  9 18:47:36 2022

@author: enado
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

md=34
lstDates=[]
lstDatesCumul=['[Fr. 5.8.]','[Fr. 12.8.]','[Fr. 19.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]','[Fr. 5.8.]', '[Fr. 5.8.]']
url=f'https://kicker.de/bundesliga/spieltag/2021-22/{md}'
               
page= requests.get(url)


if page.status_code== 200:
    content = page.content

    
klass=["kick__v100-gameList__header"]

soup = BeautifulSoup(content, 'html.parser')
#print(soup.prettify())
dates=soup.find_all("div", attrs={"class": klass})

def dateOnList(date):
    lstDates.append(date.text.strip())

def datesAllOn():
    list(map(lambda x : dateOnList(x), dates))

datesAllOn()
#for date in dates:
 #   lstDates.append(date.text.strip())
    


date1=lstDates[0][:2].strip()
date2=lstDates[0].split(',')[1].split('.')[0].strip().lstrip("0")
date3=lstDates[0].split(',')[1].split('.')[1].lstrip("0")

#if int(date2)<=9:
 #   date2=str(int(date2))
#else:
#    date2=date2

    
dateDef=f'[{date1}. {date2}.{date3}.]'
#print(dateDef) 