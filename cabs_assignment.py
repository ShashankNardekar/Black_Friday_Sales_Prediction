# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 15:58:10 2019

@author: Dell
"""

import pandas as pd
import glob, os
#import reverse_geocoder as rg 

path = r'C:\Users\nardekars\Documents\icarus-master\br personal\personal\thinkbumblebee\trips\\'

lookup_aggr_path = path + r'aggregated\\'

os.chdir(path + r'uber_2014')


uber_2014_data = pd.DataFrame()
for file in glob.glob("*.csv"):
    if file != 'uber-raw-data-janjune-15_sampled.csv':
        data = pd.read_csv(path + 'uber_2014\\' + file)
        print(file,data.columns)
        uber_2014_data = uber_2014_data.append(data)
    
    
uber_2014_data.columns
    
uber_2014_data.head()


os.chdir(path + r'uber_2015')


uber_2015_data = pd.DataFrame()
for file in glob.glob("*.csv"):
    data = pd.read_csv(path + 'uber_2015\\' + file)
    print(file)
    uber_2015_data = uber_2015_data.append(data)
    
uber_2015_data.head()

uber_2014_data = uber_2014_data.reset_index(drop=True)


uber_2014_data['date'] = uber_2014_data['Date/Time'].str.split(' ').str[0]
uber_2014_data['time'] = uber_2014_data['Date/Time'].str.split(' ').str[1]

del uber_2014_data['Date/Time']
#del uber_2014_data['Base']

##########################################################################################
geocode_data = pd.read_csv(lookup_aggr_path + 'rg_cities1000.csv')
geocode_data['lat_lon'] = geocode_data['lat'].map(str) + geocode_data['lon'].map(str)
uber_2014_data['lat_lon'] = uber_2014_data['Lat'].map(str).str[7:] + uber_2014_data['Lon'].map(str)



uber_2014_data = pd.merge(uber_2014_data,
                          geocode_data[['name', 'admin1', 'admin2','lat_lon']],
                          on='lat_lon',how='left')
  
uber_2014_data['Borough'] = ''
uber_2014_data['Zone'] = ''
##########################################################################################


# =============================================================================
# 2 a
# =============================================================================
uber_2014_data.columns

uber_14_pivot = uber_2014_data.pivot_table(values='time',index=['date'],aggfunc='count')

#uber_14_pivot = 
#uber_2014_data['trips_per_day'] = ''
#for date in uber_2014_data['date'].unique():
#    len(uber_2014_data[uber_2014_data['date']==date])

uber_14_pivot = uber_14_pivot.reset_index()
uber_14_pivot = uber_14_pivot.rename(columns={'time':'count'})

highest_trips = uber_14_pivot['count'].max()
minimum_trips = uber_14_pivot['count'].min()
average_trips = uber_14_pivot['count'].mean()


# =============================================================================
# 2 c
# =============================================================================

uber_2014_data['hour'] = uber_2014_data['time'].str.split(':').str[0]

uber_14_pivot_date_hour = uber_2014_data.pivot_table(values='time',index=['date','hour'],aggfunc='count')
uber_14_pivot_date_hour = uber_14_pivot_date_hour.reset_index()
uber_14_pivot_date_hour = uber_14_pivot_date_hour.rename(columns={'time':'count'})

# =============================================================================
# 2 d
# =============================================================================
uber_2014_data['month'] = uber_2014_data['date'].str.split('/').str[0]

uber_14_pivot_month_hour = uber_2014_data.pivot_table(values='time',index=['month','hour'],aggfunc='count')
uber_14_pivot_month_hour = uber_14_pivot_month_hour.reset_index()
uber_14_pivot_month_hour = uber_14_pivot_month_hour.rename(columns={'time':'count'})
uber_14_pivot_month_hour = uber_14_pivot_month_hour.sort_values(['hour','month'])


# =============================================================================
# 2 e
# =============================================================================

uber_2014_data['datetime_date'] = pd.to_datetime(uber_2014_data['date'])

uber_2014_data['day_of_week'] = uber_2014_data['datetime_date'].dt.day_name()

uber_2014_data['day_of_week'].unique()

uber_14_pivot_month_day = uber_2014_data.pivot_table(values='time',
                                                     index=['month','day_of_week'],
                                                     aggfunc='count')
uber_14_pivot_month_day = uber_14_pivot_month_day.reset_index()
uber_14_pivot_month_day = uber_14_pivot_month_day.rename(columns={'time':'count'})

# =============================================================================
# 3 c
# =============================================================================
import numpy as np
uber_2014_data['lat_lon'] = uber_2014_data['Lat'].map(str) + ':' + uber_2014_data['Lon'].map(str)

uber_2014_data_unq_lat_lon = pd.DataFrame(index=np.arange(len(uber_2014_data['lat_lon'].unique())))
uber_2014_data_unq_lat_lon['lat_lon'] = uber_2014_data['lat_lon'].unique().tolist()
uber_2014_data_unq_lat_lon['lat'] = uber_2014_data_unq_lat_lon['lat_lon'].str.split(':').str[0]
uber_2014_data_unq_lat_lon['lon'] = uber_2014_data_unq_lat_lon['lat_lon'].str.split(':').str[1]


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="app2")


location = geolocator.reverse("40.769, -73.9549")
geolocator.geocode('163 W 161st St High Bridge, BX')


print(location.address)
location

48,92
addr = []
lat_lon = []
for index,lat in enumerate(uber_2014_data_unq_lat_lon['lat'][92:]):
    print(index+92)
    lat_lon_string = str(uber_2014_data_unq_lat_lon['lat'][index]) + ',' + str(uber_2014_data_unq_lat_lon['lon'][index])
    addr.append(geolocator.reverse(lat_lon_string))
    lat_lon.append(lat_lon_string)
    
pd.DataFrame({'Address':addr,
              'Lat_lon':lat_lon}).to_csv(path + r'uber_2014\uber14_addresses_lat_lot.csv',
    mode='a',index=False)

def convert_lat_lon_to_address(index):
    print(index)
    lat_lon_string = str(uber_2014_data_unq_lat_lon['lat'][index]) + ',' + str(uber_2014_data_unq_lat_lon['lon'][index])
    return geolocator.reverse(lat_lon_string)
        
    
#new_data = pd.DataFrame({'addr':addr})
#new_data.to_csv(path+r'check.csv')


import multiprocessing

from joblib import Parallel, delayed

num_cores = multiprocessing.cpu_count()

inputs = uber_2014_data_unq_lat_lon['lat'].tolist()
unq_latlons = len(inputs)

processed_list = Parallel(n_jobs=num_cores)(delayed(convert_lat_lon_to_address(y) 
                                                    for y in range(unq_latlons)))




from multiprocessing.dummy import Pool as ThreadPool
aux_val = [y for y in range(unq_latlons)]
pool = ThreadPool(multiprocessing.cpu_count()) 

results = pool.map(convert_lat_lon_to_address, aux_val)



for file in glob.glob("*.csv"):
    print(file)
    data = pd.read_csv(path + 'uber_2014\\' + file)
    sampled_data = data.sample(n = 1000) 
    sampled_data.to_csv(path + 'uber_2014\\' + file.split('.')[0] + '_sampled.csv', index=False)

os.chdir(path + r'uber_2015')

for file in glob.glob("*.csv"):
    print(file)
    data = pd.read_csv(path + 'uber_2015\\' + file)
    sampled_data = data.sample(n = 6000) 
    sampled_data.to_csv(path + 'uber_2015\\' + file.split('.')[0] + '_sampled.csv', index=False)


os.chdir(path + r'other_FHV')

for file in glob.glob("*.csv"):
    print(file)
    try:
        data = pd.read_csv(path + 'other_FHV\\' + file)
        sampled_data = data.sample(n = 276) 
        sampled_data.to_csv(path + 'other_FHV\\' + file.split('.')[0] + '_sampled.csv', index=False)        
    except:
        print(file + 'NOT CONVERTED')
        continue
    
    
uber_2015 = pd.read_csv(path + r'uber_2015\uber-raw-data-janjune-15_sampled.csv')
lookup_table = pd.read_csv(path + r'aggregated\taxi-zone-lookup.csv')
lookup_table = lookup_table.rename(columns={'LocationID':'locationID'})

uber_2015_lookup = pd.merge(uber_2015,lookup_table,on='locationID',how='left')    

uber_2015_lookup.to_csv(path + r'uber_2015\uber_2015_jan_june_cleaned.csv',index=False)



# =============================================================================
# EXTRACTION OF DATA FROM ADDRESSES
# =============================================================================
import usaddress

other_american = pd.read_csv(path + r'other_FHV\addresses\other-American_B01362_sampled.csv')

other_american['place_name'] = ''
other_american['state_name'] = ''
for index,address in enumerate(other_american['PICK UP ADDRESS']):
    print(index)
    other_american['place_name'][index] = ' '.join([x[0] for x in usaddress.parse(address) if x[1]=='PlaceName'])
    other_american['state_name'][index] = ' '.join([x[0] for x in usaddress.parse(address) if x[1]=='StateName'])

other_american['place_name'] = other_american['place_name'].str.replace(',','')
other_american.to_csv(path + r'other_FHV\addresses\other-American_cleaned.csv',index=False)




other_federal = pd.read_csv(path + r'other_FHV\addresses\other-Federal_02216_sampled.csv')

other_federal['PU_Address.1'][other_federal['PU_Address.1']==' '] = other_federal[other_federal['PU_Address.1']==' ']['PU_Address'][106]

other_federal['PU_Address.1'] = other_federal['PU_Address.1'].str.split(';').str[0]

other_federal['place_name'] = ''
other_federal['state_name'] = ''
for index,address in enumerate(other_federal['PU_Address.1']):
    print(index)
    other_federal['place_name'][index] = ' '.join([x[0] for x in usaddress.parse(address) if x[1]=='PlaceName'])
    other_federal['state_name'][index] = ' '.join([x[0] for x in usaddress.parse(address) if x[1]=='StateName'])

other_federal['place_name'] = other_federal['place_name'].str.replace(',','')

other_federal[other_federal['place_name'] == '']['PU_Address.1'][9]


other_federal.to_csv(path + r'other_FHV\addresses\other-federal_cleaned.csv',index=False)

