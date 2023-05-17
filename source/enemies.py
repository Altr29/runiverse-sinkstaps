import pandas as pd
import numpy as np
import logging
import plotly.express as px
import streamlit as st
from difflib import SequenceMatcher


CR = ['Call of the Ancient Flame',
                'Drawing of Chaos',
                'The Nature of Growth',
                'Juvenile Festivities',
                'Price of Inadequacy',
                'A Giving Nature',
                'Reckless Abandon',
                'Condensed Volatility',
                'Memory of the Peaks',
                'Deeper than Sound',
                'Contemplation of Destiny',
                "The Workers' Rest"]
ER = ["Pilgrim's Staff",
                "Nature's Gift",
                "Ol' Trusty",
                "Butcher's Friend",
                "Joybringer",
                "Devouring Scythe",
                "Witch's Hat",
                "Comfy Hood",
                "Circlet of the Bold",
                "Corsair Bandana",
                "Tactician's Helm",
                "Nightseeker",
                "Witch's Robes",
                "Comfy Robes",
                "Bold Straps",
                "Corsair Apparel",
                "Tactician's Armor",
                "Nightwalker"]

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
            hover_data=['Type','Area','Sprite'],labels={"Gold Drop": "Gold unities"},color='Type',
            text_auto=True, title=f"Gold Drop by Enemies")
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    except Exception as e:
        logging.error('Error in gold_drop ', e)

def collect_(df):
    monsters = {}
    for i, j in df.iterrows():
        if '-' in df.loc[i,'Material Drop 1']:
            monsters[df.loc[i,'Monster']]={
                                     df.loc[i,'Material Drop 2']: df.loc[i,'Quantity Min / Max.1'],
                                     df.loc[i,'Material Drop 3 ']: df.loc[i,'Quantity Min / Max.2'],
                                     df.loc[i,'Recipe Drop']: df.loc[i,'Quantity Min / Max.3'],
                                     df.loc[i,'Crystal Recipe Drop']: df.loc[i,'Quantity Min / Max.4']}
        elif '-' in df.loc[i,'Material Drop 2']:
            monsters[df.loc[i,'Monster']]={
                                     df.loc[i,'Material Drop 1']: df.loc[i,'Quantity Min / Max'],
                                     df.loc[i,'Material Drop 3 ']: df.loc[i,'Quantity Min / Max.2'],
                                     df.loc[i,'Recipe Drop']: df.loc[i,'Quantity Min / Max.3'],
                                     df.loc[i,'Crystal Recipe Drop']: df.loc[i,'Quantity Min / Max.4']}
        elif '-' in df.loc[i,'Material Drop 3 ']:
            monsters[df.loc[i,'Monster']]={
                                     df.loc[i,'Material Drop 1']: df.loc[i,'Quantity Min / Max'],
                                     df.loc[i,'Material Drop 2']: df.loc[i,'Quantity Min / Max.1'],
                                     df.loc[i,'Recipe Drop']: df.loc[i,'Quantity Min / Max.3'],
                                     df.loc[i,'Crystal Recipe Drop']: df.loc[i,'Quantity Min / Max.4']}
        elif '-' in df.loc[i,'Recipe Drop']:
            monsters[df.loc[i,'Monster']]={
                                     df.loc[i,'Material Drop 1']: df.loc[i,'Quantity Min / Max'],
                                     df.loc[i,'Material Drop 2']: df.loc[i,'Quantity Min / Max.1'],
                                     df.loc[i,'Material Drop 3 ']: df.loc[i,'Quantity Min / Max.2'],
                                     df.loc[i,'Crystal Recipe Drop']: df.loc[i,'Quantity Min / Max.4']}
        elif '-' in df.loc[i,'Crystal Recipe Drop']:
            monsters[df.loc[i,'Monster']]={
                                     df.loc[i,'Material Drop 1']: df.loc[i,'Quantity Min / Max'],
                                     df.loc[i,'Material Drop 2']: df.loc[i,'Quantity Min / Max.1'],
                                     df.loc[i,'Material Drop 3 ']: df.loc[i,'Quantity Min / Max.2'],
                                     df.loc[i,'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3']}
        else:
            monsters[df.loc[i, 'Monster']] = {
                df.loc[i, 'Material Drop 1']: df.loc[i, 'Quantity Min / Max'],
                df.loc[i, 'Material Drop 2']: df.loc[i, 'Quantity Min / Max.1'],
                df.loc[i, 'Material Drop 3 ']: df.loc[i, 'Quantity Min / Max.2'],
                df.loc[i, 'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3'],
                df.loc[i, 'Crystal Recipe Drop']: df.loc[i, 'Quantity Min / Max.4']}

    elements = {}
    for key, value in monsters.items():
        #print('--------- Enemy ', key)
        for i,j in value.items():
            i=i.replace('(Rare)','')
            if i=='-':
                pass
            else:
                if j=='-':
                    j=0
                if i not in elements.keys():
                    elements[str(i)]=j
                else:
                    elements[str(i)]+=j

    return elements

def similar(a, els):
    """
    :param a: variable to compare
    :param b: variable to compare with a
    :return: a probability value of similitude
    """
    resp = False
    for el in els:
        if SequenceMatcher(None, a, el).ratio()>.9:
            resp = True
            break
        else:
            pass
    return resp

def d_type(el):
    dt = 'Recipe'
    if 'Soul' in el:
        dt = 'Soul'
    elif 'Ember' in el:
        dt = 'Ember'
    elif 'Shard' in el:
        dt = 'Shard'
    else:
        if el in CR or similar(el, CR):
            dt = 'Crystals Recipes'

        if el in ER or similar(el, ER):
            dt = 'Equipment Recipes'
    return dt



def plot_enem_items(elements):
    new = pd.DataFrame.from_dict(
        {'Items': list(elements.keys()),
         'Amount': list(elements.values()),
         'Type': [d_type(i) for i in list(elements.keys())]})

    fig = px.bar(new.sort_values('Items'), x='Items', y='Amount',color='Type', text_auto=True, title=f"Items Drop")
    fig.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)