import pandas as pd
import numpy as np
import logging
import plotly.express as px
import streamlit as st
from source.enemies import plot_enem_items
from source.inputs import d_type
import re


def reading_sheets(alpha, event):
    try:
        if alpha:
            df = pd.read_excel('source/ALPHA wild resources (1).xlsx', sheet_name='W Resources')
        else:
            SAMPLE_SPREADSHEET_ID = event['SAMPLE_SPREADSHEET_ID']
            SAMPLE_RANGE_NAME = event['SAMPLE_RANGE_NAME']
            url = f'https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SAMPLE_RANGE_NAME}'
            df = pd.read_csv(url)
        return df

    except Exception as e:
        return None
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


def nodes(el, df1, alpha):
    try:
        if alpha:
            fig = px.bar(
                df1.sort_values('Sub-Biome'), x=el, y=el + "Frecuency", color='Sub-Biome', text_auto='.2s',
                labels={el + "Frecuency": el + " nodes"},
                title=f"{el} Gathering Nodes")
        else:
            fig = px.bar(
                df1.sort_values('Sub-Biome'), x="Sub-Biome", y=el + "Frecuency", color=el, text_auto='.2s',
                labels={el + "Frecuency": el + " nodes"},
                title=f"{el}")
        fig.update_yaxes(tick0=0, dtick=1)
        fig.update_traces(textfont_size=15, textangle=0, textposition="inside", cliponaxis=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    except Exception as e:
        logging.error('Error nodes ', e)


def element_multiplier(el: object) -> object:
    try:
        if 'Gems' in el or 'Elemen' in el:
            val = 1
        elif 'Met' in el or 'Fabri' in el:
            val = 3
        else:
            val = 5
        return val

    except Exception as e:
        logging.error('Error element_multiplier >> ', e)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def __enemy(df, Monster, Area_l, batt_times):
    a1 = df[(df['MONSTER'].str.contains(str(Monster)) == True) &
            (df['AREA'].str.contains(str(Area_l)) == True)]

    bats = []
    if batt_times >= 10:
        bats = [a1.iat[0, -1]]
    else:
        for i in range(0, batt_times):
            bats.append(a1.iat[0, i + 2])

    bat_oorder = {}
    bats1 = [x for x in bats if "No Drop" not in x]

    if len(bats1) < 1:
        st.write('No enemies to encounter')
    else:
        for s in bats1:
            nums = re.findall('\d+', s)
            els = []
            N = len(nums)
            for i in range(0, N):
                if 'No Drops' in s:
                    els = []
                    break
                else:
                    if i < 1:
                        els.append(s.split(nums[i])[0].replace(' - ', '').replace('\n', ''))
                    else:
                        if i > N - 1:
                            els.append(s.split(nums[i])[-1].replace(' - ', '').replace('\n', ''))
                        else:
                            x = find_between(s, nums[i - 1], nums[i])
                            els.append(x.replace(' - ', '').replace('\n', ''))

            if els:
                for ele in els:
                    j = els.index(ele)
                    if ele not in bat_oorder.keys():
                        bat_oorder[ele] = int(nums[j])
                    else:
                        bat_oorder[ele] += int(nums[j])
            else:
                pass

    spiritual_elements = pd.DataFrame.from_dict(
        {'Items': list(bat_oorder.keys()),
         'Amount': list(bat_oorder.values()),
         'Type': [d_type(i) for i in list(bat_oorder.keys())]})

    st.write(f":green[Against {Monster}]")
    plot_enem_items(spiritual_elements)
