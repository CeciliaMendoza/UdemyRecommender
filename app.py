import streamlit as st
import pandas as pd
import re
import pickle

st.set_page_config(page_icon = "random", page_title="Udemy Recommendation", layout="wide")
st.title("Udemy Recommender System, version 1.001")

def quitar_html(x):
    expresion = r"(<\w+>|<\/\w+>)" 
    expresion = re.compile(expresion)
    if isinstance(x, str):
        return re.sub(expresion, "", x)
    else:
        return ''
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

# Just reads the results out of the dictionary.
def recommend(item_id, num):
    return results[item_id][:num]

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("data/Cursos_udemy.csv")
    df["id"] = df["id"].astype(int)
    df["description"] = df["description"].apply(quitar_html)
    return df

@st.cache(allow_output_mutation=True)
def load_diccionario():  
    diccionario = pickle.load(open("Data/results_cosine_similaries.pkl", "rb"))
    return diccionario

df = load_data()
results = load_diccionario()

#st.dataframe(df)
with st.container():
    col1, col2,col3 = st.columns((2,0.5,2.0))
    with col1:
        indice_objetivo = st.number_input('Ingresa un indice del df, van del 0 al ' + str(len(df) - 1 ), 0, len(df) - 1 )
        st.write("Item Usado: " + str(item(get_id(indice_objetivo))))
    with col3:
        num_recomendaciones = st.number_input('Cuantas recomendaciones quieres imprimir?', 1, 100)
        st.write("")

recomendaciones = recommend(item_id=get_id(indice_objetivo), num=num_recomendaciones)
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






    


