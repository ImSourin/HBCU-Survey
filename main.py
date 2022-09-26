import matplotlib.pyplot as plt
import geopandas
import pandas as pd
from mpl_toolkits.basemap import Basemap
import math
import numpy as np

# Loading data
df = pd.DataFrame(data=pd.read_csv('data/nsf-data-ranked-all.csv'),columns=['Institution', 'CS', 'Engineering', 'Latitude', 'Longitude'])

# Computing centroid
total_cs_funding = df['CS'].sum()
total_engg_funding = df['Engineering'].sum()
centroid_cs_lat = (df['CS']*df['Latitude']).sum()/total_cs_funding
centroid_cs_long = (df['CS']*df['Longitude']).sum()/total_cs_funding
centroid_engg_lat = (df['Engineering']*df['Latitude']).sum()/total_engg_funding
centroid_engg_long = (df['Engineering']*df['Longitude']).sum()/total_engg_funding

# Plotting basemap
map = Basemap(projection='lcc', resolution='h', 
            lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.,
            width=12000000,height=9000000)
map.shadedrelief()
map.drawcoastlines(color='gray')
map.drawcountries(color='gray')
map.drawstates(color='gray')

# Plotting Universities
for index, row in df.iterrows():
        x, y = map(df.iloc[index]['Longitude'], df.iloc[index]['Latitude'])
        plt.annotate(df.iloc[index]['Institution'], xy = (x,y), xytext=(x,y-20), fontsize=7)

size = np.log2(np.add(df['CS'].to_numpy(),df['Engineering'].to_numpy())).tolist()
size = [x * 30 for x in size]
map.scatter(list(df['Longitude']), list(df['Latitude']), latlon=True,c=np.add(df['CS'].to_numpy(),df['Engineering'].to_numpy()).tolist(), s=size, alpha=0.7, cmap='Reds')

# Plotting centroid
x, y = map(centroid_cs_long,centroid_cs_lat)
map.plot(x,y,marker='*',color='blue',markersize=10)
plt.annotate('Centroid CS', xy = (x,y), xytext=(x,y), fontsize=10)
x, y = map(centroid_engg_long,centroid_engg_lat)
map.plot(x,y,marker='*',color='green',markersize=10)
plt.annotate('Centroid Engg', xy = (x,y), xytext=(x,y), fontsize=10)

# Rendering plot
plt.figure(figsize=(19,20))
plt.colorbar(label='Total Funding')
plt.clim(0, 12000)
plt.show()
