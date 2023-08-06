import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

def ml_simulated_dataset(data_R, random_state=None):
    kernel = RBF(length_scale=1.0)
    model = GaussianProcessRegressor(kernel=kernel, random_state=random_state)
    model.fit(data_R, np.zeros(len(data_R)))

    mean = model.predict(data_R)
    covariance = model.kernel_(data_R)
    synthetic_data = np.random.multivariate_normal(mean, covariance, size=data_R.shape[1]).T

    return synthetic_data