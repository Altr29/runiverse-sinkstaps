from source.recipes import recipes_type
from source.recipes import *
from source.enemies import __battles_nedeed, fun_enemy
from source.enemies import *
from source.inputs import event
from source.between_areas import resources_between_areas



SAMPLE_SPREADSHEET_ID_input = event['SAMPLE_SPREADSHEET_ID']
SAMPLE_RANGE_NAME = event['SAMPLE_RANGE_NAME']

# CONTROLS
st.sidebar.markdown("## Controls")

multiplier = st.sidebar.slider('Available Extractions on G Node', min_value=1, max_value=60, value=30, step=1)
batt_times = st.sidebar.slider('Number of battles', min_value=1, max_value=10, value=1, step=1)
Area_l = st.sidebar.selectbox('Area of Battle',
                              ('Area 1', 'Area 2', 'Area 3',
                               'Area 4', 'Area 5', 'Area 6'))


alpha_reg = st.checkbox('ALPHA Version')
st.header(f":blue[INTRODUCTION: Recipes System as the mechanism to combat inflation in the Runiverse.]")

st.write(f"This dashboard illustrates how the recipes mechanism serves as a sink for Runiverse taps "
         f"(gathering nodes and enemies that drops physical, spiritual and gold). ")
st.write(f":green[Taps] we have for resources creation: on {'ALPHA Version of' if alpha_reg else 'Final Version of'} "
         f"Runiverse we have a) {'Gathering Nodes' if alpha_reg else 'Plots'} that input physical elements into the "
         f"world "
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
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else 1 * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Stone"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)

df_stone_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else 1 * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Gems"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_gems_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else 1 * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Element"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_element_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else 1 * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Fabrics"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_Fabrics_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else 1 * multiplier
                     for i in list(df1[type].unique())]
     })

type = "Metals"
nodes(type, df1, alpha_reg)
_summ(df1, type, multiplier)
df_Metals_vals = pd.DataFrame.from_dict(
    {'Items': [i for i in list(df1[type].unique())],
     'GNodesInput': [0 if df1[df1[type] == i][type + 'Frecuency'].sum() <= 0 else 1 * multiplier
                     for i in list(df1[type].unique())]
     })

frames = [df_stone_vals, df_woods_vals,
          df_Metals_vals, df_Fabrics_vals,
          df_gems_vals, df_element_vals]

result = pd.concat(frames)

print('------------------------------- ENEMIES ENEMIES ENEMIES ---------------------------------------------')
st.markdown(f"<h1 style='text-align: center; color: red;'>2. Battles </h1>", unsafe_allow_html=True)
st.write(f":blue[Spiritual Items dropped by Enemies.] "
         f"For this section, we take the numbers on battles from "
         f"[Battle Drops](https://docs.google.com/spreadsheets/d/1T2sUbs_L4tgRqlHD6aW0EmOGNmHF4PCK158Ac2kokNk/edit#gid=0).")

monsters_dict = {'Area 1': ('Wolf', 'Giant Rat', 'Giant Bat', 'Cockatrice '),
                 'Area 2': ('Giant Ant', 'Giant Wasp', 'Giant Spider', 'Gargantuan Beetle'),
                 'Area 3': ('Zombie', 'Specter', 'Flame Skull', 'Vampyre'),
                 'Area 4': ('Spitting Jelly', 'Exploding Jelly', 'Smoke Jelly',
                            'Parasitic Jelly'),
                 'Area 5': ('Eagle', 'Gunslinger', 'Harpy'),
                 'Area 6': ('Chemist ', 'Enforcer', 'Gunpowder Banshee')}

st.write(f"You chose to battle :green[{batt_times} times] on :green[{Area_l}.]")


battles_ofile = pd.read_excel('source/ALPHA wild resources (1).xlsx', sheet_name='Battles', header=0)
battles_ofile.fillna(method='ffill', inplace=True)

for Monster in monsters_dict[Area_l]:
    #print('---> ',Monster)
    df_btt = fun_enemy(battles_ofile, Monster, Area_l, batt_times)
    spiritual_elements = pd.DataFrame.from_dict(
        {'Items': list(df_btt.keys()),
         'Amount': list(df_btt.values()),
         'Type': [d_type(i) for i in list(df_btt.keys())]})

    st.write(f":green[Against {Monster}]")
    plot_enem_items(spiritual_elements)


#'-------------------------------------- FUNCTIONS -----------------------------------------------'


def df_spiritual_items(count_sp, batt):
    dictio = {
        'Items': [],
        'Area 1': [],
        'Area 2': [],
        'Area 3': [],
        'Area 4': [],
        'Area 5': [],
        'Area 6': []}

    k=0
    for key in count_sp.keys():
        if batt[key] == {}:
            pass
        else:
            dictio['Items'].append(key)
            dictio['Area 1'].append('')
            dictio['Area 2'].append('')
            dictio['Area 3'].append('')
            dictio['Area 4'].append('')
            dictio['Area 5'].append('')
            dictio['Area 6'].append('')

            for v in batt[key]:
                n1=4
                if 'Area 5' in v or 'Area 6' in v:
                    n1=3
                dictio[str(v)][k] = "{:.2f}".format(sum(batt[key][v].values())/n1)
                #dictio[str(v)][k] = batt[key][v].values()
            k+=1

    return dictio

def ___counting(resources_between_areas, count_sp, comp_keys):
    try:
        Battles = 99
        items_f = []
        items_f_2 = []
        for key, value in resources_between_areas.items():
            res = all(value.get(k) >= count_sp.get(k) for k in comp_keys)
            if res:
                Battles = key
                break
            else:
                pass

        if Battles>10:
            try:
                for key, value in resources_between_areas.items():
                    for k in comp_keys:
                        if value.get(k) < count_sp.get(k):
                            if k not in items_f:
                                if count_sp.get(k)-resources_between_areas[10][k]>0:
                                    items_f.append(k)

                                    items_f_2.append((k, resources_between_areas[10][k],
                                                      count_sp.get(k)-resources_between_areas[10][k]))
            except:
                items_f_2=[]

        return Battles, items_f_2

    except Exception as e:
        logging.error('Exception in __counting ',e)
        return -99, []

def conclusion_among_areas(a,b):
    try:
        excluded = ['Jiggly Shard', 'Jiggly Ember', 'Siphoning Soul', 'Harpy Soul','Siphoning Soul','Vampyre Soul',
                    'Cannon Soul','Chittering Ember']
        n_battles, items = ___counting(a,b, [k for k in count_sp.keys() if k not in excluded])
        if n_battles>10 or n_battles<0:
            st.write(f":red[No battles are enough to complete this recipe!!] "
                     f"{f'''We have those in 10 battles among areas (item, in 10 battles, needed): {items}''' if len(items)>0 else ''}.")
        else:
            st.write(
                    f'Get :green[{n_battles} times into battles (vs each enemies) per Area] '
                    f'are required to complete this recipe. '
                    f''
                f'* Excluded {excluded}.')

    except Exception as e:
        logging.error('Error ', e)
        pass

print('-------------------------------------- Recipes Crystals -----------------------------------------------')
st.markdown(f"<h1 style='text-align: center; color: red;'>3. Recipes Costs</h1>", unsafe_allow_html=True)

st.write(f":blue[Recipes costs] "
         f"Takes the numbers from Alpha Crystal Recipes "
         f"[link here](https://docs.google.com/spreadsheets/d/12B1JZbqtY-0UaSpIeCUO28n2R7c17UD3yRieiL4NLRY/edit?usp=sharing).")

recipe = 'AlphaCrystalRecipes'
st.header(f"{recipe[:5].upper() + ' ' + recipe[5:12] + ' ' + recipe[12:]}")

df1, els = recipes_type(recipe, 15, -8, 'CRYSTAL NAME')
df2 = totals(df1, els)

recipe_rarity = st.selectbox('Recipe rarity ', ['Common', 'Uncommon', 'Rare', 'ALL'])

if 'ALL' in recipe_rarity:
    df = df1
else:
    df = df1[df1['RARITY'] == recipe_rarity]

tier = 'I'
st.write(f''':level_slider: TIER {tier}''')
tiers_plots(df, tier, els, "CRYSTAL NAME")
count_fis, count_sp = required_items(df, tier, els, "CRYSTAL NAME")
batt = __battles_nedeed(count_sp, monsters_dict, battles_ofile)
df_summ_si = df_spiritual_items(count_sp, batt)
items_summary(count_fis, count_sp, df_summ_si, tier, 'Crystals', recipe_rarity)
conclusion_among_areas(resources_between_areas, count_sp)
gold_cost(df, tier, 'CRYSTAL NAME', 'GOLD COST')


tier = 'II'
st.write(f''':level_slider: TIER {tier}''')
tiers_plots(df, tier, els, "CRYSTAL NAME")
count_fis, count_sp = required_items(df, tier, els, "CRYSTAL NAME")
batt = __battles_nedeed(count_sp, monsters_dict, battles_ofile)
df_summ_si = df_spiritual_items(count_sp, batt)
items_summary(count_fis, count_sp, df_summ_si, tier, 'Crystals', recipe_rarity)
conclusion_among_areas(resources_between_areas, count_sp)

gold_cost(df, tier, 'CRYSTAL NAME', 'GOLD COST')



tier = 'III'
st.write(f''':level_slider: TIER {tier}''')
tiers_plots(df, tier, els, "CRYSTAL NAME")
count_fis, count_sp = required_items(df, tier, els, "CRYSTAL NAME")
batt = __battles_nedeed(count_sp, monsters_dict, battles_ofile)
df_summ_si = df_spiritual_items(count_sp, batt)
items_summary(count_fis, count_sp, df_summ_si, tier, 'Crystals', recipe_rarity)
conclusion_among_areas(resources_between_areas, count_sp)

gold_cost(df, tier, 'CRYSTAL NAME', 'GOLD COST')


print('------------------------------------- Equipment ---------------------------------------------------------')
recipe = 'ALPHA Equiment Recipes'
st.header(f"{recipe}")
st.write(f''':gear: :gear: :gear: :gear:''')
df, els = recipes_type(recipe, 9, -11, 'NAME')
df2 = totals(df, els)



tier = 'I'
st.write(f''':level_slider: TIER {tier}''')
tiers_plots(df, tier, els, "NAME")
count_fis, count_sp = required_items(df, tier, els, "NAME")
batt = __battles_nedeed(count_sp, monsters_dict, battles_ofile)
df_summ_si = df_spiritual_items(count_sp, batt)
items_summary(count_fis, count_sp, df_summ_si, tier, 'Equipment', recipe_rarity)
conclusion_among_areas(resources_between_areas, count_sp)

gold_cost(df, tier, 'NAME', 'Gold Cost')



tier = 'II'
st.write(f''':level_slider: TIER {tier}''')
tiers_plots(df, tier, els, "NAME")
count_fis, count_sp = required_items(df, tier, els, "NAME")
batt = __battles_nedeed(count_sp, monsters_dict, battles_ofile)
df_summ_si = df_spiritual_items(count_sp, batt)
items_summary(count_fis, count_sp, df_summ_si, tier, 'Equipment', recipe_rarity)
conclusion_among_areas(resources_between_areas, count_sp)

gold_cost(df, tier, 'NAME', 'Gold Cost')




tier = 'III'
st.write(f''':level_slider: TIER {tier}''')
tiers_plots(df, tier, els, "NAME")
count_fis, count_sp = required_items(df, tier, els, "NAME")
batt = __battles_nedeed(count_sp, monsters_dict, battles_ofile)
df_summ_si = df_spiritual_items(count_sp, batt)
items_summary(count_fis, count_sp, df_summ_si, tier, 'Equipment', recipe_rarity)
conclusion_among_areas(resources_between_areas, count_sp)

gold_cost(df, tier, 'NAME', 'Gold Cost')

print('-------------------------------------BUILDINGS TBD-------------------------------------------------------')
# recipe = 'BUILDINGS'
# st.write(f''':blue[TBD: {recipe} Recipes]''')
