from difflib import SequenceMatcher
import logging

family = ['Woods','Stone','Gems','Element','Fabrics','Metals']

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
    :param els: list of values to match with
    :return: probability value of similitude
    """
    try:
        umbral = .7
        resp = False
        for el in els:
            if SequenceMatcher(None, a, el).ratio() > umbral:
                resp = True
                break
            else:
                pass
        return resp
    except Exception as e:
        logging.error('Error in similar ----> ', e)
        return False

def d_type(el):
    try:
        dt = 'Recipes: Unknown'
        if 'Soul' in el:
            dt = 'Soul'
        elif 'Ember' in el:
            dt = 'Ember'
        elif 'Shard' in el:
            dt = 'Shard'
        elif el in woods_list:
            dt = 'Woods'
        elif el in stones_list:
            dt = 'Stones'
        elif el in gems_list:
            dt = 'Gems'
        elif el in els_list:
            dt = 'Elements'
        elif el in metals_list:
            dt = 'Metals'
        elif el in fabrics_list:
            dt = 'Fabrics'
        elif 'GOLD' in el or 'Gold' in el:
            dt = ''
        else:
            if el in CrystalsRecipes or similar(el, CrystalsRecipes):
                dt = 'Recipes: Crystals'

            if el in ERecipes or similar(el, ERecipes):
                dt = 'Recipes: Equipment'
        return dt

    except Exception as e:
        logging.error('Error in d_type ----> ', e)
        return None