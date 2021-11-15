import streamlit as st
import altair as alt
import os
from visualisations import *
from helper_functions import *

# Config options for streamlit
st.set_page_config(
    page_title='Singapore Housing Prices',
    layout='wide'
)

# Import relevant data
resale_flat_prices_current_year_file_path = os.path.join(
    '..', 'Cleaned Data', 'resale flat prices (current year).csv')
unique_hdb_flats_file_path = os.path.join(
    '..', 'Cleaned Data', 'unique HDB flats.csv')

resale_flat_prices_current_year_df = import_resale_prices(
    resale_flat_prices_current_year_file_path)
unique_hdb_flats_df = import_unique_hdb_flats(unique_hdb_flats_file_path)

# Introductions
st.write('''
# Choose your ideal HDB
> Thank you for visting my mini-app! This mini-app was created for me to practice web scraping, data processing and data visualisation, all using Python
''')

# Instructions
with st.beta_expander('Instructions'):
    st.write('''
        Below, you can see the Singapore map with HDB information distributed by districts.

        Above the map, you may select two towns to compare by different comparison variables

        You may also select the same town for both to focus on the specific town

        When you are ready, you can select a district below the map to learn more about the HDBs within it
    ''')

# Comparison options
comparison_1, comparison_2, comparison_variable = st.beta_columns(3)
selected_comparison_1 = comparison_1.selectbox(
    'Town 1',
    ['None', 'Ang Mo Kio', 'Bedok', 'Bishan', 'Bukit Batok', 'Geylang', 'Bukit Merah', 'Bukit Timah', 'Central Area', 'Choa Chu Kang', 'Clementi', 'Hougang', 'Jurong East', 'Jurong West',
        'Kallang/Whampoa', 'Marine Parade', 'Queenstown', 'Serangoon', 'Tampines', 'Toa Payoh', 'Woodlands', 'Yishun', 'Sembawang', 'Lim Chu Kang', 'Bukit Panjang', 'Pasir Ris', 'Sengkang', 'Punggol']
)
selected_comparison_2 = comparison_2.selectbox(
    'Town 2',
    ['None', 'Ang Mo Kio', 'Bedok', 'Bishan', 'Bukit Batok', 'Geylang', 'Bukit Merah', 'Bukit Timah', 'Central Area', 'Choa Chu Kang', 'Clementi', 'Hougang', 'Jurong East', 'Jurong West',
        'Kallang/Whampoa', 'Marine Parade', 'Queenstown', 'Serangoon', 'Tampines', 'Toa Payoh', 'Woodlands', 'Yishun', 'Sembawang', 'Lim Chu Kang', 'Bukit Panjang', 'Pasir Ris', 'Sengkang', 'Punggol']
)
selected_comparison_variable = comparison_variable.selectbox(
    'Comparison Variable',
    ['Price', 'Age', 'Distance to Closest MRT', 'Distance to Closest Bus Stop',
        'Distance to Closest Supermarket', 'Distance to Closest Primary School', 'Distance to Closest Park']
)

# Singapore Map
if comparison_variable == 'Price':
    st.altair_chart(singapore_map(resale_flat_prices_current_year_df,
                    selected_comparison_variable), use_container_width=True)
else:
    st.altair_chart(singapore_map(unique_hdb_flats_df, selected_comparison_1,
                    selected_comparison_2, selected_comparison_variable), use_container_width=True)