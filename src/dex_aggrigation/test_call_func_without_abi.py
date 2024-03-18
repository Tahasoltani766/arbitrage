import requests


def gas_price():
    res = requests.get('https://api.blocknative.com/gasprices/blockprices')
    print(res)
    response = res.json()
    a = response["blockPrices"][0]["estimatedPrices"][4]
    if a and a['confidence'] == 70:
        max_priority_gas = a['maxPriorityFeePerGas']
        max_per_gas = a['maxFeePerGas']
        print(max_priority_gas, max_per_gas)
    else:
        return None
gas_price()