import subprocess

f_names = ['decapods_adult_mort_100m_30d_*','decapods_adult_mort_150m_180d_*','decapods_adult_mort_300m_180d_*','decapods_adult_mort_300m_30d_*','decapods_adult_mort_50m_30d_*','decapods_adult_search_150m_9d_*','decapods_adult_search_300m_9d_*','decapods_adult_search_50m_9d_*','decapods_juvenile_mort_100m_*','decapods_juvenile_mort_150m_*','decapods_juvenile_mort_30m_*','decapods_juvenile_mort_50m_*','decapods_larval_mort_0m_7d_*','decapods_larval_mort_50m_7d_*']

for f_i in f_names:
    print(f_i)
    subprocess.call('ncea -h '+f_i+' '+f_i[:-2]+'_freq.nc',shell=True)
