import subprocess as subprocess

out_path = './roms_output_his/l2_scb_his_'
grid_path = '/data/project5/kesf/ROMS/L2_SCB/roms_grd.nc'

st_yr = 1997
en_yr = 2000

st_mo = 2
en_mo = 12

months_w_31_days = [1,3,5,7,8,10,12]
leap_years = [1992,1996,2000,2004,2008,2012,2016,2020]

dep0 = -5
dep1 = -50
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
        subprocess.call('zslice '+str(dep0)+' '+str(dep1)+' --vars=u,v '+grid_path+' '+out_path+fi_dt+'.nc',shell=True)

