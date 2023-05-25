from source.inputs import d_type
from source.functions import *
import re


def enemies_files(sheet):
    enemies0 = pd.read_excel('source/Alpha Enemies.xlsx', sheet_name=sheet)

    try:
        enemies0.rename(columns={'                                                                 Monster':
                                     'Monster'}, inplace=True)

        df = enemies0[enemies0.columns].astype({'Quantity Min / Max': 'string',
                                                'Quantity Min / Max.1': 'string',
                                                'Quantity Min / Max.2': 'string',
                                                'Quantity Min / Max.3': 'string',
                                                'Quantity Min / Max.4': 'string'})
        df = df[df['Monster'].str.contains('Area') == False]

        for el in ['Quantity Min / Max', 'Quantity Min / Max.1', 'Quantity Min / Max.2', 'Quantity Min / Max.3',
                   'Quantity Min / Max.4', 'Gold Drop']:
            df[el] = df[el].replace(np.nan, '0').replace('-', '0')
            df[el] = df[el].apply(lambda x: int(str(x)[8:10]) if len(str(x)) > 8 else int(x))
        return df

    except Exception as e:
        logging.error('Error in enemies_files ', e)


def enemies_multipliers(df, multipliers):
    df['Quantity Min / Max'] = df['Area'].apply(lambda x: int(multipliers[x]) if x in multipliers.keys() else 1
                                                ) * df['Quantity Min / Max'].apply(lambda x: x)
    df['Quantity Min / Max.1'] = df['Area'].apply(lambda x: int(multipliers[x]) if x in multipliers.keys() else 1
                                                  ) * df['Quantity Min / Max.1'].apply(lambda x: x)
    df['Quantity Min / Max.2'] = df['Area'].apply(lambda x: int(multipliers[x]) if x in multipliers.keys() else 1
                                                  ) * df['Quantity Min / Max.2'].apply(lambda x: x)
    df['Quantity Min / Max.3'] = df['Area'].apply(lambda x: int(multipliers[x]) if x in multipliers.keys() else 1
                                                  ) * df['Quantity Min / Max.3'].apply(lambda x: x)
    df['Gold Drop'] = df['Area'].apply(lambda x: int(multipliers[x]) if x in multipliers.keys() else 1
                                       ) * df['Gold Drop'].apply(lambda x: x)
    return df


def gold_drop(df, NAME, title):
    try:
        fig = px.bar(
            df.sort_values(NAME), x=NAME, y=title,
            hover_data=['Type', 'Area', 'Sprite'], labels={"Gold Drop": "Gold unities"}, color='Type',
            text_auto=True, title=f"Gold Dropped by Enemies")
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    except Exception as e:
        logging.error('Error in gold_drop ', e)


def collect_(df):
    try:
        monsters = {}
        for i, j in df.iterrows():
            if '-' in df.loc[i, 'Material Drop 1']:
                monsters[df.loc[i, 'Monster']] = {
                    df.loc[i, 'Material Drop 2']: df.loc[i, 'Quantity Min / Max.1'],
                    df.loc[i, 'Material Drop 3 ']: df.loc[i, 'Quantity Min / Max.2'],
                    df.loc[i, 'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3'],
                    df.loc[i, 'Crystal Recipe Drop']: df.loc[i, 'Quantity Min / Max.4']}
            elif '-' in df.loc[i, 'Material Drop 2']:
                monsters[df.loc[i, 'Monster']] = {
                    df.loc[i, 'Material Drop 1']: df.loc[i, 'Quantity Min / Max'],
                    df.loc[i, 'Material Drop 3 ']: df.loc[i, 'Quantity Min / Max.2'],
                    df.loc[i, 'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3'],
                    df.loc[i, 'Crystal Recipe Drop']: df.loc[i, 'Quantity Min / Max.4']}
            elif '-' in df.loc[i, 'Material Drop 3 ']:
                monsters[df.loc[i, 'Monster']] = {
                    df.loc[i, 'Material Drop 1']: df.loc[i, 'Quantity Min / Max'],
                    df.loc[i, 'Material Drop 2']: df.loc[i, 'Quantity Min / Max.1'],
                    df.loc[i, 'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3'],
                    df.loc[i, 'Crystal Recipe Drop']: df.loc[i, 'Quantity Min / Max.4']}
            elif '-' in df.loc[i, 'Recipe Drop']:
                monsters[df.loc[i, 'Monster']] = {
                    df.loc[i, 'Material Drop 1']: df.loc[i, 'Quantity Min / Max'],
                    df.loc[i, 'Material Drop 2']: df.loc[i, 'Quantity Min / Max.1'],
                    df.loc[i, 'Material Drop 3 ']: df.loc[i, 'Quantity Min / Max.2'],
                    df.loc[i, 'Crystal Recipe Drop']: df.loc[i, 'Quantity Min / Max.4']}
            elif '-' in df.loc[i, 'Crystal Recipe Drop']:
                monsters[df.loc[i, 'Monster']] = {
                    df.loc[i, 'Material Drop 1']: df.loc[i, 'Quantity Min / Max'],
                    df.loc[i, 'Material Drop 2']: df.loc[i, 'Quantity Min / Max.1'],
                    df.loc[i, 'Material Drop 3 ']: df.loc[i, 'Quantity Min / Max.2'],
                    df.loc[i, 'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3']}
            else:
                monsters[df.loc[i, 'Monster']] = {
                    df.loc[i, 'Material Drop 1']: df.loc[i, 'Quantity Min / Max'],
                    df.loc[i, 'Material Drop 2']: df.loc[i, 'Quantity Min / Max.1'],
                    df.loc[i, 'Material Drop 3 ']: df.loc[i, 'Quantity Min / Max.2'],
                    df.loc[i, 'Recipe Drop']: df.loc[i, 'Quantity Min / Max.3'],
                    df.loc[i, 'Crystal Recipe Drop']: df.loc[i, 'Quantity Min / Max.4']}

        elements = {}
        for key, value in monsters.items():
            for i, j in value.items():
                i = i.replace('(Rare)', '')
                if i == '-':
                    pass
                else:
                    if j == '-':
                        j = 0
                    if i not in elements.keys():
                        elements[str(i)] = j
                    else:
                        elements[str(i)] += j

        new = pd.DataFrame.from_dict(
            {'Items': list(elements.keys()),
             'Amount': list(elements.values()),
             'Type': [d_type(i) for i in list(elements.keys())]})

        return new

    except Exception as e:
        logging.error('Error in _collection >>> ', e)
        return None


def fun_enemy(df, Monster, Area_l, batt_times):
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

    return bat_oorder


def plot_enem_items(new):
    try:
        fig = px.bar(new, x='Items', y='Amount', color='Type', text_auto=True,
                     title=f"Spiritual Items Dropped by Enemies")
        fig.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    except Exception as e:
        logging.error('Error in plot_enem_items >>> ', e)


def __filt(__dict):
    try:
        for k, v in __dict.items():
            for i in range(1, 7):
                if v['Area ' + str(i)] == {}:
                    __dict[k].pop('Area ' + str(i))
        if __dict:
            return __dict
        else:
            return {}
    except Exception as e:
        logging.error('Here in __filt ', e)
        return {}


def __battles_nedeed(needed, monsters_dict, enemies_df):
    enough = {}
    for el in needed.keys():
        enough[el] = {}
        print(f"=================> {el} <=================")

        for Area_l in monsters_dict.keys():
            enough[el][Area_l] = {}
            for batt_times in range(1, 11):

                for Monster in monsters_dict[Area_l]:
                    #print(f"******* {Area_l}: {batt_times} battles against {Monster} *******")
                    df_btt = fun_enemy(enemies_df, Monster, Area_l, batt_times)
                    if el in df_btt.keys():
                        if needed[el] <= df_btt[el]:
                            if Monster in enough[el].keys():
                                if batt_times <= enough[el][Area_l][Monster]:
                                    enough[el][Area_l][Monster] = batt_times
                                else:
                                    pass
                            else:
                                enough[el][Area_l][Monster] = batt_times
                            #print(f">>>> Battle {batt_times} against Monster is OK")
                        else:
                            if batt_times > 9:
                                pass
                                # print('Not enough drops of this element even when all battles were used')
                            else:
                                pass
                                #print(f"Need more than {batt_times} battles agains {Monster}")
                    else:
                        pass
                        #print(f"No Feral Shard in {batt_times} battles agains {Monster}")
            #print('HERE in ',Monster,'--->',enough)

        print(enough)

    enou2 = __filt(enough)
    print('HERE in ', enough, '--->', enou2)

    return enou2
