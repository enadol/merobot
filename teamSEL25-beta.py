# -*- coding: utf-8 -*-
"""
Created on Mon May  9 18:47:36 2022

@author: enado
"""
"""import packages"""
import codecs
import json
import translators as ts
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

vornamen=[]
nachnamen=[]
kader=[]
team=[]
#player="Sadio Mane"
brasil_exceptions=["Paulinho", "Aaron", "Tuta", "Maurides", "Arthur", "Rogerio"]
duplicates=["Alexander Meyer", "Soumaila Coulibaly", "Tobias Strobl", "Luca Pellegrini", \
            "Patrick Herrmann", "Christian Groß", "Ilia Gruev", "Dennis Geiger", "Marco Friedl", \
                "Matthias Bader", "Fabio Carvalho", "Mahmoud Dahoud", "Denis Huseinbasic", \
            "Robert Wagner", "Carl Johansson", "Pascal Groß", "Krisztian Lisztes", \
        "Igor Matanovic", "Eljif Elmas", "Lutsharel Geertruida", "Marin Ljiubicic", \
    "Nick Schmidt", "Daniel Klein", "Nick Schmidt", "Oliver Sorg", \
"Lazar Jovanovic", "Marius Müller"]
triplicates=["Maximilian Bauer", "Florian Müller", "Luis Diaz"]
cuatruples=["Timo Becker"]
quintuples=["Arthur", "Rogerio"]
sextuples=["Andreas Müller"]
eightuples=["Romulo "]
exclude=["Michael Langer", "Malik Tillman", "Arijon Ibrahimovic"]
split_and_revert=["Dikeni Salifou", "Vieira Fabio", "Souza Vinicius"]
vereinslos=["Max Kruse", "Anwar El Ghazi", "Mats Heitmann"]
#provisional para primera jornada
no_games_season=["Gustavo Puerta", "Tarek Buchmann", "Jonah Kusi-Asare", "Jamal Musiala", "Silas ", "Dmytro Bogdanov",\
 "Bilal El Khannouss", "Bouanani Badredine"]
no_games_at_all=["Leon Klanac"]
no_complete=["Matija Marsenic", "Oluwaseun Ogbemudia", "Bungi Joyeux Masanka"]
name_plus_complex_surname=["van den Berg Rav", "El Mala Said", "El Mala Malek", "Skov Olsen Andreas",\
 "Heuer Fernandes Daniel", "Ben Seghir Eliesse", "El Khannouss Bilal", "da Costa Danny", "Pereira Cardoso Tiago"]
complex_name_surname=["Johannesson Isak Bergmann", "Lokonga Albert Sambi"]
name_leave=["Fabio Vieira", "Arthur Chaves", "Luis Diaz", "Aleix Garcia", "Tiago Tomas",\
 "Badredine Bouanani", "Kaua Santos", "Yan Couto", "Diogo Leite", "Fabio Silva"]
#que ya jugaron en bundesliga pero se fueron y luego regresaron
#prodigos=["Alexander Nübel", "Malik Tillman"]

#Bor Mönchengladbach para Gladbach
#Bayer 04 Leverkusen 1 FC Heidenheim 1 FC Union Berlin
# 1 FC Köln
# 1 FSV Mainz 05 FC St Pauli VfL Bochum Hamburger SV

club="1 FC Köln"
torneo="2025-26"

klassvita="kick__vita__header__person-detail-kvpair-info"
klassfrom="kick__vita__header__team-detail__prime"
klasspastclub="kick__vita__stationline-team"
klassalturapeso="kick__vita__header__person-detail-kvpair-info kick__vita__header__person-detail-kvpair-info-s"
klassnation="kick__vita__header__person-detail-kvpair--nation"
klasscompfilter="kick__vita__liglog"
klasstrikot="kick__player__number"
klasslaender="kick__bubble__prime"
klassages="kick__table-small-txt"
klasstarjetas="kick__site-padding kick__gameinfo-block"

def for_url(player):
    """Convierte nombre de jugador o club a formato URL de Kicker"""
    player_def=""
 #   if player in split_and_revert:
 #       name_split=player.split(" ")
 #       vorname=name_split[1]
 #       nachname=name_split[0]
 #       player=f"{vorname} {nachname}"

    player_low=player.lower()
    player_minus=player_low.replace(" ", "-")
    if "ü" in player_minus:
        player_minus=player_minus.replace("ü", "ue")
    if"ö" in player_minus:
        player_minus=player_minus.replace("ö", "oe")
    if"é" in player_minus:
        player_minus=player_minus.replace("é", "e")
    if "ß" in player_minus:
        player_minus=player_minus.replace("ß", "ss")
    if "scally" in player_minus :
        player_minus=player_minus.replace("joe", "joseph")
    if "kouadio" in player_minus:
        player_minus=player_minus.replace("kone", "manu-kone")
    elif "ä" in player_minus:
        player_minus=player_minus.replace("ä", "ae")
    player_def=player_minus
    return player_def

def convert_to_cero(indicator):
    """Convierte a 0 si el indicador no es un dígito"""
    if len(str(indicator)) !=1:
        indicator=0
    else:
        indicator=indicator
    return indicator

club_for_url=for_url(club)


DRIVER_PATH='C:/Users/enado/ChromeDriver'
service = webdriver.ChromeService(executable_path = 'C:/Users/enado/ChromeDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(0.5)
driver.maximize_window()


url_kader=f"https://www.kicker.de/{club_for_url}/kader/bundesliga/{torneo}"
kader_page= driver.get(url_kader)
WebDriverWait(driver, 10)

# 4. Click the "Google Web" option
#google_web_option.click()

# 5. Wait for the "Accept" button to be clickable
accept_button = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH,"//a[contains(text(), 'Zustimmen & weiter')]")))

# 6. Click the "Accept" button
accept_button.click()

kader_names=driver.find_elements(By.CLASS_NAME, "kick__respt-m-w-190")
#Nombres para la plantilla NO PARA URL
for i in kader_names[1:]:
    jugador=i.text
    if jugador =="Fernandes Daniel Heuer":
        jugador="Daniel Heuer Fernandes"
    
    if jugador == "Xavi":
        #nachnahme="Simons"
        jugador="Simons Xavi"

    vertrag=""
    completo=jugador.split(" ", 1)
    if jugador != "SPIELER":
        if len(completo) < 2:
            vorname = completo[0].strip()
            nachname = ""
            kader.append(f"{vorname} {nachname}")
        else:
            if jugador in name_plus_complex_surname:
                name_partition=jugador.rsplit(" ", 1)          
                vorname = name_partition[1].strip()
                nachname = name_partition[0].strip()

            elif jugador in complex_name_surname:
                name_partition=jugador.split(" ", 1)
                vorname = name_partition[1].strip()
                nachname = name_partition[0].strip()

            elif jugador in name_leave:
                vorname = completo[0].strip()
                nachname = completo[1].strip()
                
            else:
                nachname = completo[0].strip()
                vorname = completo[1].strip()

            kader.append(f"{vorname} {nachname}")

        if vorname=="Pereira Lage":
            kader.append("Mathias Pereira Lage")

        if nachname=="Heuer" and vorname=="Fernandes Daniel":
            kader.append("Daniel Heuer Fernandes")

for knombre in kader:
    player_for_url=for_url(knombre)
    #URL exception cases
    if knombre in duplicates:
        player_for_url=f"{player_for_url}-2"

    if knombre in triplicates :
        player_for_url=f"{player_for_url}-3"

    if knombre in cuatruples :
        player_for_url=f"{player_for_url}-4"

    if knombre in sextuples:
        player_for_url=f"{player_for_url}-6"

    if knombre in eightuples:
        player_for_url=f"{player_for_url}8"

    if "Perea" in knombre:
        player_for_url=f"{player_for_url}-mendoza"

    if "Paulinho" in knombre:
        player_for_url=knombre.strip()+"-12"

    if "Tuta" in knombre:
        player_for_url="tuta"

    if "Maurides" in knombre:
        player_for_url="maurides"

    if knombre=="Bernardo ":
        player_for_url="bernardo-4"

    if knombre=="Kelian Nsona":
        player_for_url=f"{player_for_url}-wa-saka"

    if knombre=="Vasilios Lampropoulos":
        player_for_url="vassilis-lampropoulos"

    if knombre=="Aurelio Buta":
        player_for_url="buta"

    if knombre=="Jeanuel Belocian":
        player_for_url="jeanu-l-belocian"

    if knombre == "Fin Stevens":
        player_for_url="finley-stevens"

    if knombre=="Colin Kleine-Bekel":
        player_for_url="colin-noah-kleine-bekel"

    if knombre=="Jan Schröder":
        player_for_url="jan-alex-wilson-schroeder"

    if knombre=="Elias Bakatukanda":
        player_for_url="elias-geoffrey-bakatukanda"

    if knombre=="Moritz-Broni Kwarteng":
        player_for_url="moritz-kwarteng"

    if knombre=="Madi Monamay":
        player_for_url="madi-monomay"

    if knombre=="Thomas Isherwood":
        player_for_url="thomas-poppler-isherwood"

    if knombre=="Olivier Deman":
        player_for_url="oliver-deman"

    if "Arthur" in knombre:
        if club=="Bayer 04 Leverkusen":
            player_for_url="arthur-5"

    if "Rogerio" in knombre:
        player_for_url="rogerio-5"

    if knombre=="Kjell Wätjen":
        player_for_url="kjell-arik-waetjen"

    if knombre=="Mohammed Amoura":
        player_for_url="mohammed-elamine-amoura"

    if knombre=="Assan Ouedraogo":
        player_for_url="forzan-ouedraogo"

    if knombre=="Isak Hansen-Aaröen":
        player_for_url="isak-hansen-aaroen"

    if knombre=="Abdenego Nankishi":
        player_for_url="abedenego-nankishi"

    if knombre=="Keke Topp":
        player_for_url="keke-maximilian-topp"

    if knombre=="Claudio Echeverri":
        player_for_url="claudio-jeremias-echeverri-2"

    if knombre =="Christian Kofane":
        player_for_url="christian-michel-kofane"

    if knombre=="Bungi Joyeux Masanka":
        player_for_url="joyeux-masanka-bungi"

    if knombre=="Filippo Mane":
        player_for_url="filippo-calixte-mane"

    if knombre == "Ebimbe Eric Junior Dina":
        player_for_url="eric-junior-dina-ebimbe"

    if knombre == "Elye Wahi":
        player_for_url="sepe-elye-wahi"

    if knombre=="Eliesse Ben Seghir":
        player_for_url="ben-seghir"

    if knombre=="Ezequiel Fernandez":
        player_for_url="ignacio-fernandez-2"

    if knombre=="Niklas Beste":
        player_for_url="jan-niklas-beste"

    if knombre=="Costa Danny da":
        player_for_url="danny-da-costa"

    if knombre=="Sanches Yvandro Borges":
        player_for_url="yvandro-borges-sanches"

    if knombre=="Cardoso Tiago Pereira":
        player_for_url="tiago-pereira-cardoso"

    if knombre=="Grant-Leon Ranos":
        player_for_url="grant-leon-mamedova"

    if knombre=="Lage Mathias Pereira":
        player_for_url="mathias-pereira-lage"

    if knombre=="Nediljko Labrovic":
        player_for_url="nedilijko-labrovic"

    if knombre=="Costa David Leal":
        player_for_url="david-leal-costa"

    if knombre=="Bilal El Khannouss":
        player_for_url="bilal-el-khannous"

    if knombre=="Daniel Heuer Fernandes":
        player_for_url="daniel-heuer-fernandes"

    if knombre=="Alexander Rössing-Lelesiit":
        player_for_url="alexander-r-ssing-lelesiit"

    if knombre=="Kristoffer Lund":
        player_for_url="kristoffer-lund-hansen"

    if knombre=="Jeff Chabot":
        player_for_url="julian-chabot"

    if knombre=="Silas ":
        player_for_url="silas-katompa-mvumpa"

    if knombre=="Chema ":
        player_for_url="chema-andres"
        
    if knombre=="Dikeni Salifou":
        player_for_url="salifou-dikeni"
        
    if knombre=="Samuel Mbangula":
        player_for_url="samuel-mbangula-tshifunda"
        
    if knombre=="Salim Musah":
        player_for_url="salim-amani-musah"

    if knombre=="Dmytro Bogdanov":
        player_for_url="dmytro-bohdanov"

    if knombre=="Cyriaque Irié":
        player_for_url="cyriaque-kalou-bi-irie"
    
    if knombre=="Badredine Bouanani":
        player_for_url="bouanani-badrerine"


# Use URL elements to get to player page
    if knombre in no_complete:
        #player_for_url=for_url(knombre)
        url_player=f'https://www.kicker.de/{player_for_url}/spieler'
    else:
        url_player=f"https://kicker.de/{player_for_url}/spieler/bundesliga/{torneo}/{club_for_url}"
 # EJEMPLO https://www.kicker.de/niclas-fuellkrug/spieler/bundesliga/2022-23/werder-bremen
    content_url= driver.get(url_player)

    #para considerar chavales que vienen de inferiores o que solo han jugado en un equipo
    def past_club_index(pastclub):
        """Tomar index del club anterior"""
        if len(pastclub)==1:
            indicepc=0
        else:
            indicepc=1
        return indicepc

    ages=driver.find_elements(By.CLASS_NAME, "kick__table-small-txt")
    dates=driver.find_elements(By.CLASS_NAME, klassvita)
    desde=driver.find_elements(By.CLASS_NAME, klassfrom)
    past_club=driver.find_elements(By.CLASS_NAME,  klasspastclub)
    #altura=driver.find_elements(By.CLASS_NAME, klassalturapeso)
    try:
        #altura=driver.find_element(By.XPATH, "//span[contains(text(), 'Größe:')]/text()")
        altura=driver.find_element(By.XPATH,'//*[@id="kick__page"]/div/div[4]/section/div[1]/div[2]/div[2]/div[2]/div[1]').text
    except:
        altura = "N.D."

    try:
        #peso=driver.find_element(By.XPATH, "//span[contains(text(), 'Gewicht:')]/text()")
        peso=driver.find_element(By.XPATH,'//*[@id="kick__page"]/div/div[4]/section/div[1]/div[2]/div[2]/div[2]/div[2]').text
    except:
        peso = "N.D."

    nacion=driver.find_elements(By.CLASS_NAME,  klassnation)
    trikot=driver.find_elements(By.CLASS_NAME,  klasstrikot)
    cards=driver.find_elements(By.CLASS_NAME, klasstarjetas)

    indicepc=past_club_index(past_club)
    try:
        born1=dates[1].text.split(" ")[1][:10]
    except:
        born1 = "N.D"

    cards=driver.find_elements(By.CLASS_NAME, "kick__gameinfo__item")
    for card in cards:
        if card.text.startswith("KARRIEREDATEN"):
            card_selected=card
            if "Länderspiele" in card_selected.text:
                #laenderspiele_elem=card.text.split('Länderspiele\n')
                laenderspiele_long=card_selected.text.split('Länderspiele\n')[1].rsplit('\nSpiele')[0]
                if len(laenderspiele_long) > 3:
                    laenderspiele=card_selected.text.split('Länderspiele\n')[1].rsplit('\nSpiel')[0]
                else:
                    laenderspiele = laenderspiele_long
            else:
                laenderspiele="No"

            if "\nBundesliga\n" in card_selected.text:
                bundesliga=card_selected.text.split('Bundesliga\n')[1].rsplit('\n')[0]
                total_bundesliga=bundesliga.strip()
            else:
                total_bundesliga="0"

    if knombre in vereinslos:
        age=""
        age_in_club=""
        vertrag=""
    elif knombre in no_complete:
        age=""
        pplayed="0"
        partidosbl="0"
        golesbl="0"
        assists="0"
        gelbe="0"
        gelbrot="0"
        rot="0"
        numero="0"
        age_in_club="N.A."
        vertrag="N.D."
        laenderspiele="No"
    else:
        try:
            age=ages[0].text[1:3]
        except:
            age = "N.D."
        #age=dates[1].text.split(" ")[45][1:3]
        if len(desde)>=2:
            try:
                age_in_club=desde[0].text
                vertrag=desde[1].text
            except:
                age_in_club="N.D."
                vertrag="N.D."
        else:
            if knombre in no_games_at_all:
                age_in_club="N.A."
                vertrag="N.D."
            else:
                age_in_club=desde[0].text
                vertrag="N.D."
    #fromclub=past_club[indicepc].text[4:].split("\n")[0]
    if knombre in no_complete:
        fromclub="N.A."
    else:
        try:
            fromclub=past_club[indicepc].text.strip()
        except:
            fromclub="N.D."

    if len(altura) > 0 and "Größe: " in altura:
        altura_txt=altura[7:10]
    else:
        altura_txt="N.D."

    if  len(peso) > 0 and "Gewicht:" in peso:
        peso_txt=peso[9:11]
    else:
        peso_txt="N.D."
    #pais=nacion[0].text.split("\r\n")[1].strip()

    pais=nacion[0].text
    nacion_txt=ts.translate_text(pais, translator='alibaba', from_language='de' , to_language='es')

    player_performance=driver.find_elements(By.TAG_NAME, "td")
    elementindex=[]
    for e in player_performance:
    #para chavales de la cantera sin debutar
        if "Bundesliga" not in e.text:
            pplayed="0"
            partidosbl="0"
            golesbl="0"
            assists="0"
            gelbe="0"
            gelbrot="0"
            rot="0"
            desde="N.A."
   #separar bundesliga de otras ligas y de 2a Bundesliga
        if e.text.strip()=="Bundesliga":
            indice=player_performance.index(e)
            #print(indice)
            elementindex.append(indice)
        elementix2=elementindex
    #para que corra el carrusel con todos los índices
    if len(elementix2)>1:
        if knombre in exclude:
            pplayed="0"
            partidosbl="0"
            golesbl="0"
            assists="0"
            gelbe="0"
            gelbrot="0"
            rot="0"

        elif knombre in no_games_season:
            pplayed="0"
            partidosbl="0"
            golesbl="0"
            assists="0"
            gelbe="0"
            gelbrot="0"
            rot="0"

        elif knombre in no_games_at_all:
            pplayed="0"
            partidosbl="0"
            golesbl="0"
            assists="0"
            gelbe="0"
            gelbrot="0"
            rot="0"
            vertrag="N.D."
        else:
            try:
                played_index=elementix2[1]+1
                pplayed=player_performance[played_index].text.strip().split("/")[0]
            except:
                pplayed="0"

            try:
                goles_index=elementindex[1]+3
                golesbl=player_performance[goles_index].text.strip()
            except:
                golesbl="0"

            try:
                assist_index=elementindex[1]+5
                assists=player_performance[assist_index].text.strip()
            except:
                assists="0"

            try:
                gelb_index=elementindex[1]+9
                gelbe=player_performance[gelb_index].text.strip()
            except:
                gelbe="N.D."

            try:
                gelb_rot_index=gelb_index+1
                gelb_rot=player_performance[gelb_rot_index].text.strip()
            except:
                gelb_rot="N.D."

            try:
                rot_index=gelb_rot_index+1
                rot=player_performance[rot_index].text.strip()
            except:
                rot="N.D."

#para número no asignado de camiseta
    if len(trikot)>0:
        numero=trikot[0].text
    else:
        numero="0"

    player_dict={"Jugador": knombre.strip(), "Nacimiento": born1, "Edad": age, "Nación": nacion_txt, "Altura": altura_txt, "Peso": peso_txt, "PJ": pplayed, "Goles": golesbl, "Asistencias": assists, "TA": gelbe, "TAR": gelbrot, "TR": rot, "Desde": age_in_club, "De": fromclub, "BL": total_bundesliga, "Número": numero, "Contrato": vertrag, "Selección": laenderspiele}
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
driver.close()
