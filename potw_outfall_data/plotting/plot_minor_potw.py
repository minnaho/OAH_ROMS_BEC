################################
# make netCDF4 file of minor POTW data
# use ncdump -h minor_potw_data_converted.nc
# to see details of file
###############################
from netCDF4 import Dataset
import pickle
import numpy as np
import datetime
from netCDF4 import num2date, date2num
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

save_figs_path = '../minor_potw_figs/'

# load data from dictionary that was created 
# in make_netcdf.py
minor_potw_data = pickle.load(open('minor_potw_data_converted.pkl','rb'))

# 0 dimension for each key is date
# 1 dimension is flowrate m^3/s
# 2 dimension is NO3  
# 3 dimension is NO2  
# 4 dimension is NH4  
# 5              BOD    
# 6              ON      
# 7              PO4    
# 8              OP     
# 9              TOC    

minors = [  'OO1-South Bay',
            'OO3-San Clemente Island WWTP',
            'OO4-San Elijo Ocean Outfall',
            'OO5-Encina Ocean Outfall',
            'OO6-Oceanside Ocean Outfall',
            'OO7-Avalon WWTF',
            'OO8-San Juan Creek Outfall',
            'OO9-Aliso Creek Ocean Outfall',
            'OO12-Terminal Island WWTP',
            'OO14-Oxnard WWTP',
            'OO15-Carpinteria WWTP',
            'OO16-El Estero WWTP',
            'OO18-Montecito WWTP',
            'OO19-Summerland WWTP'
          ]

# get rid of the OO1-,OO2-, etc
for j,m in enumerate(minors):
    i = m.index('-')+1
    minors[j] = m[i:] 

# convert data to mmol/m3
mgL_to_mgm3 = 1000


mol_wt_N = 14
mol_wt_P = 30.974
mol_wt_BOD = 16.0

# create dictionary for converted data
minor_potw_data_converted = defaultdict(list)
for plant in minors:
    minor_potw_data_converted[plant] = [ [] for i in range(len(minor_potw_data[plant]))]

# converted data calculations
for plant in minors:
    #print(plant)
    minor_potw_data_converted[plant][1] = np.asarray(minor_potw_data[plant][1],float)
    # nitrogen compounds
    for n in range(2,5):
        minor_potw_data_converted[plant][n] = np.asarray(minor_potw_data[plant][n],float)*(mgL_to_mgm3)*(1./mol_wt_N)
    minor_potw_data_converted[plant][6] = np.asarray(minor_potw_data[plant][6],float)*(mgL_to_mgm3)*(1./mol_wt_N)
    

    # BOD & TOC       
    minor_potw_data_converted[plant][5] = np.asarray(minor_potw_data[plant][5],float)*(mgL_to_mgm3)*(1./mol_wt_BOD)
    minor_potw_data_converted[plant][9] = np.asarray(minor_potw_data[plant][9],float)*(mgL_to_mgm3)*(1./mol_wt_BOD)
        
    # phophorus compounds
    for p in range(7,9):
        minor_potw_data_converted[plant][p] = np.asarray(minor_potw_data[plant][p],float)*(mgL_to_mgm3)*(1./mol_wt_P)

nutrients = ['date',
             'flow',
             'NO3',
             'NO2',        
             'NH4',              
             'BOD',  
             'ON', 
             'PO4',
             'OP',
             'TOC']

##############
# PLOT DATA
#############
'''
# plot data in separate graphs
for p in minors:
    # plot all nutrient data. nutrient list has strings of each nutrient name
    # and each n corresponds to the data for that nutrient
    # nutrient list and minor_potw_data have same order of data (see beginning of script for order)
    for n in range(2,len(nutrients)):
        plt.figure(figsize=[14,7])
        plt.xlabel('Time',fontsize=xlabel_size)
        plt.ylabel(nutrients[n]+' (mmol/m$^3$)',fontsize=ylabel_size)
        plt.title('Time Series of '+nutrients[n]+' for '+p,fontsize=title_size)
        plt.plot(minor_potw_data[p][0],minor_potw_data_converted[p][n])
        locator = mdate.YearLocator()
        plt.gca().xaxis.set_major_locator(locator)
        plt.gcf().autofmt_xdate()
        ax = plt.gca()
        ax.grid(which='both')
        plt.xlim([min(minor_potw_data[p][0]),max(minor_potw_data[p][0])])
        plt.savefig(save_figs_path+p+'_date_vs_'+nutrients[n],bboxinches='tight')
        plt.close('all')
    # date vs flow
    plt.figure(figsize=[14,7])
    plt.xlabel('Time',fontsize=xlabel_size)
    plt.ylabel('Flow (m$^3$/s)',fontsize=ylabel_size)
    plt.title('Time Series of Flow for '+p,fontsize=title_size)
    plt.plot(minor_potw_data[p][0],minor_potw_data_converted[p][1])
    locator = mdate.YearLocator()
    plt.gca().xaxis.set_major_locator(locator)
    plt.gcf().autofmt_xdate()
    ax = plt.gca()
    ax.grid(which='both')
    plt.xlim([min(minor_potw_data[p][0]),max(minor_potw_data[p][0])])
    plt.savefig(save_figs_path+p+'_date_vs_flow',bboxinches='tight')
    plt.close('all')        
'''      
'''
# plot converted data in subplots for each nutrient
# nutrients to plot: 1:flow, 2:NO3, 3:NO2, 4:NH4, 7:Fe, 11:PO4, 5: BOD
title_font = 20
subplot_title_font = 14
color = ['blue','maroon','green','purple','y']
nutrient_list = [2,4,5]
nutrient_NO2 = [2,3,4,5]
nutrient_no_BOD = [2,4]
nutrient_OO4 = [4]
nutrient_no_NO3 = [4,5]
# put end index before the dates turn to daily because data is repeated
# and collapsed together at the end
end_ind = -49
fig_w = 14
fig_h = 14
adjust_top = .95
hspace = 0 
tick_label_size = 13
location_no_NO3 = ['OO5-Encina Ocean Outfall','OO6-Oceanside Ocean Outfall','OO8-San Juan Creek Outfall','OO9-Aliso Creek Ocean Outfall','OO16-El Estero WWTP']
location_no_BOD = ['OO3-San Clemente Island WWTP','OO12-Terminal Island WWTP','OO15-Carpinteria WWTP']

for location in minor_potw_data.keys():
    print(location)
    if location == 'OO14-Oxnard WWTP':
        nutrient_plot = nutrient_NO2
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')
 
    if location == 'OO4-San Elijo Ocean Outfall':
        nutrient_plot = nutrient_OO4
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')

    if location in location_no_BOD:
        nutrient_plot = nutrient_no_BOD
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')

    if location in location_no_NO3:
        nutrient_plot = nutrient_no_NO3
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')

    elif location not in location_no_NO3 and location not in location_no_BOD and location != 'OO14-Oxnard WWTP' and location != 'OO4-San Elijo Ocean Outfall':
        nutrient_plot = nutrient_list
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.YearLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.YearLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_ts.png',bbox_inches='tight')
'''

# plot converted data in subplots for each nutrient for 1 year
# nutrients to plot: 1:flow, 2:NO3, 3:NO2, 4:NH4, 7:Fe, 11:PO4
title_font = 20
subplot_title_font = 14
color = ['blue','maroon','green','purple','y']
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
nutrient_list = [2,4]
nutrient_NO2 = [2,3,4]
nutrient_no_BOD = [2,4]
nutrient_OO4 = [4]
nutrient_no_NO3 = [4]
# put end index at the end of 1 year 
end_ind = 12 
fig_w = 10
fig_h = 8.5
adjust_top = .95
hspace = 0 
tick_label_size = 13
location_no_NO3 = ['OO5-Encina Ocean Outfall','OO6-Oceanside Ocean Outfall','OO8-San Juan Creek Outfall','OO9-Aliso Creek Ocean Outfall','OO16-El Estero WWTP']
location_no_BOD = ['OO3-San Clemente Island WWTP','OO12-Terminal Island WWTP','OO15-Carpinteria WWTP']

for location in minor_potw_data.keys():
    print(location)
    if location == 'OO14-Oxnard WWTP':
        nutrient_plot = nutrient_NO2
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.MonthLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels(months)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.MonthLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
            a.axes.xaxis.set_ticklabels(months)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_1year_ts.png',bbox_inches='tight')
 
    if location == 'OO4-San Elijo Ocean Outfall':
        nutrient_plot = nutrient_OO4
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.MonthLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels(months)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.MonthLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)  
            a.axes.xaxis.set_ticklabels(months)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_1year_ts.png',bbox_inches='tight')

    if location in location_no_BOD:
        nutrient_plot = nutrient_no_BOD
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.MonthLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True) 
        a.axes.xaxis.set_ticklabels(months)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.MonthLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size)  
            a.axes.xaxis.set_ticklabels(months)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_1year_ts.png',bbox_inches='tight')

    if location in location_no_NO3:
        nutrient_plot = nutrient_no_NO3
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.MonthLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True) 
        a.axes.xaxis.set_ticklabels(months)
        a.axes.xaxis.set_ticklabels([])
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.MonthLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size) 
            a.axes.xaxis.set_ticklabels(months)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_1year_ts.png',bbox_inches='tight')

    elif location not in location_no_NO3 and location not in location_no_BOD and location != 'OO14-Oxnard WWTP' and location != 'OO4-San Elijo Ocean Outfall':
        nutrient_plot = nutrient_list
        fig = plt.figure(figsize=[fig_w,fig_h]) 
        ax = fig.add_subplot(len(nutrient_plot)+1,1,1)
        ax.set_ylabel(nutrients[1]+' m$^3$ s$^{-1}$',fontsize=subplot_title_font)
        plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][1][:end_ind],color=color[0]) 
        locator = mdate.MonthLocator()
        a = plt.gca()
        a.xaxis.set_major_locator(locator)
        #plt.gcf().autofmt_xdate()
        a.grid(True)
        a.axes.xaxis.set_ticklabels([]) 
        a.axes.xaxis.set_ticklabels(months)
        ax.tick_params(axis='both',which='major',labelsize=tick_label_size)
        for i,n in enumerate(nutrient_plot):
            ax = fig.add_subplot(len(nutrient_plot)+1,1,i+2,sharex=ax)
            ax.set_ylabel(nutrients[n]+' mmol m$^{-3}$',fontsize=subplot_title_font)
            plt.plot(minor_potw_data[location][0][:end_ind],minor_potw_data[location][n][:end_ind],color=color[i+1]) 
            locator = mdate.MonthLocator()
            a = plt.gca()
            a.xaxis.set_major_locator(locator)
            ax.tick_params(axis='both',which='major',labelsize=tick_label_size) 
            a.axes.xaxis.set_ticklabels(months)
            #plt.gcf().autofmt_xdate()
            a.grid(True) 
            if n != nutrient_plot[-1]:
                a.axes.xaxis.set_ticklabels([])
        plt.suptitle(location,fontsize=title_font)
        plt.subplots_adjust(top=adjust_top)
        fig.subplots_adjust(hspace=hspace)       
        plt.savefig(save_figs_path+location+'_1year_ts.png',bbox_inches='tight')
