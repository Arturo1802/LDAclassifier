import streamlit as st
import pandas as pd 
from LDAtools import getFullDataSQL,first_inference
import gensim
lda_model = gensim.models.LdaMulticore.load('LDAxeon')   


visTAB, classifyTAB=st.tabs(['Visualize','Classify'])
df= getFullDataSQL()
df=df.drop("cEXT",axis=1).drop("cEMS",axis=1).drop("cAGR",axis=1).drop("cCON",axis=1).drop("cOPN",axis=1).drop("#AUTHID",axis=1).drop("finalinf",axis=1)
visTAB.subheader("Dataframe")
visTAB.dataframe(df)
class_counts = df['preinf'].value_counts() 
class_counts_df = pd.DataFrame({'preinf': class_counts.index, 'count': class_counts.values}) 
visTAB.subheader("Class ratio")
visTAB.bar_chart(class_counts )
visTAB.subheader("Polarity Ratio")
class_counts = df['polarity'].value_counts() 
class_counts_df = pd.DataFrame({'polarity': class_counts.index, 'count': class_counts.values}) 
visTAB.bar_chart(class_counts_df)
classifyTAB.subheader("Text classification")
text=classifyTAB.text_area("Write a text describing your week", "Type here....")
if classifyTAB.button("Go"):
    inf=first_inference(text.strip(),lda_model) 
    if (inf[0]==0):
        classif="Economic "
    elif inf[0]==1:
        classif="Academic"
    elif inf[0]==2:
        classif="Personal"
    else:
        classif="NONE"
    classifyTAB.success(classif+str(inf[1]*100)+"%")

 

