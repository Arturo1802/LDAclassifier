#libs
from pprint import pprint 
import pickle 
import pandas as pd 
import gensim
import os
import spacy 
import gensim.corpora as corpora
import pyLDAvis
import pyLDAvis.gensim_models
from LDAtools import process_text, getFullDataSQL,getSimilares ,process_text2
from gensim.models.coherencemodel import CoherenceModel
# Carga el modelo de spaCy para español
nlp = spacy.load("es_core_news_lg")   

print("Retreive data....")
df=getFullDataSQL()
# Aplicar la función process_text a la columna 'TEXT'  
#print("Applying bag of words")
df['TEXT_PROCESSED'] = df['TEXT'].apply(process_text2 ,nlp=nlp)   
# Crear una lista de los documentos procesados
data_words = df['TEXT_PROCESSED'].tolist()
with open('data_words.pkl', 'wb') as file:
    pickle.dump(data_words, file)  
# Crear un diccionario y un corpus(BoW format)
#dictionary = corpora.Dictionary(data_words)


dictionary=corpora.Dictionary.load("textos.dictionary")
dictionary.filter_extremes(no_below=3, no_above = 0.75)
corpus = [dictionary.doc2bow(text) for text in data_words] 
#dictionary.save("textos.dictionary")
print("Getting keywords")
#  
processed_docs = [process_text(text, nlp) for text in df['TEXT']]   


topic_keywords = {
    0: ["exámenes", "notas", "tareas", "estudio", "materias"],
    1: ["finanzas", "deudas", "trabajo", "ingresos", "presupuesto", "dinero","pago","crédito"],
    2: ["estrés", "ansiedad", "depresión", "autoestima", "relaciones"]
} 
for topico, palabras_clave in topic_keywords.items():
    print(topico)
    palabras_similares= []
    for palabra in palabras_clave:
        for doc in processed_docs:
            palabras_similares.extend(getSimilares(nlp(palabra),doc)) 
    topic_keywords[topico]=palabras_similares   
with open('topic_keywords.pkl', 'wb') as file:
    pickle.dump(topic_keywords, file)  
#with open('topic_keywords.pkl', 'rb') as file:
#    topic_keywords = pickle.load(file)

# Entrenar el modelo LDA (Calcular probabilidades y guardarlas)
num_topics = 3
print("Training LDA...........")
lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=100, random_state=3, workers=28)
lda_model.save("LDAxeon") 
# Imprimir los tópicos
pprint(lda_model.print_topics()) 

# Calcular la coherencia del modelo
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('Coherence Score: ', coherence_lda) 
# Obtener palabras clave de cada tópico con probabilidad
topics = lda_model.print_topics(num_words=20)

# Analizar y mostrar las palabras clave con mayor probabilidad
for topic in topics:
    print(f"Tópico {topic[0]}:")
    words = [word.split("*")[1] for word in topic[1].split(" + ")]
    print(words)
    print()