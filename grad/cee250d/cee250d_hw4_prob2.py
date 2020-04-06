import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#############
# PROBLEM 2
#############
dataset = pd.read_excel(open('data_hw4.xlsx','rb'),sheet_name='Sheet1',skiprows=[0,1,106,107,108],usecols='B:M',header=None)

# find monthly mean and standard deviation of dataset shape (104,12)
monthly_mean = np.mean(dataset,axis=0)
monthly_std = np.std(dataset,axis=0)

# standardize data
data_stand = np.empty((104,12))
for m_i in range(1,13):
    data_stand[:,m_i-1] = (dataset[m_i] - monthly_mean[m_i])/monthly_std[m_i]

data_flat = data_stand.reshape(12*104)
    
# find correlogram
corr = []
for lag in range(1,13):
    x_bar_t = (1/(len(data_flat)-lag))*np.sum(data_flat[:-lag])
    x_bar_k = (1/(len(data_flat)-lag))*np.sum(data_flat[lag:])
    var_t = np.var(data_flat[:-lag])
    var_k = np.var(data_flat[lag:])
    corr.append(np.sum(((data_flat[:-lag]-x_bar_t)*(data_flat[lag:]-x_bar_k)))/((len(data_flat)-lag)*var_t*var_k))

# put correlation = 1 at the beginning for lag 0
corr = [1] + corr
plt.figure(figsize=[10,7])
plt.plot(corr)
plt.gca().grid(True)
plt.title('Correlogram',fontsize=16)
plt.xlabel('lag',fontsize=14)
plt.ylabel('correlation',fontsize=14)
plt.savefig('correlogram.png',bbox_inches='tight')

# probability transition matrices
# intervals 0-1250, 1250-2500, 2500-3750, 3750+
int1 = 1250
int2 = 2500
int3 = 3750
int4 = 10000
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0
count11 = 0
count12 = 0
count13 = 0
count14 = 0
count15 = 0
count16 = 0
n_i = 1
count_matrix = np.empty((12,4,4))
for m_i in range(1,13):
    if m_i == 12:
        count1 += np.where((dataset[m_i]<int1) & (dataset[n_i]<int1))[0].shape[0]
        count2 += np.where((dataset[m_i]<int1) & (dataset[n_i]>=int1) & (dataset[n_i]<int2))[0].shape[0]
        count3 += np.where((dataset[m_i]<int1) & (dataset[n_i]>=int2) & (dataset[n_i]<int3))[0].shape[0]
        count4 += np.where((dataset[m_i]<int1) & (dataset[n_i]>=int3))[0].shape[0]
        count5 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[n_i]<int1))[0].shape[0]
        count6 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[n_i]>=int1) & (dataset[n_i]<int2))[0].shape[0]
        count7 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[n_i]>=int2) & (dataset[n_i]<int3))[0].shape[0]
        count8 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[n_i]>=int3))[0].shape[0]
        count9 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[n_i]<int1))[0].shape[0]
        count10 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[n_i]>=int1) & (dataset[n_i]<int2))[0].shape[0]
        count11 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[n_i]>=int2) & (dataset[n_i]<int3))[0].shape[0]
        count12 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[n_i]>=int3))[0].shape[0]
        count13 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[n_i]<int1))[0].shape[0]
        count14 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[n_i]>=int1) & (dataset[n_i]<int2))[0].shape[0]
        count15 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[n_i]>=int2) & (dataset[n_i]<int3))[0].shape[0]
        count16 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[n_i]>=int3))[0].shape[0]
    else:
        count1 += np.where((dataset[m_i]<int1) & (dataset[m_i+1]<int1))[0].shape[0]
        count2 += np.where((dataset[m_i]<int1) & (dataset[m_i+1]>=int1) & (dataset[m_i+1]<int2))[0].shape[0]
        count3 += np.where((dataset[m_i]<int1) & (dataset[m_i+1]>=int2) & (dataset[m_i+1]<int3))[0].shape[0]
        count4 += np.where((dataset[m_i]<int1) & (dataset[m_i+1]>=int3))[0].shape[0]
        count5 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[m_i+1]<int1))[0].shape[0]
        count6 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[m_i+1]>=int1) & (dataset[m_i+1]<int2))[0].shape[0]
        count7 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[m_i+1]>=int2) & (dataset[m_i+1]<int3))[0].shape[0]
        count8 += np.where((dataset[m_i]<int2) & (dataset[m_i]>=int1) & (dataset[m_i+1]>=int3))[0].shape[0]
        count9 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[m_i+1]<int1))[0].shape[0]
        count10 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[m_i+1]>=int1) & (dataset[m_i+1]<int2))[0].shape[0]
        count11 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[m_i+1]>=int2) & (dataset[m_i+1]<int3))[0].shape[0]
        count12 += np.where((dataset[m_i]<int3) & (dataset[m_i]>=int2) & (dataset[m_i+1]>=int3))[0].shape[0]
        count13 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[m_i+1]<int1))[0].shape[0]
        count14 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[m_i+1]>=int1) & (dataset[m_i+1]<int2))[0].shape[0]
        count15 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[m_i+1]>=int2) & (dataset[m_i+1]<int3))[0].shape[0]
        count16 += np.where((dataset[m_i]<int4) & (dataset[m_i]>=int3) & (dataset[m_i+1]>=int3))[0].shape[0]
    count_matrix[m_i-1,:,:] = np.array(([count1,count2,count3,count4],[count5,count6,count7,count8],[count9,count10,count11,count12],[count13,count14,count15,count16]))

prob_matrix = np.empty((12,4,4))
for t_i in range(prob_matrix.shape[0]):    
    for i_i in range(prob_matrix.shape[1]):
        prob_matrix[t_i,i_i,:] = count_matrix[t_i][i_i]/np.sum(count_matrix[t_i][i_i])
