import gensim.corpora as corpora
import gensim
import pickle
import spacy
from gensim.models.coherencemodel import CoherenceModel
from LDAtools import process_text2
with open('data_words.pkl', 'rb') as file:
    data_words = pickle.load(file)
lda_model = gensim.models.LdaMulticore.load('LDAxeon')
nlp = spacy.load("es_core_news_lg") 
with open('topic_keywords.pkl', 'rb') as file:
    topic_keywords = pickle.load(file)
'''topic_keywords[0].append("dinero")
topic_keywords[0].append("deudas")
topic_keywords[0].append("pago")
topic_keywords[0].append("compras")
topic_keywords[0].append("ventas")
topic_keywords[1].append("personal")
topic_keywords[0].append("crédito")
topic_keywords[0].append("débito")
topic_keywords[0].append("tarjeta")
topic_keywords[0].append("débito")'''
topic_keywords[1].append("siento")
topic_keywords[1].append("abrumado")
topic_keywords[1].append("triste")
topic_keywords[1].append("triste")
topic_keywords[1].append("molesto")


t_k=[]
t_k.append(topic_keywords[0])
t_k.append(topic_keywords[1])
t_k.append(topic_keywords[2])
t_k[0]=process_text2(" ".join(t_k[0]),nlp)
t_k[1]=process_text2(" ".join(t_k[1]),nlp)
t_k[2]=process_text2(" ".join(t_k[2]),nlp)

other_corpus = [lda_model.id2word.doc2bow(text) for text in t_k]
lda_model.update(other_corpus)
lda_model.save("LDAxeon") 
print(lda_model.print_topics()) 

# Calcular la coherencia del modelo
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, dictionary=lda_model.id2word, coherence='c_v')
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