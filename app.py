import streamlit as st
from tools import summ,polarity,ner,text_analyzer
def main():
    st.title("NLP With streamlit api ")
    st.subheader("Summarizing text for classification")

    #TOKENIZATION
    if st.checkbox("Lemmatize"):
        st.subheader("Tokenizing and lemming")
        message= st.text_area("Write your text to tokenize","Here....")
        if st.button("Tokens & Lemma"):
            nlp_result= text_analyzer(message)
            st.json(nlp_result)

    #NER
    if st.checkbox("NER"):
        st.subheader("Showing entities named")
        message= st.text_area("Write your text to Re-Na-En","Here....")
        if st.button("NER"):
            nlp_result= ner(message)
            st.json(nlp_result)

    #Sentiment & polarity
    if st.checkbox("Polarity"):
        st.subheader("Showing sentiment/polarity")
        message= st.text_area("Write your text to show polarity","Here....")
        if st.button("Polarity"): 
            st.success(f'Polarity: {polarity(message)} ')


    #Summarize
    if st.checkbox("Summarize text"):
        st.subheader("Showing summmary of text")
        message= st.text_area("Write your text to summarize","Here....")
        if st.button("Summary"): 
            suma=  summ(message) 
            st.success(suma)




if __name__ == '__main__': 
    main()