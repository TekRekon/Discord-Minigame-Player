import json


def getDataParsable():
    """
    Returns a variable representing our data file that we can search for keys/values
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


def changeData(dict, key, value):
    """
    Given the dictionary and key of a value, replace it with newVal
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    data[dict][key] = value
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def getData(dict, key):
    """
    Given a dictionary and key, return the value
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data[dict][key]


def addKey(dict, key, value):
    """
    Given a dictionary, create a new key with a new value
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    data[dict][key] = value
    with open('data.json', 'w') as g:
        json.dump(data, g, indent=4)


def addGuild(guild):
    """
    Add and initialize dictionary for a new guild
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    data.update({guild.id.text: {'guildName': guild.name, "noCommandChannels": [], "mods": [guild.owner_id],
                              "prefix": "."}})
    with open('data.json', 'w') as g:
        json.dump(data, g, indent=4)


def removeListVar(dict, list_key, del_var):
    """
    Given a dictionary and key, remove an element from the corresponding list
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    data[dict][list_key].remove(del_var)
    with open('data.json', 'w') as g:
        json.dump(data, g, indent=4)


def addListVar(dict, list_key, new_var):
    """
    Given a dictionary and key, add an element to the corresponding list
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    data[dict][list_key].append(new_var)
    with open('data.json', 'w') as g:
        json.dump(data, g, indent=4)


def renameKey(dict, old_key, new_key):
    """
    Given a dictionary and a key, rename the key to new_key
    """
    with open('data.json', 'r') as f:
        data = json.load(f)
    data[dict][new_key] = data[dict].pop(old_key)
    with open('data.json', 'w') as g:
        json.dump(data, g, indent=4)
