#Copyright 2022 Luke Johannes Graham The First (And Only)
#Sugoma Inc.

import requests
import json
import pygsheets
import pandas as pd

with open("/home/ubuntu/Spinettis/orders.txt") as f:
    lines = f.read().splitlines()
f.close()

with open('/home/ubuntu/Spinettis/orders.txt', 'r') as filehandle:
    places = [current_place.rstrip() for current_place in filehandle.readlines()]
filehandle.close()

#stupid moron

#txt_file = open("orders.txt", "r")
#orders_list = txt_file.readlines()
#file.close()

gc = pygsheets.authorize(service_file='/home/ubuntu/Spinettis/hehe.json')

df = pd.DataFrame()
sh = gc.open('test')
wks = sh[0]

url = "https://api.sellbrite.com/v1/orders?page=1&limit=100"

headers = {
    "Accept": "application/json",
    "Authorization": "Basic ODZjYmY1ZTgtYmFhOC00NmM2LWE2ZjItN2I5M2IzMGRlYTZlOmUxMGE0MjBhN2RmOWM2ZGI3NTBlZDdlNzE4NmU1Y2U0"
}

response = requests.get(url, headers=headers)

res_j = response.json()


#why the balls is it like this
#screw apis i hate recursive lists and dictionaries
dic_1 = dict()
values = []
j = 0
ordernums = ["S1", "S2"]


#im not even gonna try to document this
while j < len(res_j):
    dict_1 = res_j[j]
    listthing = dict_1["items"]
    i = 0
    order_num = dict_1["display_ref"]
    while i < len(listthing):
        if not order_num in lines:
            thing = dict(listthing[i])
            sku = thing["sku"]
            cust_name = dict_1["shipping_contact_name"]
            name = thing["title"]
            if not cust_name:
                cust_name = "Retail"
            values.append([order_num, cust_name, name, sku])
            f = open("/home/ubuntu/Spinettis/orders.txt", "a")
            f.write(order_num + "\n")
            f.close()

        i = i + 1
    j = j + 1

wks.append_table(values, start='A1', end=None, dimension='ROWS', overwrite=True)
