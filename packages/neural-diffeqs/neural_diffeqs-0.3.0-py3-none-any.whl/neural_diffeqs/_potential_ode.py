# -- import packages: ----------------------------------------------------------
import torch
import ABCParse


# -- import local dependencies: ------------------------------------------------
from .core import BaseODE


# -- import standard libraries and define types: -------------------------------
from typing import Union, List, Any

NoneType = type(None)


# -- Main operational class: ---------------------------------------------------
class PotentialODE(BaseODE):
    DIFFEQ_TYPE = "ODE"
    sde_type = "ito"
    noise_type = "general"
    brownian_dim = 1
        
    def __init__(
        self,
        state_size,
        mu_hidden: Union[List[int], int] = [2000, 2000],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.2,
        mu_bias: bool = True,
        mu_output_bias: bool = True,
        mu_n_augment: int = 0,
    ):
        super().__init__()
        
        mu_potential = True

        self.__config__(locals())

    def _potential(self, y):
        return self.mu(y)

    def _gradient(self, ψ, y):
        """use-case: output is directly psi (from a potential network)"""
        return torch.autograd.grad(ψ, y, torch.ones_like(ψ), create_graph=True)[0]

    def drift(self, y) -> torch.Tensor:
        y = y.requires_grad_()
        ψ = self._potential(y)
        return self._gradient(ψ, y)

    def diffusion(self, y) -> torch.Tensor:
        return self.sigma(y).view(y.shape[0], y.shape[1], self.brownian_dim)
