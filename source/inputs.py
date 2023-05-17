from difflib import SequenceMatcher

woods_list = ['Redwood',
                        'Pine',
                        'Willow',
                        'Olive',
                        'Oak',
                        'Ash',
                        'Holly']

stones_list = ['Basalt',
                        'Limestone',
                        'Shale',
                        'Sand',
                        'Granite',
                        'Marble',
                        'Alabaster']

fabrics_list = ['Flax',
                        'Silk',
                        'Jute',
                        'Hemp',
                        'Cotton',
                        'Cashmere',
                        'Wool']

metals_list = ['Titanium','Aluminum','Iron','Tungsten','Tin','Copper','Zinc']

gems_list = ['Ruby',
                'Sapphire',
                'Emerald',
                'Topaz',
                'Smoky Quartz',
                'Amethyst',
                'Diamond']

els_list = ['Sulfur',
                 'Hydrogen',
                 'Carbon',
                 'Nitrogen',
                 'Calcium',
                 'Silicon',
                 'Antimony']

event = {'SAMPLE_RANGE_NAME':'(Wild)EssenceStrengthsandResources',
        'SAMPLE_SPREADSHEET_ID':'1l_V71izAjkLguKZuaj43sGEYR-2bpSLxHFi7ORCcTWo',
        'key':'AIzaSyABdVwS2e28_JrMQlwHQxgUlAAkgqbHUqI'}

CrystalsRecipes = ['Call of the Ancient Flame',
                'Drawing of Chaos',
                'The Nature of Growth',
                'Juvenile Festivities',
                'Price of Inadequacy',
                'A Giving Nature',
                'Reckless Abandon',
                'Condensed Volatility',
                'Memory of the Peaks',
                'Deeper than Sound',
                'Contemplation of Destiny',
                "The Workers' Rest"]

ERecipes = ["Pilgrim's Staff",
                "Nature's Gift",
                "Ol' Trusty",
                "Butcher's Friend",
                "Joybringer",
                "Devouring Scythe",
                "Witch's Hat",
                "Comfy Hood",
                "Circlet of the Bold",
                "Corsair Bandana",
                "Tactician's Helm",
                "Nightseeker",
                "Witch's Robes",
                "Comfy Robes",
                "Bold Straps",
                "Corsair Apparel",
                "Tactician's Armor",
                "Nightwalker"]

def similar(a, els):
    """
    :param a: variable to compare
    :param b: variable to compare with a
    :return: a probability value of similitude
    """
    resp = False
    for el in els:
        if SequenceMatcher(None, a, el).ratio()>.9:
            resp = True
            break
        else:
            pass
    return resp


def d_type(el):
    dt = 'Recipes: '
    if 'Soul' in el:
        dt = 'Soul'
    elif 'Ember' in el:
        dt = 'Ember'
    elif 'Shard' in el:
        dt = 'Shard'
    elif el in woods_list+stones_list:
        dt = 'WoodsStones'
    elif el in gems_list+els_list:
        dt = 'GemsEls'
    elif el in metals_list+fabrics_list:
        dt = 'MetalsFabrics'
    elif 'GOLD' in el or 'Gold' in el:
        dt = ''
    else:
        if el in CrystalsRecipes or similar(el, CrystalsRecipes):
            dt = 'Recipes: Crystals'

        if el in ERecipes or similar(el, ERecipes):
            dt = 'Recipes: Equipment'
    return dt