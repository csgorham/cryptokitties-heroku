

import requests
import io
import dill
import json
import ast  
import  config
import pandas as pd
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from yelp.client import Client
from geopandas import GeoDataFrame
import ast
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
from uszipcode import SearchEngine
import matplotlib.pyplot as plt

wfyelp_file='./datasets/wholefoods_yelp.csv'
wflocations_file='./datasets/wholefoods_locations.csv'
states = pd.DataFrame()
snp500 = pd.read_csv("datasets/state_abbrv.csv")
states['state'] = snp500['State'].tolist()        
states['abbrv'] = snp500['Code'].to_list()

companies = ['Whole Foods']



ticker = st.sidebar.selectbox(
    'Choose State',
     states['state'])


store = st.sidebar.selectbox(
        "Company",
        companies)
    


with open(wfyelp_file, "rb") as dill_file:
    dfall= dill.load(dill_file)
    
with open(wflocations_file, "rb") as dill_file:
    dfwf = dill.load(dill_file)



dfall_zips = []
dfall_state = []
dfall_city = []
for ind, location in enumerate(dfall['location'][:]):
    #print(location)
    if location != ',':
        
        dfall_locexplode =(ast.literal_eval(location))
        dfall_state.append(dfall_locexplode['state'])
        dfall_city.append(dfall_locexplode['city'])
        dfall_zips.append(dfall_locexplode['zip_code'])
    else:
   
        dfall_zips.append('0')
        dfall_state.append('0')
        dfall_city.append('0')
        
dfall['city'] = dfall_city     
dfall['state'] = dfall_state    
dfall['zip_code'] = dfall_zips

wf = pd.DataFrame()
ca_df=pd.DataFrame()

_=""" ab """
#longlist, latlist, zipslist, citylist, statelist = [], [], [], [],[]
#calonglist, calatlist,calist_zip, ca_citylist, ca_statelist = [], [], [], [],[]
#ca_alias, ca_rating,ca_reviewcount = [], [], []
#for ind in range(len(dfwf)):
    
#    zipslist.append(dfall['zip_code'][ind])
#    citylist.append(dfall['city'][ind])
#    statelist.append(dfall['state'][ind])
#    longlist.append(dfwf['Longitude'][ind])
#    latlist.append(dfwf['Latitude'][ind])
        
wf['name'] = dfall['alias'][:]
wf['rating'] = dfall['rating'][:]
wf['review_count'] = dfall['review_count'][:]    
#wf['zipcode'] = zipslist
#wf['city'] = citylist
#wf['state'] = statelist
#wf['longitude'] = longlist
#wf['latitude'] = latlist
wf['zipcode'] = dfall['zip_code'][:]
wf['city'] = dfall['city'][:]
wf['state'] = dfall['state'][:]
wf['longitude'] = dfwf['Longitude'][:]
wf['latitude'] = dfwf['Latitude'][:]

states_file = gpd.read_file('./datasets/geopandas-tutorial/data/usa-states-census-2014.shp')
df_zipcodes = gpd.read_file('./datasets/cb_2018_us_zcta510_500k/cb_2018_us_zcta510_500k.shp')
counties = gpd.read_file('./datasets/geopandas-tutorial/data/USA_Counties/USA_Counties.shp')

geometry = [Point(xy) for xy in zip(wf['longitude'], wf['latitude'])]
gdf = GeoDataFrame(wf, geometry=geometry)   
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# Read in shapefile and examine data
df_zipcodes.rename(columns={'ZCTA5CE10':'zipcode'}, inplace=True)
df_zipcodes['zip_code'] = df_zipcodes['zipcode'].astype('str')
df_zipcodes['zip_code'] = df_zipcodes['zip_code'].str.pad(5, 'left', '0')
df_zipcodes['zip_code'] = df_zipcodes['zip_code'].str.slice(0,3)
df_zipcodes['zip_code'] = df_zipcodes['zip_code'].str.pad(5, 'right', 'x')
search = SearchEngine(simple_zipcode=True)
df_zipcodes['state'] = df_zipcodes.apply(lambda row: search.by_zipcode(row.zipcode).state, axis=1)
df_zipcodes['county'] = df_zipcodes.apply(lambda row: search.by_zipcode(row.zipcode).county, axis=1)


counties = counties[~counties.STATE_NAME.isin(['Alaska','Hawaii', 'AA', 'AE','AP','Puerto Rico','RI','VI'])]


abbrvs0 = list(states['state']).index(ticker)
abbrvs1 = states['state'][abbrvs0]
abbrvs2 = states['abbrv'][abbrvs0]


cali = counties[counties.STATE_NAME.isin([abbrvs1])]

#counties.head()
fig, ax = plt.subplots(figsize=(10,10))
#counties.boundary.plot(cmap='Pastel2',ax=ax)
cali.boundary.plot(cmap='Pastel2',ax=ax)


df_redlines_maps = df_zipcodes.merge(wf[1:], on='zipcode', how='inner')
df_redlines_maps['geometry'] =df_redlines_maps['geometry_x']

df_redlines_maps = df_redlines_maps[df_redlines_maps.state_x.isin([abbrvs2])]
df_redlines_maps_mm = GeoDataFrame(df_redlines_maps)
ax  = df_redlines_maps_mm.plot(column='review_count', ax=ax, color='red')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(fig)
