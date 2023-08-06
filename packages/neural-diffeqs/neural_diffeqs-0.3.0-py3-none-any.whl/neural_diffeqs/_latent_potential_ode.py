
# -- import packages: ----------------------------------------------------------
import torch
import ABCParse


# -- import local dependencies: ------------------------------------------------
from . import core


# -- import standard libraries and define types: -------------------------------
from typing import Union, List, Any
NoneType = type(None)


# -- Main operational class: ---------------------------------------------------
class LatentPotentialODE(core.BaseLatentODE):
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
        brownian_dim=1,
    ):
        super().__init__()

        # explicitly state that we are not learning a potential function by default
        mu_potential = False
        self.__config__(locals())
        self.potential = core.Potential(state_size)

    def drift(self, y) -> torch.Tensor:
        return self.mu(y)

    def prior_drift(self, y) -> torch.Tensor:
        return self.potential.potential_gradient(y)
