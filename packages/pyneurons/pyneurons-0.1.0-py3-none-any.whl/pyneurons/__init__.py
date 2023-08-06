from . import random
from . import vjp
from .apply import apply
from .binary import binary
from .bind import bind
from .box import Box
from .brelu1 import brelu1
from .compose import compose
from .concat import concat
from .explode import explode
from .fit import fit
from .gd import gd
from .identity import identity
from .implode import implode
from .loss import loss
from .model import Model
from .mse import mse
from .neuron import neuron
from .relu import relu
from .relu1 import relu1
from .spark import spark
from .spike import spike
from .split import split
from .stack import stack
from .unstack import unstack

Neuron = bind("Neuron", neuron, apply)
Binary = compose("Binary", Neuron, binary)
BReLU1 = compose("BReLU1", Neuron, brelu1)
ReLU = compose("ReLU", Neuron, relu)
ReLU1 = compose("ReLU1", Neuron, relu1)
Spark = BReLU1
Spike = Binary

__all__ = [
    "BReLU1",
    "Binary",
    "Box",
    "Model",
    "Neuron",
    "ReLU",
    "ReLU1",
    "Spark",
    "Spike",
    "apply",
    "binary",
    "bind",
    "brelu1",
    "compose",
    "concat",
    "explode",
    "fit",
    "gd",
    "identity",
    "implode",
    "loss",
    "mse",
    "neuron",
    "random",
    "relu",
    "relu1",
    "spark",
    "spike",
    "split",
    "stack",
    "unstack",
    "vjp",
]
