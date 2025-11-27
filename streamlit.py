import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Dashbord", page_icon="🐈", layout="wide")
st.subheader("🔎 EDA d'un dataset de chat")
df = pd.read_csv("data_cat.csv")
#st.markdown("## ")
#st.write(df.head())
#st.dataframe(df)

st.warning("⚙️ Les elements du dataset sont en anglais ")
st.sidebar.image("header.jpg", caption = "Fait par EDA_Forge")

st.sidebar.header("Selectionnez les filtres")
breed = st.sidebar.multiselect(
    "Selectionner la race",
    options= df["Breed"].unique(),
    default= df["Breed"].unique()
)
gender = st.sidebar.radio("Selectionnez le genre", ["Tous","male","female"])
if gender == "Tous":
    gender = df["Gender"]

country = st.sidebar.multiselect(
    "Selectionner le pays",
    options= df["Country"].unique(),
    default= df["Country"].unique()
)
#st.write(breed)
df_selection = df[(df['Breed'].isin(breed)) & (df["Country"].isin(country)) & (df["Gender"] == gender)]



if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def afficher_df():
    # Inverse l'état à chaque clic
    st.session_state.button_clicked = not st.session_state.button_clicked

# Bouton
if st.button("Affiché / Caché le dataset"):
    afficher_df()
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Télécharger CSV",
        data=csv,
        file_name="data_cat.csv",
        mime="text/csv"
    )

# Afficher l'état
if st.session_state.button_clicked:
    st.dataframe(df_selection)




st.header('📚 Valeurs interésentes')
race,length,wigth,food = st.columns(4)
with race:
        st.info("La race majoritaire",icon="💡")
        races = df_selection['Breed'].value_counts()
        apparition = {race:races[race]/races.sum()*100 for race in races.index}
        key_max= max(apparition, key = apparition.get)
        ap = st.metric(label= key_max,value= f'{apparition[key_max]:0.3}%')
with length:
        st.info("Taille Moyenne",icon="💡")
        st.metric(label="taille",label_visibility="hidden",value= f'{float(df_selection["Body_length"].mean()):0.3}')
with wigth:
        st.info("Poing Moyen",icon="💡")
        st.metric(label= "poig",label_visibility="hidden",value= f'{float(df_selection["Weight"].mean()):0.3}')
with food:
        st.info("Type de nouriturre",icon="💡")
        races = df_selection['Preferred_food'].value_counts()
        apparition = {race:races[race]/races.sum()*100 for race in races.index}
        key_max= max(apparition, key = apparition.get)
        ap = st.metric(label= key_max,value= f'{apparition[key_max]:0.3}%')

st.markdown("---")
    
##Graphique
# Ajouter des titre et changer la legende
col1,col2 = st.columns(2)
with col1:
    
    st.plotly_chart(px.scatter(df_selection, x="Body_length", y="Weight", color='Breed',labels = {"Breed":"Races","Weight":"Poids","Body_length":"Taille"}, title = "La taille en fonctin du point"))
    st.plotly_chart(px.bar(df_selection, x="Breed", y="Age_in_years", color="Preferred_food", labels={"Breed":"Races","Preferred_food":"Nourriture préférée","Age_in_years":"Âge en année(s)"}, title="La nourriture préférée en fonction de l'âge"),showlegend=True)
with col2:
    st.plotly_chart(px.pie(df_selection, values="Owner_play_time_minutes", names="Preferred_food"), title = "La noutiture préferée en fonction du temps de jeu",showlegend=True)
    st.plotly_chart(px.histogram(df_selection, x="Weight", y="Body_length", color="Preferred_food", labels={"Weight":"Poids","Body_length":"Taille","Preferred_food":"Nourriture préférée"}, title="La nourriture préférée en fonction du corps du chat"),showlegend=True)

st.map(df_selection, latitude="Latitude", longitude="Longitude",zoom=2)
