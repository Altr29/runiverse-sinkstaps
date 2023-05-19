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

multiplier = st.sidebar.slider('Available Extractions on G Node', min_value=1, max_value=60, value=30, step=1)
#epm = st.sidebar.slider('Extractions per minute', min_value=1, max_value=50, value=5, step=1)
gems_nu = st.sidebar.slider('Gems G Nodes used', min_value=0, max_value=12, value=3, step=1)
els_nu = st.sidebar.slider('Elements G Nodes used', min_value=0, max_value=12, value=1, step=1)
met_nu = st.sidebar.slider('Metals G Nodes used', min_value=0, max_value=12, value=2, step=1)
fab_nu = st.sidebar.slider('Fabrics G Nodes used', min_value=0, max_value=12, value=2, step=1)
woods_nu = st.sidebar.slider('Woods G Nodes used', min_value=0, max_value=12, value=2, step=1)
ston_nu = st.sidebar.slider('Stones G Nodes used', min_value=0, max_value=12, value=2, step=1)


alpha_reg = st.checkbox('ALPHA Version')
st.header(f":blue[INTRODUCTION: Recipes System as the mechanism to combat inflation in the Runiverse.]")

st.write(f"This dashboard illustrates how the recipes mechanism serves a sink for Runiverse taps (gathering nodes and enemies that drops physical, spiritual and gold). ")
st.write(f":green[Taps] we have for resources creation: on {'ALPHA Version of' if alpha_reg else 'Final Version of'} Runiverse we have a) {'Gathering Nodes' if alpha_reg else 'Plots'} that input physical elements into the world"
         f"and 2) Enemies drops spiritual and Gold.")
st.write(f":green[Sinks:] recipes requires a combination of gold and physical and spiritual materials.")
st.write(f":green[Output:] We show a balance between recipes requirements and resources obtained by gathering nodes usage and encountered enemies. Numbers are shown for ONE player analysis.")

st.write(f"Please check *ALPHA Version* button above. (In other case general conditions for Gathering Nodes will be used for recipes are ALPHA recipes.)")


st.markdown(f"<h1 style='text-align: center; color: red;'>1. Gathering Nodes in the Wild</h1>", unsafe_allow_html=True)

df1 = read_wild_depositchances(alpha_reg, event)

st.write(f":blue[Number of nodes in world, per family type and Sub-Biome.] "
         f"{'ALPHA Numbers were taken from level design document [ALPHA](https://miro.com/app/board/uXjVMIR--ak=/)' if alpha_reg else 'Game Release Version numbers come from [(Wild)EssenceStrengthsandResources](https://docs.google.com/spreadsheets/d/1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo/edit?usp=sharing).'}")


fig = px.bar(df1.sort_values('Sub-Biome'), x="Sub-Biome", y=['WoodsFrecuency', 'GemsFrecuency',
        'FabricsFrecuency', 'MetalsFrecuency', 'StoneFrecuency', 'ElementFrecuency'],
        title=f"Gathering Nodes in the Wild per Item Family and Sub Biome Location")
fig.update_yaxes(tick0=0, dtick=5)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)



type = "Woods"
nodes(type, df1,alpha_reg)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier*element_multiplier(type))
st.write(
    f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: '
    f': Frequency * available extractions per GN (control) * spawned.')
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)

df_woods_vals = pd.DataFrame.from_dict(
            {'Items': [i for i in list(df1[type].unique())],
             'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * element_multiplier(type) * multiplier
                             for i in list(df1[type].unique())]
             })


type = "Stone"
nodes(type, df1,alpha_reg)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier*element_multiplier(type))
st.write(
    f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: '
    f': Frequency * available extractions per GN (control) * spawned.')
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)

df_stone_vals = pd.DataFrame.from_dict(
            {'Items': [i for i in list(df1[type].unique())],
             'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * element_multiplier(type) * multiplier
                             for i in list(df1[type].unique())]
             })



type = "Gems"
nodes(type, df1,alpha_reg)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier*element_multiplier(type))
st.write(
    f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: '
    f': Frequency * available extractions per GN (control) * spawned.')
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)

df_gems_vals = pd.DataFrame.from_dict(
            {'Items': [i for i in list(df1[type].unique())],
             'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * element_multiplier(type) * multiplier
                             for i in list(df1[type].unique())]
             })




type = "Element"
nodes(type, df1,alpha_reg)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier*element_multiplier(type))
st.write(
    f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: '
    f': Frequency * available extractions per GN (control) * spawned.')
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)

df_element_vals = pd.DataFrame.from_dict(
            {'Items': [i for i in list(df1[type].unique())],
             'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * element_multiplier(type) * multiplier
                             for i in list(df1[type].unique())]
             })




type = "Fabrics"
nodes(type, df1,alpha_reg)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier*element_multiplier(type))
st.write(
    f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: '
    f': Frequency * available extractions per GN (control) * spawned.')
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)

df_Fabrics_vals = pd.DataFrame.from_dict(
            {'Items': [i for i in list(df1[type].unique())],
             'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * element_multiplier(type) * multiplier
                             for i in list(df1[type].unique())]
             })




type = "Metals"
nodes(type, df1,alpha_reg)
df1[type+' Amount'] = df1[type+'Frecuency'].apply(lambda x: x*multiplier*element_multiplier(type))
st.write(
    f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. The amount of resources is: '
    f': Frequency * available extractions per GN (control) * spawned.')
agg_d12 = df1.groupby(type, as_index=False).agg(
            {
                type+'Frecuency': ['sum'],
                type+' Amount': ['sum']
            })
st.dataframe(agg_d12)

df_Metals_vals = pd.DataFrame.from_dict(
            {'Items': [i for i in list(df1[type].unique())],
             'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * element_multiplier(type) * multiplier
                             for i in list(df1[type].unique())]
             })



frames = [df_stone_vals, df_woods_vals,
          df_Metals_vals, df_Fabrics_vals,
          df_gems_vals, df_element_vals]

result = pd.concat(frames)


print('------------------------------- ENEMIES ENEMIES ENEMIES ---------------------------------------------')
st.markdown(f"<h1 style='text-align: center; color: red;'>2. Enemies</h1>", unsafe_allow_html=True)
st.write(f":blue[Spiritual Items and Gold are dropped by Enemies.] "
         f"For this section, we take the numbers from Founder Enemies "
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

gold_drop(df, 'Monster', 'Gold Drop')
st.write(f"SUMMARY: Gold dropped by enemies in Elite mode: {gold_unities['Elite']}, Standard mode: {gold_unities['Standard']}, Elite+Standard: {gold_unities['Elite']+gold_unities['Standard']}")

spiritual_elements = collect_(df)
plot_enem_items(spiritual_elements)


print('-------------------------------------- Recipes Crystals -----------------------------------------------')
st.markdown(f"<h1 style='text-align: center; color: red;'>3. Recipes Costs</h1>", unsafe_allow_html=True)

st.write(f":blue[Recipes costs] "
         f"Takes the numbers from Alpha Crystal Recipes "
         f"[link here](https://docs.google.com/spreadsheets/d/12B1JZbqtY-0UaSpIeCUO28n2R7c17UD3yRieiL4NLRY/edit?usp=sharing).")

recipe = 'AlphaCrystalRecipes'
st.header(f"{recipe[:5].upper()+' '+recipe[5:12]+' '+recipe[12:]}")




df, els = recipes_type(recipe,15, -8, 'CRYSTAL NAME')
df2 = totals(df, els)

st.write(f''':level_slider:''')
tiers_plots(df, 'I', els, "CRYSTAL NAME")
gold_cost(df,'I','CRYSTAL NAME','GOLD COST')
items_summary(df, 'I', els, 'Crystals', spiritual_elements, gold_unities, result)
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider:''')
tiers_plots(df, 'II', els, "CRYSTAL NAME")
gold_cost(df,'II','CRYSTAL NAME','GOLD COST')
items_summary(df, 'II', els, 'Crystals', spiritual_elements, gold_unities, result)
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider: :level_slider:''')
tiers_plots(df, 'III', els, "CRYSTAL NAME")
gold_cost(df,'III','CRYSTAL NAME','GOLD COST')
items_summary(df, 'III', els, 'Crystals', spiritual_elements, gold_unities, result)
#time_to_collect(df,'CRYSTAL NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)


print('------------------------------------- Equipment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.header(f"{recipe}")

st.write(f''':gear: :gear: :gear: :gear:''')

df, els=recipes_type(recipe, 9, -11, 'NAME')

df2 = totals(df, els)
st.write(f''':level_slider:''')
tiers_plots(df, 'I', els,"NAME")
gold_cost(df,'I','NAME','Gold Cost')
items_summary(df, 'I', els, 'Equipment', spiritual_elements, gold_unities, result)
#time_to_collect(df,'NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider:''')
tiers_plots(df, 'II', els,"NAME")
gold_cost(df,'II','NAME','Gold Cost')
items_summary(df, 'II', els, 'Equipment', spiritual_elements, gold_unities, result)
#time_to_collect(df,'NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider: :level_slider:''')
tiers_plots(df, 'III', els,"NAME")
gold_cost(df,'III','NAME','Gold Cost')
items_summary(df, 'III', els, 'Equipment', spiritual_elements, gold_unities, result)
#time_to_collect(df,'NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)


print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')
#recipe = 'BUILDINGS'
#st.write(f''':blue[TBD: {recipe} Recipes]''')


