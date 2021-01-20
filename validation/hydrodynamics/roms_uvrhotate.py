import numpy as np
from netCDF4 import Dataset

def rho_uv(roms_file,grid_file):
    '''
    calculate u_rho and v_rho from 
    u and v in roms file

    roms_file --> roms output file name (string)
    grid_file --> grid file name (string)
    '''
    # find shape of grid
    grid_nc = Dataset(grid_file,'r')
    [Ly_nc,Lx_nc] = grid_nc.variables['pm'].shape
    # get u and v roms values
    out_nc = Dataset(roms_file,'r')
    u_rho = 0.5*(np.squeeze(out_nc.variables['u'])[:,1:,:]+np.array(out_nc.variables['u'])[:,:Ly_nc-1,:])
    v_rho = 0.5*(np.squeeze(out_nc.variables['v'])[:,:,1:]+np.array(out_nc.variables['v'])[:,:,:Lx_nc-1])

    return u_rho,v_rho
