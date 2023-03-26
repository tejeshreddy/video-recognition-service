import json

record = {
  "id": {
    "N": ""
  },
  "major": {
    "S": ""
  },
  "name": {
    "S": ""
  },
  "year": {
    "S": ""
  }
}

with open("student_data.json", "r") as fp:
    data = json.load(fp)
    for entry in data:
        record["id"]["N"] = str(entry["id"])
        record["major"]["S"] = entry["major"]
        record["name"]["S"] = entry["name"]
        record["year"]["S"] = entry["year"]
        print(record)

