from jax.numpy import mean, square


def mse(y, yhat):
    return mean(square(y - yhat))
