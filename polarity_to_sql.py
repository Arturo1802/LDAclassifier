import pandas as pd
import mysql.connector
from joblib import Parallel, delayed
from  tools import polarity 
from LDAtools import getT2DataSQL,getFullDataSQL
df=getFullDataSQL()
# Función paralelizable para calcular la polaridad 
def calcular_polaridad(texto):
    pol=polarity(texto)
    return pol

# Número de hilos  
num_hilos = 5   
# Utiliza Parallel de joblib para ejecutar calcular_polaridad en paralelo
resultados = Parallel(n_jobs=num_hilos)(delayed(calcular_polaridad)(texto) for texto in df['TEXT']) 
# Agrega los resultados como una nueva columna al DataFrame
df['polarity'] = resultados 
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
        valor_nueva_columna = row['polarity']
        authid_registro = row['#AUTHID'] 
        query = f"UPDATE cleanfulldb SET polarity = {valor_nueva_columna} WHERE `#AUTHID` = '{authid_registro}';"
        cursor.execute(query) 
    connection.commit() 
except Error as e:
    print(f"Error: {e}")

finally:
    # Cerrar la conexión y el cursor
    if connection.is_connected():
        cursor.close()
        connection.close()