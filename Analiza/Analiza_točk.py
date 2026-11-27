import laspy
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib import ticker

#-----------------------------------------------------------------------------------------------------------------------------------
#INPUT
#-----------------------------------------------------------------------------------------------------------------------------------

las = laspy.read(r".laz")

#print(len(las.points))

classification = np.array(las.classification)

#Knjižnica, katere bodo uporabljene na grafu, za razumevanje število točk, ki ima izbrana .laz datoteka

classified = {
    #'All_points [SUM]': (las.points),
    'Ground [2]': int(np.sum(classification == 2)),
    'Low_vegetation [3]': int(np.sum(classification == 3)),
    'Medium_vegetation [4]': int(np.sum(classification == 4)),
    'High_vegetation [5]': int(np.sum(classification == 5)),
    'Building [6]': int(np.sum(classification == 6)),
    'Low Noise [7]': int(np.sum(classification == 7)),
}

print(classified) 

#Pripava in izdelava grafikon
names = list(classified.keys())
all_points = list(classified.values())

plt.figure(figsize=(20, 10))

#ime, število točk in barve, ki bodo vsebovali graafikon. Barve so namerno izbrane, ki uporabljajo pri klasificiranju struktur
bars = plt.bar(names, all_points, color=["#8c564b", "#98df8a", "#2ca02c", "#006400", "#d62728", "#7f7f7f"])

#dodatne specifikacije za grafikon, glede zapisa številke in procentov
for bar, value in zip(bars, all_points):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f'{value:,}\n[{value / len(las.points):.01%}]',
            ha='center',
            va='bottom',
            fontsize=12
        )

#Dodatne informacije, ki služijo k boljšemu razumevanju grafa
plt.title('LiDAR point cloud classification - distribution of points', fontsize=18)
plt.text(2, 9500000, f'Σ of total points: {len(las.points)}', fontsize=15)
plt.xticks(rotation=15, ha='right', fontsize=12)
plt.grid(axis='y', alpha=0.3, color='black')
#plt.grid(axis='x', alpha=0.3)
formatter = ticker.ScalarFormatter()
formatter.set_scientific(False)
ax = plt.gca()

#popravljanje Y os, kjer se na milijonico spremeni številka in k temu tudi primerno označena
upper = np.ceil(max(all_points) / 1_000_000) * 1_000_000
ax.set_yticks(np.arange(0, upper + 1, 1_000_000))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

#prikaz 
plt.tight_layout()
plt.show()
