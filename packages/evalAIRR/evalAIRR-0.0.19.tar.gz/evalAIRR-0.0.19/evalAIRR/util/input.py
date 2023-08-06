import numpy as np

def read_encoded_csv(csv_path):
    print('[LOG] Reading file: ' + csv_path)
    try:
        data_file = open(csv_path, "r")
        features = data_file.readline().split(',')
        features = [f.replace('\n', '').strip() for f in features]
        print(f'[LOG] Number of features in "{csv_path}" :', len(features))
        data = []
        for row in data_file:
            row = row.replace('\n', '').split(',')
            float_row = []
            for x in row:
                float_row.append(float(x))
            data.append(float_row)
        data_file.close()
        return np.array(features), np.array(data)
    except:
        print(f'[ERROR] Failed to read file {csv_path}')
        return None, None
    
def remove_non_mutual_features(features_R, features_S, data_R, data_S):
    matching_features = set(features_R).intersection(features_S)
    
    idx_R = [i for i, feature in enumerate(features_R) if feature in matching_features]
    idx_S = [i for i, feature in enumerate(features_S) if feature in matching_features]
    
    return np.array(list(matching_features)), data_R[:,idx_R], data_S[:,idx_S]