import requests 
from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path
from collections import Counter
import streamlit as st
import pandas as pd
import plotly.express as px
from multiprocessing import Pool
import time
import numpy as np
import base64

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.DEBUG, 
                    filemode='w',
                    filename='file.log',
                    format="%(asctime)s : %(levelname)s :  %(message)s"
                    )
logging.debug("La fonction a bien été exécutée")
logging.info("Message général")
logging.warning("Attention!")
logging.error("Une erreur a été détectée")
logging.critical("Erreur critique")


count_request = 0
def counter_request():
    global count_request
    count_request +=1


def choice_id_artist():
    artist = st.text_input("Entrez le nom complet de votre artiste : ").strip().lower()
    if artist:
        API_artist = f"https://genius.com/api/search/multi?q={artist}"
        counter_request()
        r = requests.get(API_artist, verify=False)
        
        if r.status_code == 200:
            response = r.json().get('response', {})
            sections = response.get('sections', [])
            next_page = response.get('next_page')

            if sections:
                hits_list = sections[0].get("hits", [])
                
                if hits_list:
                    for hit in hits_list:
                        result = hit.get('result', {})
                        id_value = result.get('id')
                        if id_value:
                            return id_value, artist

            if not next_page:
                st.warning(":red[Artiste non trouvé !]")
    else:
        st.write("Aucun résultat trouvé pour cet artiste. Veuillez réessayer.")

    return None, None

def get_link_lyrics():
    link_tempo = []
    song_title_list = []
    page_number = 1
    id, artist = choice_id_artist()
    while True:
        API = f"https://genius.com/api/artists/{id}/songs?page={page_number}&sort=popularity"
        counter_request()
        r = requests.get(API, verify=False)
        if r.status_code == 200:
            st.write(f"Recherche en cours page_{page_number} ...")
            response = r.json().get('response', {})
            next_page = response.get('next_page')
            
            songs = response.get("songs")
            for song in songs:
                song_artist = song.get("primary_artist", {}).get("name")
                song_title = song.get('title')
                song_title_list.append(song_title)
                if song_artist.lower() == artist.lower():
                    url = song.get("url")
                    link_tempo.append(url)
                
            page_number += 1 
            if not next_page:
                st.write('No next page')
                break
        
    links = set(link_tempo)
    return list(links), song_title_list, artist

def get_lyrics(url, len_word=6):
    st.write(f"Catching Lyrics {url}...")
    counter_request()
    r = requests.get(url)
    if r.status_code != 200:
        st.write('Impossible de capturer des paroles en cours !')
        return []
    soup = BeautifulSoup(r.content, 'html.parser') 
    lyrics = soup.find('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')

    if lyrics is None:
        st.write("Aucune balise 'div' contenant les paroles trouvée.")
        return []
    
    all_words = [] 
    for sentences in lyrics.stripped_strings:
        for word in sentences.split():
            if (len(word) >= len_word) and '[' not in word and ']' not in word:
                sentence_words_clean = word.strip().strip('.').strip(',').lstrip('(').strip(')').strip("{").lower()
                all_words.extend([sentence_words_clean])
    return all_words 

def get_lyrics_POOL(url):
    return get_lyrics(url)

def get_links_lyrics():
    urls, song_title, nom_artist = get_link_lyrics()
    st.write(':red[INFO : Pas de paroles disponibles pour certains artistes sur genius.com]')
    st.write(':green[Récupération des paroles sur toutes les pages et visualisation en cours ...]') # ,font="20px"
    
    with Pool(processes = 4) as pool:  
        lyrics_list = pool.map(get_lyrics_POOL, urls)
    
    return lyrics_list, song_title, nom_artist

def all_links():
    lyrics_list, song_title, nom_artist = get_links_lyrics()
    words = []
    for lyrics in lyrics_list:
        words.extend(lyrics)
        #chemin = Path.cwd() / "data"
        #with open(chemin, 'w') as f:
            #json.dump(words, f, indent=4)

    current_word = Counter(words).most_common(10)
    return current_word, song_title, nom_artist

def all_links_without_pool():
    urls, song_title, nom_artist = get_link_lyrics()
    words = []
    for url in urls :
        lyrics = get_lyrics(url, len_word = 6)
        words.extend(lyrics)
        #chemin = Path.cwd() / "data"
        #with open(chemin, 'w') as f :
            #json.dump(words, f, indent= 4)

    current_word = Counter(words).most_common(10)
    #pprint(common_word)
    return current_word, song_title, nom_artist


def main():
    t0 = time.time()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Request avec pool et sans pool")
    st.write(":blue[Auteur: Mahamadou]")
    link = "https://genius.com/"
    
    api_choice = st.sidebar.selectbox('Choississez le type de test:', ["With_Pool", "Without_pool"])
    if api_choice == 'With_Pool':
        st.write('### Description')
        #st.markdown(f"[Cliquez ici pour visiter le lien]({link})")
        st.markdown(f"""L'objectif est de requêter la base de données de [genius]({link}) pour récupérer via une api les paroles 
                 d'un chanteur que l'utilisateur tape dans la barre de recherche.
                 Ces demandes sur le serveur distant peuvent prendre un certain temps c'est pourquoi je vous montre dans ces exemples
                  qu'utiliser le multiprocessing via pool peut vous faire gagner énormément de temps soit 3X plus vite et augmenter
                 votre productivité.""")
        
        st.write(""":red[Attention : Sans le nom complet de l'artiste, il se peut que
                  le résultat ne soit pas pertinent ou l'artiste n'est pas disponible sur la plateforme]""")
        st.write(""":green[Le fetching time peut être long pour certains artistes!]""")
    
        current_word, song_title, nom_artist = all_links()

        data = pd.DataFrame(current_word, columns=['Mot', 'Counter'])
        data["Artist"] = [nom_artist.title()]*10

        st.write('## Visualisation')
        fig = px.sunburst(data,
                        names=data['Mot'],
                        parents=data['Artist'],
                        values=data['Counter'])
        fig.update_layout(title_font_color='red',
                        title=dict(
                            text=f"10 Mots (>5 caract) plus couramment employés\n par {nom_artist.title()}",
                            y=0.97,
                            x=0.5,
                            xanchor='center',
                            yanchor='top',
                            font=dict(size=20)),
                        font=dict(size=30)
                        )
        st.plotly_chart(fig)

        st.write('## Chansons les + populaires :')
        top_five = song_title[:5]
        st.write(top_five)
        t1 = time.time()
        st.write("## Conclusion")
        st.write(f"""Avec la methode pool, nous avons obtenu le résultat 
                 en :blue[{np.round((t1 - t0), 2)}] sec pour :blue[{count_request}] requêtes au total.""")

    elif api_choice == 'Without_pool' :
        st.write(':red[Veuillez patienter cette section prend du temps !]')
       
        current_word, song_title, nom_artist = all_links_without_pool()

        data = pd.DataFrame(current_word, columns=['Mot', 'Counter'])
        data["Artist"] = [nom_artist.title()]*10

        st.write('## Visualisation')
        fig = px.sunburst(data,
                        names=data['Mot'],
                        parents=data['Artist'],
                        values=data['Counter'])
        fig.update_layout(title_font_color='red',
                        title=dict(
                            text=f"10 Mots (>5 caract) plus couramment employés\n par {nom_artist.title()}",
                            y=0.97,
                            x=0.5,
                            xanchor='center',
                            yanchor='top',
                            font=dict(size=20)),
                        font=dict(size=30)
                        )
        st.plotly_chart(fig)

        st.write('## Chansons les + populaires :')
        top_five = song_title[:5]
        st.write(top_five)
        t1 = time.time()
        st.write("## Conclusion")
        st.write(f"""Sans la methode pool, nous avons obtenu le même résultat
                  en :blue[{np.round((t1 - t0), 2)}] sec pour :blue[{count_request}] requêtes au total.""")


if __name__ == '__main__' :
    main()
