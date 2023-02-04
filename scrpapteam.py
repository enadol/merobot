# -*- coding: utf-8 -*-
"""
Created on Mon May  9 18:47:36 2022

@author: enado
"""
import requests
from bs4 import BeautifulSoup
import numpy as np
import codecs
import json

vornamen=[]
nachnamen=[]
kader=[]
team=[]
nameexceptions=["Dani Olmo", "Diogo Leite", "Joao Cancelo", "Tiago Tomas", "Gil Dias"]
#player="Sadio Mane"
brasilexceptions=["Paulinho"]
duplicates=["Alexander Meyer", "Soumaila Coulibaly", "Tobias Strobl", "Luca Pellegrini", "Patrick Herrmann", "Christian Groß", "Ilia Gruev", "Dennis Geiger"]
triplicates=["Maximilian Bauer", "Florian Müller"]
exclude=["Michael Langer"]
revert=["Dikeni Salifou"]
vereinslos=["Max Kruse"]

club="VfB Stuttgart"
torneo="2022-23"
klassvita=["kick__vita__header__person-detail-kvpair-info"]
klassfrom=["kick__vita__header__team-detail__prime"]
klasspastclub=["kick__vita__stationline-team"]
klassalturapeso=["kick__vita__header__person-detail-kvpair-info kick__vita__header__person-detail-kvpair-info-s"]
klassnation=["kick__vita__header__person-detail-kvpair--nation"]
klasscompfilter=["kick__vita__liglog"]
klasstrikot=["kick__player__number"]

def modPlayer(player):
    playerdef=""
    if(player in revert):
        partido=player.split(" ")
        vorname=partido[1]
        nachname=partido[0]
        player=vorname+" "+nachname

    playerlow=player.lower()
    playerminus=playerlow.replace(" ", "-")
    if("ü" in playerminus):
        playerminus=playerminus.replace("ü", "ue")
    if("ö" in playerminus):
        playerminus=playerminus.replace("ö", "oe")
    if("é" in playerminus):
        playerminus=playerminus.replace("é", "e")
    if("ß" in playerminus):
        playerminus=playerminus.replace("ß", "ss")
    if("scally" in playerminus):
        playerminus=playerminus.replace("joe", "joseph")
    if("kouadio" in playerminus):
           playerminus=playerminus.replace("kone", "manu-kone")
    elif("ä" in playerminus):
        playerminus=playerminus.replace("ä", "ae")
    playerdef=playerminus
    
    return playerdef

def find_indices(ltc, itf):
    array=np.array(ltc)
    indices=np.where(array == itf)[0]
    return list(indices)

club3=modPlayer(club)

urlkader=f"https://www.kicker.de/{club3}/kader/bundesliga/{torneo}" 
kaderpage= requests.get(urlkader)
if kaderpage.status_code== 200:
    kadercontent = kaderpage.content

soupnames = BeautifulSoup(kadercontent, 'html.parser')
klassnames=["kick__table--ranking__index kick__t__a__l kick__respt-m-w-190"]

kadernames=soupnames.find_all("td", attrs={"class": klassnames})

for nombre in kadernames:
#base apellidos para nombres compuestos o apellidos compuestos
#kicker pone Dani Olmo como apellido

    apellidos=nombre.find("strong") 
    for apellido in apellidos:
        if(apellido in nameexceptions):
            partido=apellido.split(" ")
            vorname=partido[0]
            nachname=partido[1]
            kader.append(vorname+" "+nachname)
        
        else:
            nombres=nombre.find("span")
            if( nombres is not None):
                vornamen.append(nombres.text)
                nachnamen.append(apellidos.text)
                kader.append(nombres.text+" "+apellidos.text)
        #para nombres brasis p.ej. Thiago sin apellido
        if(apellido in brasilexceptions):
            vorname=apellido
            nachname=" "
            kader.append(vorname+" "+nachname)
        
        if(apellido=="Silas"):
            vorname=apellido
            nachname="Katompa Mvumpa"
            kader.append(vorname+" "+nachname)

                
        #     vorname="Joseph"
        #     nachname=apellido
        #     kader.append(vorname+" "+nachname)
    
for knombre in kader:
    player3=modPlayer(knombre)
    if(knombre in duplicates):
        player3=player3+"-2"
    
    if(knombre in triplicates):
        player3=player3+"-3"
        
    if("Perea" in knombre):
        player3=player3+"-mendoza"
        
    if("Paulinho" in knombre):
        player3=knombre.strip()+"-12"
        
    if(knombre=="Kelian Nsona"):
        player3=player3+"-wa-saka"
    
    if(knombre=="Vasilios Lampropoulos"):
        player3="vassilis-lampropoulos"
    
    url=f"https://kicker.de/{player3}/spieler/bundesliga/{torneo}/{club3}"
 # EJEMPLO https://www.kicker.de/niclas-fuellkrug/spieler/bundesliga/2022-23/werder-bremen
    mdpage= requests.get(url)
    if mdpage.status_code== 200:
        content = mdpage.content

    #para considerar chavales que vienen de inferiores o que solo han jugado en un equipo
    def past_club_index(pastclub):
        if len(pastclub)==1:
            indicepc=0
        else:
            indicepc=1
        return indicepc
    
       
    soup = BeautifulSoup(content, 'html.parser')
    dates=soup.find_all("div", attrs={"class": klassvita})
    desde=soup.find_all("span", attrs={"class": klassfrom})
    pastclub=soup.find_all("a", attrs={"class": klasspastclub})
    altura=soup.find_all("div", attrs={"class": klassalturapeso})
    nacion=soup.find_all("div", attrs={"class": klassnation})
    trikot=soup.find_all("span", attrs={"class": klasstrikot})
    
    indicepc=past_club_index(pastclub)

    born1=dates[1].text.split(" ")[1][:10]
    
    if(knombre in vereinslos):
       age="35"
       ageinclub=""
    else:
        age=dates[1].text.split(" ")[45][1:3]     
        ageinclub=desde[0].text
    fromclub=pastclub[indicepc].text[4:].split("\n")[0]
    if(len(altura)<1):
        alturatxt="No consignado"
    else:  
        alturatxt=altura[0].text.split(" ")[1]
    if(len(altura)<2):
        pesotxt="No consignado"
    else:
        pesotxt=altura[1].text.split(" ")[1]
    naciontxt=nacion[0].text.split("\r\n")[1].strip()
    
        
    for i in soup:
        soup2=soup.find_all("td")
        
    elementindex=[]    
    for e in soup2:
 
        #para chavales de la cantera sin debutar
        if "Bundesliga" not in e.text:
            pplayed="0"
            partidosbl="0"
            golesbl="0"
            assists="0"
            gelbe="0"
            gelbrot="0"
            rot="0"
        #separar bundesliga de otras ligas y de 2a Bundesliga        
        if(e.text.strip()=="Bundesliga"):
            indice=soup2.index(e)
            print(indice)
            elementindex.append(indice)
    elementix2=elementindex
    #para que corra el carrusel con todos los índices
    if(len(elementix2)>1):
        if knombre in exclude:
            pplayed="0"
            partidosbl="0"
            golesbl="0"
            assists="0"
            gelbe="0"
            gelbrot="0"
            rot="0"

        else:
            playedindex=elementix2[1]+1        
            pplayed=soup2[playedindex].text.strip().split("/")[0]            
            blgamesindex=elementindex[0]+1
            partidosbl=soup2[blgamesindex].text.strip().split("\n")[0]
            golesindex=elementindex[1]+3
            golesbl=soup2[golesindex].text.strip()
            assistindex=elementindex[1]+5
            assists=soup2[assistindex].text.strip()
            gelbindex=elementindex[1]+9
            gelbe=soup2[gelbindex].text.strip()
#gelbe=datosbl2[gelbindex].text.split("\r\n")[1]

            gelbrotindex=gelbindex+1
            gelbrot=soup2[gelbrotindex].text.strip()
#gelbrot=datosbl2[gelbrotindex].text.split("\r\n")[1]

            rotindex=gelbrotindex+1
            rot=soup2[rotindex].text.strip()

#para número no asignado de camiseta    
    if(len(trikot)>0):
        numero=trikot[0].text
    else:
        numero="0"
    playerdict={"Jugador": knombre, "Nacimiento": born1, "Edad": age, "Nación": naciontxt, "Altura": alturatxt, "Peso": pesotxt, "PJ": pplayed, "Goles": golesbl, "Asistencias": assists, "TA": gelbe, "TAR": gelbrot, "TR": rot, "Desde": ageinclub, "De": fromclub, "BL": partidosbl, "Número": numero}
#     playerdict={"Jugador": knombre, "Nacimiento": born1, "Edad": age, "Nación": naciontxt, "Altura": alturatxt, "Peso": pesotxt, "PJ": pplayed, "Goles": golesbl, "Asistencias": assists, "TA": gelbe, "TAR": gelbrot, "TR": rot, "Desde": ageinclub, "De": fromclub, "BL": partidosbl, "Número": numero}
    team.append(playerdict)

with codecs.open(f"C:/Users/enado/Proyectos/Python33/merobot/{club3}.txt", "w", "utf-8") as file:
    for item in team:
        #file.write('\n')    
        for key, value in item.items():
                
            file.write(key)
            file.write(" : ")
            file.write(str(value))
            file.write(',\n')
        file.write('\n')
file.close()

teamjson=json.dumps(team, indent=4, ensure_ascii=False)

with codecs.open(f"C:/Users/enado/Proyectos/Python33/merobot/{club3}.json", "w", "utf-8") as jsonfile:
    
    jsonfile.write(teamjson)
jsonfile.close()