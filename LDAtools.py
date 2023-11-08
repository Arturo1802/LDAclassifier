import spacy
import pandas as pd
import concurrent.futures
from itertools import chain
from sqlalchemy import create_engine
nlp = spacy.load("es_core_news_lg") 

 



def getNegativeDataSQL(): 
    engine = create_engine("mysql+mysqlconnector://root:VivaItaliaCarajo2!@127.0.0.1/sentiment") 
    connection = engine.connect()   
    query = 'SELECT * FROM cleanfulldb WHERE polarity<=0' 
    df = pd.read_sql(query, connection)
    # Close the MySQL connection
    connection.close()  
    return df
def getFullDataSQL(): 
    engine = create_engine("mysql+mysqlconnector://root:VivaItaliaCarajo2!@127.0.0.1/sentiment") 
    connection = engine.connect() 
    query = 'SELECT * FROM cleanfulldb' 
    df = pd.read_sql(query, connection)
    # Close the MySQL connection
    connection.close()  
    return df
def getT2DataSQL(): 
    engine = create_engine("mysql+mysqlconnector://root:VivaItaliaCarajo2!@127.0.0.1/sentiment") 
    connection = engine.connect() 
    query = 'SELECT * FROM corpusT2' 
    df = pd.read_sql(query, connection)
    # Close the MySQL connection
    connection.close() 
    return df

# Tokenizar y procesar el texto con spaCy
def process_text(text,nlp): 
    doc = nlp(text)
    return [token for token in doc if token.is_alpha and not token.is_stop]
#Retornar solo el lemma(palabra base) de cada palabra en el dataset
def process_text2(text, nlp):
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]


def first_inference(text, lda_model): 
    processed_text = process_text2(text,nlp) 
        # Representación Bow
    bow_vector =  lda_model.id2word.doc2bow(processed_text)

        # Inferencia del tópico  
    prob, topic  =  max((fila[1],fila )for fila in lda_model.get_document_topics(bow_vector)) 
    
    return topic
def LDAprobs(text, lda_model): 
    processed_text = process_text2(text,nlp) 
        # Representación Bow
    bow_vector =  lda_model.id2word.doc2bow(processed_text)

        # Inferencia del tópico  
    prob  =  lda_model.get_document_topics(bow_vector)
    
    return prob

def getSimilares(token, list_of_docs): 
    palabras_similares = [t.text for t in list_of_docs if token.similarity(t) > 0.46]
    return set(palabras_similares)
 