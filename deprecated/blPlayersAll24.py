# -*- coding: utf-8 -*-
"""
Created on Mon May 29 15:49:05 2023

@author: enado
"""
#USAR SOLO SI TODOS LOS EQUIPOS ESTÁN ACTUALIZADOS, POR LO GENERAL AL FINAL DE TORNEO

from urllib.request import urlopen
import json
import pandas as pd

clubes=["1 FC Koeln", "1 FSV Mainz 05", "1 FC Union Berlin", "Bayer 04 Leverkusen", "Bor Moenchengladbach", "Eintracht Frankfurt", "FC Augsburg", "FC Bayern Muenchen", "1 FC Heidenheim", "SV Darmstadt 98", "RB Leipzig", "SC Freiburg", "TSG Hoffenheim", "VfB Stuttgart", "VfL Wolfsburg", "VfL Bochum", "Werder Bremen", "Borussia Dortmund"]
dfTotal=[]
for club in clubes:
    club3=club.replace(" ", "-").lower()
    dfClub={}
    url=f"https://raw.githubusercontent.com/enadol/merobot/master/{club3}.json"
    response=urlopen(url)
    club_json=json.loads(response.read())
    for element in club_json:
        element.update({'Club': club})
        dfTotal.append(element)
        
df=pd.DataFrame(dfTotal)
df.to_csv("blplayers2024.csv", index=False)

pesonum=df.loc[df['Peso'].str.isnumeric()==True].reset_index()
pesoavg=pesonum.Peso.astype(int).mean()
print(f"Peso promedio = {pesoavg}")

alturanum=df.loc[df['Altura'].str.isnumeric()==True].reset_index()
alturaavg=alturanum.Altura.astype(int).mean()
print(f"Altura promedio = {alturaavg}")