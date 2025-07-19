import time
import os
from mojang import API
import requests
import logging


mojang_api = API()

# set up basic logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

saves_exist = False
uuid = ""
api_key = ""

if os.path.exists("ign.txt"):
    saves_exist = True
    print(f"ign.txt' found!")
    content = ""
    with open("ign.txt", "r") as file:
        content = file.read()
        print(f"Session name: {content}")
else:
    print(f"ign.txt' not found - creating...")

if os.path.exists("api_key.txt"):
    print(f"api_key.txt' found!")
    content = ""
    with open("api_key.txt", "r") as file:
        content = file.read()
        api_key = content
else:
    print(f"api_key.txt' not found - waiting...")

if os.path.exists("uuid.txt"):
    print(f"uuid.txt' found!")
    content = ""
    with open("uuid.txt", "r") as file:
        content = file.read()
        uuid = content
        print(f"Session uuid: {content}")
else:
    print(f"uuid.txt' not found - creating...")

if not saves_exist:
    username = input("Enter your Minecraft IGN > ")

    try:
        # retrieve UUID
        uuid = mojang_api.get_uuid(username=username)
        if uuid:
            # set file path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_name = "uuid.txt"
            file_path = os.path.join(script_dir, file_name)

            # save UUID to file
            with open(file_path, "w") as file:
                file.write(f"{uuid}")

            print(f"UUID for {username} saved to {file_path}")
        else:
            print(f"Could not retrieve UUID for username: {username}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "ign.txt"
        file_path = os.path.join(script_dir, file_name)
        with open(file_path, "w") as file:
            file.write(f"{username}")

        print(f"IGN ({username}) saved to {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

print("Boot complete -\n| Mojang API connected\n| Hypixel API connected\n\n")
time.sleep(0.1)
print(r"   _ _ _|_")
time.sleep(0.1)
print(r"  /   $   \ ")
time.sleep(0.1)
print(r" /_________\ ")
time.sleep(0.1)
print(r" |   SBF   |")
time.sleep(0.1)
print(r"_|_________|_")
time.sleep(0.1)
print(r"|  <        | ")
time.sleep(0.1)
print(r" \        >/")
time.sleep(0.1)
print(r"  |_   > _/")
time.sleep(0.1)
print(r"    |___/")
time.sleep(0.2)
print("\nSBF - SKy BLock BAzar FLipper\n\n")
time.sleep(0.5)
#startup end

def get_skyblock_money(uuid, api_key):
    url = f"https://api.hypixel.net/v2/skyblock/profiles?key={api_key}&uuid={uuid}"
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        #print(data)

        # check if profiles exist
        if "profiles" in data and data["profiles"]:
            profiles = []
            most_recent = 0
            available_money = 0
            
            for profile in data["profiles"]:
                profile_id = profile.get("profile_id")
                profile_name = profile.get("cute_name", "Unknown")
                purse_balance = profile.get("members", {}).get(uuid, {}).get("coin_purse", 0)
                bank_balance = profile.get("banking", {}).get("balance", 0) if "banking" in profile else 0
                
                print(f"balance:{bank_balance}")
                print(f"purse:{purse_balance}")

                if bank_balance + purse_balance > most_recent:
                    available_money = bank_balance + purse_balance
                
                #store profile data
                profiles.append({
                    "profile_id": profile_id,
                    "profile_name": profile_name,
                    "purse_balance": purse_balance,
                    "bank_balance": bank_balance,
                })
            
            print(available_money)
            return available_money
        else:
            print("No profiles found for this player.")
            return []
    else:
        print(f"Failed to retrieve data for UUID {uuid}. HTTP Status: {response.status_code}")
        return []

use_key = input("Use API key (Y/N) >")
if use_key == "y" or use_key == "Y":

    if os.path.exists("api_key.txt"):
        print(f"api_key.txt' found!")
        with open("api_key.txt", "r") as file:
            use_key = "?key=" + file.read()
            
    else:
        print("\033[91m {}\033[00m".format("api_key.txt not found!"))

    if not api_key == "":
        skyblock_money = get_skyblock_money(uuid=uuid, api_key=api_key)
        available_money = input(f"Enter available money (Current data: \033[92m{skyblock_money}\033[0m enter Y to use current data) >")
        if available_money == "Y" or available_money == "y":
            available_money = round(skyblock_money)
        else:
            available_money = float(available_money)
        print(f"{available_money} : {skyblock_money}")
    else:
        api_key = input("Enter API key >")
        skyblock_money = get_skyblock_money(uuid=uuid, api_key=api_key)
        available_money = input(f"Enter available money (Current data: \033[92m{skyblock_money}\033[0m enter Y to use current data) >")
        if available_money == "Y" or available_money == "y":
            available_money = round(skyblock_money)
            print(f"{available_money} : {skyblock_money}")
        else:
            available_money = float(available_money)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "api_key.txt"
        file_path = os.path.join(script_dir, file_name)

        # save uuid to file
        with open(file_path, "w") as file:
            file.write(f"{api_key}")
else:
    available_money = float(input("Available money >"))
    use_key = ""

print(use_key)

#program start
print("Bazaar to NPC\n")
bazaar_url = f"https://api.hypixel.net/v2/skyblock/bazaar{use_key}"

response = requests.get(bazaar_url)
bazaar_data = response.json()

amounts_dict = {}

items_url = f"https://api.hypixel.net/v2/resources/skyblock/items{use_key}"

response = requests.get(items_url)
items_data = response.json()

npc_prices = {
    item["id"]: (item["npc_sell_price"], item["name"])
    for item in items_data.get("items", [])
    if "npc_sell_price" in item
}

for product_id, product_data in bazaar_data.get("products", {}).items():
    total_amount = 0
    total_profit = 0
    stackable = False
    pricePerUnit = 0
    ppucounter = 1

    if product_id in npc_prices:
        npc_sell_price, item_name = npc_prices[product_id]

    for buy_item in product_data.get("buy_summary", []):
        if product_id in npc_prices:
            npc_sell_price, item_name = npc_prices[product_id]
            if npc_sell_price > buy_item["pricePerUnit"]:
                total_amount += buy_item["amount"]
                total_profit += (buy_item["pricePerUnit"] * buy_item["amount"])
                pricePerUnit += buy_item["pricePerUnit"]
                ppucounter += 1

    if npc_sell_price > 0:
        amounts_dict[product_id] = {
            "total_amount": total_amount,
            "total_profit": pricePerUnit/ppucounter * (200000000 / npc_sell_price),
            "stackable": stackable,
            "pricePerUnit": pricePerUnit/ppucounter
        }

profit_list = []

for product_id, values in amounts_dict.items():
    if product_id in npc_prices and values["pricePerUnit"] > 0:
        npc_sell_price, item_name = npc_prices[product_id]
        if "buy_summary" in bazaar_data["products"].get(product_id, {}):
            buy_price = bazaar_data["products"][product_id]["quick_status"]["buyPrice"]
            if amounts_dict[product_id]["total_profit"] > 0:
                if (npc_sell_price - buy_price) != 0:
                    profit = npc_sell_price - buy_price
                    amount = values["total_amount"]
                    max_profit = round(profit*min(amount, (200000000/npc_sell_price)), 0)/1000000  # calculate max profit
                    stackable = values["stackable"]
                    max_amount = min(2240, (available_money/values["pricePerUnit"]))
                    efficiency = (max_amount*profit)/100
                    profit_list.append({
                        "profit": profit,
                        "item_name": item_name,
                        "npc_sell": npc_sell_price,
                        "buy_price": buy_price,
                        "amount": amount,
                        "max_profit": max_profit,  # add max profit to the dictionary
                        "stackable":  stackable,
                        "efficiency": efficiency
                    })

sorted_profit_list = sorted(profit_list, key=lambda x: x["max_profit"], reverse=True)

# print the sorted profit list
for item in sorted_profit_list:
    try:
        if item['profit'] > 0:
            print(f"Profit: \033[92m{item['profit']:.2f}\033[0m coins | Efficiency: \033[93m{item['efficiency']:.4f}\033[0m | {item['item_name']} | NPC sell: {item['npc_sell']} | Bazaar buy: {item['buy_price']:.3f} | Bazaar amount: {item['amount']} | Max profit: {item['max_profit']:.4f}M | Can stack: {item['stackable']}")
    except KeyError as e:
        print(f"KeyError: Missing key {e} while printing item data: {item}")
        logging.error(f"KeyError: Missing key {e} while printing item data: {item}")
    except Exception as e:
        print(f"Unexpected error: {e} while printing item data: {item}")
        logging.error(f"Unexpected error: {e} while printing item data: {item}")

for x in range(0, 5):
    b = "Finished" + "." * x
    print(b, end="\r")
    time.sleep(1)

while True:
    pass
