# calculate effluent constiutent values 
# and RO reject values based on
# water treatment recovery efficiency
# % TIN removal
# water recycling goals
import numpy as np

############
# WATER VOLUME FOR RECYCLING
############
# total influent volume, starting volume
vol_st = 2.42

# percent of influent going to recycling treatment plant
#per_re = 0.75
per_re = .5
#per_re = .9

# volume of influent going to recycling treatment plant
vol_in = vol_st*per_re

# water recovery efficiency
#rec_eff = 0.76
rec_eff = 0.8
#rec_eff = 0.82
#rec_eff = 0.85
#rec_eff = 0.87 # oc san
#rec_eff = 0.9

# return brine volume
vol_br = vol_in*(1-rec_eff)

# volume water recycled
vol_re = vol_in*rec_eff

# volume of effluent
vol_ef = vol_br+(vol_st-vol_in)

#######################
# CONSTITUENTS NITROGEN
######################

# DIN percent removal
nh4_rem = .95
no3_rem = .85
#din_rem = .85
#din_rem = .90
#din_rem = .95

# influent DIN conc (mg/L)
# nitrification
#nh4_in = 1
#no3_in = 34

# partial NDN
nh4_in = 500.15
no3_in = 928.85

# full NDN
#nh4_in = 1
#no3_in = 4

din_in = nh4_in+no3_in

# RO permeate cocentration
nh4_pm = nh4_in*(1-nh4_rem)
no3_pm = no3_in*(1-no3_rem)

# RO reject cocentration
nh4_rj = (nh4_in-nh4_pm)/(1-rec_eff)
no3_rj = (no3_in-no3_pm)/(1-rec_eff)

din_pm = nh4_pm+no3_pm
din_rj = nh4_rj+no3_rj

###############
# final effluent
##############

nh4_fi = ((nh4_rj*vol_br)+((vol_st-vol_in)*nh4_in))/vol_ef
no3_fi = ((no3_rj*vol_br)+((vol_st-vol_in)*no3_in))/vol_ef
