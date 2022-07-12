import requests
import json
from gsheets import Sheets

sheets = Sheets.from_files('C:\\Users\\it\\apistuff\\asdf.json', 'storage.json')


url = "https://api.sellbrite.com/v1/orders?page=1&limit=10"

headers = {
    "Accept": "application/json",
    "Authorization": "Basic ODZjYmY1ZTgtYmFhOC00NmM2LWE2ZjItN2I5M2IzMGRlYTZlOmUxMGE0MjBhN2RmOWM2ZGI3NTBlZDdlNzE4NmU1Y2U0"
}

response = requests.get(url, headers=headers)

res_j = response.json()

dic_1 = dict()

j = 0
while j < len(res_j):
    dict_1 = res_j[j]
    listthing = dict_1["items"]
    i = 0
    while i < len(listthing):
        thing = dict(listthing[i])
        sku = thing["sku"]
        name = thing["title"]
        print("Title: " + name + "   SKU: ", end='')
        print(sku)
        i = i + 1
    j = j + 1
    











