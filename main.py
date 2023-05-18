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



#CONTROLS
st.sidebar.markdown("## Controls")
alpha_reg = st.checkbox('ALPHA')

multiplier = st.sidebar.slider('Available Extractions on G Node', min_value=1, max_value=100, value=30, step=5)
#epm = st.sidebar.slider('Extractions per minute', min_value=1, max_value=50, value=5, step=1)
gems_nu = st.sidebar.slider('Gems G Nodes used', min_value=1, max_value=50, value=4, step=1)
els_nu = st.sidebar.slider('Elements G Nodes used', min_value=1, max_value=50, value=3, step=1)
met_nu = st.sidebar.slider('Metals G Nodes used', min_value=1, max_value=50, value=2, step=1)
fab_nu = st.sidebar.slider('Fabrics G Nodes used', min_value=1, max_value=50, value=2, step=1)
woods_nu = st.sidebar.slider('Woods G Nodes used', min_value=1, max_value=50, value=2, step=1)
ston_nu = st.sidebar.slider('Stones G Nodes used', min_value=1, max_value=50, value=2, step=1)
#ember_ipm = st.sidebar.slider('Ember - items per minute', min_value=1, max_value=50, value=5, step=1)
#soul_ipm = st.sidebar.slider('Soul - items per minute', min_value=1, max_value=50, value=5, step=1)

st.header(f"1. Gathering Nodes in the Wild")

wdc = read_wild_depositchances(event['SAMPLE_SPREADSHEET_ID'], event['SAMPLE_RANGE_NAME'])
if alpha_reg:
    df1 = wdc[(wdc['Sub-Biome'].isin(['Toadstools',"Frogmaster's Marsh"]))
    or (wdc['Land Type'].isin(['Southern Grasslands','Mountains','Thorn','Northern Grasslands']))]
else:
    df1 = wdc

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
woods_vals = {}
for i in list(df1[type].unique()):
    woods_vals[i] = df1[df1[type]==i][type+' Amount'].sum()

df_woods_vals = pd.DataFrame.from_dict(
            {'Items': list(woods_vals.keys()),
             'GNodesInput': [element_multiplier(type)*multiplier*woods_nu]*len(list(woods_vals.keys()))
             })

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

stone_vals = {}
for i in list(df1[type].unique()):
    stone_vals[i] = df1[df1[type]==i][type+' Amount'].sum()

df_stone_vals = pd.DataFrame.from_dict(
            {'Items': list(stone_vals.keys()),
             'GNodesInput': [element_multiplier(type)*multiplier*ston_nu]*len(list(woods_vals.keys()))
             })

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

gems_vals = {}
for i in list(df1[type].unique()):
    gems_vals[i] = df1[df1[type]==i][type+' Amount'].sum()

df_gems_vals = pd.DataFrame.from_dict(
            {'Items': list(gems_vals.keys()),
             'GNodesInput': [element_multiplier(type)*multiplier*gems_nu]*len(list(woods_vals.keys()))
             })

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
element_vals = {}
for i in list(df1[type].unique()):
    element_vals[i] = df1[df1[type]==i][type+' Amount'].sum()

df_element_vals = pd.DataFrame.from_dict(
            {'Items': list(element_vals.keys()),
             'GNodesInput': [element_multiplier(type)*multiplier*els_nu]*len(list(woods_vals.keys()))
             })

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
Fabrics_vals = {}
for i in list(df1[type].unique()):
    Fabrics_vals[i] = df1[df1[type]==i][type+' Amount'].sum()

df_Fabrics_vals = pd.DataFrame.from_dict(
            {'Items': list(Fabrics_vals.keys()),
             'GNodesInput': [element_multiplier(type)*multiplier*fab_nu]*len(list(woods_vals.keys()))
             })

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
Metals_vals = {}
for i in list(df1[type].unique()):
    Metals_vals[i] = df1[df1[type]==i][type+' Amount'].sum()

df_Metals_vals = pd.DataFrame.from_dict(
            {'Items': list(Metals_vals.keys()),
             'GNodesInput': [element_multiplier(type)*multiplier*met_nu]*len(list(woods_vals.keys()))
             })

frames = [df_stone_vals, df_woods_vals,
          df_Metals_vals, df_Fabrics_vals,
          df_gems_vals, df_element_vals]

result = pd.concat(frames)


print('------------------------------- ENEMIES ENEMIES ENEMIES ---------------------------------------------')
st.header(f"2. ENEMIES")
st.write(f":blue[Spiritual Items dropped by Enemies.] "
         f"Takes the numbers from Founder Enemies "
         f"[link here](https://docs.google.com/spreadsheets/d/1BaMpBSAiMdAUsfel7UweenSSbIwrLra1oScWWOsCNDk/edit?usp=sharing).")


alpha_wild_areas = {'The Hedge Maze':3,
                    'Raptor Peak':3,
                    'The Spore Fens':3,
                    'The Golden Canyon':5,
                    'The Mush':7,
                    'Dead Lake Island':2}



df_e = enemies_files('Founder Enemies')
df = enemies_multipliers(df_e, alpha_wild_areas)
if alpha_reg:
    df_e_f = df_e[df_e['Area'].isin(alpha_wild_areas.keys())]
    df = enemies_multipliers(df_e_f, alpha_wild_areas)
    dict_ = pd.DataFrame.from_dict(
            {'Areas': list(alpha_wild_areas.keys()),
             'Enemies': list(alpha_wild_areas.values())
             })
    st.dataframe(dict_)



gold_unities={'Elite':df[df['Type']=='Elite']['Gold Drop'].sum(),
              'Standard':df[df['Type']=='Standard']['Gold Drop'].sum()}

st.write(f"Gold dropped by enemies in Elite : {gold_unities['Elite']}, Standard : {gold_unities['Standard']}, Elite+Standard: {gold_unities['Elite']+gold_unities['Standard']}")
gold_drop(df, 'Monster', 'Gold Drop')

spiritual_elements = collect_(df)


plot_enem_items(spiritual_elements)



print('-------------------------------------- Recipes Crystals -----------------------------------------------')
st.header(f"3. Recipes Costs")
st.write(f":blue[Recipes costs] "
         f"Takes the numbers from Alpha Crystal Recipes "
         f"[link here](https://docs.google.com/spreadsheets/d/12B1JZbqtY-0UaSpIeCUO28n2R7c17UD3yRieiL4NLRY/edit?usp=sharing).")
recipe = 'AlphaCrystalRecipes'
st.write(f''':blue[{recipe[:5].upper()+' '+recipe[5:12]+' '+recipe[12:]}]''')
df, els = recipes_type(recipe,15, -8, 'CRYSTAL NAME')
df2 = totals(df, els)

tiers_plots(df, 'I', els, "CRYSTAL NAME")
gold_cost(df,'I','CRYSTAL NAME','GOLD COST')
items_summary(df, 'I', els, 'Crystals', spiritual_elements, gold_unities, result)
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)


tiers_plots(df, 'II', els, "CRYSTAL NAME")
gold_cost(df,'II','CRYSTAL NAME','GOLD COST')
items_summary(df, 'II', els, 'Crystals', spiritual_elements, gold_unities, result)
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)


tiers_plots(df, 'III', els, "CRYSTAL NAME")
gold_cost(df,'III','CRYSTAL NAME','GOLD COST')
items_summary(df, 'III', els, 'Crystals', spiritual_elements, gold_unities, result)
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)


print('------------------------------------- Equipment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.write(f''':blue[{recipe}]''')
df, els=recipes_type(recipe, 9, -11, 'NAME')

df2 = totals(df, els)

tiers_plots(df, 'I', els,"NAME")
gold_cost(df,'I','NAME','Gold Cost')
items_summary(df, 'I', els, 'Equipment', spiritual_elements, gold_unities, result)
#time_to_collect(df,'NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)


tiers_plots(df, 'II', els,"NAME")
gold_cost(df,'II','NAME','Gold Cost')
items_summary(df, 'II', els, 'Equipment', spiritual_elements, gold_unities, result)
#time_to_collect(df,'NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)


tiers_plots(df, 'III', els,"NAME")
gold_cost(df,'III','NAME','Gold Cost')
items_summary(df, 'III', els, 'Equipment', spiritual_elements, gold_unities, result)
#time_to_collect(df,'NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)


print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')
recipe = 'BUILDINGS'
st.write(f''':blue[TBD: {recipe} Recipes]''')


#st.header(f"2. DYNAMICS - Items used by Recipes")
# COSTS
