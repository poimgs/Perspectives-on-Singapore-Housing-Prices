import streamlit as st
import pandas as pd
import altair as alt
# import requests
# from streamlit_vega_lite import altair_component
import os

# # Import data 
resale_flat_prices_file_path = os.path.join('..', 'Cleaned Data', 'resale flat prices.csv')
resale_flat_prices_small_file_path = os.path.join('..', 'Cleaned Data', 'resale flat prices (small).csv')
mrt_file_path = os.path.join('..', 'Cleaned Data', 'MRT information.csv')
bus_stops_file_path = os.path.join('..', 'Cleaned Data', 'Bus Stops information.csv')
bus_services_file_path = os.path.join('..', 'Cleaned Data', 'Bus Services information.csv')
schools_file_path = os.path.join('..', 'Cleaned Data', 'Schools information.csv')
supermarkets_file_path = os.path.join('..', 'Cleaned Data', 'supermarkets information.csv')
parks_file_path = os.path.join('..', 'Cleaned Data', 'parks information.csv')

resale_flat_prices_df = pd.read_csv(resale_flat_prices_file_path)
resale_flat_prices_small_df = pd.read_csv(resale_flat_prices_small_file_path)
mrt_df = pd.read_csv(mrt_file_path)
bus_stops_df = pd.read_csv(bus_stops_file_path)
bus_services_df = pd.read_csv(bus_services_file_path)
schools_df = pd.read_csv(schools_file_path)
supermarkets_df = pd.read_csv(supermarkets_file_path)
parks_df = pd.read_csv(parks_file_path)

# data urls
resale_flat_prices_small_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/resale%20flat%20prices%20(small).csv'
mrt_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/MRT%20information.csv'
bus_stops_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Bus%20Stops%20information.csv'
bus_services_url = 'raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Bus%20Services%20information.csv'
schools_url = 'hhttps://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Schools%20information.csv'
supermarkets_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/supermarkets%20information.csv'
parks_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/parks%20information.csv'

#Altair charts

# price index
resale_flat_prices_index_viz = alt.Chart(resale_flat_prices_small_url).mark_line().encode(
    x='date_sold:T',
    y='mean(resale_price):Q'
).interactive()



# Streamlit app 
st.title('HDB resale prices in Singapore')

# Altair visualisations on stremalit
st.altair_chart(resale_flat_prices_index_viz)