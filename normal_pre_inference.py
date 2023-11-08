from LDAtools import process_text,getSimilares,first_inference,getFullDataSQL,getT2DataSQL
import gensim 
import spacy  
from sqlalchemy import create_engine
import concurrent.futures 
import pickle 
import mysql.connector
import pandas as pd
from joblib import Parallel, delayed
from VisualizeApp.tools import polarity,summ

nlp = spacy.load("es_core_news_lg") 

def pre_inference(text): 
    with open('topic_keywords.pkl', 'rb') as file:
        topic_keywords = pickle.load(file) 
    topic_keywords[0] = [str(elemento) for elemento in topic_keywords[0]]
    topic_keywords[1] = [str(elemento) for elemento in topic_keywords[1]]
    topic_keywords[2] = [str(elemento) for elemento in topic_keywords[2]]

    topic_keywords[0] = " ".join(topic_keywords[0])
    topic_keywords[1] = " ".join(topic_keywords[1])
    topic_keywords[2] = " ".join(topic_keywords[2])
    with nlp.disable_pipes():
        topic_keywords[0]=nlp(topic_keywords[0])
        topic_keywords[1]=nlp(topic_keywords[1])
        topic_keywords[2]=nlp(topic_keywords[2])

        text=nlp(text) 
        scores=[]
        scores.append(topic_keywords[0].similarity(text)) 
        scores.append(topic_keywords[1].similarity(text))
        scores.append(topic_keywords[2].similarity(text))
        topic=scores.index(max(scores))
    return topic


engine = create_engine("mysql+mysqlconnector://root:VivaItaliaCarajo2!@127.0.0.1/sentiment") 
connection = engine.connect()  
query = 'SELECT * FROM corpusT2'  
df = pd.read_sql(query, connection) 
df['TEXT']= df['TEXT'].apply(summ)
#paralelizando para eficientar tiempos
num_hilos = 11    
print("Inference...........")
with concurrent.futures.ThreadPoolExecutor(max_workers=num_hilos) as executor:
    resultados = list(executor.map(pre_inference, df['TEXT']))
df['FI'] = resultados 
df=df.drop('TEXT',axis=1)
if 1 in df['FI'] and 2 in df['FI'] and 0 in df['FI']:
    print("SI")
print("Uploading.....")
from mysql.connector import Error
try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="VivaItaliaCarajo2!",
        database="sentiment"
    ) 
    cursor = connection.cursor() 
    for index, row in df.iterrows():
        valor_nueva_columna = row['FI']
        authid_registro = row['#AUTHID'] 
        query = f"UPDATE corpusT2 SET firstinf = {valor_nueva_columna} WHERE `#AUTHID` = '{authid_registro}';"
        cursor.execute(query) 
    connection.commit() 
except Error as e:
    print(f"Error: {e}") 
finally: 
    if connection.is_connected():
        cursor.close()
        connection.close()
    print("Done")