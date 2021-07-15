import streamlit as st
import pandas as pd
import altair as alt
import os

alt.data_transformers.disable_max_rows()

# Import data
resale_flat_prices_small_file_path = os.path.join('..', 'Cleaned Data', 'resale flat prices (small).csv')
mrt_file_path = os.path.join('..', 'Cleaned Data', 'MRT information.csv')
bus_stops_file_path = os.path.join('..', 'Cleaned Data', 'Bus Stops information.csv')
bus_services_file_path = os.path.join('..', 'Cleaned Data', 'Bus Services information.csv')
schools_file_path = os.path.join('..', 'Cleaned Data', 'Schools information.csv')
supermarkets_file_path = os.path.join('..', 'Cleaned Data', 'supermarkets information.csv')
parks_file_path = os.path.join('..', 'Cleaned Data', 'parks information.csv')

resale_flat_prices_small_df = pd.read_csv(resale_flat_prices_small_file_path)
mrt_df = pd.read_csv(mrt_file_path)
bus_stops_df = pd.read_csv(bus_stops_file_path)
bus_services_df = pd.read_csv(bus_services_file_path)
schools_df = pd.read_csv(schools_file_path)
supermarkets_df = pd.read_csv(supermarkets_file_path)
parks_df = pd.read_csv(parks_file_path)

resale_flat_prices_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/resale%20flat%20prices.csv'
resale_flat_prices_small_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/resale%20flat%20prices%20(small).csv'
mrt_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/MRT%20information.csv'
bus_stops_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Bus%20Stops%20information.csv'
bus_services_url = 'raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Bus%20Services%20information.csv'
schools_url = 'hhttps://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/Schools%20information.csv'
supermarkets_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/supermarkets%20information.csv'
parks_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Cleaned%20Data/parks%20information.csv'

st.title('Hello World')

desired_state = st.radio('Overview or single address?', ('Overview', 'Single'))

if desired_state == 'Overview':
    st.write('overview it is!')
else:
    st.write('Single address it is!')

singapore_districts_map_url = 'https://raw.githubusercontent.com/lozy219/angular-singapore-district-map/master/src/district.json'
singapore_districts = alt.Data(url=singapore_districts_map_url,
                               format=alt.DataFormat(property='features',
                                                     type='json'))

singapore_districts_map = alt.Chart(singapore_districts).mark_geoshape(
    fill='lightgrey',
    stroke='white',
).encode(
    # color='properties.id:N',
    tooltip='properties.id:N')

bus_stops = alt.Chart(bus_stops_url).mark_circle(color='orange').encode(
    longitude='Longitude:Q', latitude='Latitude:Q', tooltip='Description:N')

mrt_stations = alt.Chart(mrt_df.drop_duplicates(
    subset=['STN_NAME'])).mark_circle(color='red').encode(
        longitude='Longitude:Q', latitude='Latitude:Q', tooltip='STN_NAME:N')

schools = alt.Chart(schools_df.dropna(subset=['longitude'])).mark_circle(
    color='yellow').encode(longitude='longitude:Q',
                           latitude='latitude:Q',
                           tooltip='school_name:N')

supermarkets = alt.Chart(supermarkets_df.dropna(
    subset=['longitude'])).mark_circle(color='green').encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        tooltip='business_name:N')

parks = alt.Chart(parks_url).mark_circle(color='blue').encode(
    longitude='longitude:Q', latitude='latitude:Q', tooltip='Name:N')

test_chart = alt.layer(singapore_districts_map, mrt_stations, schools,
                       supermarkets, parks).properties(
                           width=800, height=600).configure_view(strokeWidth=0)

st.altair_chart(test_chart)