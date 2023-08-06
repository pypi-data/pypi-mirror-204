import time
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from evalAIRR.util.pca import pca
from evalAIRR.util.ml import ml_simulated_dataset

def export_corr_heatmap(data_real, data_sim, n_real_feat = 0, n_sim_feat = 0, reduce_to_n_features = 0, with_ml_sim = False, ml_random_state = None):
    print('[LOG] CORR: Exporting correlation matrix heatmap')
    if with_ml_sim:
        print('[LOG] CORR: Generating ML dataset')
        data_ML = ml_simulated_dataset(data_real, ml_random_state)
    if n_real_feat != 0 and n_sim_feat != 0 and reduce_to_n_features != 0:
        print('[LOG] CORR: Reducing dimentions using PCA')
        _, data_real = pca(data_real, reduce_to_n_features)
        _, data_sim = pca(data_sim, reduce_to_n_features)
        if with_ml_sim:
            _, data_ML = pca(data_ML, reduce_to_n_features)
    if reduce_to_n_features == 0:
        print('[WARNING] CORR: reduce_to_n_features not provided and dimensionality reduction will not be applied. This may result in very long calculation times.')

    print('[LOG] CORR: Calculating correlation matrices')
    corr_real = pd.DataFrame(data_real).corr()
    corr_sim = pd.DataFrame(data_sim).corr()

    diff_corrs = corr_real.sub(corr_sim).abs()

    if with_ml_sim:
        corr_ML = pd.DataFrame(data_ML).corr()
        diff_corrs_ML = corr_ML.sub(corr_sim).abs()

    print('[LOG] CORR: Displaying correlation heatmaps')
    if with_ml_sim:
        f,(ax1,ax2,ax3,ax4, axcb) = plt.subplots(1,5,gridspec_kw={'width_ratios':[1,1,1,1,0.08]})
        f.set_size_inches(18, 5)
        ax1.get_shared_y_axes().join(ax2,ax3,ax4)
    else:
        f,(ax1,ax2,ax3, axcb) = plt.subplots(1,4,gridspec_kw={'width_ratios':[1,1,1,0.08]})
        f.set_size_inches(15, 5)
        ax1.get_shared_y_axes().join(ax2,ax3)
    f.suptitle('Correlation heatmaps')
    g1 = sns.heatmap(corr_real,cmap="YlGnBu",cbar=False,ax=ax1)
    g1.set_title('Real dataset')
    g1.set_ylabel('')
    g1.set_xlabel('')
    g2 = sns.heatmap(corr_sim,cmap="YlGnBu",cbar=False,ax=ax2)
    g2.set_title('Simulated dataset')
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_yticks([])
    g3 = sns.heatmap(diff_corrs,cmap="YlGnBu",ax=ax3, cbar=(not with_ml_sim), cbar_ax=(axcb if not with_ml_sim else None))
    g3.set_title('Difference in correlation')
    g3.set_ylabel('')
    g3.set_xlabel('')
    g3.set_yticks([])
    if with_ml_sim:
        g4 = sns.heatmap(diff_corrs_ML,cmap="YlGnBu",ax=ax4, cbar_ax=axcb)
        g4.set_title('Difference in correlation between\nsimulated and ML generated datasets')
        g4.set_ylabel('')
        g4.set_xlabel('')
        g4.set_yticks([])

    f.savefig(f'./output/temp_figures/corr_matrix_{int(time.time())}.svg')
    del f
    plt.close()

def export_csv_corr_matrix(data_real, data_sim, output):
    corr_real = pd.DataFrame(data_real).corr()
    corr_sim = pd.DataFrame(data_sim).corr()
    diff_corrs = corr_real.sub(corr_sim).abs()
    diff_corrs = np.array(diff_corrs)
    if output:
        try:
            with open(output, 'w', encoding="utf-8") as output_file:
                for row in diff_corrs:
                    output_file.write(','.join([str(i) for i in row]) + '\n')
            print('[LOG] CORR Matrix file created')
        except Exception as e: 
            print(e)
            print('[ERROR] Failed to export CORR Matrix to file')