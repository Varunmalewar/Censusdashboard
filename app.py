import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


st.set_page_config(layout='wide')
# upload dataset
df = pd.read_csv('india.csv')

list_of_states = list(df['State'].unique())
list_of_states.insert( 0,'Overall India')


st.sidebar.title("Data Visualization App")

selected_state = st.sidebar.selectbox('Select a state', list_of_states)

primary = st.sidebar.selectbox('Select Primary Parameter ',sorted(df[['Population','Households_with_Internet','sex_ratio','literacy_rate']]))

secondary = st.sidebar.selectbox('Select Secondary Parameter ',sorted(df[['Population','Households_with_Internet','sex_ratio','literacy_rate']]))


plot = st.sidebar.button('Generate Graph')

if plot :
    st.text('Size represent primary parameter and color represent secondary parameter')
    if selected_state == 'Overall India':
        # plotting for overall India
        fig = px.scatter_map(df, lat="Latitude", lon="Longitude",size = primary,size_max=35,color = secondary ,zoom=3,hover_name="District")

        st.plotly_chart(fig, use_container_width=True)




    
    else:
        # plotting for selected state
        state_df = df[df['State']==selected_state]

        fig = px.scatter_map(state_df, lat="Latitude", lon="Longitude",size = primary,size_max=35,color = secondary ,zoom=6,hover_name="District")

        st.plotly_chart(fig, use_container_width=True)      