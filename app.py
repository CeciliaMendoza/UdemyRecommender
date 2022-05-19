import streamlit as st

import pandas as pd
import re

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import string
import nltk
nltk.download('stopwords')
stopword_en = nltk.corpus.stopwords.words('english')
stopword_es = nltk.corpus.stopwords.words('spanish')
nltk.download('punkt')

st.set_page_config(page_icon = "random", page_title="Udemy Recommendation", layout="wide")
st.title("Udemy Recommender System, version 1.001")

def quitar_html(x):
    expresion = r"(<\w+>|<\/\w+>)" 
    expresion = re.compile(expresion)
    if isinstance(x, str):
        return re.sub(expresion, "", x)
    else:
        return ''

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def quitar_numeros(text):
    expresion = r"(\s|\b)\d+(\b)" 
    expresion = re.compile(expresion)
    if isinstance(text, str):
        return re.sub(expresion, "", text)
    else:
        return ''

def remove_mystopwords(sentence):
    tokens = sentence.split(" ")
    tokens_filtered= [word for word in tokens if not word in stop_words]
    return " ".join(tokens_filtered)

def clean_busqueda(termino):
    termino = termino.lower()
    termino = remove_punctuations(termino)
    termino = remove_mystopwords(termino)
    termino = quitar_numeros(termino)
    return termino

otras_palabras_a_remover = ['advanced',
 'beginner',
 'beginners',
 'build',
 'cero',
 'certification',
 'certified',
 'complete',
 'completo',
 'course',
 'curso',
 'exam',
 'fundamentals',
 'guide',
 'introduction',
 'learn',
 'learning',
 'master',
 'masterclass',
 'training',
 'using']

stop_words = stopword_en + stopword_es  + otras_palabras_a_remover

#retorna el id segun el indice en el df
def get_id(indice):
    return df.iloc[indice]["id"]
#Retorna el title segun el id
def item(id):
    return df.loc[df['id'] == id]['title'].tolist()[0].split(' - ')[0]
#retorna la descripcion segun el id
def item_informacion(id):
    row = df.loc[df['id'] == id]
    titulo = row['title'].tolist()[0].split(' - ')[0]
    description =  row['description'].tolist()[0].split(' - ')[0]
    category = row['primary_category'].tolist()[0].split(' - ')[0]
    url = row['url'].tolist()[0].split(' - ')[0]
    datos = {"title" : titulo, 
    "description": description,
    "category" : category, 
    "url": url} 
    return datos

def recomendaciones_busqueda(busqueda, num_recomendaciones):
  #instancia de TfidfVectorizer
  tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words=('english', "spanish"))
  #poner la busqueda en una serie
  busqueda = pd.Series(data=[busqueda])
  #serie de la columna rs, rs es resultado de modificar la columan title 
  rs = df['rs']
  #append de la busqueda
  rs= rs.append(busqueda, ignore_index=True)
  #aprender el vocabulario con fit
  tfidf_matrix = tf.fit_transform(rs)
  #cosine similarities
  cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
  #cosines de la busqueda, siendo esta el ultimo elemento de la serie 
  sim_scores = list(enumerate(cosine_similarities[len(rs)-1]))
  #ordenar por cosine similarity
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  #num de recomendaciones + 1, por si tenemos que quitar el cosine de busqueda
  sim_scores = sim_scores[0:num_recomendaciones + 1]
  #quitar la busqueda si esta dentro del las recomendaiones
  sim_scores = list(filter(lambda x: x[0] != len(rs)-1, sim_scores))
  #modificar para que regrese cosine similarity, id
  sim_scores = [(i[1] , get_id(i[0])  ) for i in sim_scores]
  return sim_scores[0:num_recomendaciones]

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("Data/Cursos_udemy.csv")
    df["id"] = df["id"].astype(int)
    df["description"] = df["description"].apply(quitar_html)
    df["rs"] = df["title"].str.lower()
    #quitar stop words and punctuation
    df["rs"] = df["rs"].apply(remove_punctuations)
    df["rs"] = df["rs"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
    #quitar numeros, esto es para quitar por ejemplo 2022, 2021 en los titulos 
    df["rs"] = df["rs"].apply(quitar_numeros)

    return df


df = load_data()

#st.dataframe(df)
with st.container():
    col1, col2,col3 = st.columns((2,0.5,2.0))
    with col1:
        termino_a_buscar = st.text_input('Termino de Busqueda', '')
        st.write("Item Usado: " + termino_a_buscar)
    with col3:
        num_recomendaciones = st.number_input('Cuantas recomendaciones quieres imprimir?', 1, 100)
        st.write("")
if (termino_a_buscar != ""):

    recomendaciones = recomendaciones_busqueda(clean_busqueda(termino_a_buscar), num_recomendaciones)
    i = 0
    with st.container():
        col1, col2,col3 = st.columns((2,0.5,2.0))
        for r in recomendaciones:
            info = item_informacion(r[1])
            if i%2==0:
                with col1:
                    #st.write(id)
                    st.write(info["title"])
                    with st.expander("Ver mas detalles"):
                        st.write("Descripcion")
                        st.write(info["description"])
                        st.write("Categoria:")
                        st.write(info["category"])
                        st.write("Url:")
                        st.write(info["url"])

            else:
                with col3:
                    #st.write(id)
                    st.write(info["title"])
                    with st.expander("Ver mas detalles"):
                        st.write("Descripcion")
                        st.write(info["description"])
                        st.write("Categoria:")
                        st.write(info["category"])
                        st.write("Url:")
                        st.write(info["url"])
            i = i+1