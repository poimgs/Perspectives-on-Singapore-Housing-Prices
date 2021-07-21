import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
# import requests
# from streamlit_vega_lite import altair_component
import os
import datetime
from helper_functions import *
from visualisations import *

# Config options for streamlit
st.set_page_config(
    page_title='Singapore Housing Prices',
    layout='wide'
)

# data file paths
resale_flat_prices_file_path = os.path.join('data', 'resale flat prices.csv')
resale_flat_prices_small_file_path = os.path.join('data', 'resale flat prices (small).csv')
mrt_file_path = os.path.join('data', 'MRT information.csv')
bus_stops_file_path = os.path.join('data', 'Bus Stops information.csv')
bus_services_file_path = os.path.join('data', 'Bus Services information.csv')
schools_file_path = os.path.join('data', 'Schools information.csv')
supermarkets_file_path = os.path.join('data', 'supermarkets information.csv')
parks_file_path = os.path.join('data', 'parks information.csv')

# Import needed data
resale_flat_prices_df = import_resale_prices_df(resale_flat_prices_file_path)

# data urls
resale_flat_prices_small_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/resale%20flat%20prices%20(small).csv'
mrt_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/MRT%20information.csv'
bus_stops_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Bus%20Stops%20information.csv'
bus_services_url = 'raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Bus%20Services%20information.csv'
schools_url = 'hhttps://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Schools%20information.csv'
supermarkets_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/supermarkets%20information.csv'
parks_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/parks%20information.csv'

# Filters
first, second, third, fourth, fifth = st.beta_columns(5)

# Dates
start_date = first.date_input('Start Date', datetime.date(1990,1,1))
end_date = second.date_input('End Date')
# Town
selected_towns = third.multiselect(
    'Town', 
    ['Ang Mo Kio', 'Bedok', 'Bishan', 'Bukit Batok', 'Geylang', 'Bukit Merah', 'Bukit Timah', 'Central Area', 'Choa Chu Kang', 'Clementi', 'Hougang', 'Jurong East', 'Jurong West', 'Kallang/Whampoa', 'Marine Parade', 'Queenstown', 'Serangoon', 'Tampines', 'Toa Payoh', 'Woodlands', 'Yishun', 'Sembawang', 'Lim Chu Kang', 'Bukit Panjang', 'Pasir Ris', 'Sengkang', 'Punggol']
)
# Flat type
selected_flat_types = fourth.multiselect(
    'Flat Type', 
    ['1 Room', '2 Room', '3 Room', '4 Room', '5 Room', 'Multi-Generation', 'Executive']
)
# Compare by
compare_option = fifth.selectbox(
    'Compare prices by:',
    ['None', 'Town', 'Flat Type']
)

# Transform selected inputs from filters
selected_towns = list(map(lambda town: town.upper(), selected_towns))
selected_flat_types = list(map(lambda flat_type: flat_type.upper(), selected_flat_types))

# Transform data based on filters 
resale_flat_prices_df_filtered = transform_resale_flat_prices_df(resale_flat_prices_df, selected_towns, selected_flat_types, start_date, end_date)

# Singapore Map
st.altair_chart(create_singapore_districts_chart(resale_flat_prices_df_filtered), use_container_width=True)

left_chart, right_chart = st.beta_columns(2)
# Price resale index chart
left_chart.altair_chart(create_price_index_chart(resale_flat_prices_df_filtered, compare_option), use_container_width=True)
# Distribution chart
right_chart.altair_chart(create_distribution_chart(resale_flat_prices_df_filtered, compare_option), use_container_width=True)
