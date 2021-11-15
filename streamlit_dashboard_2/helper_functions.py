import pandas as pd
import streamlit as st

@st.cache
def import_resale_prices(file_path):
    df = pd.read_csv(file_path)
    return df 

@st.cache 
def import_unique_hdb_flats(file_path):
    df = pd.read_csv(file_path)
    return df 