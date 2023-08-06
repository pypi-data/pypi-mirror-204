import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.spatial
import scipy.stats
import decimal
import time

from evalAIRR.util.ml import ml_simulated_dataset

from sklearn.preprocessing import MinMaxScaler

def cdf(data):
    data_sorted = np.sort(data)
    p = 1. * np.arange(len(data)) / (len(data) - 1)
    return data_sorted, np.array(p)

def get_feature_data(feature, data, features):
    try:
        idx = np.where(features == feature)[0][0]
        if idx == None:
            print(f'[ERROR] Feature {feature} not found!')
            return np.array([])
        return data[:, idx].flatten()
    except:
        print(f'[ERROR] Feature {feature} not found!')
        return np.array([])

def get_observation_data(observation_index, data):
    if observation_index < 0 or observation_index >= len(data):
        print(f'[ERROR] Observation with index {observation_index} does not exist!')
        return np.array([])
    return data[observation_index, :].flatten()

def export_ks_test(data_R, data_S, features_R, features_S, output):
    ks_results = []
    pvalue_results = []
    for f_idx in range(len(features_R)):
        data_R_f = get_feature_data(features_R[f_idx], data_R, features_R)
        data_S_f = get_feature_data(features_S[f_idx], data_S, features_S)

        ks = scipy.stats.ks_2samp(data_R_f, data_S_f)
        ks_results.append(str(ks.statistic))
        pvalue_results.append(str(ks.pvalue))
    ks_results = np.array(ks_results)
    if output:
        try:
            with open(output, 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(ks_results) + '\n')
                output_file.write(','.join(pvalue_results))
            print('[LOG] KS test result file created')
        except: 
            print('[ERROR] Failed to export KS test results to file')


def export_feature_ks_test(feature, data_R, data_S, features_R, features_S):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    cdf_1_x, cdf_1_y = cdf(data_R_f)
    cdf_2_x, cdf_2_y = cdf(data_S_f)
    res = scipy.stats.ks_2samp(data_R_f, data_S_f)
    
    f, ax = plt.subplots(1, 1)
    f.set_size_inches(5, 5)
    f.suptitle(f'CDF comparison of feature {feature}\nin real and simulated datasets')
    ax.plot(cdf_1_x, cdf_1_y, c='#1b24a8', label='Real dataset')
    ax.plot(cdf_2_x, cdf_2_y, c='r', label='Simulated dataset')
    ax.grid(visible=True)
    ax.legend()
    
    print(f'[RESULT] Feature {feature} KS statistic =', res.statistic)
    print(f'[RESULT] Feature {feature} P value =', res.pvalue)
    with open(f'./output/temp_results/ks_test_{feature}.txt', 'w', encoding="utf-8") as file:
        file.write('\t\t<tr colspan="2">\n')
        file.write(f'\t\t\t<td>Feature {feature} KS statistic</td>\n')
        file.write(f'\t\t\t<td>{res.statistic}</td>\n')
        file.write('\t\t</tr>\n')

        file.write('\t\t<tr colspan="2">\n')
        file.write(f'\t\t\t<td>Feature {feature} P value</td>\n')
        file.write(f'\t\t\t<td>{res.pvalue}</td>\n')
        file.write('\t\t</tr>\n')

    f.savefig(f'./output/temp_figures/ks_test_{feature}_{int(time.time())}.svg')
    del f
    plt.close()

def export_distr_histogram(feature, data_R, data_S, features_R, features_S, n_bins=30):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    bins = np.linspace(min(min(data_R_f), min(data_S_f)), max(max(data_R_f), max(data_S_f)), n_bins)

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution histograms of feature {feature}')
    ax.hist([data_R_f, data_S_f], bins, label=['Real dataset', 'Simulated dataset'])
    ax.legend(loc='upper right')
    
    f.savefig(f'./output/temp_figures/histogram_{feature}_{int(time.time())}.svg')
    del f
    plt.close()

def export_obs_distr_histogram(observation_index, data_R, data_S, n_bins=30):
    if observation_index == 'all':
        print('[ERROR] Observation distribution histogram report does not support the visualization of all observations')
        return
    data_R_o = get_observation_data(observation_index, data_R)
    data_S_o = get_observation_data(observation_index, data_S)
    if not any(data_R_o) or not any(data_S_o):
        return

    bins = np.linspace(min(min(data_R_o), min(data_S_o)), max(max(data_R_o), max(data_S_o)), n_bins)

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution histograms of observation with index {observation_index}')
    ax.hist([data_R_o, data_S_o], bins, label=['Real dataset', 'Simulated dataset'])
    ax.legend(loc='upper right')
    
    f.savefig(f'./output/temp_figures/histogram_obs_{observation_index}_{int(time.time())}.svg')
    del f
    plt.close()

def export_distr_boxplot(feature, data_R, data_S, features_R, features_S):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution boxplots of feature {feature}')
    ax.boxplot([data_R_f, data_S_f], labels=['Real dataset', 'Simulated dataset'])
    
    f.savefig(f'./output/temp_figures/box_plot_{feature}_{int(time.time())}.svg')
    del f
    plt.close()

def export_obs_distr_boxplot(observation_index, data_R, data_S):
    if observation_index == 'all':
        print('[ERROR] Observation distribution box plot report does not support the visualization of all observations')
        return
    data_R_o = get_observation_data(observation_index, data_R)
    data_S_o = get_observation_data(observation_index, data_S)
    if not any(data_R_o) or not any(data_S_o):
        return

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution boxplots of observation with index {observation_index}')
    ax.boxplot([data_R_o, data_S_o], labels=['Real dataset', 'Simulated dataset'])
    
    f.savefig(f'./output/temp_figures/box_plot_obs_{observation_index}_{int(time.time())}.svg')
    del f
    plt.close()

def export_distr_violinplot(feature, data_R, data_S, features_R, features_S):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    f, [ax1, ax2] = plt.subplots(2, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution violin plots of feature {feature}')
    ax1.violinplot(data_R_f, vert=False, widths=0.7,
                     showmeans=True, showextrema=True, showmedians=True)
    ax1.set_title('Real dataset')
    ax1.set_yticklabels([])
    ax1.set_yticks([])
    ax1.set
    ax2.violinplot(data_S_f, vert=False, widths=0.7,
                     showmeans=True, showextrema=True, showmedians=True)
    ax2.set_title('Simulated dataset')
    ax2.set_yticklabels([])
    ax2.set_yticks([])

    xbound = (min(ax1.get_xbound()[0], ax2.get_xbound()[0]), max(ax1.get_xbound()[1], ax2.get_xbound()[1]))
    ybound = (min(ax1.get_ybound()[0], ax2.get_ybound()[0]), max(ax1.get_ybound()[1], ax2.get_ybound()[1]))

    ax1.set_xbound(xbound)
    ax1.set_ybound(ybound)
    ax2.set_xbound(xbound)
    ax2.set_ybound(ybound)

    f.savefig(f'./output/temp_figures/violin_plot_{feature}_{int(time.time())}.svg')
    del f
    plt.close()

def export_obs_distr_violinplot(observation_index, data_R, data_S):
    if observation_index == 'all':
        print('[ERROR] Observation distribution violin plot report does not support the visualization of all observations')
        return
    data_R_o = get_observation_data(observation_index, data_R)
    data_S_o = get_observation_data(observation_index, data_S)
    if not any(data_R_o) or not any(data_S_o):
        return
    
    f, [ax1, ax2] = plt.subplots(2, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution violin plots of observation with index {observation_index}')
    ax1.violinplot(data_R_o, vert=False, widths=0.7,
                     showmeans=True, showextrema=True, showmedians=True)
    ax1.set_title('Real dataset')
    ax1.set_yticklabels([])
    ax1.set_yticks([])
    ax1.set
    ax2.violinplot(data_S_o, vert=False, widths=0.7,
                     showmeans=True, showextrema=True, showmedians=True)
    ax2.set_title('Simulated dataset')
    ax2.set_yticklabels([])
    ax2.set_yticks([])

    xbound = (min(ax1.get_xbound()[0], ax2.get_xbound()[0]), max(ax1.get_xbound()[1], ax2.get_xbound()[1]))
    ybound = (min(ax1.get_ybound()[0], ax2.get_ybound()[0]), max(ax1.get_ybound()[1], ax2.get_ybound()[1]))

    ax1.set_xbound(xbound)
    ax1.set_ybound(ybound)
    ax2.set_xbound(xbound)
    ax2.set_ybound(ybound)

    f.savefig(f'./output/temp_figures/violin_plot_obs_{observation_index}_{int(time.time())}.svg')
    del f
    plt.close()

def export_distr_densityplot(feature, data_R, data_S, features_R, features_S):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    f.suptitle(f'Distribution density plot of feature {feature}')
    sns.kdeplot(data_R_f, ax=ax, label='Real dataset', fill=True, common_norm=False, color='#5480d1', alpha=0.5, linewidth=0)
    sns.kdeplot(data_S_f, ax=ax, label='Simulated dataset', fill=True, common_norm=False, color='#d65161', alpha=0.5, linewidth=0)
    ax.legend()

    f.savefig(f'./output/temp_figures/density_plot_{feature}_{int(time.time())}.svg')
    del f
    plt.close()

def export_obs_distr_densityplot(observation_index, data_R, data_S, with_ml_sim, ml_random_state):
    if observation_index != 'all':
        data_R_o = get_observation_data(observation_index, data_R)
        data_S_o = get_observation_data(observation_index, data_S)
        if not any(data_R_o) or not any(data_S_o):
            return

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    
    if observation_index == 'all':
        if with_ml_sim:
            print('[LOG] OBS DENSITY PLT: Generating ML dataset')
            data_ML = ml_simulated_dataset(data_R, ml_random_state)
        f.suptitle(f'Distribution density plot of all observations')
        for index in range(len(data_R)):
            data_R_o = get_observation_data(index, data_R)
            data_S_o = get_observation_data(index, data_S)
            label = 'Real dataset' if index == 0 else None
            sns.kdeplot(data_R_o, ax=ax, label=label, fill=True, common_norm=False, color='#5480d1', alpha=0.2, linewidth=0)
            label = 'Simulated dataset' if index == 0 else None
            sns.kdeplot(data_S_o, ax=ax, label=label, fill=True, common_norm=False, color='#d65161', alpha=0.2, linewidth=0)
            if with_ml_sim:
                data_ML_o = get_observation_data(index, data_ML)
                label = 'ML generated dataset' if index == 0 else None
                sns.kdeplot(data_ML_o, ax=ax, label=label, fill=True, common_norm=False, color='#2af52d', alpha=0.2, linewidth=0)
    else:
        f.suptitle(f'Distribution density plot of observation with index {observation_index}')
        sns.kdeplot(data_R_o, ax=ax, label='Real dataset', fill=True, common_norm=False, color='#5480d1', alpha=0.5, linewidth=0)
        sns.kdeplot(data_S_o, ax=ax, label='Simulated dataset', fill=True, common_norm=False, color='#d65161', alpha=0.5, linewidth=0)

    ax.legend()
    f.savefig(f'./output/temp_figures/density_plot_obs_{observation_index}_{int(time.time())}.svg')
    del f
    plt.close()

def export_avg_var_scatter_plot(data_R, data_S, axis=0, with_ml_sim = False, ml_random_state = None):
    data_R_x = np.average(data_R, axis=axis)
    data_R_y = np.var(data_R, axis=axis)
    data_S_x = np.average(data_S, axis=axis)
    data_S_y = np.var(data_S, axis=axis)
    if with_ml_sim:
        print('[LOG] AVG VS VAR: Generating ML dataset')
        data_ML = ml_simulated_dataset(data_R, ml_random_state)
        data_ML_x = np.average(data_ML, axis=axis)
        data_ML_y = np.var(data_ML, axis=axis)

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(9, 7)
    f.suptitle('Feature average value vs variance' if axis == 0 else 'Observation average value vs variance')
    ax.scatter(data_R_x, data_R_y, c='#5480d1', linewidths=None, alpha=0.5, label='Real')
    ax.scatter(data_S_x, data_S_y, c='#d65161', linewidths=None, alpha=0.5, label='Simulated')
    if with_ml_sim:
        ax.scatter(data_ML_x, data_ML_y, c='#53d453', linewidths=None, alpha=0.5, label='ML generated')
    ax.set_xlabel('Average value')
    ax.set_ylabel('Variance value')
    ax.legend()
    
    f.savefig(f'./output/temp_figures/avg_var_{"feat" if axis == 0 else "obs"}_scatter_plot_{int(time.time())}.svg')
    del f
    plt.close()

def export_distance(feature, data_R, data_S, features_R, features_S):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    dist = np.linalg.norm(data_R_f - data_S_f)
    print(f'[RESULT] Euclidean distance of feature {feature} : {dist}')

    with open(f'./output/temp_results/distance_{feature}.txt', 'w', encoding="utf-8") as file:
        file.write('\t\t<tr colspan="2">\n')
        file.write(f'\t\t\t<td>Euclidean distance of feature {feature}</td>\n')
        file.write(f'\t\t\t<td>{dist}</td>\n')
        file.write('\t\t</tr>\n')

def export_distance_all(data_R, data_S, features_R, features_S, output):
    distance_results = []
    for f_idx in range(len(features_R)):
        data_R_f = get_feature_data(features_R[f_idx], data_R, features_R)
        data_S_f = get_feature_data(features_S[f_idx], data_S, features_S)

        dist = np.linalg.norm(data_R_f - data_S_f)
        distance_results.append(str(dist))
    distance_results = np.array(distance_results)
    if output:
        try:
            with open(output, 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(distance_results))
            print('[LOG] Distance result file created')
        except: 
            print('[ERROR] Failed to export distance results to file')

def export_jensenshannon(data_R, data_S, output, axis=0):
    scaler = MinMaxScaler((0, 1))
    data_R = scaler.fit_transform(data_R)
    data_S = scaler.fit_transform(data_S)
    jenshan = scipy.spatial.distance.jensenshannon(data_R, data_S, base=2, axis=axis) ** 2
    if output:
        try:
            with open(output, 'w', encoding="utf-8") as output_file:
                output_file.write(','.join([str(i) for i in jenshan]))
            print('[LOG] Jensen-Shannon divergence result file created')
        except Exception as e: 
            print(e)
            print('[ERROR] Failed to export Jensen-Shannon divergence results to file')

def export_obs_distance(observation_index, data_R, data_S):
    if observation_index == 'all':
        print('[ERROR] Observation Euclidean distance report does not support reporting on all observations. Use general report to csv `observation_distance` instead.')
        return
    data_R_o = get_observation_data(observation_index, data_R)
    data_S_o = get_observation_data(observation_index, data_S)
    if not any(data_R_o) or not any(data_S_o):
        return

    dist = []
    if data_S_o.shape[0] < data_R_o.shape[0]:
        data_S_o_padded = np.zeros(data_R_o.shape)
        data_S_o_padded[:data_S_o.shape[0]] = data_S_o
        dist = np.linalg.norm(data_R_o - data_S_o_padded)
    elif data_R_o.shape[0] < data_S_o.shape[0]:
        data_R_o_padded = np.zeros(data_S_o.shape)
        data_R_o_padded[:data_R_o.shape[0]] = data_R_o
        dist = np.linalg.norm(data_S_o - data_R_o_padded)
    else:
        dist = np.linalg.norm(data_R_o - data_S_o)

    print(f'[RESULT] Euclidean distance of observation with index {observation_index} : {dist}')

    with open(f'./output/temp_results/distance_obs_{observation_index}.txt', 'w', encoding="utf-8") as file:
        file.write('\t\t<tr colspan="2">\n')
        file.write(f'\t\t\t<td>Euclidean distance of observation with index {observation_index}</td>\n')
        file.write(f'\t\t\t<td>{dist}</td>\n')
        file.write('\t\t</tr>\n')

def export_obs_distance_all(data_R, data_S, output):
    distance_results = []
    for o_idx in range(len(data_R)):
        data_R_o = get_observation_data(o_idx, data_R)
        data_S_o = get_observation_data(o_idx, data_S)

        dist = []
        if data_S_o.shape[0] < data_R_o.shape[0]:
            data_S_o_padded = np.zeros(data_R_o.shape)
            data_S_o_padded[:data_S_o.shape[0]] = data_S_o
            dist = np.linalg.norm(data_R_o - data_S_o_padded)
        elif data_R_o.shape[0] < data_S_o.shape[0]:
            data_R_o_padded = np.zeros(data_S_o.shape)
            data_R_o_padded[:data_R_o.shape[0]] = data_R_o
            dist = np.linalg.norm(data_S_o - data_R_o_padded)
        else:
            dist = np.linalg.norm(data_R_o - data_S_o)
        distance_results.append(str(dist))
    distance_results = np.array(distance_results)
    if output:
        try:
            with open(output, 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(distance_results))
            print('[LOG] Observation distance result file created')
        except: 
            print('[ERROR] Failed to export observation distance results to file')

def export_statistics(feature, data_R, data_S, features_R, features_S):
    data_R_f = get_feature_data(feature, data_R, features_R)
    data_S_f = get_feature_data(feature, data_S, features_S)
    if not any(data_R_f) or not any(data_S_f):
        return

    avg = { 'real': np.average(data_R_f), 'sim': np.average(data_S_f)}
    median = { 'real': np.median(data_R_f), 'sim': np.median(data_S_f)}
    std = { 'real': np.std(data_R_f), 'sim': np.std(data_S_f)}
    var = { 'real': np.var(data_R_f), 'sim': np.var(data_S_f)}

    print('[RESULT] Average of feature {0:>16} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(feature, avg['real'], avg['sim']))
    print('[RESULT] Median of feature {0:>17} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(feature, median['real'], median['sim']))
    print('[RESULT] Standard deviation of feature {0:>5} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(feature, std['real'], std['sim']))
    print('[RESULT] Variance of feature {0:>15} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(feature, var['real'], var['sim']))

    with open(f'./output/temp_statistics/{feature}.txt', 'w', encoding="utf-8") as file:
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Average of feature {feature}</td>\n')
        file.write(f'\t\t\t<td>{avg["real"]}</td>\n')
        file.write(f'\t\t\t<td>{avg["sim"]}</td>\n')
        file.write('\t\t</tr>\n')
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Median of feature {feature}</td>\n')
        file.write(f'\t\t\t<td>{median["real"]}</td>\n')
        file.write(f'\t\t\t<td>{median["sim"]}</td>\n')
        file.write('\t\t</tr>\n')
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Standard deviation of feature {feature}</td>\n')
        file.write(f'\t\t\t<td>{std["real"]}</td>\n')
        file.write(f'\t\t\t<td>{std["sim"]}</td>\n')
        file.write('\t\t</tr>\n')
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Variance of feature {feature}</td>\n')
        file.write(f'\t\t\t<td>{var["real"]}</td>\n')
        file.write(f'\t\t\t<td>{var["sim"]}</td>\n')
        file.write('\t\t</tr>\n')

def export_statistics_all(data_R, data_S, features_R, features_S, output_dir):
    R_avg, S_avg = [], []
    R_median, S_median = [], []
    R_std, S_std = [], []
    R_var, S_var = [], []
    for f_idx in range(len(features_R)):
        data_R_f = np.array(get_feature_data(features_R[f_idx], data_R, features_R), dtype=float)
        data_S_f = np.array(get_feature_data(features_S[f_idx], data_S, features_S), dtype=float)

        R_avg.append(str(np.average(data_R_f)))
        R_median.append(str(np.median(data_R_f)))
        R_std.append(str(np.std(data_R_f)))
        R_var.append(str(np.var(data_R_f)))

        S_avg.append(str(np.average(data_S_f)))
        S_median.append(str(np.median(data_S_f)))
        S_std.append(str(np.std(data_S_f)))
        S_var.append(str(np.var(data_S_f)))
        
    if output_dir:
        try:
            if not str(output_dir).strip().endswith('/') and not str(output_dir).endswith('\\'):
                output_dir = output_dir.strip() + '/'
            with open(output_dir + '/real_stat.csv', 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(R_avg) + '\n')
                output_file.write(','.join(R_median) + '\n')
                output_file.write(','.join(R_std) + '\n')
                output_file.write(','.join(R_var))
            with open(output_dir + '/sim_stat.csv', 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(S_avg) + '\n')
                output_file.write(','.join(S_median) + '\n')
                output_file.write(','.join(S_std) + '\n')
                output_file.write(','.join(S_var))
            print('[LOG] Statistics result files created')
        except: 
            print('[ERROR] Failed to export statistic results to file')

def export_obs_statistics_all(data_R, data_S, output_dir):
    R_avg, S_avg = [], []
    R_median, S_median = [], []
    R_std, S_std = [], []
    R_var, S_var = [], []
    for o_idx in range(len(data_R)):
        data_R_o = np.array(get_observation_data(o_idx, data_R), dtype=float)
        data_S_o = np.array(get_observation_data(o_idx, data_S), dtype=float)

        R_avg.append(str(np.average(data_R_o)))
        R_median.append(str(np.median(data_R_o)))
        R_std.append(str(np.std(data_R_o)))
        R_var.append(str(np.var(data_R_o)))

        S_avg.append(str(np.average(data_S_o)))
        S_median.append(str(np.median(data_S_o)))
        S_std.append(str(np.std(data_S_o)))
        S_var.append(str(np.var(data_S_o)))
        
    if output_dir:
        try:
            if not str(output_dir).strip().endswith('/') and not str(output_dir).endswith('\\'):
                output_dir = output_dir.strip() + '/'
            with open(output_dir + '/real_obs_stat.csv', 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(R_avg) + '\n')
                output_file.write(','.join(R_median) + '\n')
                output_file.write(','.join(R_std) + '\n')
                output_file.write(','.join(R_var))
            with open(output_dir + '/sim_obs_stat.csv', 'w', encoding="utf-8") as output_file:
                output_file.write(','.join(S_avg) + '\n')
                output_file.write(','.join(S_median) + '\n')
                output_file.write(','.join(S_std) + '\n')
                output_file.write(','.join(S_var))
            print('[LOG] Observation statistics result files created')
        except: 
            print('[ERROR] Failed to export observation statistic results to file')

def export_obs_statistics(observation_index, data_R, data_S):
    if observation_index == 'all':
        print('[ERROR] Observation statistics report does not support reporting on all observations. Use general report to csv `observation_statistics` instead.')
        return
    data_R_o = get_observation_data(observation_index, data_R)
    data_S_o = get_observation_data(observation_index, data_S)
    if not any(data_R_o) or not any(data_S_o):
        return

    avg = { 'real': np.average(data_R_o), 'sim': np.average(data_S_o)}
    median = { 'real': np.median(data_R_o), 'sim': np.median(data_S_o)}
    std = { 'real': np.std(data_R_o), 'sim': np.std(data_S_o)}
    var = { 'real': np.var(data_R_o), 'sim': np.var(data_S_o)}

    print('[RESULT] Average of observation with index {0:>16} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(observation_index, avg['real'], avg['sim']))
    print('[RESULT] Median of observation with index {0:>17} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(observation_index, median['real'], median['sim']))
    print('[RESULT] Standard deviation of observation with index {0:>5} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(observation_index, std['real'], std['sim']))
    print('[RESULT] Variance of observation with index {0:>15} : REAL = {1:>25}, SIMULATED = {2:>25}'.format(observation_index, var['real'], var['sim']))

    with open(f'./output/temp_statistics/obs_{observation_index}.txt', 'w', encoding="utf-8") as file:
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Average of observation with index {observation_index}</td>\n')
        file.write(f'\t\t\t<td>{avg["real"]}</td>\n')
        file.write(f'\t\t\t<td>{avg["sim"]}</td>\n')
        file.write('\t\t</tr>\n')
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Median of observation with index {observation_index}</td>\n')
        file.write(f'\t\t\t<td>{median["real"]}</td>\n')
        file.write(f'\t\t\t<td>{median["sim"]}</td>\n')
        file.write('\t\t</tr>\n')
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Standard deviation of observation with index {observation_index}</td>\n')
        file.write(f'\t\t\t<td>{std["real"]}</td>\n')
        file.write(f'\t\t\t<td>{std["sim"]}</td>\n')
        file.write('\t\t</tr>\n')
        file.write('\t\t<tr>\n')
        file.write(f'\t\t\t<td>Variance of observation with index {observation_index}</td>\n')
        file.write(f'\t\t\t<td>{var["real"]}</td>\n')
        file.write(f'\t\t\t<td>{var["sim"]}</td>\n')
        file.write('\t\t</tr>\n')