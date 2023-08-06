import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from evalAIRR.util.ml import ml_simulated_dataset

def pca(A,m):
    max_m = min(A.shape[0], A.shape[1])
    if (m > max_m):
        print(f'[WARNING] PCA: reduce_to_n_features value is higher than min(n_samples, n_features)={max_m}. Using value reduce_to_n_features={max_m} instead.')
        m = max_m
    pca = PCA(n_components=m, copy=True)
    pca.fit(A)
    return pca.components_, pca.transform(A)

def export_pca_2d_comparison(data_real, data_sim, with_ml_sim = False, ml_random_state = None):
    components_R, pca_R = pca(data_real, 2)
    components_S, pca_S = pca(data_sim, 2)

    pc_R_x = np.linspace(min(pca_R[:, 0]), max(pca_R[:, 0]), 1000)
    pc_R_y = components_R[1][0] / components_R[0][0] * pc_R_x

    pc_S_x = np.linspace(min(pca_S[:, 0]), max(pca_S[:, 0]), 1000)
    pc_S_y = components_S[1][0] / components_S[0][0] * pc_S_x

    if with_ml_sim:
        print('[LOG] PCA: Generating ML dataset')
        data_ML = ml_simulated_dataset(data_real, ml_random_state)
        components_ML, pca_ML = pca(data_ML, 2)

        pc_ML_x = np.linspace(min(pca_ML[:, 0]), max(pca_ML[:, 0]), 1000)
        pc_ML_y = components_ML[1][0] / components_ML[0][0] * pc_ML_x

        f,(ax1, ax2, ax3) = plt.subplots(1, 3)
        f.set_size_inches(15, 5)
    else:
        f,(ax1, ax2) = plt.subplots(1, 2)
        f.set_size_inches(10, 5)

    f.suptitle('PCA comparison in two dimensions')

    ax1.scatter(pca_R[:, 0], pca_R[:, 1])
    ax1.plot(pc_R_x, pc_R_y, c='#1b24a8')
    ax1.set_title('Real dataset')

    ax2.scatter(pca_S[:, 0], pca_S[:, 1], c='red')
    ax2.plot(pc_S_x, pc_S_y, c='#781010')
    # ax2.set_ylabel('')
    # ax2.set_yticklabels([])
    # ax2.set_yticks([])
    ax2.set_title('Simulated dataset')

    if with_ml_sim:
        ax3.scatter(pca_ML[:, 0], pca_ML[:, 1], c='green')
        ax3.plot(pc_ML_x, pc_ML_y, c='#0a4711')
        ax3.set_title('ML generated dataset')

        xbound = (min(ax1.get_xbound()[0], ax2.get_xbound()[0], ax3.get_xbound()[0]), max(ax1.get_xbound()[1], ax2.get_xbound()[1], ax3.get_xbound()[1]))
        ybound = (min(ax1.get_ybound()[0], ax2.get_ybound()[0], ax3.get_ybound()[0]), max(ax1.get_ybound()[1], ax2.get_ybound()[1], ax3.get_ybound()[1]))

        ax3.set_xbound(xbound)
        ax3.set_ybound(ybound)
    else:
        xbound = (min(ax1.get_xbound()[0], ax2.get_xbound()[0]), max(ax1.get_xbound()[1], ax2.get_xbound()[1]))
        ybound = (min(ax1.get_ybound()[0], ax2.get_ybound()[0]), max(ax1.get_ybound()[1], ax2.get_ybound()[1]))

    ax1.set_xbound(xbound)
    ax1.set_ybound(ybound)
    ax2.set_xbound(xbound)
    ax2.set_ybound(ybound)

    f.savefig(f'./output/temp_figures/pca_2d_comparison_{int(time.time())}.svg')
    del f
    plt.close()