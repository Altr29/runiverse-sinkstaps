import streamlit as st

from source.functions import *
from source.recipes import *


event = {'SAMPLE_RANGE_NAME':'(Wild)EssenceStrengthsandResources',
        'SAMPLE_SPREADSHEET_ID':'1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo',
        'key':'AIzaSyABdVwS2e28_JrMQlwHQxgUlAAkgqbHUqI'}
SAMPLE_SPREADSHEET_ID_input = event['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = event['SAMPLE_RANGE_NAME']

df1 = read_wild_depositchances(event['SAMPLE_SPREADSHEET_ID'], event['SAMPLE_RANGE_NAME'])

#CONTROLS
st.sidebar.markdown("## Controls")
multiplier = st.sidebar.slider('Global Multiplier', min_value=1, max_value=50, value=13, step=1)
epm = st.sidebar.slider('Extractions per minute', min_value=1, max_value=50, value=5, step=1)


st.header(f"Gathering Nodes in the Wild")
st.write(f":blue[Number of nodes in world, per family type and Sub-Biome.]")

nodes("Woods", df1)
nodes("Stone", df1)
nodes("Gems", df1)
nodes("Element", df1)
nodes("Fabrics", df1)
nodes("Metals", df1)

st.write(f":blue[Amount of resources in the wild.]")
df2 = resources(df1, multiplier)

resources_plot("Woods_amount", df2)
resources_plot("Stone_amount", df2)
resources_plot("Gems_amount", df2)
resources_plot("Element_amount", df2)
resources_plot("Fabrics_amount", df2)
resources_plot("Metals_amount", df2)

print('-------------------------------------- Crystals -------------------------------------------------------')
st.header(f"Recipes")
recipe = 'AlphaCrystalRecipes'
st.write(f''':blue[{recipe}]''')
df,els=recipes_type(recipe,15, -8, 'CRYSTAL NAME')
df2 = totals(df, els)
tiers_plots(df, 'I', els, "CRYSTAL NAME")
tiers_plots(df, 'II', els, "CRYSTAL NAME")
tiers_plots(df, 'III', els, "CRYSTAL NAME")

print('------------------------------------- Equiment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.write(f''':blue[{recipe}]''')
df, els=recipes_type(recipe, 9, -11, 'NAME')
df2 = totals(df, els)
tiers_plots(df, 'I', els,"NAME")
tiers_plots(df, 'II', els,"NAME")
tiers_plots(df, 'III', els,"NAME")


print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')

st.header(f"ENEMIES")

# COSTS