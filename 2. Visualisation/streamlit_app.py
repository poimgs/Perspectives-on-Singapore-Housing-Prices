import streamlit as st
import pandas as pd
import altair as alt
# from streamlit_vega_lite import altair_component
import os

# Import data
resale_flat_prices_file_path = os.path.join('..', 'Cleaned Data', 'resale flat prices.csv')
resale_flat_prices_df = pd.read_csv(resale_flat_prices_file_path)

resale_flat_prices_grouped = resale_flat_prices_df.groupby('district').mean().reset_index()[['district', 'resale_price']]
resale_flat_prices_index = resale_flat_prices_df.groupby('date_sold').mean().reset_index()

# csv file from github url
singapore_districts_map_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Helper%20Data/singapore%20topo%20map.json'

# Price Index
@st.cache
def create_price_index():
    selection = alt.selection_interval()

    return alt.Chart(resale_flat_prices_index).mark_line().encode(
        x=alt.X('date_sold:T'),
        y='resale_price:Q',
    ).add_selection(
        selection
    )

# Map
single_selection = alt.selection_single()

singapore_districts = alt.topo_feature(singapore_districts_map_url, 'data')
singapore_districts_map = alt.Chart(singapore_districts).mark_geoshape(
    stroke='white'
).transform_lookup(
    lookup='properties.id',
    from_=alt.LookupData(resale_flat_prices_grouped, 'district', ['resale_price'])
).encode(
    color=alt.condition(single_selection, 'resale_price:Q', alt.value('lightgray')),
    tooltip=['properties.name:N', 'properties.id:N', 'resale_price:Q']
)

singapore_districts_map_outline = alt.Chart(singapore_districts).mark_geoshape(
    fill='lightgrey',
    stroke='white',
)

singapore_resale_choropleth_map = alt.layer(singapore_districts_map_outline, singapore_districts_map).encode(
    tooltip=['properties.name:N', 'properties.id:N']
).add_selection(
    single_selection
).properties(
    height=600,
    width=800
).configure_view(
    strokeWidth=0
)


st.title('Hello World!')
# st.altair_chart(create_map())

st.altair_chart(singapore_resale_choropleth_map)
# st.altair_chart(HDB_resale_price_index)
# test_selection = altair_component(create_price_index())
# st.write(test_selection)
# st.altair_chart(district_text)