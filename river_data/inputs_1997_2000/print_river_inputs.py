import numpy as np
from netCDF4 import Dataset
import pickle

nm10 = pickle.load(open('river_names_10.pkl','rb'))
nm24 = pickle.load(open('river_names_24.pkl','rb'))

# rename
nm10 = ['san_juan_creek', 
'san_jose_creek', 
'montecito_creek', 
'san_diego_river', 
'sweetwater_river', 
'solstice_canyon', 
'los_angeles_river', 
'atascadero_creek', 
'salt_creek', 
'little_sycamore', 
'santa_ana_river', 
'pena_canyon', 
'moro_canyon', 
'ballona_creek', 
'tijuana_river', 
'santa_margarita_river', 
'los_angeles_harbor', 
'tuna_canyon', 
'rincon_creek', 
'marie_canyon', 
'santa_clara', 
'santa_monica_canyon', 
'aliso_creek', 
'las_flores_canyon', 
'mission_bay', 
'otay_river', 
'los_penasquitos_lagoon', 
'encinas_creek', 
'arroyo_sequit_creek', 
'san_diego_creek', 
'ventura_river', 
'redondo_beach_king_harbor', 
'mission_creek', 
'walnut_canyon', 
'trancas_canyon', 
'carbon_canyon', 
'calleguas_creek', 
'san_gabriel_river', 
'san_luis_rey_river', 
'agua_hedionda_lagoon', 
'buena_vista_creek', 
'escondido_creek', 
'las_flores_creek', 
'san_dieguito_river', 
'san_onofre_creek', 
'san_marcos_creek', 
'tecolote_creek', 
'chollas_creek']

nm24 = [
'arroyo_trabuco_creek',
'bolsa_chica_westminster_channel', 
'bonita_creek', 
'carpinteria_creek', 
'costa_mesa_channel', 
'coyote_creek',
'cristianitos_creek',
'devereux_lagoon',
'dominguez_channel',
'e_garden_grove_wintersberg_channel',
'goleta_tecolotito_creek',
'laguna_canyon',
'malibu_creek',
'prima_deshecha',
'revolon_slough',
'san_mateo_creek',
'san_pedro_creek',
'santa_ana_delhi',
'segunda_deshecha',
'topanga_creek',
'zuma_canyon',
'arroyo_burro_creek',
'canada_de_la_gaviota',
'franklin_creek']

nc10 = Dataset('south_coast_rivers_10_years_monthly_new.nc','r')
nc24 = Dataset('south_coast_rivers_24_years_monthly_new.nc','r')

nc10.variables['flow']
