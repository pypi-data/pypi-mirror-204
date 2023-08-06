
# -- import packages: ----------------------------------------------------------
import torch
import ABCParse


# -- import local dependencies: ------------------------------------------------
from .core._base_neural_sde import BaseSDE


# -- import standard libraries and define types: -------------------------------
from typing import Union, List, Any
NoneType = type(None)


# -- Main operational class: ---------------------------------------------------
class NeuralSDE(BaseSDE):
    DIFFEQ_TYPE = "SDE"
    def __init__(
        self,
        state_size,
        mu_hidden: Union[List[int], int] = [2000, 2000],
        sigma_hidden: Union[List[int], int] = [400, 400],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        sigma_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.2,
        sigma_dropout: Union[float, List[float]] = 0.2,
        mu_bias: bool = True,
        sigma_bias: List[bool] = True,
        mu_output_bias: bool = True,
        sigma_output_bias: bool = True,
        mu_n_augment: int = 0,
        sigma_n_augment: int = 0,
        sde_type="ito",
        noise_type="general",
        brownian_dim=1,
        coef_drift: float = 1.,
        coef_diffusion: float = 1.,
    ):
        super().__init__()

        self.__config__(locals())

    def drift(self, y)->torch.Tensor:
        return self.mu(y) * self.coef_drift

    def diffusion(self, y)->torch.Tensor:
        return self.sigma(y).view(y.shape[0], y.shape[1], self.brownian_dim) * self.coef_diffusion
