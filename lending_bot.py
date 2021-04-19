import client
import time
import yaml

config_path = './lending.yml'

def create_dict_by_coin(x):
    return {i['coin']: i for i in x}

def main():
    with open(config_path, 'r') as stream:
        config = yaml.safe_load(stream)

    api_key = config['ftx']['api_key']
    api_secret = config['ftx']['api_secret']
    subaccount_name = config['ftx']['subaccount_name']
    
    lending = config['lending']
    ratio = config['ratio']    

    ftx = client.FtxClient(api_key=api_key, api_secret=api_secret, subaccount_name=subaccount_name)
    
    while True:
        try:
            info = create_dict_by_coin(filter(lambda x: x['coin'] in lending.keys(), ftx.get_lending_rates()))
            balances = create_dict_by_coin(ftx.get_balances())
            offers = []
            for coin, amount in lending.items():
                if coin not in balances:
                    continue

                if lending[coin] < 0:
                    amount = balances[coin]['total']

                rate = info[coin]['estimate'] * ratio
                offers.append({'coin': coin, 'size': amount, 'rate': rate})

            print(offers)

            for offer in offers:
                ftx.submit_lending_offer(offer)
        except Exception as e:
            print(e)
            
        time.sleep(1 * 60)
        
if __name__ == '__main__':
    main()
