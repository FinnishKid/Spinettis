#Copyright 2022 Luke Johannes Graham The First (And Only)
#Sugoma Inc.

import requests
import json
import pygsheets
import pandas as pd

with open("chiporders.txt") as f:
   lines = f.read().splitlines()
f.close()

with open('chiporders.txt', 'r') as filehandle:
    places = [current_place.rstrip() for current_place in filehandle.readlines()]
filehandle.close()

#stupid moron

#txt_file = open("orders.txt", "r")
#orders_list = txt_file.readlines()
#file.close()

gc = pygsheets.authorize(service_file='hehe.json')
sku = ""
df = pd.DataFrame()
sh = gc.open('Sold Chips')
wks = sh[0]
#ithang = input("Page #: ")
#thang = str(ithang)
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
channel = ""
storeurl = ""
quan = ""
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
            quan = thing["quantity"]
            channel = dict_1["channel_type_display_name"] 
            date = dict_1["ordered_at"]
            #only time you can have a blank customer is if they are rung up in retail so they get the customer name "Retail"
            if not cust_name:
                cust_name = "Retail"
            
            f = open("chiporders.txt", "a")
            f.write(order_num + "\n")
            f.close()

            #holy crap this is big brain time
            if sku:
                url2 = ("https://api.sellbrite.com/v1/products/" + sku)

                headers2 = {
                    "Accept": "application/json",
                    "Authorization": "Basic ODZjYmY1ZTgtYmFhOC00NmM2LWE2ZjItN2I5M2IzMGRlYTZlOmUxMGE0MjBhN2RmOWM2ZGI3NTBlZDdlNzE4NmU1Y2U0"
                }


                #2 api calls in 1 program? tripping balls my friend
                response2 = requests.get(url2, headers=headers2)

                chip_j = response2.json()

                #print(chip_j)
                #error handling
                try:
                    cat_name = chip_j["category_name"]
                    storeurl = chip_j["store_product_url"]

                    #print(channel)
                except(KeyError):
                    cat_name = ""
                    #print("b")
                    pass
                values.append([order_num, cust_name, name, sku, quan, storeurl, channel, date])
                if (cat_name == "Collector Chips"):
                    #if everything is copasetic, adds stuff to the spreadsheet
                    #print("a")
                    wks.insert_rows(row =1, number=1, values =values)

                #resets values for next recursion so shizzle don't go nizzle
                values = []
                cat_name = ""
                storeurl = ""
        #screwed myself by using whiles but here we are
        i = i + 1
    j = j + 1

#Security? Nah fam we put our API keys on GitHub :dab:
