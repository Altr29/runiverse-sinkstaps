import pandas as pd
import numpy as np
import logging
import plotly.express as px
import streamlit as st
# COSTS


woods_stones = {
    'Primary':[24,48,72,96],
    'Secondary':[16,32,48,64],
    'Tertiary':[8,16,24,32]
}
fabrics_metals = {
    'Primary':[12,24,36,48],
    'Secondary':[8,16,24,32],
    'Tertiary':[4,8,12,16]
}
gems_els = {
    'Primary':[6,12,18,24],
    'Secondary':[4,8,12,16],
    'Tertiary':[2,4,6,8]
}

shard = {
    'Primary':[9,18,27,36],
    'Secondary':[6,12,18,24],
    'Tertiary':[3,6,9,12]
}
ember = {
    'Primary':[6,	12,	18,	24],
    'Secondary':[4,8,12,16],
    'Tertiary':[2,4,6,8]
}
soul = {
    'Primary':[3,6,9,12],
    'Secondary':[2,4,6,8],
    'Tertiary':[1,2,3,4]
}

costs = {'PhysicalMaterials':[woods_stones, fabrics_metals, gems_els],
         'SpiritualMaterials':[shard, ember, soul]}



def recipes_type(recipe_type, init, fin, NAME):
    try:
        alpha_recipes = pd.read_excel('source/ALPHA Recipes (2).xlsx',sheet_name=recipe_type, header = 1)
        alpha_recipes0 = pd.read_excel('source/ALPHA Recipes (2).xlsx',sheet_name=recipe_type, header = 0)
        alpha_recipes0 = alpha_recipes0[alpha_recipes0[NAME].str.contains('item|Item') == False]
        alpha_recipes0.rename(columns={'TIER ':'TIER'}, inplace=True)
        cols_names = {}
        for k in range(0,46):
            if 'Unnamed' in alpha_recipes0.columns[k] and 'Unnamed' not in alpha_recipes.columns[k]:
                cols_names[alpha_recipes0.columns[k]]=alpha_recipes.columns[k]
            else:
                if 'Unnamed' in alpha_recipes.columns[k] and 'Unnamed' not in alpha_recipes0.columns[k]:
                    cols_names[alpha_recipes0.columns[k]]=alpha_recipes0.columns[k]
                else:
                    if 'Unnamed' in alpha_recipes.columns[k] and 'Unnamed' in alpha_recipes0.columns[k]:
                        cols_names[alpha_recipes0.columns[k]]=k

        alpha_recipes0.rename(columns=cols_names, inplace=True)
        alpha_recipes0.drop(index=alpha_recipes0.index[0], axis=0, inplace=True)
        print('COLS ----> ', alpha_recipes0.columns[:fin])
        cols = alpha_recipes0.columns[:fin]
        alpha_recipes_f = alpha_recipes0[cols]
        els = list(cols)[init:-1]
        print('ELS ----> ', els)

        alpha_recipes_f['TIER'] = alpha_recipes_f['TIER'].replace('1', 'I').replace(1, 'I').replace(
                                                '2','II').replace('3', 'III').replace(2, 'II').replace(3, 'III')
        for col in els:
            alpha_recipes_f[col] = alpha_recipes_f[col].replace('-', 'None').replace('1', 'Primary').replace('2',
                    'Secondary').replace('3', 'Tertiary').replace(1,'Primary').replace(2, 'Secondary').replace(3,'Tertiary')

        for el in els:
            field = gems_els
            if 'Shard' in el:
                field = shard
            elif 'Ember' in el:
                field = ember
            elif 'Soul' in soul:
                field = soul
            elif el in ['Redwood',
                        'Pine',
                        'Willow',
                        'Olive',
                        'Oak',
                        'Ash',
                        'Holly',
                        'Basalt',
                        'Limestone',
                        'Shale',
                        'Sand',
                        'Granite',
                        'Marble',
                        'Alabaster']:
                field = woods_stones
            elif el in ['Flax', 'Zinc',
                        'Silk', 'Tungsten',
                        'Jute', 'Tin',
                        'Hemp', 'Copper',
                        'Cotton', 'Iron',
                        'Cashmere', 'Aluminum',
                        'Wool', 'Titanium']:
                field = fabrics_metals
            alpha_recipes_f[el] = np.select(
                [
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Primary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Primary'),


                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Secondary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Secondary'),


                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Common') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Uncommon') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'I') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'II') & (
                                alpha_recipes_f[el] == 'Tertiary'),
                    (alpha_recipes_f['RARITY'] == 'Rare') & (alpha_recipes_f['TIER'] == 'III') & (
                                alpha_recipes_f[el] == 'Tertiary')
                ],
                [
                    field['Primary'][0],
                    int(field['Primary'][0] * 1.8),
                    field['Primary'][0] * 2,
                    field['Primary'][1],
                    field['Primary'][2],
                    int(field['Primary'][2] * 1.25),
                    field['Primary'][-1],
                    field['Primary'][-1] * 2,
                    int(field['Primary'][-1] * 2.25),

                    field['Secondary'][0],
                    int(field['Secondary'][0] * 1.8),
                    field['Secondary'][0] * 2,
                    field['Secondary'][1],
                    field['Secondary'][2],
                    int(field['Secondary'][2] * 1.25),
                    field['Secondary'][-1],
                    field['Secondary'][-1] * 2,
                    int(field['Secondary'][-1] * 2.25),

                    field['Tertiary'][0],
                    int(field['Tertiary'][0] * 1.8),
                    field['Tertiary'][0] * 2,
                    field['Tertiary'][1],
                    field['Tertiary'][2],
                    int(field['Tertiary'][2] * 1.25),
                    field['Tertiary'][-1],
                    field['Tertiary'][-1] * 2,
                    int(field['Tertiary'][-1] * 2.25)

                ],
            )

        alpha_recipes_f2 = alpha_recipes_f
        return alpha_recipes_f2, els
    except Exception as e:
        logging.error('Error here ', e)
        return None, []

def totals(alpha_recipes_f2, els):
    try:
        field = {}
        field['Shard'] = []
        field['Ember'] = []
        field['Soul'] = []
        field['w_s'] = []
        field['m_f'] = []
        field['g_e'] = []
        print('ELS IN TOTALS ----> ', els)
        for el in els:
            if 'Shard' in el:
                field['Shard'].append(el)
            elif 'Ember' in el:
                field['Ember'].append(el)
            elif 'Soul' in soul:
                field['Soul'].append(el)
            elif el in ['Redwood',
                      'Pine',
                      'Willow',
                      'Olive',
                      'Oak',
                      'Ash',
                      'Holly',
                      'Basalt',
                      'Limestone',
                      'Shale',
                      'Sand',
                      'Granite',
                      'Marble',
                      'Alabaster']:
                field['w_s'].append(el)
            elif el in ['Flax',	'Zinc',
                    'Silk','Tungsten',
                    'Jute','Tin',
                    'Hemp','Copper',
                    'Cotton','Iron',
                    'Cashmere','Aluminum',
                    'Wool','Titanium']:
                field['m_f'].append(el)
            else:
                field['g_e'].append(el)

        alpha_recipes_f2['Shard_total'] = alpha_recipes_f2[field['Shard']].sum(axis=1)
        alpha_recipes_f2['Ember_total'] = alpha_recipes_f2[field['Ember']].sum(axis=1)
        alpha_recipes_f2['Soul_total'] = alpha_recipes_f2[field['Soul']].sum(axis=1)
        alpha_recipes_f2['WoodsStones_total'] = alpha_recipes_f2[field['w_s']].sum(axis=1)
        alpha_recipes_f2['MetalsFabrics_total'] = alpha_recipes_f2[field['m_f']].sum(axis=1)
        alpha_recipes_f2['GemsElements_total'] = alpha_recipes_f2[field['g_e']].sum(axis=1)

        return alpha_recipes_f2
    except Exception as e:
        logging.error('Error in totals ', e)
        return None

def tiers_plots(df, tier, els, NAME):
    try:
        df1 = df[df['TIER']==tier]
        fig = px.bar(
            df1, x=NAME, y=els,
            hover_data=['RARITY', 'TIER'],labels={"value": "Items"},
            text_auto=True, title=f"Items needed per recipe - TIER {tier}")
        fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    except Exception as e:
        logging.error('Error in tier_plots ', e)
