# Importation des librairies utiles
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from collections import Counter
import json

# Fonction pour obtenir les mots de chansion
def get_lyrics(url : str , len_word = 3) -> list :
    """_summary_

    Args:
        url (str): Lien vers une chanson
        len_word (int, optional): Filtrer selon plus de 3 caractères. Defaults to 3.

    Returns:        
        list: Liste de tous les mots
    """    
    print(f"Fetching Lyrics {url}...")
    r = requests.get(url)
    if r.status_code != 200:
        print('Impossible de recuperer la page.')
        return []
    soup = BeautifulSoup(r.content, 'html.parser' )
    lyrics = soup.find('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL') # 'Lyrics__Container-sc-1ynbvzw-1 kUgSbL'

    if not lyrics:
        return get_lyrics(url, len_word = 3)
    
    all_words = []

    for sentences in lyrics.stripped_strings :
        sentences_words = [word.strip().strip(',').strip('.').lstrip('(').strip(')').lower() for word in sentences.split()  if len(word) > len_word and '[' not in word and ']' not in word]
        all_words.extend(sentences_words)
    # Autre façon de faire:
    #def is_valid(word, word_len = 4):
        #if len(word) < word_len:
           # return False
        
       # return "[" not in word and "]" not in word
    
    #return all_words
    #pprint(all_words)
    return all_words

# Fonction pour obtenir un lien vers les chansons
def get_url() -> list :
    """_summary_

    Returns:
        list: Retourne le lien vers la chanson
    """    
    # Alpha Blondy == 338478
    page_number = 1
    links = []
    while True:
        r = requests.get(f" https://genius.com/api/artists/338478/songs?page={page_number}&sort=popularity")
       
        if r.status_code == 200:
            print(f"Fetching {page_number}")

            #pprint(r.json().get('response')

            response = r.json().get('response', {}) 
            # Obtenir next_page
            #pprint(response)
            next_page = response.get("next_page")
            songs = response.get("songs")
            links.extend([song.get('url') for song in songs])

            page_number += 1

            if not next_page :
                print("Pas de nouvelle page")
                break
    #pprint(links)
    #print(len(links))
    return links
            
# Fonction pour obtenir tous les liens vers les chansons 
def get_all_urls ():
    all_ulrs = get_url()
    
    words = []
    for url in all_ulrs:
        lyrics = get_lyrics(url, len_word=4)
        words.extend(lyrics)

    with open('data.json', "w") as f:
        json.dump(words, f, indent=4)

    counter = Counter(words).most_common(15) # Counter([w for w in words if len(w) > 8])
    pprint(counter)


get_all_urls()
