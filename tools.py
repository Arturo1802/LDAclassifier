import spacy  
from spacy.lang.es.stop_words import STOP_WORDS   
from csvTools.translating import traducir_linea
from spacytextblob.spacytextblob import SpacyTextBlob

nlp= spacy.load('es_core_news_lg') 
eng_nlp=spacy.load('en_core_web_lg') 
eng_nlp.add_pipe("spacytextblob")
stopwords=list(STOP_WORDS)
from string import punctuation
from heapq import nlargest
punctuation=punctuation+ '\n'

def polarity(text):
    text=traducir_linea(text)
    doc = eng_nlp(text) 
    tokens_sin_puntuacion = [token.text for token in doc if not token.is_punct] 
    texto_sin_puntuacion = ' '.join(tokens_sin_puntuacion)
    return -1 if doc._.blob.polarity<0 else 1
    

def text_analyzer(text): 
    docx = nlp(text) 
    #print(f"Idioma: {nlp.lang}")
    data= [ ('"Tokens": {},\n"Lemma": {}'.format(token.text,token.lemma_))  for token in docx]
    return data

def ner(text): 
    docx = nlp(text)
    print(f"Idioma: {nlp.lang}") 
    entities= [(entity.text, entity.label_) for entity in docx.ents]
    return entities

def summ(text): 
    doc= nlp(text)
    tokens=[token.text for token in doc ]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1 
    
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
 
    #get sentence tokens
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
               if sent not in sentence_scores.keys():                            
                  sentence_scores[sent]=word_frequencies[word.text.lower()]
               else:
                  sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*0.3)
    select_length
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary] 
    summary=''.join(final_summary) 
    return summary
