import seaborn as sns
import pandas as pd
import pylab as plt


def createPlot(x, y1, y2, label1, label2):
    df = pd.DataFrame(
        {'Time': x,
         label1: y1,
         label2: y2
         }
    )
    sns.set()
    viz = df.plot(x='Time')
    viz.set_ylabel("Time (Seconds)")
    plt.show()


x = range(5)
a = [1, 2, 4, 8, 16]
b = [1, 4, 9, 16, 25]
createPlot(x, a, b, 'Heuristic A', 'Heuristic B')
