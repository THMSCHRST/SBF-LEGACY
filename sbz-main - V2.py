#7d6bb049-968b-42e8-b7f7-07de1c166697

import requests
import logging

# Set up basic logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

response = requests.get(bazaar_url)
data = response.json()

amounts_dict = {}

items_url = "https://api.hypixel.net/v2/resources/skyblock/items"

response = requests.get(items_url)
items_data = response.json()

npc_prices = {
    item["id"]: (item["npc_sell_price"], item["name"])
    for item in items_data.get("items", [])
    if "npc_sell_price" in item
}

# Iterate through Bazaar products and collect relevant data
for product_id, product_data in data.get("products", {}).items():
    total_amount = 0
    total_profit = 0
    stackable = False

    # Check if the product has a "category" tag in npc_prices
    if product_id in npc_prices:
        npc_sell_price, item_name = npc_prices[product_id]
        # If the item doesn't have a "category" tag, it's stackable
        stackable = "category" not in item_name  # or check if the item does not have the "category" tag

    for buy_item in product_data.get("buy_summary", []):
        if product_id in npc_prices:
            npc_sell_price, item_name = npc_prices[product_id]
            if npc_sell_price > buy_item["pricePerUnit"]:
                total_amount += buy_item["amount"]
                total_profit += (buy_item["pricePerUnit"] * buy_item["amount"])

    # Store the values for each product in amounts_dict, including the stackable flag
    amounts_dict[product_id] = {
        "total_amount": total_amount,
        "total_profit": total_profit,
        "stackable": stackable
    }

profit_list = []

# Build profit list by comparing NPC sell price with Bazaar buy price
for product_id, values in amounts_dict.items():
    if product_id in npc_prices:
        npc_sell_price, item_name = npc_prices[product_id]
        if "buy_summary" in data["products"].get(product_id, {}):
            buy_price = data["products"][product_id]["quick_status"]["buyPrice"]
            if npc_sell_price > buy_price:
                if buy_price != 0:
                    profit = npc_sell_price - buy_price
                    amount = values["total_amount"]
                    max_profit = values["total_profit"]
                    stackable = values["stackable"]
                    profit_list.append({
                        "profit": profit,
                        "item_name": item_name,
                        "npc_sell": npc_sell_price,
                        "buy_price": buy_price,
                        "amount": amount,
                        "max_profit": max_profit,
                        "stackable":  stackable
                    })

# Sort the profit list by profit in descending order
sorted_profit_list = sorted(profit_list, key=lambda x: x["profit"], reverse=True)

# Print the sorted profit list
for item in sorted_profit_list:
    try:
        print(f"Profit: {item['profit']:.2f} coins | {item['item_name']} | NPC sell: {item['npc_sell']} | Bazaar buy: {item['buy_price']:.3f} | Bazaar amount: {item['amount']} | Max profit: {item['max_profit']:.2f} | Can stack: {item['stackable']}")
    except KeyError as e:
        print(f"KeyError: Missing key {e} while printing item data: {item}")
        logging.error(f"KeyError: Missing key {e} while printing item data: {item}")
    except Exception as e:
        print(f"Unexpected error: {e} while printing item data: {item}")
        logging.error(f"Unexpected error: {e} while printing item data: {item}")

while True:
    pass