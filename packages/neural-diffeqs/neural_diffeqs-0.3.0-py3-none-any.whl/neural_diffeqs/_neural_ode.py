
# -- import packages: ----------------------------------------------------------
import torch
import ABCParse


# -- import local dependencies: ------------------------------------------------
from .core._base_neural_ode import BaseODE


# -- import standard libraries and define types: -------------------------------
from typing import Union, List, Any
NoneType = type(None)


# -- Main operational class: ---------------------------------------------------
class NeuralODE(BaseODE):
    DIFFEQ_TYPE = "ODE"
    def __init__(
        self,
        state_size,
        mu_hidden: Union[List[int], int] = [2000, 2000],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.2,
        mu_bias: bool = True,
        mu_output_bias: bool = True,
        mu_n_augment: int = 0,
        sde_type="ito",
        noise_type="general",
    ):
        sigma_hidden = []
        sigma_output_bias = False
        brownian_dim = 1

        super().__init__()

        self.__config__(locals())

    def drift(self, y) -> torch.Tensor:
        return self.mu(y)

    def forward(self, t, y):
        return self.mu(y)
