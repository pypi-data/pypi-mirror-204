import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_res_curve(csv,output):
    csv = pd.read_csv(csv, sep='\t')
    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    for i in range(1, 5):
        plt.subplot(2, 3, i)
        title = csv.columns[i]

        plt.plot(csv[title])
        plt.title(title)
        plt.savefig(output + 'res.jpg', dpi=500)


