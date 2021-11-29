import numpy as np
from .utils import *


def test_random_contamination(
    power: int,
    w_low: float,
    w_high: float,
    x_low: float,
    x_high: float,
    noise_level: float,
    epsilon: float,
    training_size: int,
    testing_size: int,
    regressor: PolynomialRegressor
):
    rng = np.random.default_rng()
    w = generate_random_weights(power, w_low, w_high)
    x_training, y_training = generate_random_samples(
        w,
        x_low,
        x_high,
        noise_level,
        training_size
    )
    contamination_size = int(training_size * epsilon)
    contaminated_indices = rng.choice(training_size, contamination_size, False)
    x_contamination = rng.uniform(
        x_training.min(),
        x_training.max(),
        contamination_size
    )
    y_contamination = rng.uniform(
        y_training.min(),
        y_training.max(),
        contamination_size
    )
    x_training[contaminated_indices] = x_contamination
    y_training[contaminated_indices] = y_contamination
    x_testing, y_testing = generate_random_samples(
        w,
        x_low,
        x_high,
        0,
        testing_size)
    test_model(
        x_training,
        y_training,
        contaminated_indices,
        x_testing,
        y_testing,
        power,
        regressor,
        "random contamination"
    )


if __name__ == "__main__":
    true_power = 9
    w_low = -10
    w_high = 10
    x_low = -1
    x_high = 1
    noise_level = 1
    training_size = 1000
    testing_size = 1000
    kernel_size = (0.1, 5)  # to be tuned
    strides = (0.02, 1)  # to be tuned
    preprocessor_threshold = 0.01  # to be tuned
    fitted_power = 5
    regularization_weight = 0
    epsilon = 0.49
    huber_loss_threshold = 20
    learning_rate = 0.01
    batch_size = 100
    max_iter = 100000

    test_random_contamination(
        true_power,
        w_low,
        w_high,
        x_low,
        x_high,
        noise_level,
        epsilon,
        training_size,
        testing_size,
        PolynomialRegressor(
            MeanKernelPreprocessor(
                kernel_size,
                strides,
                preprocessor_threshold
            ),
            fitted_power,
            L1Regularization(),
            regularization_weight,
            HuberLoss(epsilon, huber_loss_threshold),
            learning_rate,
            batch_size,
            max_iter
        )
    )
