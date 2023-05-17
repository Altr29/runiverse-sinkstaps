import pandas as pd
import numpy as np
import logging
import plotly.express as px
import streamlit as st


family = ['Woods','Stone','Gems','Element','Fabrics','Metals']

def reading_sheets(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME):
    try:
        url = f'https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SAMPLE_RANGE_NAME}'
        return pd.read_csv(url)

    except Exception as e:
        logging.error('Exception ', e)

def read_wild_depositchances(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    try:
        df1 = reading_sheets(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
        rename_cols = {
            'Frecuency': 'WoodsFrecuency',
            'Frecuency.1': 'GemsFrecuency',
            'Frecuency.2': 'FabricsFrecuency',
            'Frecuency.3': 'MetalsFrecuency',
            'Frecuency.4': 'StoneFrecuency',
            'Frecuency.5': 'ElementFrecuency'}

        df1.rename(columns=rename_cols, inplace=True)
        df = df1.copy()
        df['WoodsFrecuency'] = df['WoodsFrecuency'].replace(np.nan, 0)
        df['GemsFrecuency'] = df['GemsFrecuency'].replace(np.nan, 0)
        df['FabricsFrecuency'] = df['FabricsFrecuency'].replace(np.nan, 0)
        df['MetalsFrecuency'] = df['MetalsFrecuency'].replace(np.nan, 0)
        df['StoneFrecuency'] = df['StoneFrecuency'].replace(np.nan, 0)
        df['ElementFrecuency'] = df['ElementFrecuency'].replace(np.nan, 0)
        df = df[df['Woods'] != 'Total']
        df.fillna(method='ffill', inplace=True)
        df = df[['Zone Number', 'Land Type', 'Sub-Biome', 'Essence',
                 'Essence Strength', 'Multiplier', 'Woods', 'WoodsFrecuency', 'Gems',
                 'GemsFrecuency', 'Fabrics', 'FabricsFrecuency', 'Metals',
                 'MetalsFrecuency', 'Stone', 'StoneFrecuency', 'Element',
                 'ElementFrecuency']]
        logging.info(f"""Fix sheet {len(df)} ---""")


    except Exception as e:
        logging.error('Error reading deposit chances ', e)
        df = None
    return df


def nodes(el, df1):
    fig = px.bar(
        df1.sort_values('Sub-Biome'), x="Sub-Biome", y=el + "Frecuency", color=el, text_auto='.2s',
        labels={el + "Frecuency": el + " nodes"},
        title=f"{el}")
    fig.update_yaxes(tick0=0, dtick=1)
    fig.update_traces(textfont_size=15, textangle=0, textposition="inside", cliponaxis=False)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def element_multiplier(el: object) -> object:
    val = 5
    if 'Gems' in el or 'Elemen' in el:
        val = 1
    else:
        if 'Met' in el or 'Fabri' in el:
            val = 3
    return val

