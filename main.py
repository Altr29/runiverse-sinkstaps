import streamlit as st

from source.functions import *
from source.recipes import *
from source.recipes import recipes_type
from source.enemies import *
from source.inputs import gems_list, els_list, stones_list, woods_list, fabrics_list, metals_list

event = {'SAMPLE_RANGE_NAME':'(Wild)EssenceStrengthsandResources',
        'SAMPLE_SPREADSHEET_ID':'1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo',
        'key':'AIzaSyABdVwS2e28_JrMQlwHQxgUlAAkgqbHUqI'}

SAMPLE_SPREADSHEET_ID_input = event['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = event['SAMPLE_RANGE_NAME']

df1 = read_wild_depositchances(event['SAMPLE_SPREADSHEET_ID'], event['SAMPLE_RANGE_NAME'])

#CONTROLS
st.sidebar.markdown("## Controls")
multiplier = st.sidebar.slider('Available Extractions on G Node', min_value=1, max_value=50, value=13, step=1)
epm = st.sidebar.slider('Extractions per minute', min_value=1, max_value=50, value=5, step=1)
shard_ipm = st.sidebar.slider('Shard - items per minute', min_value=1, max_value=50, value=5, step=1)
ember_ipm = st.sidebar.slider('Ember - items per minute', min_value=1, max_value=50, value=5, step=1)
soul_ipm = st.sidebar.slider('Soul - items per minute', min_value=1, max_value=50, value=5, step=1)

st.header(f"1. Gathering Nodes in the Wild")
st.write(f":blue[Number of nodes in world, per family type and Sub-Biome.] "
         f"Numbers were taken from level design document [(Wild)EssenceStrengthsandResources](https://docs.google.com/spreadsheets/d/1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo/edit?usp=sharing).")

print('---<>>>>>>', df1.columns[0:])


fig = px.bar(df1.sort_values('Sub-Biome'), x="Sub-Biome", y=['WoodsFrecuency', 'GemsFrecuency',
        'FabricsFrecuency', 'MetalsFrecuency', 'StoneFrecuency', 'ElementFrecuency'],
        title=f"Gathering Nodes in the Wild per Item Family and Sub Biome Location")
fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


type = "Woods"
nodes(type, df1)
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum']
            })
st.dataframe(agg_d12)

type = "Stone"
nodes(type, df1)
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum']
            })
st.dataframe(agg_d12)

type = "Gems"
nodes(type, df1)
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum']
            })
st.dataframe(agg_d12)

type = "Element"
nodes(type, df1)
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum']
            })
st.dataframe(agg_d12)

type = "Fabrics"
nodes(type, df1)
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum']
            })
st.dataframe(agg_d12)

type = "Metals"
nodes(type, df1)
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum']
            })
st.dataframe(agg_d12)


st.write(f":blue[Amount of resources in the wild.] Takes the nodes existence, the Available Extractions on G Node as a global multiplier, and the items proportion (1:3:5, Gems and Elements : Metals and Fabrics: Woods Stones)")
df2 = resources(df1, multiplier)

resources_plot("Woods_amount", df2)
resources_plot("Stone_amount", df2)
resources_plot("Gems_amount", df2)
resources_plot("Element_amount", df2)
resources_plot("Fabrics_amount", df2)
resources_plot("Metals_amount", df2)

print('------------------------------- ENEMIES ENEMIES ENEMIES ---------------------------------------------')
st.header(f"2. ENEMIES")
st.write(f":blue[Spiritual Items dropped by Enemies.] "
         f"Takes the numbers from [Founder Enemies](https://docs.google.com/spreadsheets/d/1BaMpBSAiMdAUsfel7UweenSSbIwrLra1oScWWOsCNDk/edit?usp=sharing).")
df = enemies_files('Alpha Enemies')
gold_drop(df, 'Monster', 'Gold Drop')
elements = collect_(df)
plot_enem_items(elements)



print('-------------------------------------- Recipes Crystals -----------------------------------------------')
st.header(f"3. Recipes Costs")
st.write(f":blue[Spiritual Items dropped by Enemies] "
         f"Takes the numbers from [Founder Enemies](https://docs.google.com/spreadsheets/d/12B1JZbqtY-0UaSpIeCUO28n2R7c17UD3yRieiL4NLRY/edit?usp=sharing).")
recipe = 'AlphaCrystalRecipes'
st.write(f''':blue[{recipe[:5].upper()+' '+recipe[5:12]+' '+recipe[12:]}]''')
df, els = recipes_type(recipe,15, -8, 'CRYSTAL NAME')
df2 = totals(df, els)
tiers_plots(df, 'I', els, "CRYSTAL NAME")
gold_cost(df,'I','CRYSTAL NAME','GOLD COST')
time_to_collect(df,'CRYSTAL NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'II', els, "CRYSTAL NAME")
gold_cost(df,'II','CRYSTAL NAME','GOLD COST')
time_to_collect(df,'CRYSTAL NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'III', els, "CRYSTAL NAME")
gold_cost(df,'III','CRYSTAL NAME','GOLD COST')
time_to_collect(df,'CRYSTAL NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)

print('------------------------------------- Equipment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.write(f''':blue[{recipe}]''')
df, els=recipes_type(recipe, 9, -11, 'NAME')
df2 = totals(df, els)

tiers_plots(df, 'I', els,"NAME")
gold_cost(df,'I','NAME','Gold Cost')
time_to_collect(df,'NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'II', els,"NAME")
gold_cost(df,'II','NAME','Gold Cost')
time_to_collect(df,'NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'III', els,"NAME")
gold_cost(df,'III','NAME','Gold Cost')
time_to_collect(df,'NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)

print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')
recipe = 'BUILDINGS'
st.write(f''':blue[{recipe} TBD]''')


st.header(f"2. DYNAMICS - Items used by Recipes")
# COSTS
