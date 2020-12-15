# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:34:36 2020

@author: Ga
"""
# In[1]:
# Import des bibliothèques

import psycopg2, config
import pandas as pd

from wordcloud import WordCloud
import matplotlib.pyplot as plt


from PIL import Image
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from collections import Counter
import seaborn as sns

def executeMining():
    
    # In[2]:
    # Connexion à la BDD PG bdd_scantonnet et requêtage
    
    conn = psycopg2.connect(database="bdd_scantonnet", user=config.user,password=config.password, host='127.0.0.1') 
    
    sql = """select jokes from "chuckJokes";"""
    df = pd.read_sql_query(sql, conn)
    
    # In[3]:
    # Tokenisation et traitement préalable de la liste des mots de chaque blague
    
    # On stocke toutes les blagues du df dans une string
    text = ""
    for comment in df.jokes : 
        text+=comment
        text+=" "
        
    text = text.lower()
    
    # On définit la liste des stopwords (à ne pas prendre en compte)
    stop_words = set(stopwords.words('english'))
    addingStopWordsList = [",", ".","'","n't","'s","to","of",'and',"with","was","?","!",'``',"...","''"]
    for mot in addingStopWordsList:
        stop_words.add(mot)
        
    # On fait une liste qui sépare chacun des mots de la string text et exclue les stopwords
    
    text_tokenized = word_tokenize(text, language='english')
    
    tokens = []
    for mot in text_tokenized:
        if mot not in stop_words:
            tokens.append(mot)
    
    # In[4]:
    # Création du nuage de mots suivant une image
    
    def plot_word_cloud(txt, masque, background_color = "black") :
        # Définir un masque
        # mask_coloring = np.array(Image.open(str(masque)))
        # from wordcloud import ImageColorGenerator
        mask = np.array(Image.open(masque))
        # img_color = ImageColorGenerator(mask)
        
        # Définir le calque du nuage des mots
        wc = WordCloud(mask=mask, random_state=42, collocations=False,
                  width=400, height=200, margin=2,
                  ranks_only=None, prefer_horizontal=0.9,
                  scale=1, color_func=None,
                  max_words=1000,
                  min_font_size=4, stopwords=stop_words,
                  background_color='black',
                  max_font_size=90, font_step=1, mode='RGB',
                  relative_scaling=0.5, regexp=None, colormap=None, normalize_plurals=True)
        
        plt.figure(figsize= (15,10)) # Initialisation d'une figure
        wc.generate(txt)           # "Calcul" du wordcloud
        plt.imshow(wc) # Affichage
        plt.show()
      
    plot_word_cloud(text, "chuck2.jpg")
    
    # # Code d'affichage du masque
    # import matplotlib.image as mpimg
    # img = mpimg.imread("chuck2.jpg")
    # plt.imshow(img)
    # plt.show()
    
    # In[5]:
    # Bar graphs des 15 mots les plus utilisés (avec et sans Chuck Norris)
    dico = Counter(tokens)
    dico.most_common(17)
    
    mots = [m[0] for m in dico.most_common(15)]
    freq = [m[1] for m in dico.most_common(15)]
    
    plt.figure(figsize= (15,10))
    sns.barplot(x=mots, y=freq)
    plt.title('15 mots les plus fréquemment employés')
    
    #On retire les mots "Chuck" et "Norris" de la liste
    
    dico.pop("chuck")
    dico.pop("norris")
    mots = [m[0] for m in dico.most_common(15)]
    freq = [m[1] for m in dico.most_common(15)]
    
    plt.figure(figsize= (15,10))
    sns.barplot(x=mots, y=freq)
    plt.title('15 mots les plus fréquemment employés excluant Chuck et Norris')
    
    print("TextMining done, check ur plots")
    conn.close()