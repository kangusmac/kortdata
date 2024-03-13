from kalender import kalender, datoer_i_måned
import streamlit as st
from datetime import datetime
from sommerhuse import SOMMERHUSE, mygeodata
from streamlit_folium import st_folium
import folium
#  Get date today
today = datetime.now().strftime('%d %m %Y')




#  Get the calendar for the current month
indeværende_måned = 'mar'
#marts = kalender(indeværende_måned)
marts = datoer_i_måned()

# brug nøglerne til at lave en liste af datoer
# vis denne liste i en selectbox
datoer = list(marts.keys())
dato = st.selectbox("Vælg dato", datoer)
st.write(f"Du har valgt {dato}")
st.write(f"Der er {len(marts[dato])} sommerhuse ledige på denne dato")
#st.dataframe(marts[dato],
#             column_config={ "value": "Placering",})
# do not show column 'Henvisning'

st.dataframe(marts[dato], column_config={ "value": "Placering",})


mygeo = mygeodata(marts[dato])
lat_avg = mygeo['latitude'].mean()
lon_avg = mygeo['longitude'].mean()
m = folium.Map(location=[lat_avg, lon_avg], zoom_start=20)
for i in range(len(mygeo)):
    folium.Marker([mygeo.iloc[i]['latitude'], mygeo.iloc[i]['longitude']], popup=mygeo.iloc[i]['Placering']).add_to(m)
st_folium(m)
#st.map(mygeo,)

