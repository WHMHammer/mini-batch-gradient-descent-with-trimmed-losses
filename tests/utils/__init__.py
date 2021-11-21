from os import makedirs
from os.path import join

from .polynomial_regressor import *
from .figures import *


def mean_square_error(y: np.ndarray, y_bar: np.ndarray) -> float:
    return np.square(y_bar - y).sum() / y_bar.shape[0]


def test_model(
    x_training: np.ndarray, y_training: np.ndarray,
    contaminated_indices: np.ndarray,
    x_testing: np.ndarray, y_testing: np.ndarray,
    regressor: PolynomialRegressor,
    test_name: str
):
    dir_name = join("test_results", test_name.replace(" ", "_"))
    try:
        makedirs(dir_name)
    except FileExistsError:
        pass

    regressor.fit(x_training, y_training)
    y_bar_training = regressor.predict(x_training)
    y_bar_testing = regressor.predict(x_testing)
    mse = mean_square_error(y_testing, y_bar_testing)
    export_figure(x_training, y_training, y_bar_training, contaminated_indices,
                  f"{test_name} with trimming", "training set", join(dir_name, "with_trimming_training"))
    export_figure(x_testing, y_testing, y_bar_testing, None,
                  f"{test_name} with trimming", f"testing set - MSE={mse}", join(dir_name, "with_trimming_testing"))

    regressor.model.loss.contamination_proportion = 0
    regressor.fit(x_training, y_training)
    y_bar_training = regressor.predict(x_training)
    y_bar_testing = regressor.predict(x_testing)
    mse = mean_square_error(y_testing, y_bar_testing)
    export_figure(x_training, y_training, y_bar_training, contaminated_indices,
                  f"{test_name} without trimming", "training set", join(dir_name, "without_trimming_training"))
    export_figure(x_testing, y_testing, y_bar_testing, None,
                  f"{test_name} without trimming", f"testing set - MSE={mse}", join(dir_name, "without_trimming_testing"))
