
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import seaborn as sns
import pandas as pd
import numpy as np
import random as rng
from SCRBenchmark import FEYNMAN_SRSD_HARD


mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

EQUATIONS_COUNT = len(FEYNMAN_SRSD_HARD)
REPETITIONS  = 5

font = {'size'   : 9}

mpl.rc('font', **font)

results = pd.read_csv('./results/4-R2Score-and-Violations.csv')
results['EquationName'] = [val.split('_')[0] for val in results["Instance"]]
results['SampleSize'] = [ int(filename.split('_')[1]) for filename in results['Instance']]
results['NoiseLevel'] = [ float(filename.split('_')[2].replace(',','.')) for filename in results['Instance']]

print(np.unique(results['EquationName']))
print(len(np.unique(results['EquationName'])))

results['ConstraintsCount'].fillna(1, inplace=True)
results['ConstraintsDerivative1Count'].fillna(1, inplace=True)
results['ConstraintsDerivative2Count'].fillna(1, inplace=True)
results['ConstraintsViolated'].fillna(1, inplace=True)
results['ConstraintsViolatedDerivative1Count'].fillna(1, inplace=True)
results['ConstraintsViolatedDerivative2Count'].fillna(1, inplace=True)
results['Test'].fillna(-10, inplace=True)

results['ConstraintsAchievedScaled'] = (1-(results['ConstraintsViolated']/results['ConstraintsCount']) ) * 100
results['ConstraintsAchievedDerivative1Scaled'] = (1-(results['ConstraintsViolatedDerivative1Count']/results['ConstraintsDerivative1Count'])) * 100
results['ConstraintsAchievedDerivative2Scaled'] = (1-(results['ConstraintsViolatedDerivative2Count']/results['ConstraintsDerivative2Count'])) * 100

results['ConstraintsAchievedScaled'].fillna(0, inplace=True)
results['ConstraintsAchievedDerivative1Scaled'].fillna(0, inplace=True)
results['ConstraintsAchievedDerivative2Scaled'].fillna(0, inplace=True)

results['CountHelper'] = [1] * len(results)
results['EquationName'] = results['EquationName'].astype("category")
results['EquationName'] = results['EquationName'].cat.set_categories(FEYNMAN_SRSD_HARD)


print(results[['ConstraintsCount','ConstraintsViolated','ConstraintsAchievedScaled']])
results = results[['EquationName','SampleSize','NoiseLevel', 'Test',"ConstraintsAchievedScaled","ConstraintsAchievedDerivative1Scaled","ConstraintsAchievedDerivative2Scaled" ]]
results = results.groupby(
    ['EquationName','SampleSize','NoiseLevel' ]).median().reset_index()
results.index = pd.RangeIndex(len(results.index))

results = results.sort_values("EquationName", ascending=False)

# df = results[ results['SampleSize'] == 100 ]

for sampleSize in [1000,10000]:
  df = results[ results['SampleSize'] == sampleSize ]

  df = df.sort_values(['EquationName','SampleSize','NoiseLevel'])
  g = sns.PairGrid(df,
                  x_vars=['Test',"ConstraintsAchievedScaled","ConstraintsAchievedDerivative1Scaled","ConstraintsAchievedDerivative2Scaled"], y_vars=["EquationName"],
                  height=8, aspect=.25, hue = 'NoiseLevel')
  plt.subplots_adjust(left=0.17, bottom=0.09, right=0.90, top=0.97, wspace=0.16, hspace=0.1)

  # Draw a dot plot using the stripplot function
  g.map(sns.stripplot, size=7, orient="h", jitter=False,
        palette="flare_r", linewidth=0, edgecolor=None, marker = '^', alpha = 0.5)
  g.add_legend()

  for ax in g.axes.flat:

      ax.xaxis.grid(False)
      ax.yaxis.grid(True)
      label = ax.get_xlabel()
      if(label == "Test"):
        ax.set( xlabel="mean $R^2$ validation", ylabel="")
      if(label == "ConstraintsAchievedScaled"):
        ax.set(xlim=(-10,110), xlabel="mean %\nachieved constraints\ntotal", ylabel="")
      if(label == "ConstraintsAchievedDerivative1Scaled"):
        ax.set(xlim=(-10,110), xlabel="mean %\nachieved constraints\ndegree 1", ylabel="")
      if(label == "ConstraintsAchievedDerivative2Scaled"):
        ax.set(xlim=(-10,110), xlabel="mean %\nachieved constraints\ndegree 2", ylabel="")


  sns.despine(left=True, bottom=True)

  plt.savefig(f'./result-figures/scsr-dotplot_SampleSize{sampleSize}.pdf',dpi = 500)
  plt.savefig(f'./result-figures/scsr-dotplot_SampleSize{sampleSize}.png',dpi = 500)
  plt.clf()
  plt.close()