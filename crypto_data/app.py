import requests
from flask import Flask, jsonify

app = Flask(__name__)

CRYPTO_DATA = [
    {'platform': 'Ethena', 'assets': 'USDe', 'amount': 2500, 'apy': 15.0},
    {'platform': 'Pendle', 'assets': 'PENDLE', 'amount': 2500, 'apy': 20.0},
    {'platform': 'GMX', 'assets': 'GMX', 'amount': 2500, 'apy': 25.0},
    {'platform': 'LIT', 'assets': 'LIT', 'amount': 2500, 'apy': 18.0},
]

def get_crypto_prices(assets):
    """Fetches cryptocurrency prices from CoinGecko."""
    prices = {}
    asset_ids = {
        'USDe': 'usd-stablecoin-by-ethena',  # Corrected CoinGecko ID
        'PENDLE': 'pendle',
        'GMX': 'gmx',
        'LIT': 'litentry',
    }
    
    asset_ids_to_fetch = [asset_ids[asset] for asset in assets if asset in asset_ids]

    if not asset_ids_to_fetch:
        return prices

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(asset_ids_to_fetch)}&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        for asset, gecko_id in asset_ids.items():
            if gecko_id in data:
                prices[asset] = data[gecko_id]['usd']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices: {e}")
    return prices

@app.route('/crypto_data', methods=['GET'])
def crypto_data():
    """Returns crypto data with current prices."""
    assets = [item['assets'] for item in CRYPTO_DATA]
    prices = get_crypto_prices(assets)
    
    result = []
    for item in CRYPTO_DATA:
        price = prices.get(item['assets'], None)
        item_with_price = item.copy()
        item_with_price['current_price'] = price
        if price is not None :
            item_with_price['current_value'] = price * item['amount']
        else:
            item_with_price['current_value'] = None
        
        result.append(item_with_price)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
