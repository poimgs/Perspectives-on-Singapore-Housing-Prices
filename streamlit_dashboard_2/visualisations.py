import altair as alt
import pandas as pd

singapore_districts_map_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Helper%20Data/singapore%20topo%20map.json'
singapore_districts = alt.topo_feature(singapore_districts_map_url, 'data')

# Helper function to create appropriate tooltip for Singapore Map based on variable
def create_tooltip(variable, title, format_=None):
    if format_ is None:
        return alt.Tooltip(f'{variable}:Q', title=title)
    else:
        return alt.Tooltip(f'{variable}:Q', title=title, format=format_)

def singapore_map(df, selected_comparison_1, selected_comparison_2, comparison_variable):
    if selected_comparison_1 == 'None' or selected_comparison_2 == 'None':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['town'].isin([selected_comparison_1.upper(), selected_comparison_2.upper()])]

    transformed_df = filtered_df.groupby('district').mean().reset_index()
    
    var = ''
    title = ''
    format_ = None
    if comparison_variable == 'Price':
        var = 'resale_price'
        title = 'Average Resale Price'
        format_ = '$,.3r'
    elif comparison_variable == 'Age':
        var = 'HDB_age'
        title = 'Average Age of HDBs (Years)'
        format_ = 'd'
    elif comparison_variable == 'Distance to Closest MRT':
        var = 'mrt_distance'
        title = 'Avg. Distance (meters)'
        format_ = 'd'
    elif comparison_variable == 'Distance to Closest Bus Stop':
        var = 'bus_distance'
        title = 'Avg. Distance (meters)'
        format_ = 'd'
    elif comparison_variable == 'Distance to Closest Supermarket':
        var = 'supermarket_distance'
        title = 'Avg. Distance (meters)'
        format_ = 'd'
    elif comparison_variable == 'Distance to Closest Primary School':
        var = 'primary_school_distance'
        title = 'Avg. Distance (meters)'
        format_ = 'd'
    elif comparison_variable == 'Distance to Closest Park':
        var = 'park_distance'
        title = 'Avg. Distance (meters)'
        format_ = 'd'

    tooltip = create_tooltip(var, title, format_)

    singapore_districts_map = alt.Chart(singapore_districts).mark_geoshape(
        stroke='white'
    ).encode(
        color=f'{var}:Q',
        tooltip=[
            alt.Tooltip('properties.id:N', title='District ID'), 
            alt.Tooltip('properties.name:N', title='District General Location'), 
            tooltip
        ]
    ).transform_lookup(
        lookup='properties.id',
        from_=alt.LookupData(transformed_df, 'district', [f'{var}'])
    )

    singapore_districts_map_outline = alt.Chart(singapore_districts).mark_geoshape(
        fill='lightgrey',
        stroke='white',
    )

    singapore_map = alt.layer(singapore_districts_map_outline, singapore_districts_map).properties(
        height=400
    ).configure_view(
        strokeWidth=0
    )

    return singapore_map