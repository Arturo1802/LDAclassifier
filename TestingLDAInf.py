import gensim
import spacy
import pandas as pd
import mysql.connector
from tools import summ
from LDAtools import first_inference,LDAprobs
import gensim.corpora as corpora


lda_model = gensim.models.LdaMulticore.load('LDAxeon')
topics = lda_model.print_topics(num_words=20)

# Analizar y mostrar las palabras clave con mayor probabilidad
for topic in topics:
    print(f"Tópico {topic[0]}:")
    words = [word.split("*")[1] for word in topic[1].split(" + ")]
    print(words)
    print()


print("0=Economico\n 1=Psicologico\n 2=Academico")
x=["Siempre siento que estoy lidiando con problemas personales. Mis relaciones son un desastre, y no importa lo que haga, parece que nunca puedo encontrar la felicidad en mi vida personal. Es agotador.",
    "Estoy abrumado por mis problemas personales. La presión en el trabajo y los conflictos familiares me están afectando más de lo que puedo soportar. No sé qué hacer.",
    "Mis problemas académicos son un verdadero dolor de cabeza. No importa cuánto estudio, sigo obteniendo malas calificaciones en mis exámenes. Me siento como si nunca pudiera alcanzar mis metas académicas.",
    "La presión de mis problemas académicos me está afectando la salud. No puedo concentrarme, y siento que estoy perdiendo el rumbo en la escuela. ¿Cómo puedo superar esto?",
    "La situación económica es terrible. Las facturas se acumulan, y no tengo suficiente dinero para cubrir mis gastos básicos. Esta tensión financiera está arruinando mi vida.",
    "Los problemas económicos me han llevado al borde . No sé cómo pagaré mis deudas y mantener a mi. Parece que no hay salida a esta crisis financiera."]

for item in x:
    c=LDAprobs(item,lda_model)
    if c[0][1]>c[1][1] and c[0][1]>c[2][1]:
        print(c[0])
    elif c[1][1]>c[0][1] and c[1][1]>c[2][1]:
        print(c[1])
    else:
        print(c[2])
    print()
