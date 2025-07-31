import pandas as pd
import streamlit as st
from load_data import load_data
import matplotlib.pyplot as plt
import io

plt.rcParams.update({
    'font.family': 'Times New Roman',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.facecolor': '#071330',
    'axes.facecolor': '#0c4160',
    'axes.edgecolor': '#000000',
    'axes.labelcolor': '#ffffff',
    'xtick.color': '#ffffff',
    'ytick.color': '#ffffff',
    'text.color': 'white',
    'grid.color': '#3ffcc9'
})

players = load_data()

#
_,c = st.columns([1,5])
with c:
    st.title('Understand the Data Set')

# Description
buffer = io.StringIO()
players.info(buf=buffer)

Columns = buffer.getvalue().split('\n')[3].split()
Null_Count = pd.DataFrame(columns=[Columns[i] for i in [1,2,4]])
index = 0
for i in buffer.getvalue().split('\n'):
    if i and i.split()[0].isnumeric():
        Null_Count.loc[index, :] = [i.split()[j] for j in [1,2, 4]]
        index+=1
st.subheader('Description Of DataSet Columns')
st.dataframe(Null_Count)

# Select plot
plot = st.sidebar.multiselect('Choose One Of The Plots', options=['Scatter Plot', 'Histogram', 'Correlation'])

# image
st.sidebar.image('images/data.jpg')

# Value Distribution
if 'Histogram' in plot:
    from numpy import log
    fig, ax = plt.subplots(figsize=(10,5))
    st.subheader('Logarithmic Distribution Of Column \'value\'')
    ax.set_xlabel('Log(players.value)')
    ax.set_ylabel('No. Of Player')
    ax.hist(log(players.value), bins=100)
    st.pyplot(fig)

# Correlation
if 'Correlation' in plot:
    features = players.select_dtypes(include=['int64', 'float64'])
    st.subheader('Correlation Of All Features With \'Value\' Column')
    fig, ax=plt.subplots(figsize=(10,7))
    ax.set_ylabel('Player Feaatures')
    ax.set_xlabel('Correlation Value')
    ax.barh(features.drop(columns='value').columns, features.corr()['value'].drop('value'))
    st.pyplot(fig=fig)

# Scatter Plot
if 'Scatter Plot' in plot:
    st.subheader('Distribution Using ScatterPlot')
    fig, ax = plt.subplots(figsize = (10,5))
    ax.set_xlabel('Player Reactions')
    ax.set_ylabel('Player Value')
    ax.scatter(y=players.value, x=players.reactions)
    st.pyplot(fig)