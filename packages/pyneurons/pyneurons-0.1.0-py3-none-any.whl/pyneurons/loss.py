from .mse import mse


def loss(model, x, y):
    yhat = model(x)
    return mse(y, yhat)
