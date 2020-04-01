import json


# Returns a variable representing our data file that we can search for keys/values
def getDataParsable():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


# Given the location dict and key of a value, replace it with newVal
def changeData(dict, key, new_val):
    with open('data.json', 'r') as f:
        data = json.load(f)
    data[dict][key] = new_val
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


# Add a dict for a new guild
def addGuild(guild):
    with open('data.json', 'r') as f:
        data = json.load(f)
    data.update({guild.name: {'guildID': guild.id, "noCommandChannels": [], "mods": [guild.owner_id],
                              "prefix": "."}})
    with open('data.json', 'w') as g:
        json.dump(data, g, indent=4)
