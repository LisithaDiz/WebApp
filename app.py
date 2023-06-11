import streamlit as st
from predict_page import show_predication
from explore import show_explore

page = st.sidebar.selectbox('Explore or Predict', ('Predict', 'Explore'))

if page == 'Predict':
    show_predication()
else:
    show_explore()
