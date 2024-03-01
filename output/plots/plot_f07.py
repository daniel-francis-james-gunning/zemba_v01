# -*- coding: utf-8 -*-
"""
Plot Figure 7 (Pre-Industrial - Results - Transport)

@author: Daniel Gunning 
"""


import numpy as np
import proplot as pplt
from matplotlib.font_manager import FontProperties
import os
import pickle
import xarray as xr

output_path  = os.path.dirname(os.getcwd())
script_path  = os.path.dirname(output_path)
input_path   = script_path + '/input'

# change directory
os.chdir(script_path)

from utilities import *

#---------
# EBM data
#---------

# load pre-industrial results
#----------------------------

# load data
with open('output/equilibrium/pi_moist_res5.0.pkl', 'rb') as f:
    pi_dict = pickle.load(f)
pi  = pi_dict['StateYear']
Var = pi_dict['Var']
INPUT = pi_dict['Input']
    
ebm = {}
noresm = {}
era5 = {}

# annual and zonal mean
#----------------------

# moist static energy in atmosphere
ebm_atm = np.nanmean(pi["mse_north"], axis = 1)/1e15
ebm_atm_max_sh = -np.min(ebm_atm[0:int(Var["idxeq"])])
ebm_atm_max_nh = np.max(ebm_atm[int(Var["idxeq"]):])


# dry static energy in atmosphere
ebm_dse = np.nanmean(pi["dry_north"], axis = 1)/1e15

# latent energy in atmosphere
ebm_latent = np.nanmean(pi["latent_north"], axis = 1)/1e15

# ocean heat transport
ebm_ocean = np.nanmean(pi['advf'][0:Var['olatb'].size, :] + pi['advf'][Var['olatb'].size*5:Var['olatb'].size*6, :] + pi["hdiffs"][0:Var['olatb'].size, :], axis = 1)/1e15 
ebm_ocean = np.concatenate((np.zeros((Var["idxnocs"].size)), ebm_ocean, np.zeros((Var["idxnocn"].size))))

ebm_ocean_max_sh = -np.min(ebm_ocean[0:int(Var["idxeq"])])
ebm_ocean_max_nh = np.max(ebm_ocean[int(Var["idxeq"]):])

# jja mean
#---------

# moist static energy in atmosphere
ebm_atm_jja = np.nanmean(pi["mse_north"][:,151:242+1], axis = 1)/1e15

# dry static energy in atmosphere
ebm_dse_jja = np.nanmean(pi["dry_north"][:,151:242+1], axis = 1)/1e15

# latent energy in atmosphere
ebm_latent_jja = np.nanmean(pi["latent_north"][:,151:242+1], axis = 1)/1e15

# ocean heat transport
ebm_ocean_jja         = np.nanmean(pi["advf"][0:Var['olatb'].size,151:242+1] + pi["advf"][Var['olatb'].size*5:Var['olatb'].size*6,151:242+1] + pi["hdiffs"][0:Var['olatb'].size:Var['olatb'].size,151:242+1], axis = 1)/1e15 
ebm_ocean_jja_  = np.concatenate((np.zeros((Var["idxnocs"].size)), ebm_ocean_jja , np.zeros((Var["idxnocn"].size))))

# djf mean
#---------

# moist static energy in atmosphere
ebm_atm_djf = ((np.append(pi["mse_north"][:,0:58+1], pi["mse_north"][:,334:], axis = 1)).mean(axis=1))/1e15

# dry static energy in atmosphere
ebm_dse_djf = ((np.append(pi["dry_north"][:,0:58+1], pi["dry_north"][:,334:], axis = 1)).mean(axis=1))/1e15

# moist static energy in atmosphere
ebm_latent_djf = ((np.append(pi["latent_north"][:,0:58+1], pi["latent_north"][:,334:], axis = 1)).mean(axis=1))/1e15

# ocean heat transport
ebm_ocean_djf   = ((np.append(
    
                            pi["advf"][0:Var['olatb'].size,0:58+1] + pi["advf"][Var['olatb'].size*5:Var['olatb'].size*6,0:58+1] + pi["hdiffs"][0:Var['olatb'].size,0:58+1],
                            
                            pi["advf"][0:Var['olatb'].size,334:] + pi["advf"][Var['olatb'].size*5:Var['olatb'].size*6,334:] + pi["hdiffs"][0:Var['olatb'].size,334:], axis=1)).mean(axis=1))/1e15

ebm_ocean_djf = np.concatenate((np.zeros((Var["idxnocs"].size)), ebm_ocean_djf, np.zeros((Var["idxnocn"].size))))
    

#----------------
# Add NorSM2 data
#----------------

def inferred_heat_transport(energy_in, lat):
    
    '''
    Infers northward heat transport from energy imbalance.
    '''
    
    # load modules
    from scipy import integrate
    
    # latitude in radians
    latr = np.deg2rad(lat)
    
    # cosine of latitude
    coslat = np.cos(latr)
    
    # weighted-mean energy flux
    field = coslat*energy_in
    
    # integral of energy flux for each latitude
    integral = integrate.cumtrapz(field, x=latr, initial=0)
    
    # scale
    result = (1E-15 * 2 * np.math.pi * 6371e3**2 * integral)
    
    return result


# load annual data
noresm2_lat     = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=0)
noresm2_pr      = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=2)
noresm2_prsn    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=3)
noresm2_evap    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=4)
noresm2_rsdt    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=5)
noresm2_rsut    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=6)
noresm2_rsds    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=7)
noresm2_rsus    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=8)
noresm2_rlut    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=9)
noresm2_rlds    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=10)
noresm2_rlus    = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=11)
noresm2_shf     = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=12)
noresm2_lhf     = np.loadtxt(script_path+'/other_data/noresm2/noresm2_annual.txt', skiprows=5, usecols=13)

# interpolate data
# noresm2_pr      = np.interp(Var['lat'], noresm2_lat, noresm2_pr)
# noresm2_prsn    = np.interp(Var['lat'], noresm2_lat, noresm2_prsn)
# noresm2_evap    = np.interp(Var['lat'], noresm2_lat, noresm2_evap)
# noresm2_rsdt    = np.interp(Var['lat'], noresm2_lat, noresm2_rsdt)
# noresm2_rsut    = np.interp(Var['lat'], noresm2_lat, noresm2_rsut)
# noresm2_rsds    = np.interp(Var['lat'], noresm2_lat, noresm2_rsds)
# noresm2_rsus    = np.interp(Var['lat'], noresm2_lat, noresm2_rsus)
# noresm2_rlut    = np.interp(Var['lat'], noresm2_lat, noresm2_rlut)
# noresm2_rlds    = np.interp(Var['lat'], noresm2_lat, noresm2_rlds)
# noresm2_rlus    = np.interp(Var['lat'], noresm2_lat, noresm2_rlus)
# noresm2_shf     = np.interp(Var['lat'], noresm2_lat, noresm2_shf)
# noresm2_lhf     = np.interp(Var['lat'], noresm2_lat, noresm2_lhf)

# net radiation at TOA
rtnet_noresm2 = (noresm2_rsdt - noresm2_rsut) - noresm2_rlut

# net radiation at SFC
rsnet_noresm2 = (noresm2_rsds - noresm2_rsus) + (noresm2_rlds - noresm2_rlus)

# net radiation of atmosphere
ratmnet_noresm2 = rtnet_noresm2 - rsnet_noresm2

# upwards sensible heat flux
shf_noresm2 = noresm2_shf

# evaporation latent heat flux 
lhf_noresm2 =  noresm2_evap*2.5e6

# evaporation 
evap_noresm2 =  noresm2_evap

# precipitation 
precip_noresm2 =  noresm2_pr

# precipitation latent heat flux  
precip_latent_noresm2 =  noresm2_pr*2.5e6

# snowfall latent heat flux  
snowfall_latent_noresm2 =  noresm2_prsn*334000

# net heat flux into atmosphere
Fatm_noresm2 = ratmnet_noresm2 + lhf_noresm2 + snowfall_latent_noresm2 + shf_noresm2

# net heat flux into surface
Fs_noresm2 = rsnet_noresm2 - snowfall_latent_noresm2 - shf_noresm2 - lhf_noresm2

# latent heat flux
Flatent_noresm2 = lhf_noresm2 - precip_latent_noresm2  

# total heat transport from TOA energy flux imbalance
noresm2_total = inferred_heat_transport(rtnet_noresm2, noresm2_lat)

# atmospheric heat transport from atmospheric energy flux imbalance
noresm2_atm = inferred_heat_transport(Fatm_noresm2, noresm2_lat)

# ocean heat transport from surface energy flux imbalance
noresm2_ocean = inferred_heat_transport(Fs_noresm2, noresm2_lat)

# latent heat transport in atmosphere from moisture imbalance
noresm2_latent = inferred_heat_transport(Flatent_noresm2, noresm2_lat)

# dry static transport in atmosphereas residual
noresm2_dse = noresm2_atm - noresm2_latent 


noresm2_ocean_max_sh = -np.min(noresm2_ocean[0:int(Var["idxeq"])])
noresm2_ocean_max_nh = np.max(noresm2_ocean[int(Var["idxeq"]):])

noresm2_atm_max_sh = -np.min(noresm2_atm[0:int(Var["idxeq"])])
noresm2_atm_max_nh = np.max(noresm2_atm[int(Var["idxeq"]):])


#---------
# Plotting
#---------

# constants
#----------

ebm_color = "black"
ebm_lw    = 1
ebm_ls    = "-"

noresm_color = "blue9"
noresm_lw    = 1
noresm_ls    = "-"

era5_color = "red9"
era5_lw    = 1
era5_ls    = "-"

legend_fs = 7.

# shape
shape = [  
        [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
        [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],]

# figure and axes
fig, axs = pplt.subplots(shape, figsize = (10,3), sharey = False, sharex = False, grid = False)


# fonts
axs.format(ticklabelsize=7, ticklabelweight='normal', 
           ylabelsize=8, ylabelweight='normal',
            xlabelsize=8, xlabelweight='normal', 
            titlesize=8, titleweight='normal',)

# x-axis
locatorx      = np.arange(-90, 120, 30)
minorlocatorx = np.arange(-90, 100, 10)
axs.format(xminorlocator = minorlocatorx, xlocator = locatorx, xlim = (-90, 90))
axs.format(xlabel = "Latitude", xformatter='deglat')   

# format top left subplot
for i in np.arange(0,1):
    
    # y-axis
    axs[i].format(ylim = (-6, 6), yminorlocator=np.arange(-6, 6+1, 1), ylocator = np.arange(-6, 6+2, 2))
    
    
    # hline
    axs[i].axhline(0, Var["lat"].min(), Var["lat"].max(), color = "black", lw = 0.2, linestyle ="--")
    
    
# format middle plot
for i in np.arange(1,2):
    
    # y-axis
    axs[i].format(ylim = (-6, 6), yminorlocator=[], ylocator = np.arange(-6, 6+1, 1))
    axs[i].yaxis.set_ticklabels([])
    
    # hline
    axs[i].axhline(0, Var["lat"].min(), Var["lat"].max(), color = "black", lw = 0.2, linestyle ="--")
    
    
# format right plot
for i in np.arange(2,3):
    
    # y-axis
    axs[i].format(ylim = (-6, 6), yminorlocator=[], ylocator = np.arange(-6, 6+1, 1))
    axs[i].yaxis.set_ticklabels([])
    
    # hline
    axs[i].axhline(0, Var["lat"].min(), Var["lat"].max(), color = "black", lw = 0.2, linestyle ="--")
    

# titles
axs[0].format(title = r'(a) Total Heat Transport (PW)', titleloc = 'left')
axs[1].format(title = r'(b) Atmospheric and Ocean Heat Transport (PW)', titleloc = 'left')
axs[2].format(title = r'(c) Dry Static and Latent Heat Transport (PW)', titleloc = 'left')



# plot total heat transport
#--------------------------

# lines
ebm_total_line    = axs[0].plot(Var["latb"], ebm_atm + ebm_ocean, color = ebm_color, lw = ebm_lw, ls = ebm_ls)
noresm_total_line = axs[0].plot(noresm2_lat, noresm2_total, color = noresm_color, lw = noresm_lw, ls = noresm_ls)

# legend
axs[0].legend(handles = [ebm_total_line, noresm_total_line],
              labels  = ["ZEMBA", "NorESM2"], 
                          frameon = False, loc = "ul", bbox_to_anchor=(0.2, 0.9), 
                          ncols = 1, prop={'size':legend_fs})


# plot atmospheric + ocean
#-------------------------

# lines
ebm_atm_line = axs[1].plot(Var["latb"], ebm_atm, color = ebm_color, lw = ebm_lw, ls = ebm_ls)
noresm_atm_line = axs[1].plot(noresm2_lat, noresm2_atm, color = noresm_color, lw = noresm_lw, ls = noresm_ls)
ebm_ocean_line = axs[1].plot(Var["latb"], ebm_ocean, color = ebm_color, lw = ebm_lw, ls = ":")
noresm_ocean_line = axs[1].plot(noresm2_lat, noresm2_ocean, color = noresm_color, lw = noresm_lw, ls = ":")

# legend
axs[1].legend(handles = [ebm_atm_line, noresm_atm_line],
              labels  = ["ZEMBA (Atmosphere)", "NorESM2 (Atmosphere)"], 
                          frameon = False, loc = "ul", bbox_to_anchor=(0.1, 0.9), 
                          ncols = 1, prop={'size':legend_fs})

# legend
axs[1].legend(handles = [ebm_ocean_line, noresm_ocean_line],
              labels  = ["ZEMBA (Ocean)", "NorESM2 (Ocean)"], 
                          frameon = False, loc = "lr", bbox_to_anchor=(0.9, 0.2), 
                          ncols = 1, prop={'size':legend_fs})

# plot atmospheric partition
#---------------------------

# lines
ebm_dse_line       = axs[2].plot(Var["latb"], ebm_dse, color = ebm_color, lw = ebm_lw, ls = ebm_ls)
noresm_dse_line    = axs[2].plot(noresm2_lat, noresm2_dse, color = noresm_color, lw = noresm_lw, ls = noresm_ls)
ebm_latent_line    = axs[2].plot(Var["latb"], ebm_latent, color = ebm_color, lw = ebm_lw, ls = ":", alpha = 0.5)
noresm_latent_line = axs[2].plot(noresm2_lat, noresm2_latent, color = noresm_color, lw = noresm_lw, ls = ":", alpha = 0.5)

# legend
axs[2].legend(handles = [ebm_dse_line, noresm_dse_line],
              labels  = ["ZEMBA (Dry Static)", "NorESM2 (Dry Static)"], 
                          frameon = False, loc = "ul", bbox_to_anchor=(0.2, 0.9), 
                          ncols = 1, prop={'size':legend_fs})

# legend
axs[2].legend(handles = [ebm_latent_line, noresm_latent_line,],
              labels  = ["ZEMBA (Latent)","NorESM2 (Latent)"], 
                          frameon = False, loc = "lr", bbox_to_anchor=(0.9, 0.15), 
                          ncols = 1, prop={'size':legend_fs})

# save figure
fig.save(os.getcwd()+"/output/plots/f07.png", dpi = 400)
fig.save(os.getcwd()+"/output/plots/f07.pdf", dpi = 400)

print('###########################')
print("Peak Atmospheric Heat Transport....")
print('###########################')

print("pyEBM (SH): " + str(round(ebm_atm_max_sh, 2)))
print("pyEBM (NH): " + str(round(ebm_atm_max_nh, 2)))

print("NorESM2 (SH): " + str(round(noresm2_atm_max_sh, 2)))
print("NorESM2 (NH): " + str(round(noresm2_atm_max_nh, 2))+'\n')

# print("ERA5 (SH): " + str(round(era5_atm_max_sh, 2)))
# print("ERA5 (NH): " + str(round(era5_atm_max_nh, 2)))

print('###########################')
print("Peak Ocean Heat Transport....")
print('###########################')

print("pyEBM (SH): " + str(round(ebm_ocean_max_sh, 2)))
print("pyEBM (NH): " + str(round(ebm_ocean_max_nh, 2)))

print("NorESM2 (SH): " + str(round(noresm2_ocean_max_sh, 2)))
print("NorESM2 (NH): " + str(round(noresm2_ocean_max_nh, 2))+'\n')

# print("ERA5 (SH): " + str(round(era5_ocean_max_sh, 2)))
# print("ERA5 (NH): " + str(round(era5_ocean_max_nh, 2)))








