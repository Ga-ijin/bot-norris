# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:45:49 2020

@author: Ga
"""
import psycopg2, config
import pandas as pd
from datetime import date

def executeReport():
    conn = psycopg2.connect(database="bdd_scantonnet", user=config.user,password=config.password, host='127.0.0.1') 
    cur = conn.cursor()
    
    cur.execute("""SELECT COUNT(*) FROM "chuckJokes";""")
    result = cur.fetchone()
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    print("Il y a dans cette BDD {} blagues le {}".format(result[0], today))
    
    sql = ("""SELECT "chuckJokes".jokes, "chuckRating".rating FROM "chuckJokes"
                INNER JOIN "chuckRating" ON "chuckJokes".id = "chuckRating".id
                WHERE rating >4
                ORDER BY rating DESC;""")
    df = pd.read_sql_query(sql, conn)
    
    nbBestJokes = (len(df.index))
    print("Il y a {} blagues qui ont plus de 4/5".format(nbBestJokes))
    print("Voici les 5 meilleures : ")
    print(df.head(5))