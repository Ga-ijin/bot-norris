# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:45:49 2020

@author: Ga
"""
# In[0]:
# Import libraries et connexion
import psycopg2, config
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def executeGraphs():
    conn = psycopg2.connect(database="bdd_scantonnet", user=config.user,password=config.password, host='127.0.0.1') 
    
    # In[1]:
    # Req1 : Répartition par note
    sql = """select rating from "chuckRating";"""
    dfRatings = pd.read_sql_query(sql, conn)
    # Description du df (vision globale)
    print(dfRatings.describe())
    
    # "Distplot" --> Histogramme de distribution des notes
    note_fig, note_ax = plt.subplots()
    sns.distplot(a=dfRatings.rating)
    
    violon_fig, violon_ax = plt.subplots()
    sns.violinplot(data=dfRatings, palette="Set3", bw=.2, cut=1, linewidth=1)
    
    # In[2]:
    # Req2 : "Est-ce que les meilleures blagues sont les plus courtes ?
        
    sql = ("""SELECT "chuckJokes".jokes, "chuckRating".rating FROM "chuckJokes"
                INNER JOIN "chuckRating" ON "chuckJokes".id = "chuckRating".id;""")
    dfLenJoke = pd.read_sql_query(sql, conn)
    
    dfLenJoke["lenJoke"] = dfLenJoke["jokes"].apply(lambda x: len(x))
    
    print(dfLenJoke.describe())
    
    dfLenJoke["repartitionLen"] = pd.qcut(x = dfLenJoke["lenJoke"], q = 10, labels=range(10))
    
    dfMean = dfLenJoke.groupby(['repartitionLen']).mean()
    
    len_fig, len_ax = plt.subplots()
    sns.barplot(x= round(dfMean["lenJoke"]), y = dfMean["rating"])