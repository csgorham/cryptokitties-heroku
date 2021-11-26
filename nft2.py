import streamlit as st
import requests, json
import pandas as pd 
from web3 import Web3

#offset, order_by, order_direction 

offset = 0 
data = {'assets':[]}

modelresults=pd.read_csv("./results.csv")

def render_asset(asset):
	st.markdown('Cryptokitty   ID: ' , asset['ID_token'].astype(str))
	st.image(list(asset["image_url_png"]))
	st.write(list(asset["image_url_png"]))
	st.write('Mouth Type: ' + asset['mouth_value']  + '   Rarity: ' + asset['mouth_rarity'].astype(str) )

endpoint = st.sidebar.selectbox("Navigation", [ "Model", "Cattribute Results", "Price Arbitrage Downloads" ], index = 0) 


if endpoint == 'Model':

	st.title(f"Introduction")

	st.markdown("""Non-fungible tokens (NFTs) are a modern digital investment vehicle based on the Ethereum blockchain. These assets have been a thing for a while now, but many of us are just catching on – and wondering what is driving the prices sky-high. NFTs, sold on online marketplaces (a most common one being OpenSea Marketplace), are organized into collections which fall into a variety of categories including art, collectible, games, metaverse, and utility. 

The most popular NFT collection (by number of assets) is known as ‘CryptoKitties’ – a collection of artistic images of virtual cats that are used in a game on Ethereum that allows players to purchase, collect and breed their virtual cats. Since gaining in popularity in 2017, the total volume exchanged daily has grown to $10 million dollars in March 2021. 

All CryptoKitties belong to a particular ‘generation,’ those that were “magically” created belong to Generation 0 – any new CryptoKitty NFTs are created by breeding and belong  to “Generation +1” of the oldest parent. There are currently over 2 million cats with the highest generation of 4593. """)

	st.header(f"Business Objective ")

	st.markdown("""This machine learning project focuses on the price prediction of individual Generation 0 CryptoKitties. I have developed a model to predict the price of virtual cats that have been previously sold, based on factors including the rarity of their attributes and their age (token ID). 

Having achieved a reasonably high degree of accuracy, we suggest looking at where the model has over-predicted or under-predicted the price as special cases that lend themselves to arbitrage (buying under-priced assets and subsequently marking them up, and vice versa – selling over-priced assets prior to their presumed loss of value).""")

	st.header(f"Generation 0")

	st.markdown("""We have decided to focus on Generation 0 kitties since they are considered the most valuable and are valued as a cryptocurrency in their own right, on account of their generation being the only one with a capped number of cats at 50,000. This makes them particularly rare, and in demand. """)

	st.header(f"Cattribute Rarity, Cooldown and Exclusive Cats")

	st.markdown("""Being an NFT, which is a unit of data stored on the blockchain that certifies a digital asset to be unique and not interchangeable, each cat has its own set of ‘cat attributes’ or ‘cattributes.’ Cattributes describe physical features of the virtual cats, such as: fur type, pattern, eye color and shape, background color, mouth style, eyebrows and even mood. Each attribute has a different frequency of realization within each generation of collection, and the combination of them are indicative of the rarity of the NFT. 

We calculate the overall rarity of each kitty as a sum of the rarities of each trait. For instance, there is only one kitty in Generation 0 with ‘Manx’ fur and that component of rarity is 1/50,000.

Other factors that contribute to the value of a cryptokitty are instances where the cat is “Special Edition” “Exclusive” or “Fancy.” While the appearance of “Normal Cats” is based on genetic cattributes, “Fancy Cats” are limited edition CryptoKitties with special artwork that are created by finding a particular genetic recipe. “Exclusives” are the rarest cats that are released to commemorate special events, and “Special Editions” are similar to “Exclusives” but are released in larger numbers.

A final factor in assessing the value of a cryptokitty is what is known as its “cooldown period.” This is the period of time that it will take a particular cat to recover after breeding, to breed again. “Virgin” cats are highly valued, since each time that a cat breeds its “cooldown period” becomes longer. """)


	st.title(f"Project Description") 

	st.header(""" **Data Ingestion:**  """)

	st.markdown("""(1)	Sale price and NFT trait information has been collected using the OpenSea API Asset request function.

(2)	Additional cattributes have been collected from KittyHelper API.

(3)	Cattribute rarity has been scraped from the KittyHelper website. """)

	st.image('./graphics/cleaned_data.png')

	st.header("""** Machine Learning Model:**""")

	st.markdown("""Random Forest Regression (RFR), from the sklearn toolkit, has been chosen to perform price prediction on the set of all generation-0 kitties (currently 36,258 exist). Random Forest is a supervised learning algorithm that operates by constructing multiple decision trees and outputting the mean prediction of the individual trees. Thanks to weighting multiple decision trees, RFR achieves high accuracies and generally produces better results than linear regression models or single decision trees.

•	RandomSearchCV and GridSearchCV have been utilized to find the optimized RFR hyperparameters:  n_estimators=170, min_samples_split=20, min_samples_leaf=6, max_features=auto, max_depth=101, bootstrap=True, oob_score=False.""")

	st.image('./graphics/pipe.png')


	st.header(f"Model Validation and Results:") 

	st.subheader("Feature Importance")
	st.image('./graphics/features.png')

	st.subheader("R2 Score")
	st.image('./graphics/R2.png')

	st.subheader("Oversold/Undersold vs. Rarity")
	st.image('./graphics/overallrarityVSprediction.png')

if endpoint == 'Cattribute Results':

        st.subheader("Virginity")
        st.image('./graphics/virginity_r2.png')

        st.subheader("Cooldown Index")
        st.image('./graphics/cooldown_r2.png')

        st.subheader("Eye Shape")
        st.image('./graphics/eyeshape_r2.png')

if endpoint == 'Price Arbitrage Downloads':
	ids = st.sidebar.selectbox('ID token', list(modelresults['ID_token'].sort_values()))
	idx = modelresults[(modelresults['ID_token'] == ids)].index
	asset = modelresults.iloc[idx]
	render_asset(asset)


