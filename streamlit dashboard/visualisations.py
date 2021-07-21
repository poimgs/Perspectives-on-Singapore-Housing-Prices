import altair as alt
import pandas as pd
import streamlit as st

# Singapore districts map
def create_singapore_districts_chart(df):
    singapore_districts_map_url = 'https://raw.githubusercontent.com/poimgs/Perspectives-on-Singapore-Housing-Prices/main/Helper%20Data/singapore%20topo%20map.json'
    singapore_districts = alt.topo_feature(singapore_districts_map_url, 'data')

    transformed_df = df.groupby('district').mean().reset_index()[['district', 'resale_price']]

    singapore_districts_map = alt.Chart(singapore_districts).mark_geoshape(
        stroke='white'
    ).encode(
        color='resale_price:Q',
        # tooltip=['properties.name:N', 'properties.id:N', 'resale_price:Q']
        tooltip=[
            alt.Tooltip('properties.id:N', title='District ID'), 
            alt.Tooltip('properties.name:N', title='District General Location'), 
            alt.Tooltip('resale_price:Q', title='Average Resale Price', format='$,.3r')
        ]
    ).transform_lookup(
        lookup='properties.id',
        from_=alt.LookupData(transformed_df, 'district', ['resale_price'])
    )

    singapore_districts_map_outline = alt.Chart(singapore_districts).mark_geoshape(
        fill='lightgrey',
        stroke='white',
    )

    singapore_districts_chart = alt.layer(singapore_districts_map_outline, singapore_districts_map).properties(
        height=400
    ).configure_view(
        strokeWidth=0
    )

    return singapore_districts_chart

# Price Index Chart
def create_price_index_chart(df, compare_option):
    transformed_df = df.groupby(['town', 'district', 'flat_type', 'date_sold']).mean().reset_index()[['date_sold', 'resale_price', 'town', 'flat_type']]

    HDB_resale_price_index = alt.Chart(transformed_df).mark_line().encode(
        x='date_sold:T',
        y='mean(resale_price):Q',
        tooltip=[
            alt.Tooltip('date_sold:T', title='Date Sold', format='%b %Y'), 
            alt.Tooltip('mean(resale_price):Q', title='Average Resale Price', format='$,.3r')
            ]
    ).interactive()

    if compare_option == 'Town':
        HDB_resale_price_index = HDB_resale_price_index.encode(
            color='town:N'
        ).encode(
            tooltip=[
                alt.Tooltip('date_sold:T', title='Date Sold', format='%b %Y'), 
                alt.Tooltip('mean(resale_price):Q', title='Average Resale Price', format='$,.3r'),
                alt.Tooltip('town:N', title='Town')
            ]
        ).configure_legend(
            orient='bottom'
        )

    if compare_option == 'Flat Type':
        HDB_resale_price_index = HDB_resale_price_index.encode(
            color='flat_type:N'
        ).encode(
            tooltip=[
                alt.Tooltip('date_sold:T', title='Date Sold', format='%b %Y'), 
                alt.Tooltip('mean(resale_price):Q', title='Average Resale Price', format='$,.3r'),
                alt.Tooltip('flat_type:N', title='Flat Type')
            ]
        ).configure_legend(
            orient='bottom'
        )

    return HDB_resale_price_index

def create_distribution_chart(resale_df, compare_option):
    binned_dfs = []

    if compare_option == 'None':
        mask, bins = pd.cut(resale_df['resale_price'], bins=15, retbins=True)
        binned = resale_df.groupby(mask).count()[['resale_price']]
        binned['bin_min'] = bins[:-1]
        binned['bin_max'] = bins[1:]
        binned = binned.reset_index(drop=True)

        distribution_chart = alt.Chart(binned).mark_bar().encode(
            x=alt.X('bin_min', bin='binned'),
            x2='bin_max',
            y='resale_price'
        ).interactive()

    if compare_option == 'Town':
        for index, df in resale_df.groupby('town'):
            town = df['town'].iloc[0]

            mask, bins = pd.cut(df['resale_price'], bins=15, retbins=True)
            binned = df.groupby(mask).count()[['resale_price']]
            binned['bin_min'] = bins[:-1]
            binned['bin_max'] = bins[1:]
            binned['town'] = town
            binned = binned.reset_index(drop=True)

            binned_dfs.append(binned)

        binned = pd.concat(binned_dfs)

        distribution_chart = alt.Chart(binned).mark_bar().encode(
            x=alt.X('bin_min', bin='binned'),
            x2='bin_max',
            y='resale_price',
            color = 'town',
            opacity = alt.value(0.7)
        ).configure_legend(
            orient='bottom'
        ) 

    if compare_option == 'Flat Type':
        for index, df in resale_df.groupby('flat_type'):
            flat_type = df['flat_type'].iloc[0]

            mask, bins = pd.cut(df['resale_price'], bins=15, retbins=True)
            binned = df.groupby(mask).count()[['resale_price']]
            binned['bin_min'] = bins[:-1]
            binned['bin_max'] = bins[1:]
            binned['flat_type'] = flat_type
            binned = binned.reset_index(drop=True)

            binned_dfs.append(binned)

        binned = pd.concat(binned_dfs)

        distribution_chart = alt.Chart(binned).mark_bar().encode(
            x=alt.X('bin_min', bin='binned'),
            x2='bin_max',
            y='resale_price',
            color = 'flat_type',
            opacity = alt.value(0.7)
        ).configure_legend(
            orient='bottom'
        ).interactive()

    return distribution_chart