import streamlit as st
import requests, json
import pandas as pd 
from web3 import Web3

#offset, order_by, order_direction 

offset = 0 
data = {'assets':[]}

modelresults=pd.read_csv("./results.csv")

def render_asset(asset):
	st.write('Cryptokitty   ID: ' + asset['ID_token'].astype(str))
	st.image(list(asset["image_url_png"]))
	st.write('Mouth Type: ' + list(asset['mouth_value'])  + 'Rarity: ' + list(asset['mouth_rarity']) )

endpoint = st.sidebar.selectbox("Navigation", [ "Model", "Pricing" ], index = 1) 
st.header(f"Cryptokitties NFT Explorer: {endpoint}")


if endpoint == 'Model':
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


if endpoint == 'Pricing':
	ids = st.sidebar.selectbox('ID token', list(modelresults['ID_token'].sort_values()))
	idx = modelresults[(modelresults['ID_token'] == ids)].index
	asset = modelresults.iloc[idx]
	render_asset(asset)


