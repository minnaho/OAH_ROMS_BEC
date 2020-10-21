import pandas as pd

fi = pd.read_csv('daily_flow_1997_2006_santa_margarita.txt',skiprows=30,sep='\t')
fi['20d'] = pd.to_datetime(fi['20d'])
fi.set_index(fi['20d'],inplace=True)
mn = fi.resample('M').mean()
fi['14n'] = fi['14n']*0.02831685
mn['14n'] = mn['14n']*0.02831685
mn['14n'].to_csv('smr_flow_m3s_1997_2006_monthly.csv')
fi['14n'].to_csv('smr_flow_m3s_1997_2006_daily.csv')
