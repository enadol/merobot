# -*- coding: utf-8 -*-
"""
Created on Mon May  9 18:47:36 2022

@author: enado
"""
import requests
from bs4 import BeautifulSoup
#import numpy as np
import codecs
import json
import translators as ts

ts.translator="google"
vornamen=[]
nachnamen=[]
kader=[]
team=[]
name_exceptions=["Dani Olmo", "Diogo Leite", "Joao Cancelo", "Tiago Tomas", \
                 "Gil Dias","Fabio Carvalho", "Ilaix Moriba"]
#player="Sadio Mane"
brasil_exceptions=["Paulinho", "Aaron", "Jordan"]
duplicates=["Alexander Meyer", "Soumaila Coulibaly", "Tobias Strobl", "Luca Pellegrini", "Patrick Herrmann", "Christian Groß", "Ilia Gruev", "Dennis Geiger", "Marco Friedl", "Matthias Bader", "Fabio Carvalho"]
triplicates=["Maximilian Bauer", "Florian Müller"]
sextuples=["Andreas Müller"]
exclude=["Michael Langer", "Malik Tillman", "Paul Wanner", "Arijon Ibrahimovic"]
revert=["Dikeni Salifou"]
vereinslos=["Max Kruse"]
#que ya jugaron en bundesliga pero se fueron y luego regresaron
#prodigos=["Alexander Nübel", "Malik Tillman"]

#Bor Mönchengladbach para Gladbach
#Bayer 04 Leverkusen 1FC Heidenheim
club="TSG Hoffenheim"
torneo="2023-24"
klassvita="kick__vita__header__person-detail-kvpair-info"
klassfrom="kick__vita__header__team-detail__prime"
klasspastclub="kick__vita__stationline-team"
klassalturapeso="kick__vita__header__person-detail-kvpair-info kick__vita__header__person-detail-kvpair-info-s"
klassnation="kick__vita__header__person-detail-kvpair--nation"
klasscompfilter="kick__vita__liglog"
klasstrikot="kick__player__number"
klasslaender="kick__bubble__prime"
klassages="kick__table-small-txt"

def mod_player(player):
    player_def=""
    if(player in revert):
        partido=player.split(" ")
        vorname=partido[1]
        nachname=partido[0]
        player=f"{vorname} {nachname}"

    player_low=player.lower()
    player_minus=player_low.replace(" ", "-")
    if("ü" in player_minus):
        player_minus=player_minus.replace("ü", "ue")
    if("ö" in player_minus):
        player_minus=player_minus.replace("ö", "oe")
    if("é" in player_minus):
        player_minus=player_minus.replace("é", "e")
    if("ß" in player_minus):
        player_minus=player_minus.replace("ß", "ss")
    if("scally" in player_minus):
        player_minus=player_minus.replace("joe", "joseph")
    if("kouadio" in player_minus):
           player_minus=player_minus.replace("kone", "manu-kone")
#    if("Aaron" in playerminus):
 #      playerminus=playerminus.replace(" ", "")    
    elif("ä" in player_minus):
        player_minus=player_minus.replace("ä", "ae")
    player_def=player_minus
    
    return player_def

#def find_indices(ltc, itf):
 #   array=np.array(ltc)
  #  indices=np.where(array == itf)[0]
  #  return list(indices)

club_for_url=mod_player(club)

url_kader=f"https://www.kicker.de/{club_for_url}/kader/bundesliga/{torneo}" 
kaderpage= requests.get(url_kader)
if kaderpage.status_code== 200:
    kadercontent = kaderpage.content

soupnames = BeautifulSoup(kadercontent, 'html.parser')
klass_names="kick__table--ranking__index kick__t__a__l kick__respt-m-w-190"

kader_names=soupnames.find_all("td", attrs={"class": klass_names})

for nombre in kader_names:
#base apellidos para nombres compuestos o apellidos compuestos
#kicker pone Dani Olmo como apellido
    vertrag=""

        
    apellidos=nombre.find("strong") 
    for apellido in apellidos:
        if(apellido in name_exceptions):
            partido=apellido.split(" ")
            vorname=partido[0]
            nachname=partido[1]
            kader.append(f"{vorname} {nachname}")
        else:
            nombres=nombre.find("span")
            if( nombres is not None):
                vornamen.append(nombres.text)
                nachnamen.append(apellidos.text)
                kader.append(nombres.text+" "+apellidos.text)
        #para nombres brasis p.ej. Thiago sin apellido
        if(apellido in brasil_exceptions):
            vorname=apellido
            nachname=" "
            kader.append(f"{vorname} {nachname}")
        
        if(apellido=="Silas"):
            vorname=apellido
            nachname="Katompa Mvumpa"
            kader.append(f"{vorname} {nachname}")

        if(apellido=="Jordan"):
            if(club=="Bor Moenchengladbach"):
                vorname=apellido
                nachname="Siebatcheu"
                kader.append(f"{vorname} {nachname}")
        
        if(apellido=="Tuta"):
#            if(club=="1 FC Union Berlin"):
            vorname="Lucas"
            nachname="Silva Melo"
            kader.append(f"{vorname} {nachname}")

        if(apellido=="Xavi"):
            vorname=apellido
            nachname="Simons"
            kader.append(f"{vorname} {nachname}")
                
        #     vorname="Joseph"
        #     nachname=apellido
        #     kader.append(vorname+" "+nachname)
    
for knombre in kader:
    player_for_url=mod_player(knombre)
    if(knombre in duplicates):
        player_for_url=f"{player_for_url}-2"
    
    if(knombre in triplicates):
        player_for_url=f"{player_for_url}-3"
        
    if(knombre in sextuples):
        player_for_url=f"{player_for_url}-6"

        
    if("Perea" in knombre):
        player_for_url=f"{player_for_url}-mendoza"
        
    if("Paulinho" in knombre):
        player_for_url=knombre.strip()+"-12"
    
    #if("Aaron" in knombre):
      #  player3="aaron-2"
        
    if(knombre=="Kelian Nsona"):
        player_for_url=f"{player_for_url}-wa-saka"
    
    if(knombre=="Vasilios Lampropoulos"):
        player_for_url="vassilis-lampropoulos"
        
    if(knombre=="Aurelio Buta"):
        player_for_url="buta"
    
    if(knombre=="Lucas Silva Melo"):
        player_for_url="tuta"
        
    if(knombre=="Jan Schröder"):
        player_for_url="jan-alex-wilson-schroeder"
        
    if(knombre=="Elias Bakatukanda"):
        player_for_url="elias-geoffrey-bakatukanda"
        
    if(knombre=="Moritz-Broni Kwarteng"):
        player_for_url="moritz-kwarteng"
        
    if(knombre=="Madi Monamay"):
        player_for_url="madi-monomay"
        
    if(knombre=="Thomas Isherwood"):
        player_for_url="thomas-poppler-isherwood"
        
    if(knombre=="Willian Pacho"):
        player_for_url="william-pacho"
        
    if(knombre=="Olivier Deman"):
        player_for_url="oliver-deman"
    
    
    url_player=f"https://kicker.de/{player_for_url}/spieler/bundesliga/{torneo}/{club_for_url}"
 # EJEMPLO https://www.kicker.de/niclas-fuellkrug/spieler/bundesliga/2022-23/werder-bremen
    mdpage= requests.get(url_player)
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
    ages=soup.find_all("span", attrs={"class": klassages})
    dates=soup.find_all("div", attrs={"class": klassvita})
    desde=soup.find_all("span", attrs={"class": klassfrom})
    past_club=soup.find_all("a", attrs={"class": klasspastclub})
    altura=soup.find_all("div", attrs={"class": klassalturapeso})
    nacion=soup.find_all("div", attrs={"class": klassnation})
    trikot=soup.find_all("span", attrs={"class": klasstrikot})
        
    
    indicepc=past_club_index(past_club)

    born1=dates[1].text.split(" ")[1][:10]
    
    lfilter1=soup.find_all("tbody")
    lfilter2=soup.find_all("span", attrs={"class": klasslaender})
    
    if len(lfilter1)>1:
        if lfilter1[1].text.strip().startswith("Länderspiele"):
            laenderspiele=lfilter2[0].text
        else:
            laenderspiele="No"
    else:
        laenderspiele="No"
    
    
    if(knombre in vereinslos):
       age=""
       ageinclub=""
       vertrag=""
    else:
        age=ages[0].text[1:3]
        #age=dates[1].text.split(" ")[45][1:3]     
        if len(desde)>=2:
            ageinclub=desde[0].text
            vertrag=desde[1].text
        else:
            ageinclub=desde[0].text
            vertrag="N.D."
    fromclub=past_club[indicepc].text[4:].split("\n")[0]
    if len(altura)<1:
        alturatxt="N.D."
    else:  
        alturatxt=altura[0].text.split(" ")[1]
    if len(altura)<2:
        pesotxt="N.D."
    else:
        pesotxt=altura[1].text.split(" ")[1]
    pais=nacion[0].text.split("\r\n")[1].strip()
    naciontxt=ts.translate_text(pais, from_language="de", to_language="es")

    
        
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
            played_index=elementix2[1]+1        
            pplayed=soup2[played_index].text.strip().split("/")[0]            
            blgames_index=elementindex[0]+1
            partidosbl=soup2[blgames_index].text.strip().split("\n")[0]
            goles_index=elementindex[1]+3
            golesbl=soup2[goles_index].text.strip()
            assist_index=elementindex[1]+5
            assists=soup2[assist_index].text.strip()
            gelb_index=elementindex[1]+9
            gelbe=soup2[gelb_index].text.strip()
#gelbe=datosbl2[gelbindex].text.split("\r\n")[1]

            gelb_rot_index=gelb_index+1
            gelb_rot=soup2[gelb_rot_index].text.strip()
#gelbrot=datosbl2[gelbrotindex].text.split("\r\n")[1]

            rot_index=gelb_rot_index+1
            rot=soup2[rot_index].text.strip()

#para número no asignado de camiseta    
    if(len(trikot)>0):
        numero=trikot[0].text
    else:
        numero="0"
    player_dict={"Jugador": knombre.strip(), "Nacimiento": born1, "Edad": age, "Nación": naciontxt, "Altura": alturatxt, "Peso": pesotxt, "PJ": pplayed, "Goles": golesbl, "Asistencias": assists, "TA": gelbe, "TAR": gelbrot, "TR": rot, "Desde": ageinclub, "De": fromclub, "BL": partidosbl, "Número": numero, "Contrato": vertrag, "Selección": laenderspiele}
#     playerdict={"Jugador": knombre, "Nacimiento": born1, "Edad": age, "Nación": naciontxt, "Altura": alturatxt, "Peso": pesotxt, "PJ": pplayed, "Goles": golesbl, "Asistencias": assists, "TA": gelbe, "TAR": gelbrot, "TR": rot, "Desde": ageinclub, "De": fromclub, "BL": partidosbl, "Número": numero}
    team.append(player_dict)

with codecs.open(f"C:/Users/enado/Proyectos/Python33/merobot/{club_for_url}.txt", "w", "utf-8") as file:
    for item in team:
        #file.write('\n')    
        for key, value in item.items():
            file.write(key)
            file.write(" : ")
            file.write(str(value))
            file.write(',\n')
        file.write('\n')
file.close()

team_json=json.dumps(team, indent=4, ensure_ascii=False)

with codecs.open(f"C:/Users/enado/Proyectos/Python33/merobot/{club_for_url}.json", "w", "utf-8") as jsonfile:
    
    jsonfile.write(team_json)
jsonfile.close()