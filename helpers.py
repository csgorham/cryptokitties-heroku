'''
title           : helpers.py
description     : Helper functions used for parsing the outcome of OpenSea APIs.
author          : Adil Moujahid
date_created    : 20210627
date_modified   : 20210627
version         : 1.0
python_version  : 3.6.8
'''

def parse_meebit_data(meebit_dict):
    
    meebit_id = meebit_dict['token_id']
    
    try:
        creator_username = meebit_dict['creator']['user']['username']
    except:
        creator_username = None
    try:
        creator_address = meebit_dict['creator']['address']
    except:
        creator_address = None
    
    try:
        owner_username = meebit_dict['owner']['user']['username']
    except:
        owner_username = None
    
    owner_address = meebit_dict['owner']['address']
    
    try:
        contractaddress = meebit_dict['asset_contract']['address']
    except:
        contractaddress = None
    try:
        names = meebit_dict['asset_contract']['name']
    except:
        names = None

    traits = meebit_dict['traits']
    image = meebit_dict['collection']['featured_image_url']
    permalink= meebit_dict['permalink']
    
    created = meebit_dict['asset_contract']['created_date']
    description = meebit_dict['description']
    num_sales = int(meebit_dict['num_sales'])

    if num_sales !=0: 
        if 'last_sale' in meebit_dict:
            if meebit_dict['last_sale'] != None:
                total_price =  meebit_dict['last_sale']['total_price']
            else:
                total_price = 0
        else:
            total_price = 0
    else:
        total_price=int(meebit_dict['num_sales'])

    result = {'ID_token': meebit_id,
	      'collection' : names,
	      'Smart_contract' : contractaddress,
              'created' : created,
              'creator_username': creator_username,
              'creator_address': creator_address,
              'owner_username': owner_username,
              'owner_address': owner_address,
              'description': description,
              'permalink' : permalink,
              'image_url'  : image, 
              'traits': traits,
              'total_price':total_price,
              'num_sales': num_sales}
    
    return result
    #if num_sales !=0:
    #    total_price = int(meebit_dict['last_sale']['total_price'])
    #else:
    #    total_price=None

def parse_sale_data(sale_dict):
    
    is_bundle = False

    if sale_dict['asset'] != None:
        meebit_id = sale_dict['asset']['token_id']
    elif sale_dict['asset_bundle'] != None:
        meebit_id = [asset['token_id'] for asset in sale_dict['asset_bundle']['assets']]
        is_bundle = True

#    contractaddress = None
#    if sale_dict['asset_contract'] !=None:
#        contractaddress = sale_dict['asset_contract']['address']
    
    timestamp = sale_dict['transaction']['timestamp']
    total_price = float(sale_dict['total_price'])
    payment_token = sale_dict['payment_token']['symbol']
    usd_price = float(sale_dict['payment_token']['usd_price'])
    transaction_hash = sale_dict['transaction']['transaction_hash']
    

    result = {'is_bundle': is_bundle,
              'ID_token': meebit_id,
              'timestamp': timestamp,
              'total_price': total_price, 
              'payment_token': payment_token,
              'usd_price': usd_price,
              'transaction_hash': transaction_hash}
    
              #'seller_address': seller_address,
              #'buyer_address': buyer_address,
              #'buyer_username': buyer_username,
              #'seller_username':seller_username,
    return result


_="""    if sale_dict['seller'] != None:
        seller_address = sale_dict['seller']['address']
    else:
        seller_address = None

    try:
        buyer_address = sale_dict['winner_account']['address']
    except:
        buyer_address = None

    try:
        seller_username = sale_dict['seller']['user']['username']
    except:
        seller_username = None
    try:
        buyer_username = sale_dict['winner_account']['user']['username']
    except:
        buyer_username = None """
