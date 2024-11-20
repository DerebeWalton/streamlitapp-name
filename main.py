import numpy as np
import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import *
import streamlit as st

@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data

@st.cache_data
def ohw(df):
    nunique_year = df.groupby(['name', 'sex'])['year'].nunique()
    one_hit_wonders = nunique_year[nunique_year == 1].index
    one_hit_wonder_data = df.set_index(['name', 'sex']).loc[one_hit_wonders].reset_index()
    return one_hit_wonder_data

data = load_name_data()
ohw_data = ohw(data)


df = pd.DataFrame(data = {'Ice Cream flavors': ['chocolate', 'vanilla', 'strawberry cheesecake'], 'Ranking': [3, 2, 1]})


st.title('My Cool App')
# st.dataframe(df)

with st.sidebar:
    input_name = st.text_input('Enter a name:')
    year_input = st.slider('Year', min_value =1880, max_value=2023, value = 2000)
    n_names = st.radio('Number of names per sex', [3,5,10])


tab1, tab2, tab3, tab4 = st.tabs(["Names", "Year", "Sexes", "One Hit Wonders"]) 
 
with tab1: 
    # tab 1 contents 

    name_data = data[data['name'] == input_name].copy()
    fig = px.line(name_data, x='year', y='count', color='sex')
    fig3 = name_sex_balance_plot(data, input_name)

    st.plotly_chart(fig)
    st.plotly_chart(fig3)
 
with tab2: 
    # tab 2 contents 
    fig2 = top_names_plot(data, n=n_names, year=year_input)

    st.plotly_chart(fig2)
    st.dataframe(unique_names_summary(data, 2000))


with tab3:
    # tab4 content
    table_one_hits = one_hit_wonders(ohw(data))

    st.dataframe(table_one_hits)

#     Your app should have at least the following elements:

#     four input widgets
#     one graph that updates based on an input 
#     three other text, tables, or graphs that update based on an input
#     two tabs
#     a sidebar 
#     one other container or layout element

#     Deploy your app using GitHub and Streamlit Community Cloud