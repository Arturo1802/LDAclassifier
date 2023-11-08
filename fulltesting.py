from LDAtools import process_text,getSimilares,first_inference,getFullDataSQL,getT2DataSQL
import gensim 
import spacy
import joblib 
import json
from multiprocessing import Pool 
import gensim.corpora as corpora
from gensim.models.coherencemodel import CoherenceModel
from VisualizeApp.tools import ner,summ

nlp = spacy.load("es_core_news_lg") 
text = '''
En general, mi situación académica es un aspecto importante en mi vida en este momento. Aunque me siento agradecido por la oportunidad de estudiar y aprender, también he enfrentado desafíos a lo largo de mi carrera. He tenido que equilibrar mis responsabilidades académicas con mi vida personal y, a veces, la presión de las evaluaciones y los plazos puede resultar abrumadora.
Una de las partes más satisfactorias de mi experiencia académica es la posibilidad de explorar mis intereses y descubrir nuevas áreas de conocimiento. He tenido la suerte de tener profesores excepcionales que han influido en mi pasión por ciertas materias. Además, he tenido la oportunidad de colaborar en proyectos interesantes y enriquecedores con compañeros de clase.
''' 
print(ner(summ(text)))
df =getT2DataSQL()  


processed_docs = [process_text(text, nlp) for text in df['TEXT']]  
topic_keywords = {
    0: ["exámenes", "notas", "tareas", "estudio", "materias"],
    1: ["finanzas", "deudas", "trabajo", "ingresos", "presupuesto"],
    2: ["estrés", "ansiedad", "depresión", "autoestima", "relaciones"]
} 
for topico, palabras_clave in topic_keywords.items():
    print(topico)
    palabras_similares= []
    for palabra in palabras_clave:
        for doc in processed_docs:
            palabras_similares.extend(getSimilares(nlp(palabra),doc)) 
    topic_keywords[topico]=palabras_similares  

print(topic_keywords[0])
#Cargar el modelo entrenado con Xeon
lda_model = gensim.models.LdaMulticore.load('LDAxeon')
#Pruebas de inferencia y similitud

tokenized = process_text(text,nlp)
print(f'tokens: {tokenized}') 
similares=getSimilares(nlp("escolar"),processed_docs)
fi=first_inference(text,lda_model)
print(f'First inf: {fi}') 
print(f'similares: {similares}')  
