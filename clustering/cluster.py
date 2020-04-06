from sklearn.cluster import KMeans
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

data_path = '/data/project3/kesf/ROMS/USSW1/DAILY/'
data_file = 'ussw1_avg.Y2002M01D01.nc'

nc_file = Dataset(data_path+data_file,'r')
temp_nc = nc_file.variables['temp']
temp = np.copy(temp_nc)
X = np.copy(temp[0][59])

kmeans = KMeans(n_clusters=12)
kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_
#plt.scatter(X[:,3],X[:,0],X[:,2],c=labels.astype(np.float))
