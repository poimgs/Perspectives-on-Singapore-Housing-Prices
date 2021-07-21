import pandas as pd
import altair as alt
import streamlit as st

@st.cache
def import_resale_prices_df(file_path):
    df = pd.read_csv(file_path)
    df['date_sold'] = pd.to_datetime(df['date_sold'])
    return df 

def transform_resale_flat_prices_df(df, selected_towns, selected_flat_types, start_date, end_date):
    if len(selected_towns) == 0 and len(selected_flat_types) == 0:
        filtered_df = df[
            (df['date_sold'].dt.date > start_date) & 
            (df['date_sold'].dt.date < end_date)
        ]    
    elif len(selected_towns) == 0 and len(selected_flat_types) > 0:
        filtered_df = df[
            (df['date_sold'].dt.date > start_date) & 
            (df['date_sold'].dt.date < end_date) & 
            (df['flat_type'].isin(selected_flat_types)) 
        ]
    elif len(selected_towns) > 0 and len(selected_flat_types) == 0:
        filtered_df = df[
            (df['date_sold'].dt.date > start_date) & 
            (df['date_sold'].dt.date < end_date) & 
            (df['town'].isin(selected_towns))
        ]
    else:
        filtered_df = df[
            (df['date_sold'].dt.date > start_date) & 
            (df['date_sold'].dt.date < end_date) & 
            (df['town'].isin(selected_towns)) &
            (df['flat_type'].isin(selected_flat_types)) 
        ]

    return filtered_df