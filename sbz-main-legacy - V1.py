import requests

# fetch NPC sell prices and Bazaar prices
def fetch_npc_prices():
    items_url = "https://api.hypixel.net/v2/resources/skyblock/items"
    try:
        response = requests.get(items_url)
        response.raise_for_status()
        data = response.json()

        # extract items with npc_sell_price
        npc_prices = {
            item["id"]: item["npc_sell_price"]
            for item in data.get("items", [])
            if "npc_sell_price" in item
        }
        return npc_prices

    except requests.exceptions.RequestException as e:
        print(f"Error fetching NPC prices: {e}")
        return {}

def compare_prices():
    bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

    try:
        # fetch Bazaar prices
        response = requests.get(bazaar_url)
        response.raise_for_status()
        bazaar_data = response.json()

        if "products" not in bazaar_data:
            print("Error: 'products' key not found in the Bazaar API response.")
            return

        bazaar_prices = bazaar_data["products"]

        # fetch NPC prices and item names
        items_url = "https://api.hypixel.net/v2/resources/skyblock/items"
        items_response = requests.get(items_url)
        items_response.raise_for_status()
        items_data = items_response.json()

        # extract NPC prices and names
        npc_prices = {
            item["id"]: (item["npc_sell_price"], item["name"])
            for item in items_data.get("items", [])
            if "npc_sell_price" in item
        }

        # list to store profitable items
        profitable_items = []

        # compare each NPC price with the Bazaar buy price
        for item_id, (npc_price, item_name) in npc_prices.items():
            product = bazaar_prices.get(item_id)
            if not product:
                continue  # skip items not found in Bazaar

            quick_status = product.get("quick_status", {})
            bazaar_buy_price = quick_status.get("buyPrice", 0)

            # calculate profit
            if npc_price > bazaar_buy_price:
                if bazaar_buy_price != 0: # important stuff!
                    profit = npc_price - bazaar_buy_price
                    profitable_items.append((item_name, profit, bazaar_buy_price, npc_price))

        # print profitable items
        if profitable_items:
            print("Profitable Items:")
            for item_name, profit, bazaar_buy_price, npc_price in sorted(profitable_items, key=lambda x: x[1], reverse=True):
                print(f"| Profit: {profit:.2f} coins  |  {item_name:<20}  |  Bazaar buy: {bazaar_buy_price}  |  NPC sell: {npc_price}")
        else:
            print("No profitable items found.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")


# run the comparison function
compare_prices()

while True:
    pass