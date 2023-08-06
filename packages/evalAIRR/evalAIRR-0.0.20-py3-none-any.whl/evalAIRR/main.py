import os
import yaml
import argparse

from evalAIRR.version import __version__
from evalAIRR.util.input import read_encoded_csv, remove_non_mutual_features
from evalAIRR.util.corr import export_corr_heatmap, export_csv_corr_matrix
from evalAIRR.util.pca import export_pca_2d_comparison
from evalAIRR.util.univar import export_feature_ks_test, export_ks_test
from evalAIRR.util.univar import export_distr_histogram, export_obs_distr_histogram
from evalAIRR.util.univar import export_distr_boxplot, export_obs_distr_boxplot
from evalAIRR.util.univar import export_distr_violinplot, export_obs_distr_violinplot
from evalAIRR.util.univar import export_distr_densityplot, export_obs_distr_densityplot
from evalAIRR.util.univar import export_avg_var_scatter_plot
from evalAIRR.util.univar import export_jensenshannon
from evalAIRR.util.univar import export_distance, export_obs_distance
from evalAIRR.util.univar import export_statistics, export_obs_statistics
from evalAIRR.util.univar import export_distance_all, export_obs_distance_all
from evalAIRR.util.univar import export_statistics_all, export_obs_statistics_all
from evalAIRR.util.copula import export_copula_2d_scatter_plot, export_copula_3d_scatter_plot
from evalAIRR.util.report import export_report

#######################
### PARSE ARGUMENTS ###
#######################

parser = argparse.ArgumentParser(prog='evalairr')
parser.add_argument('-i', '--config', help='path to YAML confuguration file', required=True)
parser.add_argument('-v', '--version', action='version', version=__version__, help='check the version of evalAIRR')

def run():

    #################
    ### READ YAML ###
    #################

    YAML_FILE = parser.parse_args().config
    CONFIG = []
    with open(YAML_FILE, 'r') as stream:
        try:
            CONFIG = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    REPORTS = CONFIG['reports']

    try:
        OUTPUT = CONFIG['output']['path']
        if str(OUTPUT).lower().strip() == 'none':
            OUTPUT = None
    except: 
        OUTPUT = './output/report.html'
        
    #####################
    ### READ DATASETS ###
    #####################

    features_R, data_R = read_encoded_csv(CONFIG['datasets']['real']['path'])
    if data_R is None:
        return
    features_S, data_S = read_encoded_csv(CONFIG['datasets']['sim']['path'])
    if data_S is None:
        return

    # IF THE DATA IS PRE-ENCODED, ONLY USE MATCHING FEATURES
    matching_features, data_R, data_S = remove_non_mutual_features(features_R, features_S, data_R, data_S)
    features_R = features_S = matching_features

    ##########################################
    ### CREATE OUTPUT AND TEMP DIRECTORIES ###
    ##########################################

    if not os.path.exists('./output'):
        os.makedirs('./output')
    if not os.path.exists('./output/temp_figures'):
        os.makedirs('./output/temp_figures')
    if not os.path.exists('./output/temp_results'):
        os.makedirs('./output/temp_results')
    if not os.path.exists('./output/temp_statistics'):
        os.makedirs('./output/temp_statistics')

    #############################
    ### FEATURE BASED REPORTS ###
    #############################

    if ('feature_based' in REPORTS):
        reports_f = REPORTS['feature_based']
        for report in reports_f:
            features = reports_f[report]['features']
            report_types = reports_f[report]['report_types']
            for feature in features:

                # KOLMOGOROV-SMIRNOV TEST REPORT
                if 'ks' in report_types:
                    export_feature_ks_test(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION HISTOGRAM REPORT
                if 'distr_histogram' in report_types:
                    export_distr_histogram(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION BOX PLOT REPORT
                if 'distr_boxplot' in report_types:
                    export_distr_boxplot(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION VIOLIN PLOT REPORT
                if 'distr_violinplot' in report_types:
                    export_distr_violinplot(feature, data_R, data_S, features_R, features_S)

                # DISTRIBUTION DENSITY PLOT REPORT
                if 'distr_densityplot' in report_types:
                    export_distr_densityplot(feature, data_R, data_S, features_R, features_S)

                # EUCLIDEAN DISTANCE REPORT
                if 'distance' in report_types:
                    export_distance(feature, data_R, data_S, features_R, features_S)

                # STATISTICS REPORT
                if 'statistics' in report_types:
                    export_statistics(feature, data_R, data_S, features_R, features_S)

    #################################
    ### OBSERVATION BASED REPORTS ###
    #################################

    if ('observation_based' in REPORTS):
        reports_o = REPORTS['observation_based']
        for report in reports_o:
            observations = reports_o[report]['observations']
            report_types = reports_o[report]['report_types']
            for observation_index in observations:

                # OBSERVATION DISTRIBUTION HISTOGRAM REPORT
                if 'observation_distr_histogram' in report_types:
                    export_obs_distr_histogram(observation_index, data_R, data_S)

                # OBSERVATION DISTRIBUTION BOX PLOT REPORT
                if 'observation_distr_boxplot' in report_types:
                    export_obs_distr_boxplot(observation_index, data_R, data_S)

                # OBSERVATION DISTRIBUTION VIOLIN PLOT REPORT
                if 'observation_distr_violinplot' in report_types:
                    export_obs_distr_violinplot(observation_index, data_R, data_S)

                # OBSERVATION DISTRIBUTION DENSITY PLOT REPORT
                if 'observation_distr_densityplot' in report_types:
                    try:
                        with_ml_sim = reports_o[report]['with_ml_sim']
                    except: 
                        with_ml_sim = False
                    try:
                        ml_random_state = reports_o[report]['ml_random_state']
                    except: 
                        ml_random_state = None
                    export_obs_distr_densityplot(observation_index, data_R, data_S, with_ml_sim, ml_random_state)

                # OBSERVATION EUCLIDEAN DISTANCE REPORT
                if 'observation_distance' in report_types:
                    export_obs_distance(observation_index, data_R, data_S)

                # OBSERVATION STATISTICS REPORT
                if 'observation_statistics' in report_types:
                    export_obs_statistics(observation_index, data_R, data_S)

    #######################
    ### GENERAL REPORTS ###
    #######################

    if ('general' in REPORTS):
        reports_g = REPORTS['general']

        # KOLMOGOROV-SMIRNOV TEST REPORT FOR ALL FEATURES
        if ('ks' in reports_g):
            try:
                output = reports_g['ks']['output']
            except: 
                output = './output/ks.csv'
            export_ks_test(data_R, data_S, features_R, features_S, output)

        # STATISTICS REPORT
        if 'statistics' in reports_g:
            try:
                output_dir = reports_g['statistics']['output_dir']
            except:
                output_dir = './output/'
            export_statistics_all(data_R, data_S, features_R, features_S, output_dir)

        # OBSERVATION STATISTICS REPORT
        if 'observation_statistics' in reports_g:
            try:
                output_dir = reports_g['observation_statistics']['output_dir']
            except: 
                output_dir = './output/'
            export_obs_statistics_all(data_R, data_S, output_dir)

        # EUCLIDEAN DISTANCE REPORT
        if 'distance' in reports_g:
            try:
                output = reports_g['distance']['output']
            except:
                output = './output/dist.csv'
            export_distance_all(data_R, data_S, features_R, features_S, output)

        # OBSERVATION EUCLIDEAN DISTANCE REPORT
        if 'observation_distance' in reports_g:
            try:
                output = reports_g['observation_distance']['output']
            except: 
                output = './output/obs_dist.csv'
            export_obs_distance_all(data_R, data_S, output)

        # JENSEN-SHANNON DIVERGENCE REPORT
        if 'jensen_shannon' in reports_g:
            try:
                output = reports_g['jensen_shannon']['output']
            except:
                output = './output/jenshan.csv'
            export_jensenshannon(data_R, data_S, output, axis=0)

        # OBSERVATION JENSEN-SHANNON DIVERGENCE REPORT
        if 'observation_jensen_shannon' in reports_g:
            try:
                output = reports_g['observation_jensen_shannon']['output']
            except: 
                output = './output/obs_jenshan.csv'
            export_jensenshannon(data_R, data_S, output, axis=1)

        # CORRELATION MATRIX REPORT
        if ('corr' in reports_g):
            try:
                reduce_to_n_features = reports_g['corr']['reduce_to_n_features']
            except: 
                reduce_to_n_features = 0
            try:
                with_ml_sim = reports_g['corr']['with_ml_sim']
            except: 
                with_ml_sim = False
            try:
                ml_random_state = reports_g['corr']['ml_random_state']
            except: 
                ml_random_state = None
            export_corr_heatmap(data_R, data_S, len(features_R), len(features_S), reduce_to_n_features, with_ml_sim, ml_random_state)

        # CORRELATION MATRIX CSV EXPORT
        if ('corr_csv' in reports_g):
            try:
                output = reports_g['corr_csv']['output']
            except: 
                output = './output/corr.csv'
            export_csv_corr_matrix(data_R, data_S, output)

        # PCA 2D REPORT
        if ('pca_2d' in reports_g):
            try:
                with_ml_sim = reports_g['pca_2d']['with_ml_sim']
            except: 
                with_ml_sim = False
            try:
                ml_random_state = reports_g['pca_2d']['ml_random_state']
            except: 
                ml_random_state = None
            export_pca_2d_comparison(data_R, data_S, with_ml_sim, ml_random_state)

        # FEATURE AVERAGE VALUE VS VARIANCE REPORT
        if ('feature_average_vs_variance' in reports_g):
            try:
                with_ml_sim = reports_g['feature_average_vs_variance']['with_ml_sim']
            except: 
                with_ml_sim = False
            try:
                ml_random_state = reports_g['feature_average_vs_variance']['ml_random_state']
            except: 
                ml_random_state = None
            export_avg_var_scatter_plot(data_R, data_S, axis=0, with_ml_sim=with_ml_sim, ml_random_state=ml_random_state)

        # OBSERVATION AVERAGE VALUE VS VARIANCE REPORT
        if ('observation_average_vs_variance' in reports_g):
            try:
                with_ml_sim = reports_g['observation_average_vs_variance']['with_ml_sim']
            except: 
                with_ml_sim = False
            try:
                ml_random_state = reports_g['observation_average_vs_variance']['ml_random_state']
            except: 
                ml_random_state = None
            export_avg_var_scatter_plot(data_R, data_S, axis=1, with_ml_sim=with_ml_sim, ml_random_state=ml_random_state)

        # COPULA 2D REPORT
        if ('copula_2d' in reports_g):
            copula_reports = reports_g['copula_2d']
            for copula_report in copula_reports:
                if len(copula_reports[copula_report]) > 2:
                    print(f'[WARNING] More than 2 features provided in \'{copula_report}\'! Using only the first 2 for calculations.')
                elif len(copula_reports[copula_report]) < 2:
                    print(f'[ERROR] 2D copula scatter plot report \'{copula_report}\' requires 2 features!')
                    continue
                export_copula_2d_scatter_plot(copula_reports[copula_report][0], copula_reports[copula_report][1], data_R, data_S, features_R, features_S)

        # COPULA 3D REPORT
        if ('copula_3d' in reports_g):
            copula_reports = reports_g['copula_3d']
            for copula_report in copula_reports:
                if len(copula_reports[copula_report]) > 3:
                    print(f'[WARNING] More than 3 features provided in \'{copula_report}\'! Using only the first 3 for calculations.')
                elif len(copula_reports[copula_report]) < 3:
                    print(f'[ERROR] 3D copula scatter plot report \'{copula_report}\' requires 3 features!')
                    continue
                export_copula_3d_scatter_plot(copula_reports[copula_report][0], copula_reports[copula_report][1], copula_reports[copula_report][2], data_R, data_S, features_R, features_S)

    ##########################
    ### EXPORT HTML REPORT ###
    ##########################

    if OUTPUT is not None:
        export_report(OUTPUT)