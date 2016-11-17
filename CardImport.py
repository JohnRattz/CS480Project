from Card import *
from globals import heroesList, cardsList
import json # For Json handling

JSON_CARD_PATH = "data\cards.json"

def loadCards():
    global heroesList
    global cardsList

    # Re-initializes global card lists
    heroesList.clear()
    cardsList.clear()

    jsonData = None

    try:
        # Attempts to read json data from file
        with open(JSON_CARD_PATH) as jsonFile:
            jsonData = json.load(jsonFile)
    except:
        # Failure (Returns)
        print("Unable to load cards from json file")
        return
    
    # Enumerates through each card
    for card in jsonData:
        type = card["type"]

        # Filters card by type
        if type == "HERO":
            # 171 cards
            heroesList.append(parseHeroCard(card))
        elif type == "MINION":
            # 1038 cards
            cardsList.append(parseMinionCard(card))
        elif type == "SPELL":
            # 604 cards
            #cardsList.append(parseSpellCard(card))
            continue
        else:
            continue
    
    print("Loaded", len(heroesList), "hero cards and", len(cardsList), "minion cards")
    
def parseHeroCard(card):
    # Gets card info from json object
    cost = 0 # Hero has no cost attribute?
    name = card["name"]
    isLegendary = card.get("rarity", "") == "LEGENDARY" # Rarity attribute isn't always present
    health = card["health"]
    
    return Hero(cost, name, isLegendary, health)

def parseMinionCard(card):
    # Gets card info from json object
    cost = card["cost"]
    name = card["name"]
    isLegendary = card.get("rarity", "") == "LEGENDARY"
    health = card["health"]
    attack = card["attack"]

    return Minion(cost, name, isLegendary, health, attack)

def parseSpellCard(card):
    # Gets card info from json object
    cost = card["cost"]
    name = card["name"]
    isLegendary = card.get("rarity", "") == "LEGENDARY"
    attack = 0

    # TODO: Parse damage/attack value from text attribute (Might be too much work)

    return Spell(cost, name, isLegendary, attack)