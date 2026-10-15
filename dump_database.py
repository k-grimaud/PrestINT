import requests


def dump_database():
    response = requests.get("https://cal.minet.net/api/organizations")
    data = response.json()
    for i in data:
        asso_id = i["id"]
        asso_name = i["name"]
        status = i["type"]
        response = requests.get("https://cal.minet.net/api/organizations")
        data1 = response.json()
        for j in data1:
            


dump_database()
