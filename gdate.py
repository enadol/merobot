# -*- coding: utf-8 -*-
"""
Created on Mon May  9 18:47:36 2022

@author: enado
"""

import requests
from bs4 import BeautifulSoup

md=34
lstDates=[]
lstDatesCumul=['[Fr. 13.8.]',
 '[Fr. 20.8.]',
 '[Fr. 27.8.]',
 '[Sa. 11.9.]',
 '[Fr. 17.9.]',
 '[Fr. 24.9.]',
 '[Fr. 1.10.]',
 '[Fr. 15.10.]',
 '[Fr. 22.10.]',
 '[Fr. 29.10.]',
 '[Fr. 5.11.]',
 '[Fr. 19.11.]',
 '[Fr. 26.11.]',
 '[Fr. 3.12.]',
 '[Fr. 11.12.]',
 '[Di. 14.12.]',
 '[Fr. 17.12.]',
 '[Fr. 7.1.]',
 '[Fr. 14.1.]',
 '[Fr. 21.1.]',
 '[Fr. 4.2.]',
 '[Fr. 11.2.]',
 '[Fr. 18.2.]',
 '[Fr. 25.2.]',
 '[Fr. 4.3.]',
 '[Fr. 11.3.]',
 '[Fr. 18.3.]',
 '[Fr. 1.4.]',
 '[Fr. 8.4.]',
 '[Fr. 15.4.]',
 '[Fr. 22.4.]',
 '[Fr. 29.4.]',
 '[Fr. 6.5.]']

page= requests.get(f'https://kicker.de/bundesliga/spieltag/2021-22/{md}')


if page.status_code== 200:
    content = page.content

    
klass=["kick__v100-gameList__header"]

soup = BeautifulSoup(content, 'html.parser')
#print(soup.prettify())
dates=soup.find_all("div", attrs={"class": klass})

for date in dates:
    lstDates.append(date.text.strip())
    


date1=lstDates[0][:2].strip()
date2=lstDates[0].split(',')[1].split('.')[0].strip().lstrip("0")
date3=lstDates[0].split(',')[1].split('.')[1].lstrip("0")

#if int(date2)<=9:
 #   date2=str(int(date2))
#else:
#    date2=date2

    
dateDef=f'[{date1}. {date2}.{date3}.]'
#print(dateDef) 