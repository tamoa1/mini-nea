import json
f = open("trip.json", 'r')
data = json.load(f)
print(data["students"][0]["firstName"])