# extract time series from model
# at certain grid points
import subprocess as subprocess

out_path = '/data/project5/kesf/ROMS/L2_SCB/monthly/l2_scb_avg.'
ext_path = '/data/project1/minnaho/psource/freshwater_nutrients/temp_salt_extractions/'

st_yr = 1999
en_yr = 2000

st_mo = 6
en_mo = 8

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

nc_vars = 'temp,salt'

'''
# hyperion
svname = '_htp'
xi_rho = 556
eta_rho = 661
s_rho = 14

'''
# jwpcp
svname = '_jwp'
xi_rho = 531
eta_rho = 578
s_rho = 20

'''
# ocsd
svname = '_ocs'
xi_rho = 551
eta_rho = 479
s_rho = 19

# plwtp
svname = '_plw'
xi_rho = 415
eta_rho = 147
s_rho = 15
'''


# get vertical profile 1km around each mooring
for y_i in range(st_yr,en_yr+1):
    print('year: ',y_i)
    if y_i == st_yr:
        s_m = st_mo
    else:
        s_m = 1
    if y_i == en_yr:
        e_m = en_mo+1
    else:
        e_m = 13
    for m_i in range(s_m,e_m):
        print('month: ',m_i)
        fi_dt = 'Y'+str(y_i)+'M'+'%02d'%m_i
        subprocess.call('ncks -O -v '+nc_vars+' -d xi_rho,'+str(xi_rho)+' -d eta_rho,'+str(eta_rho)+' -d s_rho,'+str(s_rho)+' '+out_path+fi_dt+'.nc '+ext_path+'l2_scb_avg.'+fi_dt+svname+'.nc',shell=True)

subprocess.call('ncrcat '+ext_path+'l2_scb_avg.Y*'+svname+'.nc '+ext_path+'l2_scb_avg.Y1999M06_Y2000M08'+svname+'.nc',shell=True)
