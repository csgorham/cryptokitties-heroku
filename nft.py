import streamlit as st
import requests, json
import pandas as pd 
from web3 import Web3

#offset, order_by, order_direction 

offset = 0 
data = {'assets':[]}

def render_asset(asset):
        if asset['name']:
                st.write(asset['name'])
        else:
                st.write(f"{asset['collection']['name']} #{asset['token_id']}")
        if asset['image_url'].endswith('mp4') or asset['image_url'].endswith('mov'):
                st.video(asset['image_url'])
        else:
                st.image(asset["image_url"])

endpoint = st.sidebar.selectbox("Endpoints", ["Assets", "Events", "Rarity", " " ], index = 3) 
st.header(f"OpenSea NFT API Explorer {endpoint}")


if endpoint == 'Assets':
	st.sidebar.subheader("Filters")
	collection = st.sidebar.text_input("Collection", value='the-wanderers')
	owner = st.sidebar.text_input("Owner")

	while True:

		params={"limit": 50, 'offset' : offset}
		if collection:
			params['collection'] = collection
		if owner:
			params['owner'] = owner

		r = requests.get("https://api.opensea.io/api/v1/assets", params=params)
		response_json = r.json()
		data['assets'].extend(response_json['assets'])

		if len(response_json['assets']) < 50:
			break
		offset +=50

	for asset in data['assets']:
		render_asset(asset)
	st.subheader("Raw JSON Data")
	st.write(r.json())
	json.dumps(data)


if endpoint == 'Rarity':
	with open('assets.json') as f:
		data = json.loads(f.read())
		asset_rarities = []

if endpoint == 'Events':
	st.sidebar.subheader("Filters")
	collection = st.sidebar.text_input("Collection", value='the-wanderers')
	asset_contract_address = st.sidebar.text_input("Contract Address")
	token_id = st.sidebar.text_input("Token ID")
	event_type = st.sidebar.selectbox("Event Type", ['offer_entered', 
		'cancelled', 'bid_withdrawn', 'transfer', 'approve'])
	params = {}
	if collection:
		params['collection_slug'] = collection
	if asset_contract_address:
		params['asset_contract_address'] = asset_contract_address
	if token_id:
		params['token_id'] = token_id
	if event_type:
		params['event_type'] = event_type
	r = requests.get("https://api.opensea.io/api/v1/events", params=params)

	events = r.json()
	event_list = []
	for event in events['asset_events']:
		if event_type == 'offer_entered':
			if event['bid_amount']:
				bid_amount = Web3.fromWei(int(event['bid_amount']), 'ether')
			if event['from_account']['user']:
				bidder = event['from_account']['user']['username']
			else:
				bidder = event['from_account']['address']

			event_list.append([event['created_date'], bidder, float(bid_amount), event['asset']['collection']['name'], event['asset']['token_id']])

	df = pd.DataFrame(event_list, columns = ['time', 'bidder', 'bid_amount',
		'collection', 'token_id'])
	st.write(df)
	st.write(events)

if endpoint == 'Rarity':
	with open('assets.json') as f:
		data = json.loads(f.read())
		asset_rarities=[]

		for asset in data['assets']:
			asset_rarity = 1
			for trait in asset['traits']:
				trait_rarity = trait['trait_count'] / 8888
				asset_rarity += trait_rarity

			asset_rarities.append({
				'token_id' : asset['token_id'],
				'name': f"Wanderers {asset['token_id']}",
				'description' : asset['description'],
				'rarity' : asset_rarity,
				'traits' : asset['traits'],
				'image_url' : asset['image_url'],
				'collection': asset['collection']
 					})
		assets_sorted = sorted(asset_rarities, key=lambda asset: asset['rarity'])
		
		for asset in assets_sorted[:20]:
			render_asset(asset)
			st.subheader(f"{len(asset['traits'])} Traits")
			for trait in asset['traits']:
				st.write(f"{trait['trait_type']} - {trait['value']} - {trait['trait_count']} have this")
