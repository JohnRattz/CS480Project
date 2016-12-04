from Card import *
from globals import heroesList, cardsList
import json # For Json handling

JSON_CARD_PATH = "data\cards.json"

def loadCards():
    global heroesList
    cardsList = []
    # Re-initializes global card lists
    heroesList.clear()
    cardsList.clear()

    populatHeroesList(heroesList)
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
        if type == "MINION":
            # 1038 cards
            cardsList.append(parseMinionCard(card))
        elif type == "SPELL":
            # 604 cards
            #cardsList.append(parseSpellCard(card))
            continue
        else:
            continue
    
    print("Loaded", len(heroesList), "hero cards and", len(cardsList), "minion cards")
    return cardsList
    
def populatHeroesList(list):
    list.append(Hero("Paladin"))
    list.append(Hero("Rogue"))
    list.append(Hero("Warrior"))
    list.append(Hero("Shaman"))
    list.append(Hero("Mage"))
    list.append(Hero("Hunter"))
    list.append(Hero("Warlock"))
    list.append(Hero("Druid"))
    list.append(Hero("Priest"))

def parseMinionCard(card):
    # Gets card info from json object
    cost = card["cost"]
    name = card["name"]
    isLegendary = card.get("rarity", "") == "LEGENDARY"
    health = card["health"]
    attack = card["attack"]
    text = ""
    if "text" in card:
        text = card["text"]

    return Minion(cost, name, isLegendary, health, attack, card["playerClass"], text)

def parseSpellCard(card):
    # Gets card info from json object
    cost = card["cost"]
    name = card["name"]
    isLegendary = card.get("rarity", "") == "LEGENDARY"
    attack = 0
    text = ""
    if "text" in card:
        text = card["text"]
    # TODO: Parse damage/attack value from text attribute (Might be too much work)

    return Spell(cost, name, isLegendary, attack, card["playerClass"], text)