import streamlit as st

from source.functions import element_multiplier
from source.functions import *
from source.recipes import *
from source.recipes import recipes_type
from source.enemies import *
from source.inputs import gems_list, els_list, stones_list, woods_list, fabrics_list, metals_list, event
import plotly.graph_objects as go
import re
from source.inputs import d_type

SAMPLE_SPREADSHEET_ID_input = event['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = event['SAMPLE_RANGE_NAME']

# CONTROLS
st.sidebar.markdown("## Controls")

multiplier = st.sidebar.slider('Available Extractions on G Node', min_value=1, max_value=60, value=30, step=1)
batt_times = st.sidebar.slider('Number of battles', min_value=1, max_value=10, value=1, step=1)
Area_l = st.sidebar.selectbox('Area of Battle',
                              ('Area 1', 'Area 2', 'Area 3',
                               'Area 4', 'Area 5', 'Area 6'))
# epm = st.sidebar.slider('Extractions per minute', min_value=1, max_value=50, value=5, step=1)
gems_nu = st.sidebar.slider('Gems G Nodes used', min_value=0, max_value=12, value=3, step=1)
els_nu = st.sidebar.slider('Elements G Nodes used', min_value=0, max_value=12, value=1, step=1)
met_nu = st.sidebar.slider('Metals G Nodes used', min_value=0, max_value=12, value=2, step=1)
fab_nu = st.sidebar.slider('Fabrics G Nodes used', min_value=0, max_value=12, value=2, step=1)
woods_nu = st.sidebar.slider('Woods G Nodes used', min_value=0, max_value=12, value=2, step=1)
ston_nu = st.sidebar.slider('Stones G Nodes used', min_value=0, max_value=12, value=2, step=1)

alpha_reg = st.checkbox('ALPHA Version')
st.header(f":blue[INTRODUCTION: Recipes System as the mechanism to combat inflation in the Runiverse.]")

st.write(f"This dashboard illustrates how the recipes mechanism serves as a sink for Runiverse taps "
         f"(gathering nodes and enemies that drops physical, spiritual and gold). ")
st.write(f":green[Taps] we have for resources creation: on {'ALPHA Version of' if alpha_reg else 'Final Version of'} "
         f"Runiverse we have a) {'Gathering Nodes' if alpha_reg else 'Plots'} that input physical elements into the world"
         f"and 2) Enemies drops spiritual and Gold.")
st.write(f":green[Sinks:] recipes requires a combination of gold and physical and spiritual materials.")
st.write(
    f":green[Output:] We show a balance between recipes requirements and resources obtained by gathering nodes usage "
    f"and encountered enemies. Numbers are shown for ONE player analysis.")

st.write(f"Please check *ALPHA Version* button above. (In other case general conditions for Gathering Nodes "
         f"will be used for recipes are ALPHA recipes.)")

st.markdown(f"<h1 style='text-align: center; color: red;'>1. Gathering Nodes in the Wild</h1>", unsafe_allow_html=True)

df1 = read_wild_depositchances(alpha_reg, event)

st.write(f":blue[Number of nodes in world, per family type and Sub-Biome.] "
         f"{'ALPHA Numbers were taken from level design document [ALPHA](https://miro.com/app/board/uXjVMIR--ak=/)' if alpha_reg else 'Game Release Version numbers come from [(Wild)EssenceStrengthsandResources](https://docs.google.com/spreadsheets/d/1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo/edit?usp=sharing).'}")

fig = px.bar(df1.sort_values('Sub-Biome'), x="Sub-Biome", y=['WoodsFrecuency', 'GemsFrecuency',
                                                             'FabricsFrecuency', 'MetalsFrecuency', 'StoneFrecuency',
                                                             'ElementFrecuency'],
             title=f"Gathering Nodes in the Wild per Item Family and Sub Biome Location")
fig.update_yaxes(tick0=0, dtick=5)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def _summ(df1, type, multiplier):
    df1[type + ' Amount'] = df1[type + 'Frecuency'].apply(lambda x: x * multiplier * element_multiplier(type))
    st.write(
        f'Each {type} Gathering Node (Frequency) spawns {element_multiplier(type)} items per extraction. '
        f'The amount of resources follows the formula: Frequency * available extractions per GN (control) * spawned.')
    agg_d12 = df1.groupby(type, as_index=False).agg(
        {
            type + 'Frecuency': ['sum'],
            type + ' Amount': ['sum']
        })
    st.dataframe(agg_d12)


type = "Woods"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)

df_woods_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else woods_nu * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Stone"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)

df_stone_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else ston_nu * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Gems"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_gems_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else gems_nu * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Element"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_element_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else els_nu * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Fabrics"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_Fabrics_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else fab_nu * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Metals"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_Metals_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else met_nu * multiplier
                     for i in list(df1[type].unique())]
     })

frames = [df_stone_vals, df_woods_vals,
          df_Metals_vals, df_Fabrics_vals,
          df_gems_vals, df_element_vals]

result = pd.concat(frames)

print('------------------------------- ENEMIES ENEMIES ENEMIES ---------------------------------------------')
st.markdown(f"<h1 style='text-align: center; color: red;'>2. Battles </h1>", unsafe_allow_html=True)
st.write(f":blue[Spiritual Items dropped by Enemies.] "
         f"For this section, we take the numbers from "
         f"[Battle Drops](https://docs.google.com/spreadsheets/d/1T2sUbs_L4tgRqlHD6aW0EmOGNmHF4PCK158Ac2kokNk/edit#gid=0).")

monsters_dict = {'Area 1': ('Wolf', 'Giant Rat', 'Giant Bat', 'Cockatrice '),
                 'Area 2': ('Giant Ant', 'Giant Wasp', 'Giant Spider', 'Gargantuan Beetle'),
                 'Area 3': ('Zombie', 'Specter', 'Flame Skull', 'Vampyre'),
                 'Area 4': ('Spitting Jelly', 'Exploding Jelly', 'Smoke Jelly',
                            'Parasitic Jelly'),
                 'Area 5': ('Eagle', 'Gunslinger', 'Harpy'),
                 'Area 6': ('Chemist ', 'Enforcer', 'Gunpowder Banshee')}

Monster_l = st.selectbox(
    'Monster choice',
    monsters_dict[Area_l])

st.write('You chose to battle ', batt_times, 'times on', Area_l, ' Against ', Monster_l)

battles_ofile = pd.read_excel('source/ALPHA wild resources (1).xlsx', sheet_name='Battles', header=0)
battles_ofile.fillna(method='ffill', inplace=True)

a1 = battles_ofile[(battles_ofile['MONSTER'].str.contains(str(Monster_l)) == True) &
                   (battles_ofile['AREA'].str.contains(str(Area_l)) == True)]

# st.dataframe(a1)

battles_all = []


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


bats = []
if batt_times >= 10:
    bats = [a1.iat[0, -1]]
else:
    for i in range(0, batt_times):
        bats.append(a1.iat[0, i + 2])

battles_d = {}
bat_oorder = {}
bats1 = [x for x in bats if "No Drop" not in x]

# st.write('Battles: ', len(bats1))
if len(bats1) < 1:
    st.write('No enemies to enconter')
else:
    for s in bats1:
        # st.write('first enemy ', s)
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

# st.dataframe(spiritual_elements)

plot_enem_items(spiritual_elements)

# spiritual_elements = collect_(df)
# plot_enem_items(spiritual_elements)


print('-------------------------------------- Recipes Crystals -----------------------------------------------')
st.markdown(f"<h1 style='text-align: center; color: red;'>3. Recipes Costs</h1>", unsafe_allow_html=True)

st.write(f":blue[Recipes costs] "
         f"Takes the numbers from Alpha Crystal Recipes "
         f"[link here](https://docs.google.com/spreadsheets/d/12B1JZbqtY-0UaSpIeCUO28n2R7c17UD3yRieiL4NLRY/edit?usp=sharing).")

recipe = 'AlphaCrystalRecipes'
st.header(f"{recipe[:5].upper() + ' ' + recipe[5:12] + ' ' + recipe[12:]}")

df, els = recipes_type(recipe, 15, -8, 'CRYSTAL NAME')
df2 = totals(df, els)

st.write(f''':level_slider:''')
tiers_plots(df, 'I', els, "CRYSTAL NAME")
# gold_cost(df, 'I', 'CRYSTAL NAME', 'GOLD COST')
items_summary(df, 'I', els, 'Crystals', spiritual_elements, result)
# time_to_collect(df,'CRYSTAL NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider:''')
tiers_plots(df, 'II', els, "CRYSTAL NAME")
# gold_cost(df,'II','CRYSTAL NAME','GOLD COST')
items_summary(df, 'II', els, 'Crystals', spiritual_elements, result)
# time_to_collect(df,'CRYSTAL NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider: :level_slider:''')
tiers_plots(df, 'III', els, "CRYSTAL NAME")
# gold_cost(df,'III','CRYSTAL NAME','GOLD COST')
items_summary(df, 'III', els, 'Crystals', spiritual_elements, result)
# time_to_collect(df,'CRYSTAL NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)


print('------------------------------------- Equipment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.header(f"{recipe}")

st.write(f''':gear: :gear: :gear: :gear:''')

df, els = recipes_type(recipe, 9, -11, 'NAME')

df2 = totals(df, els)
st.write(f''':level_slider:''')
tiers_plots(df, 'I', els, "NAME")
# gold_cost(df,'I','NAME','Gold Cost')
items_summary(df, 'I', els, 'Equipment', spiritual_elements, result)
# time_to_collect(df,'NAME', epm, els, 'I', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider:''')
tiers_plots(df, 'II', els, "NAME")
# gold_cost(df,'II','NAME','Gold Cost')
items_summary(df, 'II', els, 'Equipment', spiritual_elements, result)
# time_to_collect(df,'NAME', epm, els, 'II', shard_ipm, ember_ipm, soul_ipm)

st.write(f''':level_slider: :level_slider: :level_slider:''')
tiers_plots(df, 'III', els, "NAME")
# gold_cost(df,'III','NAME','Gold Cost')
items_summary(df, 'III', els, 'Equipment', spiritual_elements, result)
# time_to_collect(df,'NAME', epm, els, 'III', shard_ipm, ember_ipm, soul_ipm)


print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')
# recipe = 'BUILDINGS'
# st.write(f''':blue[TBD: {recipe} Recipes]''')
