import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



dp_times = [line.rstrip() for line in open('output.txt')]
heur_times = [line.rstrip() for line in open('output_heuristic.txt')]

print(dp_times)
print(heur_times)

plt.plot(dp_times, 'k', label = 'dpll')
plt.plot(heur_times, 'r--', label = 'heuristic 1')
plt.xlabel('Sudokus', fontsize=16)
plt.ylabel('Time', fontsize=16)
plt.yticks(range(len(dp_times)), dp_times)
plt.yticks(np.arange(0, 1, step=0.2), rotation=90)
plt.gca().invert_yaxis()
plt.yticks([])
plt.legend(loc='best')
plt.show()
plt.savefig("plot.png")
plt.close()


