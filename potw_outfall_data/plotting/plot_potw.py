#############################################
# plot_potw.py
# plot data from POTW_INTERP-ms edits_Minna_edits.xlsx
# converted to python data through open_excel_potw.py 
#####################################################
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdate 
import datetime
import copy
from collections import defaultdict

###################
# FOLDER PATHS
####################
save_figs_path = '../potw_figs/'
converted_path = 'converted_figs/'
avg_path = 'annual_average_figs/'
seasonal_path = 'seasonal_figs/'
max_path = 'max_values/'
min_path = 'min_values/'

################################
# CALL DATA FROM open_excel.py
################################
potw_data = pickle.load(open('potw_data.pkl','rb'))
# each key is one location
# 0 dimension for each key is date
# 1 dimension is flowrate m3/s
# 2 dimension is NO3 in mg/L 
# 3 dimension is NO2 in mg/L 
# 4 dimension is NH4 in mg/L 
# 5              BOD    mg/L 
# 6              COD    mg/L 
# 7              Fe     mg/L 
# 8              SO2    mg/L 
# 9              ON     mg/L  (organic nitrogen?)
# 10             TP     mg/L 
# 11             PO4    mg/L 
# 12             OP     mg/L 
# 13             TOC    mg/L 

locations = list(potw_data.keys())

nutrients = ['date',
             'flow', 
             'NO3',
             'NO2',
             'NH4',
             'BOD',
             'COD',
             'Fe', 
             'SO2',
             'ON',
             'TP', 
             'PO4',
             'OP', 
             'TOC'
                ]

####################################################################
# convert raw data from kg/m3 to mmol/m3
#####################################################################
potw_data_copy = copy.deepcopy(potw_data)


#kg_to_mg = 1000000
# ACTUALLY mg/L, NOT kg/m3, so multiply by 1000 to convert /L to /m3 
kg_to_mg = 1000

# molecular weights 
# N --> 14
# SO2 --> S
# PO4 --> P
# BOD, COD --> 16 
mol_wt_NO3 = 14.007 #62.0
mol_wt_NO2 = 14.007 #46.0
mol_wt_NH4 = 14.007 #18.038 # (units g/mol or mg/mmol)
mol_wt_BOD = 16.0 #32 BOD and COD measured by O2 consumed
mol_wt_Fe = 55.845
mol_wt_SO2 = 32.065 #64.07
mol_wt_ON = 14.007 # organic nitrogen
mol_wt_TP = 30.974 # total phosphorus
mol_wt_PO4 = 30.974 #94.97
mol_wt_OP = 30.974 #organic phosphorous 
mol_wt_TOC = 12.011 # total organic carbon

for location in potw_data.keys():
    for i in range(len(potw_data_copy[location])):
        for j in range(len(potw_data_copy[location][i])):
            if potw_data_copy[location][i][j] == 'NA' or potw_data_copy[location][i][j]==None:
                potw_data_copy[location][i][j] = np.nan

potw_data_converted = copy.deepcopy(potw_data_copy)
               
for location in potw_data.keys():
    print(location) 
    # convert NO3, nitrate, from kg/m3 to mmol/m3 
    potw_data_converted[location][2] = np.asarray(potw_data_copy[location][2],float)*(kg_to_mg)*(1/mol_wt_NO3)
    
    # NO2 convert from kg/m3 to mmol/m3 
    potw_data_converted[location][3] = np.asarray(potw_data_copy[location][3],float)*(kg_to_mg)*(1/mol_wt_NO2)
    
    # NH4 convert from kg/m3 to mmol/m3
    potw_data_converted[location][4] = np.asarray(potw_data_copy[location][4],float)*(kg_to_mg)*(1/mol_wt_NH4)   

    # BOD convert from kg/m3 to mmol/m3
    potw_data_converted[location][5] = np.asarray(potw_data_copy[location][5],float)*(kg_to_mg)*(1/mol_wt_BOD)   

    # COD convert from kg/m3 to mmol/m3
    potw_data_converted[location][6] = np.asarray(potw_data_copy[location][6],float)*(kg_to_mg)*(1/mol_wt_BOD)   

    # Fe convert from kg/m3 to mmol/m3
    potw_data_converted[location][7] = np.asarray(potw_data_copy[location][7],float)*(kg_to_mg)*(1/mol_wt_Fe)   

    # SO2 convert from kg/m3 to mmol/m3
    potw_data_converted[location][8] = np.asarray(potw_data_copy[location][8],float)*(kg_to_mg)*(1/mol_wt_SO2)   

    # ON convert from kg/m3 to mmol/m3
    potw_data_converted[location][9] = np.asarray(potw_data_copy[location][9],float)*(kg_to_mg)*(1/mol_wt_ON)   

    # TP convert from kg/m3 to mmol/m3
    potw_data_converted[location][10] = np.asarray(potw_data_copy[location][10],float)*(kg_to_mg)*(1/mol_wt_TP)   

    # PO4 convert from kg/m3 to mmol/m3
    potw_data_converted[location][11] = np.asarray(potw_data_copy[location][11],float)*(kg_to_mg)*(1/mol_wt_PO4)   

    # OP convert from kg/m3 to mmol/m3
    potw_data_converted[location][12] = np.asarray(potw_data_copy[location][12],float)*(kg_to_mg)*(1/mol_wt_OP)   

    # TOC convert from kg/m3 to mmol/m3
    potw_data_converted[location][13] = np.asarray(potw_data_copy[location][13],float)*(kg_to_mg)*(1/mol_wt_TOC)   

#######################################
# plot timeseries with converted data
#######################################
xlabel_size = 18
ylabel_size = 18
title_size = 24
'''
# plot in separate figures
for location in potw_data.keys(): 
    # plot all nutrient data. nutrient list has strings of each nutrient name
    # and each i corresponds to the data for that nutrient 
    # nutrient list and potw_data have same order of data (see beginning of script for order)
    for i in range(2,len(potw_data[location])): 
        plt.figure(figsize=[14,7])  
        plt.xlabel('Time',fontsize=xlabel_size) 
        plt.ylabel(nutrients[i]+' (mmol/m$^3$)',fontsize=ylabel_size)
        plt.title('Time Series of '+nutrients[i]+' for '+location,fontsize=title_size) 
        plt.plot(potw_data_converted[location][0],potw_data_converted[location][i]) 
        locator = mdate.YearLocator()
        plt.gca().xaxis.set_major_locator(locator)
        plt.gcf().autofmt_xdate() 
        ax = plt.gca()  
        ax.grid(which='both')
        plt.xlim([min(potw_data[location][0]),max(potw_data[location][0])])    
        plt.savefig(save_figs_path+location+'/'+converted_path+location+'_date_vs_'+nutrients[i],bboxinches='tight') 
        plt.close('all')
           
    # date vs flow 
    plt.figure(figsize=[14,7])  
    plt.xlabel('Time',fontsize=xlabel_size) 
    plt.ylabel('Flow (m$^3$/s)',fontsize=ylabel_size)
    plt.title('Time Series of Flow for '+location,fontsize=title_size) 
    plt.plot(potw_data_converted[location][0],potw_data_converted[location][1]) 
    locator = mdate.YearLocator()
    plt.gca().xaxis.set_major_locator(locator)
    plt.gcf().autofmt_xdate() 
    ax = plt.gca()  
    ax.grid(which='both')
    plt.xlim([min(potw_data[location][0]),max(potw_data[location][0])])    
    plt.savefig(save_figs_path+location+'/'+converted_path+location+'_date_vs_flow',bboxinches='tight') 
    plt.close('all')
'''
# plot converted data in subplots for each nutrient
# nutrients to plot: 1:flow, 2:NO3, 3:NO2, 4:NH4, 7:Fe, 11:PO4
title_font = 20
subplot_title_font = 14
color = ['blue','maroon','green','purple','darkorange','goldenrod']
ts_nutrients_fe = [2,3,4,7,11]
ts_nutrients = [2,3,4,11]
OCSD_nutrients = [4,11]
PLWTP_nutrients = [2,4,7,11]
date_1997_index = 313
date_2013_index = 516
fig_w = 14
fig_h = 14
adjust_top = .95
hspace = 0 
tick_label_size = 12

# forward fill iron data for JWPCP to be able to plot
# (get rid of nans)
for j in range(potw_data_converted['JWPCP'][7].shape[0]):
    if np.isnan(potw_data_converted['JWPCP'][7][j]) == True:
        potw_data_converted['JWPCP'][7][j] = potw_data_converted['JWPCP'][7][j-1]
potw_data_converted['JWPCP'][7][433:] = np.nan

for location in potw_data.keys():
# plot PLWTP AND JWPCP with iron data           
    # PLWTP removes NO2 because data is constant
    if location == 'PLWTP':         
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(PLWTP_nutrients)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][1][date_1997_index:date_2013_index],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(PLWTP_nutrients):
            ax = fig.add_subplot(len(PLWTP_nutrients)+1,1,i+PLWTP_nutrients[0],sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][n][date_1997_index:date_2013_index],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != ts_nutrients[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')
    if location == 'JWPCP':
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(ts_nutrients_fe)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][1][date_1997_index:date_2013_index],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(ts_nutrients_fe):
            ax = fig.add_subplot(len(ts_nutrients_fe)+1,1,i+ts_nutrients_fe[0],sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][n][date_1997_index:date_2013_index],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            if n != ts_nutrients[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')
# plot Hyperion and OCSD without iron data (because they have none)
    # plot Hyperion with NO3 and NO2
    if location == 'Hyperion':
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(ts_nutrients)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][1][date_1997_index:date_2013_index],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([]) 
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(ts_nutrients):
            ax = fig.add_subplot(len(ts_nutrients)+1,1,i+ts_nutrients[0],sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][n][date_1997_index:date_2013_index],color=color[i+1])
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            #plt.gcf().autofmt_xdate()
            a.grid(True)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            if n != ts_nutrients[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')  
    # plot OCSD without NO3 and NO2 (because data is constant throughout all years)
    if location == 'OCSD': 
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(OCSD_nutrients)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][1][date_1997_index:date_2013_index],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(OCSD_nutrients):
            ax = fig.add_subplot(len(OCSD_nutrients)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(potw_data_converted[location][0][date_1997_index:date_2013_index],potw_data_converted[location][n][date_1997_index:date_2013_index],color=color[i+1])
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            #plt.gcf().autofmt_xdate()
            a.grid(True)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            if n != OCSD_nutrients[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight') 
 
#################################
# FIND ANNUAL RUNNING AVERAGE
#################################
#range_years = range(1970,2018)
range_years = range(1997,2014) # 1997-2013 for report

potw_annual_data = defaultdict(list)

for location in potw_data.keys():
    potw_annual_data[location] = [ [] for i in range(len(nutrients))]
    for nutrient in range(len(nutrients)): 
        potw_annual_data[location][nutrient] = [ [] for j in range(len(range_years))]

potw_annual_avg = defaultdict(list)
for location in potw_data.keys():
    potw_annual_avg[location] = [ [] for i in range(len(nutrients))]

# sort data by year and append them to each dictionary by year: ex. potw_annual_data[location][nutrient][0] =all_1970_data
'''
for location in potw_data.keys():
    # start with runoff data at 1
    for nutrient in range(1,len(potw_data[location])):
        for d in range(len(potw_data[location][nutrient])):
            year = potw_data[location][0][d+start_year_ind].year
            year = year - range_years[0]
            potw_annual_data[location][nutrient][year].append(potw_data_converted[location][nutrient][d+start_year_ind])
'''
start_year_ind = 313 # start index for year 1997
end_year_ind = 516 # end index for 2013 (PLWTP and Hyperion only)
for location in potw_data.keys():
    # start with runoff data at 1
    for nutrient in range(1,len(potw_data[location])):
        if location == 'PLWTP' or location == 'Hyperion':
            for d in range(len(potw_data[location][nutrient][start_year_ind:end_year_ind])):
                year = potw_data[location][0][d+start_year_ind].year
                year = year - range_years[0]
                potw_annual_data[location][nutrient][year].append(potw_data_converted[location][nutrient][d+start_year_ind])
        else:
            for d in range(len(potw_data[location][nutrient][start_year_ind:])):
                year = potw_data[location][0][d+start_year_ind].year
                year = year - range_years[0]
                potw_annual_data[location][nutrient][year].append(potw_data_converted[location][nutrient][d+start_year_ind])

# append annual averages into list in form of: potw_annual_avg[location][nutrient] = [avg_1970,avg_1971,...] 
for location in potw_data.keys():
    for nutrient in range(1,len(potw_annual_data[location])):
        for year in range(len(range_years)):
            potw_annual_avg[location][nutrient].append(np.nanmean(potw_annual_data[location][nutrient][year])) 
            if len(potw_annual_data[location][nutrient][year])==0:
                potw_annual_data[location][nutrient][year] = np.nan

'''
#############################
# plot annual averages
#############################
for location in potw_data.keys(): 
    # date vs flow 
    plt.figure(figsize=[14,7])  
    plt.xlabel('Time') 
    plt.ylabel('Flow (m$^3$/s)')
    plt.title('Time Series of Average Annual Flow for '+location) 
    plt.plot(range_years,potw_annual_avg[location][1]) 
    ax = plt.gca()  
    ax.grid(which='both')
    plt.xlim([range_years[0],range_years[-1]])
    plt.xticks(range(range_years[0],range_years[-1]+1,3))
    plt.savefig(save_figs_path+location+'/'+avg_path+location+'_avg_date_vs_flow',bboxinches='tight') 
    plt.close('all')    
 
    for i in range(2,len(potw_data[location])): 
        plt.figure(figsize=[14,7])  
        plt.xlabel('Time') 
        plt.ylabel(nutrients[i]+' (mmol/m$^3$)')
        plt.title('Time Series of Average Annual '+nutrients[i]+' for '+location) 
        plt.plot(range_years,potw_annual_avg[location][i])  
        ax = plt.gca()  
        ax.grid(which='both')
        plt.xlim([range_years[0],range_years[-1]])    
        plt.xticks(range(range_years[0],range_years[-1]+1,3)) 
        plt.savefig(save_figs_path+location+'/'+avg_path+location+'_avg_date_vs_'+nutrients[i],bboxinches='tight') 
        plt.close('all')
'''                   
 
################################
# FIND SEASONAL VARIABILITY
################################
 
# "day of year" ranges for the northern hemisphere
spring = range(80, 172)
summer = range(172, 264)
fall = range(264, 355)

potw_seasonal_data = defaultdict(list)
for location in potw_data.keys():
    potw_seasonal_data[location] = [ [] for i in range(len(nutrients))]
    for nutrient in range(len(potw_seasonal_data[location])):
        # create 4 lists within each nutrient for data for each season (spring will be 0, summer 1, etc)
        potw_seasonal_data[location][nutrient] = [ [] for j in range(4) ]

for location in potw_data.keys():
    for nutrient in range(len(potw_seasonal_data[location])):
        for d in range(len(potw_data[location][0])):
            # get day of year in a tuple form 
            tuple_date = datetime.datetime.timetuple(potw_data[location][0][d]).tm_yday
            # append seasonal data to appropriate season 
            if tuple_date in spring:
                potw_seasonal_data[location][nutrient][0].append(potw_data_converted[location][nutrient][d])
                     
            elif tuple_date in summer:   
                potw_seasonal_data[location][nutrient][1].append(potw_data_converted[location][nutrient][d])

            elif tuple_date in fall:
                potw_seasonal_data[location][nutrient][2].append(potw_data_converted[location][nutrient][d])

            else:
                potw_seasonal_data[location][nutrient][3].append(potw_data_converted[location][nutrient][d])

#################################
# find average of seasons
##################################
potw_seasonal_avg = defaultdict(list)
# average seasonal data stored as such: potw_seasonal_avg[location][nutrient] = [avg_spring,avg_summer,...]

for location in potw_data.keys():
    potw_seasonal_avg[location] = [ [] for i in range(len(nutrients))]
    for nutrient in range(1,len(potw_seasonal_data[location])):
        for season in range(4):
            potw_seasonal_avg[location][nutrient].append(np.nanmean(potw_seasonal_data[location][nutrient][season]))       
'''
###########################
# plot seasonal average
###########################
for location in potw_data.keys(): 
    # date vs flow 
    plt.figure(figsize=[14,7])  
    plt.xlabel('Season') 
    plt.ylabel('Flow (m$^3$/s)')
    plt.title('Average Seasonal Flow for '+location) 
    plt.plot(potw_seasonal_avg[location][1]) 
    plt.xticks([0,1,2,3],['Spring','Summer','Fall','Winter']) 
    ax = plt.gca()  
    ax.grid(which='both')
    plt.savefig(save_figs_path+location+'/'+seasonal_path+location+'_seasonal_date_vs_flow',bboxinches='tight') 
    plt.close('all')    
 
    for i in range(2,len(potw_data[location])): 
        plt.figure(figsize=[14,7])  
        plt.xlabel('Season') 
        plt.ylabel(nutrients[i]+' (mmol/m$^3$)')
        plt.title('Seasonal Average of '+nutrients[i]+' for '+location) 
        plt.plot(potw_seasonal_avg[location][i])  
        plt.xticks([0,1,2,3],['Spring','Summer','Fall','Winter'])        
        ax = plt.gca()  
        ax.grid(which='both')    
        plt.savefig(save_figs_path+location+'/'+seasonal_path+location+'_seasonal_date_vs_'+nutrients[i],bboxinches='tight') 
        plt.close('all')
'''

################################################
# STATISTICS
# find mean over all data, standard deviation, max, and min values
################################################
# contains standard deviation of converted data from all data points over all yaers for each nutrient
converted_std = defaultdict(list)

# find max and min values for converted data, annual, and seasonal
# within each location and nutrient,
# 0 is max/min for converted data, 1 is annual_avg_data, 2 is seasonal data
# ex. max_value[location][nutrient][0] = max_value_converted_data
#     max_value[location][nutrient][1][year] = max_value_of_that_year (starting from 1970)
max_values = defaultdict(list)
min_values = defaultdict(list)
mean_values = defaultdict(list)

# contains std of annual averages for each nutrient
annual_avg_std = defaultdict(list)

# contains std of each season over all years 
seasonal_std = defaultdict(list)

start_ind = 313 # start index for year 1997
end_ind = 516 # end index for 2013 (PLWTP and Hyperion only)
for location in potw_data.keys():
    converted_std[location] = [ [] for i in range(len(nutrients))]
    max_values[location] = [ [] for i in range(len(nutrients))]
    min_values[location] = [ [] for i in range(len(nutrients))]
    annual_avg_std[location] = [ [] for i in range(len(nutrients))]
    seasonal_std[location] = [ [] for i in range(len(nutrients))]
    mean_values[location] = [ [] for i in range(len(nutrients))]
    for nutrient in range(1,len(nutrients)):
        # create 4 lists within each nutrient for data for each season (spring will be 0, summer 1, etc)
        seasonal_std[location][nutrient] = [ [] for j in range(4) ]
               
        # create a list for each year within each nutrient with yearly data
        # annual_avg_data[location][nutrient][year] = all_data_for_a_year 
        annual_avg_std[location][nutrient] = [ [] for j in range(len(range_years))]

        # create list for converted, annual, and seasonal data 
        max_values[location][nutrient] = [ [] for i in range(3)]
        min_values[location][nutrient] = [ [] for i in range(3)]

# create 4 more lists within the seasonal data category to append data for each season
# and create lists of number of years to put max/min value for each year
for location in potw_data.keys():
    for nutrient in range(1,len(nutrients)):
        max_values[location][nutrient][2] = [ [] for i in range(4)]
        min_values[location][nutrient][2] = [ [] for i in range(4)]

        max_values[location][nutrient][1] = [ [] for i in range(len(range_years))]
        min_values[location][nutrient][1] = [ [] for i in range(len(range_years))]

# standard deviation, mean, and max/min calculation
for location in potw_data.keys():
    for nutrient in range(1,len(potw_data[location])):
        if location == 'JWPCP' or location == 'OCSD':
            converted_std[location][nutrient] = np.nanstd(potw_data_converted[location][nutrient][start_ind:])
            max_values[location][nutrient][0] = np.nanmax(potw_data_converted[location][nutrient][start_ind:])
        # find nonzero minimum 
            min_values[location][nutrient][0] = np.nanmin(np.asarray(potw_data_converted[location][nutrient][start_ind:])[np.nonzero(potw_data_converted[location][nutrient][start_ind:])])
            mean_values[location][nutrient] = np.nanmean(potw_data_converted[location][nutrient][start_ind:])

        elif location == 'Hyperion' or location == 'PLWTP':
            converted_std[location][nutrient] = np.nanstd(potw_data_converted[location][nutrient][start_ind:end_ind])
            max_values[location][nutrient][0] = np.nanmax(potw_data_converted[location][nutrient][start_ind:end_ind])
        # find nonzero minimum 
            min_values[location][nutrient][0] = np.nanmin(np.asarray(potw_data_converted[location][nutrient][start_ind:end_ind])[np.nonzero(potw_data_converted[location][nutrient][start_ind:end_ind])])
            mean_values[location][nutrient] = np.nanmean(potw_data_converted[location][nutrient][start_ind:end_ind])

        for year in range(len(range_years)): 
            annual_avg_std[location][nutrient][year] = np.nanstd(potw_annual_data[location][nutrient][year])
                       
            # error occurs when taking max/min of empty list; this bypasses that error             
            try:
                max_values[location][nutrient][1][year] = np.nanmax(potw_annual_data[location][nutrient][year])
                min_values[location][nutrient][1][year] = np.nanmin(np.asarray(potw_annual_data[location][nutrient][year])[np.nonzero(potw_annual_data[location][nutrient][year])])
         
            except (ValueError,IndexError): 
                min_values[location][nutrient][1][year] = np.nan 
                max_values[location][nutrient][1][year] = np.nan 

        for season in range(len(seasonal_std[location][nutrient])): 
            seasonal_std[location][nutrient][season] = np.nanstd(potw_seasonal_data[location][nutrient][season])
            # find max and min data that corresponds to each season
            max_values[location][nutrient][2][season] = np.nanmax(potw_seasonal_data[location][nutrient][season])
            min_values[location][nutrient][2][season] = np.nanmin(np.asarray(potw_seasonal_data[location][nutrient][season])[np.nonzero(potw_seasonal_data[location][nutrient][season])]) 
        print(location,nutrients[nutrient],"{0:.3f}".format(mean_values[location][nutrient])+' & '+"{0:.3f}".format(converted_std[location][nutrient])+' & '+"{0:.3f}".format(max_values[location][nutrient][0])+' & '+"{0:.3f}".format(min_values[location][nutrient][0]))

''' 
#############################################################################
# PLOT MIN/MAX DATA
# # 0 is max/min for converted data, 1 is annual_avg_data, 2 is seasonal data
# min_values[location][nutrient][0] = min_converted_data
#############################################################################
for location in potw_data.keys(): 

    # plot max annual data flow
    plt.figure(figsize=[14,7])  
    plt.xlabel('Time',fontsize=xlabel_size) 
    plt.ylabel('Flow (m$^3$/s)',fontsize=ylabel_size)
    plt.title('Time Series of Maximum Annual Flow for '+location,fontsize=title_size) 
    plt.plot(range_years,max_values[location][1][1],'-k') 
    ax = plt.gca()  
    ax.grid(which='both')
    plt.xlim([range_years[0],range_years[-1]])
    plt.xticks(range(range_years[0],range_years[-1]+1,2))
    plt.savefig(save_figs_path+location+'/'+max_path+location+'_max_date_vs_flow',bboxinches='tight') 
    plt.close('all')    

    # plot min annual data flow
    plt.figure(figsize=[14,7])  
    plt.xlabel('Time',fontsize=xlabel_size) 
    plt.ylabel('Flow (m$^3$/s)',fontsize=ylabel_size)
    plt.title('Time Series of Minimum Annual Flow for '+location,fontsize=title_size) 
    plt.plot(range_years,min_values[location][1][1],'-k') 
    ax = plt.gca()  
    ax.grid(which='both')
    plt.xlim([range_years[0],range_years[-1]])
    plt.xticks(range(range_years[0],range_years[-1]+1,2))
    plt.savefig(save_figs_path+location+'/'+min_path+location+'_min_date_vs_flow',bboxinches='tight') 
    plt.close('all')    


    
    for i in range(2,len(max_values[location])):
        # plot max annual nutrient data
        plt.figure(figsize=[14,7])  
        plt.xlabel('Time',fontsize=xlabel_size) 
        plt.ylabel(nutrients[i]+' (mmol/m$^3$)',fontsize=ylabel_size)
        plt.title('Time Series of Maximum Annual '+nutrients[i]+' for ' +location,fontsize=title_size) 
        plt.plot(range_years,max_values[location][i][1],'-k') 
        ax = plt.gca()  
        ax.grid(which='both')
        plt.xlim([range_years[0],range_years[-1]])
        plt.xticks(range(range_years[0],range_years[-1]+1,2))
        plt.savefig(save_figs_path+location+'/'+max_path+location+'_max_date_vs_'+nutrients[i],bboxinches='tight') 
        plt.close('all')             

        # plot min annual nutrient data
        plt.figure(figsize=[14,7])  
        plt.xlabel('Time',fontsize=xlabel_size) 
        plt.ylabel(nutrients[i] +' (m$^3$/s)',fontsize=ylabel_size)
        plt.title('Time Series of Minimum Annual '+nutrients[i]+' for ' +location,fontsize=title_size) 
        plt.plot(range_years,min_values[location][i][1],'-k') 
        ax = plt.gca()  
        ax.grid(which='both')
        plt.xlim([range_years[0],range_years[-1]])
        plt.xticks(range(range_years[0],range_years[-1]+1,2))
        plt.savefig(save_figs_path+location+'/'+min_path+location+'_min_date_vs_'+nutrients[i],bboxinches='tight') 
        plt.close('all')             
'''

###############################################################
# REplot annual averages with standard deviation as error bars
###############################################################
title_font = 20
subplot_title_font = 14
ts_nutrients_fe = [2,3,4,7,11]
ts_nutrients = [2,3,4,11]
OCSD_nutrients = [4,11]
PLWTP_nutrients = [2,4,7,11]
date_1997_index = 313
date_2013_index = 516
fig_w = 12
fig_h = 14
adjust_top = .95
hspace = 0 
tick_label_size = 12
color_line = 'navy'

# PLOT WITH SUBPLOTS
for location in potw_data.keys():
# plot PLWTP AND JWPCP with iron data           
    # PLWTP removes NO2 because data is constant
    if location == 'PLWTP':         
        nutrient_list = PLWTP_nutrients
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_list)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(range_years,potw_annual_avg[location][1],linestyle='-',color=color_line) 
        plt.fill_between(range_years,np.asarray(potw_annual_avg[location][1])-np.asarray(annual_avg_std[location][1]),np.asarray(potw_annual_avg[location][1])+np.asarray(annual_avg_std[location][1]),facecolor='lightblue')
        a = plt.gca()
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_list):
            ax = fig.add_subplot(len(nutrient_list)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(range_years,potw_annual_avg[location][n],linestyle='-',color=color[i+1]) 
            plt.fill_between(range_years,np.asarray(potw_annual_avg[location][n])-np.asarray(annual_avg_std[location][n]),np.asarray(potw_annual_avg[location][n])+np.asarray(annual_avg_std[location][n]),facecolor='lightblue')
            a = plt.gca()
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            plt.xticks(range_years)
            a.axes.xaxis.set_ticklabels(range_years)
            if n != nutrient_list[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_avg_ts.png',bbox_inches='tight')

    if location == 'JWPCP':         
        nutrient_list = ts_nutrients_fe
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_list)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(range_years,potw_annual_avg[location][1],linestyle='-',color=color_line) 
        plt.fill_between(range_years,np.asarray(potw_annual_avg[location][1])-np.asarray(annual_avg_std[location][1]),np.asarray(potw_annual_avg[location][1])+np.asarray(annual_avg_std[location][1]),facecolor='lightblue')
        a = plt.gca()
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.set_xticks(np.array(range_years)) 
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_list):
            ax = fig.add_subplot(len(nutrient_list)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(range_years,potw_annual_avg[location][n],linestyle='-',color=color[i+1]) 
            plt.fill_between(range_years,np.asarray(potw_annual_avg[location][n])-np.asarray(annual_avg_std[location][n]),np.asarray(potw_annual_avg[location][n])+np.asarray(annual_avg_std[location][n]),facecolor='lightblue')
            a = plt.gca()
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            #plt.xticks(range_years)
            a.axes.xaxis.set_ticklabels(range_years)
            if n != nutrient_list[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_avg_ts.png',bbox_inches='tight')

    if location == 'Hyperion':         
        nutrient_list = ts_nutrients
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_list)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(range_years,potw_annual_avg[location][1],linestyle='-',color=color_line) 
        plt.fill_between(range_years,np.asarray(potw_annual_avg[location][1])-np.asarray(annual_avg_std[location][1]),np.asarray(potw_annual_avg[location][1])+np.asarray(annual_avg_std[location][1]),facecolor='lightblue')
        a = plt.gca()
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_list):
            ax = fig.add_subplot(len(nutrient_list)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(range_years,potw_annual_avg[location][n],linestyle='-',color=color[i+1]) 
            plt.fill_between(range_years,np.asarray(potw_annual_avg[location][n])-np.asarray(annual_avg_std[location][n]),np.asarray(potw_annual_avg[location][n])+np.asarray(annual_avg_std[location][n]),facecolor='lightblue')
            a = plt.gca()
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            plt.xticks(range_years)
            a.axes.xaxis.set_ticklabels(range_years)
            if n != nutrient_list[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_avg_ts.png',bbox_inches='tight')

    if location == 'OCSD':         
        nutrient_list = OCSD_nutrients
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_list)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(range_years,potw_annual_avg[location][1],linestyle='-',color=color_line) 
        plt.fill_between(range_years,np.asarray(potw_annual_avg[location][1])-np.asarray(annual_avg_std[location][1]),np.asarray(potw_annual_avg[location][1])+np.asarray(annual_avg_std[location][1]),facecolor='lightblue')
        a = plt.gca()
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        ax.set_xticks(np.array(range_years)) 
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_list):
            ax = fig.add_subplot(len(nutrient_list)+1,1,i+2)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(range_years,potw_annual_avg[location][n],linestyle='-',color=color[i+1]) 
            plt.fill_between(range_years,np.asarray(potw_annual_avg[location][n])-np.asarray(annual_avg_std[location][n]),np.asarray(potw_annual_avg[location][n])+np.asarray(annual_avg_std[location][n]),facecolor='lightblue')
            a = plt.gca()
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            plt.xticks(range_years)
            a.axes.xaxis.set_ticklabels(range_years)
            if n != nutrient_list[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_avg_ts.png',bbox_inches='tight')




'''
# plot average with standard deviation in separate plots 
for location in potw_data.keys(): 
    # date vs flow 
    plt.figure(figsize=[14,7])  
    plt.xlabel('Time',fontsize=xlabel_size) 
    plt.ylabel('Flow (m$^3$/s)',fontsize=ylabel_size)
    plt.title('Time Series of Average Annual Flow for '+location,fontsize=title_size) 
    plt.plot(range_years,potw_annual_avg[location][1],'-k') 
    plt.fill_between(range_years,np.asarray(potw_annual_avg[location][1])-np.asarray(annual_avg_std[location][1]),np.asarray(potw_annual_avg[location][1])+np.asarray(annual_avg_std[location][1]),facecolor='lightblue')
    ax = plt.gca()  
    ax.grid(which='both')
    plt.xlim([range_years[0],range_years[-1]])
    plt.xticks(range(range_years[0],range_years[-1]+1,2))
    plt.savefig(save_figs_path+location+'/'+avg_path+location+'_avg_date_vs_flow',bboxinches='tight') 
    plt.close('all')    
 
    for i in range(2,len(potw_data[location])): 
        plt.figure(figsize=[14,7])  
        plt.xlabel('Time',fontsize=xlabel_size) 
        plt.ylabel(nutrients[i]+' (mmol/m$^3$)',fontsize=ylabel_size)
        plt.title('Time Series of Average Annual '+nutrients[i]+' for '+location,fontsize=title_size) 
        plt.plot(range_years,potw_annual_avg[location][i],'-k')  
        plt.fill_between(range_years,np.asarray(potw_annual_avg[location][i])-np.asarray(annual_avg_std[location][i]),np.asarray(potw_annual_avg[location][i])+np.asarray(annual_avg_std[location][i]),facecolor='lightblue')
        ax = plt.gca()  
        ax.grid(which='both')
        plt.xlim([range_years[0],range_years[-1]])    
        plt.xticks(range(range_years[0],range_years[-1]+1,2)) 
        plt.savefig(save_figs_path+location+'/'+avg_path+location+'_avg_date_vs_'+nutrients[i],bboxinches='tight') 
        plt.close('all')
'''
 
'''
################################################
# manually change x limits for data without certain years
#################################################

location_p = 'PLWTP'

# converted time series PLWTP
# Fe
plt.figure(figsize=[14,7])  
plt.xlabel('Time',fontsize=xlabel_size) 
plt.ylabel(nutrients[7]+' (mmol/m$^3$)',fontsize=ylabel_size)
plt.title('Time Series of '+nutrients[7]+' for '+location_p,fontsize=title_size) 
plt.plot(potw_data_converted[location_p][0],potw_data_converted[location_p][7]) 
locator = mdate.YearLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate() 
ax = plt.gca()  
ax.grid(which='both')
plt.xlim([potw_data_converted[location_p][0][313],potw_data_converted[location_p][0][517]])    
plt.savefig(save_figs_path+location_p+'/'+converted_path+location_p+'_date_vs_'+nutrients[7],bboxinches='tight') 
plt.close('all')

# SO2
plt.figure(figsize=[14,7])  
plt.xlabel('Time',fontsize=xlabel_size) 
plt.ylabel(nutrients[8]+' (mmol/m$^3$)',fontsize=ylabel_size)
plt.title('Time Series of '+nutrients[8]+' for '+location_p,fontsize=title_size) 
plt.plot(potw_data_converted[location_p][0],potw_data_converted[location_p][8]) 
locator = mdate.YearLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate() 
ax = plt.gca()  
ax.grid(which='both')
plt.xlim([potw_data_converted[location_p][0][349],potw_data_converted[location_p][0][517]])    
plt.savefig(save_figs_path+location_p+'/'+converted_path+location_p+'_date_vs_'+nutrients[8],bboxinches='tight') 
plt.close('all')


# annual average for PLWTP
# Fe
plt.figure(figsize=[14,7])
plt.xlabel('Time',fontsize=xlabel_size)
plt.ylabel(nutrients[7]+' (mmol/m$^3$)',fontsize=ylabel_size)
plt.title('Time Series of Average Annual '+nutrients[7]+' for '+location_p,fontsize=title_size)
plt.plot(range_years,potw_annual_avg[location_p][7],'-k')
plt.fill_between(range_years,np.asarray(potw_annual_avg[location_p][7])-np.asarray(annual_avg_std[location_p][7]),np.asarray(potw_annual_avg[location_p][7])+np.asarray(annual_avg_std[location_p][7]),facecolor='lightblue')
ax = plt.gca()
ax.grid(which='both')
plt.xticks(range(range_years[0],range_years[-1]+1,2))
plt.xlim([1997,2013])
plt.savefig(save_figs_path+location_p+'/'+avg_path+location_p+'_avg_date_vs_'+nutrients[7],bboxinches='tight')

# SO2
plt.figure(figsize=[14,7])
plt.xlabel('Time',fontsize=xlabel_size)
plt.ylabel(nutrients[8]+' (mmol/m$^3$)',fontsize=ylabel_size)
plt.title('Time Series of Average Annual '+nutrients[8]+' for '+location_p,fontsize=title_size)
plt.plot(range_years,potw_annual_avg[location_p][8],'-k')
plt.fill_between(range_years,np.asarray(potw_annual_avg[location_p][8])-np.asarray(annual_avg_std[location_p][8]),np.asarray(potw_annual_avg[location_p][8])+np.asarray(annual_avg_std[location_p][8]),facecolor='lightblue')
ax = plt.gca()
ax.grid(which='both')
plt.xticks(range(range_years[0],range_years[-1]+1,2))
plt.xlim([2000,2013])
plt.savefig(save_figs_path+location_p+'/'+avg_path+location_p+'_avg_date_vs_'+nutrients[8],bboxinches='tight')


'''
###############################
# save dicts to add to excel 
# in write_to_excel.py
###############################
pickle.dump(potw_data_converted,open('potw_data_converted.pkl','wb'))
pickle.dump(potw_annual_avg,open('potw_annual_avg.pkl','wb'))
pickle.dump(potw_seasonal_avg,open('potw_seasonal_avg.pkl','wb'))
pickle.dump(annual_avg_std,open('potw_annual_avg_std.pkl','wb'))
pickle.dump(converted_std,open('potw_converted_std.pkl','wb'))
pickle.dump(seasonal_std,open('potw_seasonal_std.pkl','wb'))
pickle.dump(max_values,open('potw_max.pkl','wb'))
pickle.dump(min_values,open('potw_min.pkl','wb'))
pickle.dump(mean_values,open('potw_mean.pkl','wb'))

