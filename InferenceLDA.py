import gensim
import spacy
import pandas as pd
import mysql.connector
from tools import summ
import gensim.corpora as corpora
from sqlalchemy import create_engine

from LDAtools import process_text2,first_inference,getT2DataSQL,getFullDataSQL 

df=getFullDataSQL()
nlp = spacy.load("es_core_news_lg") 
lda_model = gensim.models.LdaMulticore.load('LDAxeon')    

#df['TEXT']= df['TEXT'].apply(summ)
df['FI']=df['TEXT'].apply(lambda x: first_inference(x, lda_model))
print(df['FI'])
if 1 in df['FI'] and 2 in df['FI'] and 0 in df['FI']:
    print("SI") 
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
            valor_nueva_columna = row['FI'][0]
            authid_registro = row['#AUTHID']
            query = f"UPDATE cleanfulldb SET preinf = {valor_nueva_columna} WHERE `#AUTHID` = '{authid_registro}';"
            cursor.execute(query)

        # Confirmar los cambios
        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión y el cursor
        if connection.is_connected():
            cursor.close()
            connection.close()