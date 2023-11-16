import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

# CARGA DE DADOS
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')          # Create a text element and let the reader know the data is loading.
data = load_data(10000)                               # Load 10,000 rows of data into the dataframe.
data_load_state.text("Done! (using st.cache_data)")   # Notify the reader that the data was successfully loaded.

# GRÁFICO DE BARRAS
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

#GRÁFICO DE MAPA
st.subheader('Map of all pickups')
st.map(data)
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h