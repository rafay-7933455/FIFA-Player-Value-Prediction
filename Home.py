import streamlit as st
import pandas as pd
from PIL import Image
from load_data import load_data

def show(path, h, w, caption):
     img = Image.open(path).resize((h, w))
     st.image(img, caption=caption, use_container_width=True)

players = load_data()

_, c = st.columns([0.85, 2])
with c:
     st.title('FIFA WEB APP')

c1, c2, c3 = st.columns([1, 1,1])

st.sidebar.title('Options Menu')
with c1:
     show("images/messi.jpg", 400,600, "The Magician")
with c2:
     show("images/ronaldo.jpg", 400,600, "The Conquerer")
with c3:
     show("images/bruyne.jpg", 400,600, 'The Future Viewer')

st.markdown('#### This Streamlit Project was built to practice and showcase my skills. I have made different pages in this project eah of which has a separate role.')

desc = {
     'Pages':['Home','Best Free Kick Takers','Find Players','Understand The Dataset','Value Prediction'],
     'Description':['Gives brief description of this project.','Here you can find 10 best free kick takersin a given range of free kick','Here you can find players according to the criteria you provide.','This Page provides understanding of the dataset (cleaned)','This page provides an ML model to predict the \'Value ($)\' based on the characteristics.']
}
desc_df = pd.DataFrame(desc)
st.dataframe(desc_df)