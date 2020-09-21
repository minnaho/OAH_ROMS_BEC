#########################
# python version of 
# rainfall runoff model
# rationale method
# originally made by Ashmita Sengupta
#########################
import numpy as np
import pandas as pd
import glob as glob

#############
# load files
#############
# rainfall in each watershed
rain_loc = '/data/project1/minnaho/river_data/updated_2013_2017/rational_method_rivers/prism_ppt/'
rain_files = sorted(glob.glob(rain_loc+'*'))

# watershed area divided into land types
# agriculture, commercial, industry, open, residential, other, water 
warea = pd.read_csv('Annual total runoff_2.txt',header=None,sep='\t')
ar_agr = warea[2]
ar_com = warea[3]
ar_ind = warea[4]
ar_ope = warea[5]
ar_res = warea[6]
ar_oth = warea[7]
ar_wat = warea[8]

# land type coefficient
coef = pd.read_csv('Coef.txt',header=None)
co_agr = coef[0][0]
co_com = coef[0][1]
co_ind = coef[0][2]
co_ope = coef[0][3]
co_res = coef[0][4]
co_oth = coef[0][5]
co_wat = coef[0][6]

# load calleguas, need to runoff model on 10/31/2016-12/31/2018
ft3_to_m3 = 0.02831685
cal_p = '/data/project1/minnaho/river_data/updated_2013_2017/usgs_rivers/daily/daily_flow_2007_2016_calleguas_creek.txt'
cal_df = pd.read_csv(cal_p,header=None,skiprows=27,sep='\t')
cal_flow = np.array(cal_df[3][2:]).astype(float)*ft3_to_m3

# river names
names = []
for n_i in range(len(rain_files)):
    try:
        names.append(rain_files[n_i][rain_files[n_i].index('PRISM_ppt_')+10:rain_files[n_i].index('_2007')])
    except:
        names.append(rain_files[n_i][rain_files[n_i].index('PRISM_ppt_')+10:rain_files[n_i].index('_2016')])


#################################################
# run rationale method/rainfall runoff model
# multiply daily precipitation over the watershed by 
# watershed area and land type coefficient
##################################################
ppt = pd.read_csv(rain_files[0],header=None,skiprows=11) # read file
river_ts = np.empty((ppt[0].shape[0],len(rain_files)))
for r_i in range(len(rain_files)):
    print('river '+str(r_i)+' of '+str(len(rain_files)))
    ppt = pd.read_csv(rain_files[r_i],header=None,skiprows=11) # read file
    precip = np.array(ppt[1])*(1./1000) # precipitation convert mm to m
    wnum = ppt[2][0] # watershed number
    # two columns of potential watershed numbers, 
    # try the one with more unique values first
    try:
        fnum = np.where(wnum==warea[1])[0][0]
    except:
        fnum = np.where(wnum==warea[0])[0][0]
    # convert m3/day to m3/s
    if wnum == 151 and names[r_i]=='los_angeles_harbor': # special case for LA harbor, take into account 3 watersheds
        wnum1 = 341
        wnum2 = 143
        try:
            fnum1 = np.where(wnum1==warea[1])[0][0]
            fnum2 = np.where(wnum2==warea[1])[0][0]
        except:
            fnum1 = np.where(wnum1==warea[0])[0][0]
            fnum2 = np.where(wnum2==warea[0])[0][0]
        river_ts[:,r_i] = (np.nansum((ar_agr[fnum]*co_agr*precip,ar_com[fnum]*co_com*precip,ar_ind[fnum]*co_ind*precip,ar_ope[fnum]*co_ope*precip,ar_res[fnum]*co_res*precip,ar_oth[fnum]*co_oth*precip,ar_wat[fnum]*co_wat*precip),axis=0)/86400) + (np.nansum((ar_agr[fnum1]*co_agr*precip,ar_com[fnum1]*co_com*precip,ar_ind[fnum1]*co_ind*precip,ar_ope[fnum1]*co_ope*precip,ar_res[fnum1]*co_res*precip,ar_oth[fnum1]*co_oth*precip,ar_wat[fnum1]*co_wat*precip),axis=0)/86400) + (np.nansum((ar_agr[fnum2]*co_agr*precip,ar_com[fnum2]*co_com*precip,ar_ind[fnum2]*co_ind*precip,ar_ope[fnum2]*co_ope*precip,ar_res[fnum2]*co_res*precip,ar_oth[fnum2]*co_oth*precip,ar_wat[fnum2]*co_wat*precip),axis=0)/86400)
    elif wnum == 267 and names[r_i] == 'mission_bay': # special case for mission bay, take into account 2 watersheds
        wnum1 = 285
        try:
            fnum1 = np.where(wnum1==warea[1])[0][0]
        except:
            fnum1 = np.where(wnum1==warea[0])[0][0]
        river_ts[:,r_i] = (np.nansum((ar_agr[fnum]*co_agr*precip,ar_com[fnum]*co_com*precip,ar_ind[fnum]*co_ind*precip,ar_ope[fnum]*co_ope*precip,ar_res[fnum]*co_res*precip,ar_oth[fnum]*co_oth*precip,ar_wat[fnum]*co_wat*precip),axis=0)/86400) + (np.nansum((ar_agr[fnum1]*co_agr*precip,ar_com[fnum1]*co_com*precip,ar_ind[fnum1]*co_ind*precip,ar_ope[fnum1]*co_ope*precip,ar_res[fnum1]*co_res*precip,ar_oth[fnum1]*co_oth*precip,ar_wat[fnum1]*co_wat*precip),axis=0)/86400) 
    elif wnum == 37 and names[r_i] == 'calleguas_creek': # calleguas creek, combine usgs and this model
        dst = cal_flow.shape[0] # start where usgs ends
        river_ts[dst:,r_i] = np.nansum((ar_agr[fnum]*co_agr*precip,ar_com[fnum]*co_com*precip,ar_ind[fnum]*co_ind*precip,ar_ope[fnum]*co_ope*precip,ar_res[fnum]*co_res*precip,ar_oth[fnum]*co_oth*precip,ar_wat[fnum]*co_wat*precip),axis=0)/86400
        river_ts[:dst,r_i] = cal_flow
    else:
        river_ts[:,r_i] = np.nansum((ar_agr[fnum]*co_agr*precip,ar_com[fnum]*co_com*precip,ar_ind[fnum]*co_ind*precip,ar_ope[fnum]*co_ope*precip,ar_res[fnum]*co_res*precip,ar_oth[fnum]*co_oth*precip,ar_wat[fnum]*co_wat*precip),axis=0)/86400

###################
# write to csv files
###################
savepath = '/data/project1/minnaho/river_data/updated_2013_2017/rational_method_rivers/runoff_model_output/'
for n_i in range(len(names)):
    riv_df = pd.DataFrame({'date':ppt[0],'flow m3/s':river_ts[:,n_i]},index=None)
    riv_df.to_csv(savepath+names[n_i]+'_2007_2018.csv')
                 
