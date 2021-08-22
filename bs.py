# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 12:50:41 2021

@author: enado
"""

import requests
from bs4 import BeautifulSoup
import codecs

lstJornadas=[]
lstClubes=[]
lstHome=[]
lstAway=[]
count=0
lstMatch=[]
lstMD=[]


page= requests.get('https://kicker.de/bundesliga/spieltag/2021-22/-1')

if page.status_code== 200:
    content = page.content
    

soup = BeautifulSoup(content, 'html.parser')
#print(soup.prettify())
clubes=soup.find_all("div", attrs={"class": "kick__v100-gameCell__team__name"})


for club in clubes:
    lstClubes.append(club.text.strip())
    
for club in lstClubes:
    #count=2
    if count%2==0:
        lstHome.append(club)
        count=count+1
    else:
        lstAway.append(club)
        count=count+1
        
    
jornadas=soup.find_all("h3", attrs={"class": "kick__section-headline"})

for jornada in jornadas:
    lstJornadas.append(jornada.text.strip())




def matchIn():
    for i in range(0, 306):
       lstMatch.append("    "+ lstHome[i] + "  -  "+ lstAway[i]+"\n")
        
def mdIn():

    for j in(1,35):
        #f.write(lstJornadas[j]+"\n")
        md=matchIn(j)
        lstMD.append(md)
        

def meRobot():
    f=codecs.open("bundesliga-22.txt", "w", "utf-8")       
    f.write("\ufeff")
    f.write(str(lstMD))
    f.write("\n\n")    
    f.close()
    
with codecs.open("bundesliga-2022.txt", "w", "utf-8") as file:
    count=0
    for line in lstMatch:
        g=lstMatch.index(line)
        if g%9==0:
            file.write(lstJornadas[count]+ "\n")
            file.write("    "+line)
            count=count+1
                        
        else:
            file.write("    "+line)
file.close() 

matchIn()
meRobot()