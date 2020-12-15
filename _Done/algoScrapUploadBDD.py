# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:24:09 2020

@author: Ga
"""

import requests
from bs4 import BeautifulSoup
import psycopg2, config
import re


# In[88]:

# connection à PG, BDD scantonnet
conn = psycopg2.connect(database="bdd_scantonnet", user=config.user,password=config.password, host='127.0.0.1') 
cur = conn.cursor()

# In[91]:
# Upload dans la BDD

# Traitement de chaque ligne: affichage & enregistrement
def traiteInfo(id, rate, vote, fact):
    #print("%4d : %.2f %5d %s" % (id, rate, vote, fact))
    cur.execute("""INSERT INTO public."chuckJokes" VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;""", (id, fact))
    cur.execute("""INSERT INTO public."chuckRating" VALUES (NOW()::Date, %s, %s, %s) ON CONFLICT DO NOTHING;""", (id, rate, vote))

# Definition de la procédure qui traite 1 page
def recupPage(page):
    url = "https://chucknorrisfacts.net/facts.php?page=%d" % (page)
    print("\nRécupération de %s" %(url))
    # extraction du document HTML
    r = requests.get(url, headers={"User-Agent": "Mon navigateur perso d'ici"})
    soup = BeautifulSoup(r.content, 'html.parser')
    # Récupération de tous les blocks qui contiennent les info qui nous intéressent.
    # Utilisation de soup.select avec un selecteur CSS
    blocks = soup.select("#content > div:nth-of-type(n+2)")
    # 2ime boucle sur les block récupérée
    for block in blocks: 
        #~ print(block)
        # On récupé les champs individuels (rate, vote, fact)
        # On affiche (si fact non vide)
        fact = block.select_one("p")
        if fact is not None:
            id = block.select_one("ul.star-rating").attrs['id']
            #print(id)
            rate = block.select_one("span.out5Class")
            vote = block.select_one("span.votesClass")
            
            traiteInfo(int(id[6:]), float(rate.text), int(vote.text[:-6]), fact.text)
            #~ print("------------------------")

# Fonction qui détecte le lien de la dernière page pour arrêter le scrap
def lastPage():
    url = "https://chucknorrisfacts.net/facts"
    r = requests.get(url, headers={"User-Agent": "Mon navigateur perso d'ici"})
    soup = BeautifulSoup(r.content, 'html.parser')
    lastPage = soup.select("#content a:link")
    lastPageToStr = str(lastPage[-1].get('href'))
    
    numPage = re.findall(r'\d+', lastPageToStr)
    
    return(int(numPage[0]))
    
# In[92]:
# Core scrapping

for p in range(1, lastPage()):
    recupPage(page = p)

conn.close()
