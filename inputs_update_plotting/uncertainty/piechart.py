import matplotlib.pyplot as plt

labels = ['Ocean Outfalls','Rivers','Atmospheric Deposition']

# data from PNAS paper 1997-2000 kg/day
sizes = [148170+21445,17975,8589]

# data from 1997-2017 kg/year
sizes = [57519404,4484759,8589*365]

plt.ion()
fig,ax = plt.subplots()

ax.pie(sizes,labels=labels,autopct='%1.1f%%',textprops={'fontsize': 16})
ax.axis('equal')
