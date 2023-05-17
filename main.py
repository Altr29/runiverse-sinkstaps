import streamlit as st

from source.functions import element_multiplier
from source.functions import *
from source.recipes import *
from source.recipes import recipes_type
from source.enemies import *
from source.inputs import gems_list, els_list, stones_list, woods_list, fabrics_list, metals_list, event
import plotly.graph_objects as go




SAMPLE_SPREADSHEET_ID_input = event['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = event['SAMPLE_RANGE_NAME']

df1 = read_wild_depositchances(event['SAMPLE_SPREADSHEET_ID'], event['SAMPLE_RANGE_NAME'])

#CONTROLS
st.sidebar.markdown("## Controls")
multiplier = st.sidebar.slider('Available Extractions on G Node', min_value=1, max_value=50, value=13, step=1)
epm = st.sidebar.slider('Extractions per minute', min_value=1, max_value=50, value=5, step=1)
#shard_ipm = st.sidebar.slider('Shard - items per minute', min_value=1, max_value=50, value=5, step=1)
#ember_ipm = st.sidebar.slider('Ember - items per minute', min_value=1, max_value=50, value=5, step=1)
#soul_ipm = st.sidebar.slider('Soul - items per minute', min_value=1, max_value=50, value=5, step=1)

st.header(f"1. Gathering Nodes in the Wild")
st.write(f":blue[Number of nodes in world, per family type and Sub-Biome.] "
         f"Numbers were taken from level design document [(Wild)EssenceStrengthsandResources](https://docs.google.com/spreadsheets/d/1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo/edit?usp=sharing).")


fig = px.bar(df1.sort_values('Sub-Biome'), x="Sub-Biome", y=['WoodsFrecuency', 'GemsFrecuency',
        'FabricsFrecuency', 'MetalsFrecuency', 'StoneFrecuency', 'ElementFrecuency'],
        title=f"Gathering Nodes in the Wild per Item Family and Sub Biome Location")
fig.update_yaxes(tick0=0, dtick=5)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


type = "Woods"
nodes(type, df1)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier)*df1[type].apply(lambda x: element_multiplier(x))
st.write(f"Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: "
         f"- Frequency * spawned * available extractions per GN (control).")
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)


type = "Stone"
nodes(type, df1)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier)*df1[type].apply(lambda x: element_multiplier(x))
st.write(f"Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: "
         f"- Frequency * spawned * available extractions per GN (control).")
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)


type = "Gems"
nodes(type, df1)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier)*df1[type].apply(lambda x: element_multiplier(x))
st.write(f"Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: "
         f"- Frequency * spawned * available extractions per GN (control).")
gems = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(gems)


type = "Element"
nodes(type, df1)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier)*df1[type].apply(lambda x: element_multiplier(x))
st.write(f"Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: "
         f"- Frequency * spawned * available extractions per GN (control).")
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)


type = "Fabrics"
nodes(type, df1)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier)*df1[type].apply(lambda x: element_multiplier(x))
st.write(f"Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: "
         f"- Frequency * spawned * available extractions per GN (control).")
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)


type = "Metals"
nodes(type, df1)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier)*df1[type].apply(lambda x: element_multiplier(x))
st.write(f"Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: "
         f"- Frequency * spawned * available extractions per GN (control).")
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)


print('------------------------------- ENEMIES ENEMIES ENEMIES ---------------------------------------------')
st.header(f"2. ENEMIES")
st.write(f":blue[Spiritual Items dropped by Enemies.] "
         f"Takes the numbers from [Founder Enemies](https://docs.google.com/spreadsheets/d/1BaMpBSAiMdAUsfel7UweenSSbIwrLra1oScWWOsCNDk/edit?usp=sharing).")
df = enemies_files('Alpha Enemies')
gold_drop(df, 'Monster', 'Gold Drop')
elements = collect_(df)

#st.dataframe(elements)

print('Elements in Enemies')
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
items_summary(df, 'I', els, 'Crystals')
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'II', els, "CRYSTAL NAME")
gold_cost(df,'II','CRYSTAL NAME','GOLD COST')
items_summary(df, 'II', els, 'Crystals')
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'III', els, "CRYSTAL NAME")
gold_cost(df,'III','CRYSTAL NAME','GOLD COST')
items_summary(df, 'III', els, 'Crystals')
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)

print('------------------------------------- Equipment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.write(f''':blue[{recipe}]''')
df, els=recipes_type(recipe, 9, -11, 'NAME')

df2 = totals(df, els)

tiers_plots(df, 'I', els,"NAME")
gold_cost(df,'I','NAME','Gold Cost')
items_summary(df, 'I', els, 'Equipment')
#time_to_collect(df,'NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'II', els,"NAME")
gold_cost(df,'II','NAME','Gold Cost')
items_summary(df, 'II', els, 'Equipment')
#time_to_collect(df,'NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

tiers_plots(df, 'III', els,"NAME")
gold_cost(df,'III','NAME','Gold Cost')
items_summary(df, 'III', els, 'Equipment')
#time_to_collect(df,'NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)

print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')
recipe = 'BUILDINGS'
st.write(f''':blue[TBD: {recipe} Recipes]''')


st.header(f"2. DYNAMICS - Items used by Recipes")
# COSTS
