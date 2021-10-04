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
countgoles=0
lstMatch=[]
lstMD=[]
lstGoles=[]
lstGHome=[]
lstGAway=[]
lstGHomeH=[]
lstGAwayH=[]
lstIndexesH=[]
lstIndexesA=[]

page= requests.get('https://kicker.de/bundesliga/spieltag/2021-22/-1')

if page.status_code== 200:
    content = page.content
    

soup = BeautifulSoup(content, 'html.parser')
#print(soup.prettify())
clubes=soup.find_all("div", attrs={"class": "kick__v100-gameCell__team__name"})
goles=soup.find_all("div", attrs={"class": "kick__v100-scoreBoard__scoreHolder__score"})

for club in clubes:
    lstClubes.append(club.text.strip())

for gol in goles:
    lstGoles.append(gol.text.strip())
    
for club in lstClubes:
    #count=2
    if count%2==0:
        lstHome.append(club)
        count=count+1
    else:
        lstAway.append(club)
        count=count+1
        
def golesClass():
    nbuffer=0
    for n in range(0, len(lstGoles)):
        nbuffer=nbuffer+n
        goal=lstGoles[nbuffer]
        lstGHome.append(goal)
        nbuffer=nbuffer+1
        goal=lstGoles[nbuffer]
        lstGHomeH.append(goal)
        nbuffer=nbuffer+1
        goal=lstGoles[nbuffer]
        lstGAway.append(goal)
        nbuffer=nbuffer+1
        goal=lstGoles[nbuffer]
        lstGAwayH.append(goal)
        nbuffer=nbuffer+1

    
jornadas=soup.find_all("h3", attrs={"class": "kick__section-headline"})

for jornada in jornadas:
    lstJornadas.append(jornada.text.strip())

def getGAIndexes():
    factor=2
    while(factor<len(lstGoles)):
        lstIndexesA.append(factor)
        factor=factor+4

def getGHIndexes():
    factor=0
    while(factor<len(lstGoles)):
        lstIndexesH.append(factor)
        factor=factor+4


getGAIndexes()
getGHIndexes()

#for gol in lstGoles:
#    if countgoles%4==0:
#       lstGHome.append(gol)
#    countgoles=countgoles+1
 #   else:
 #       for index in lstIndexes:
 #           lstGAway.append(lstGoles[index])
 #       countgoles=countgoles+1
        
for index in lstIndexesA:
    element=lstGoles[index-1]
    lstGAway.append(element)


for index in lstIndexesH:
    element=lstGoles[index]
    lstGHome.append(element)


def matchIn():
    for i in range(0, len(lstGHome)):
        if(i <len(lstGHome)):
            lstMatch.append("    "+ lstHome[i] + "  "+lstGHome[i]+"-"+lstGAway[i]+"  "+ lstAway[i]+"\n")
        
def mdIn():

    for j in range(1,35):
        #f.write(lstJornadas[j]+"\n")
        md=matchIn()
        lstMD.append(md)
        

def meRobot():
    #f=codecs.open("bundesliga-21.txt", "w", "utf-8")       
    #f.write("\ufeff")
    #f.write(str(lstMD))
    #f.write("\n\n")    
    #f.close()
    
    with codecs.open("bundesliga-2022.txt", "w", "utf-8") as file:
        file.write("\ufeff")
        countjornadas=0
        count2=0
        for line in lstMatch:
            g=lstMatch.index(line)
            if g%9==0:
                file.write(lstJornadas[countjornadas]+ "\n")
                file.write("    "+ line)
                countjornadas=countjornadas+1
            else:
                if count2<=len(lstMatch):
                    file.write("    "+line)
            count2=count2+1
                                
            #else:
                #file.write("    "+line)
    file.close() 
    


matchIn()
meRobot()