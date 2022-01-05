import numpy as np
from netCDF4 import Dataset

def rho_uv(roms_file,grid_file):
    '''
    calculate u_rho and v_rho from 
    u and v in roms file

    roms_file --> roms output file name (string)
    grid_file --> grid file name (string)
    '''
    # get u and v roms values
    out_nc = Dataset(roms_file,'r')

    # u interpolation
    [s_rho,Mp,L] = np.squeeze(out_nc.variables['u']).shape
    Lp = L+1
    Lm = L-1
    u_temp = 0.5*(np.squeeze(out_nc.variables['u'])[:,:,1:L]+np.squeeze(out_nc.variables['u'])[:,:,:Lm])
    u_rho = np.zeros((s_rho,Mp,Lp))
    u_rho[:,:,1:-1] = u_temp
    u_rho[:,:,0] = u_temp[:,:,0]
    u_rho[:,:,-1] = u_temp[:,:,-1]

    # v interpolation
    [s_rho,M,Lp] = np.squeeze(out_nc.variables['v']).shape
    Mp = M+1
    Mm = M-1
    v_temp = 0.5*(np.squeeze(out_nc.variables['v'])[:,1:M,:]+np.squeeze(out_nc.variables['v'])[:,:Mm,:])
    v_rho = np.zeros((s_rho,Mp,Lp))
    v_rho[:,1:-1,:] = v_temp
    v_rho[:,0,:] = v_temp[:,0,:]
    v_rho[:,-1,:] = v_temp[:,-1,:]
    

    return u_rho,v_rho
