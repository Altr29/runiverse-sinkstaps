import pandas as pd
import numpy as np
import logging
import plotly.express as px
import streamlit as st


def enemies_files(sheet):
    try:
        enemies0 = pd.read_excel('source/Alpha Enemies.xlsx',sheet_name=sheet)
        enemies0.rename(columns={'                                                                 Monster':
                                     'Monster'}, inplace=True)

        df = enemies0[enemies0.columns[:-7]].astype({'Quantity Min / Max':'string',
                                                     'Quantity Min / Max.1':'string',
                                                     'Quantity Min / Max.2':'string',
                                                     'Quantity Min / Max.3':'string',
                                                     'Quantity Min / Max.4':'string'})

        df=df[df['Monster'].str.contains('Area') == False]

        for el in ['Quantity Min / Max','Quantity Min / Max.1','Quantity Min / Max.2','Quantity Min / Max.3',
                   'Quantity Min / Max.4','Gold Drop']:
          df[el] = df[el].replace(np.nan, '0').replace('-', '0')
          df[el] = df[el].apply(lambda x: int(str(x)[8:10]) if len(str(x))>8 else int(x))

        return df

    except Exception as e:
        logging.error('Error in enemies_files ', e)

def gold_drop(df, NAME, title):
    try:
        fig = px.bar(
            df.sort_values(NAME), x=NAME, y=title,
            hover_data=['Type','Area','Sprite'],labels={"value": "Items"},
            text_auto=True, title=f"Gold Drop by Enemies")
        fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    except Exception as e:
        logging.error('Error in gold_drop ', e)