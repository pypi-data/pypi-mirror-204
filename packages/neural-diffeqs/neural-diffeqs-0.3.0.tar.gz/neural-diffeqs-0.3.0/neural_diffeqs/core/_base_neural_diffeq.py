

# -- import packages: ----------------------------------------------------------
import torch
import ABCParse


# -- import standard libraries: ------------------------------------------------
from abc import abstractmethod


# -- import local dependencies: ------------------------------------------------
from ._diffeq_config import DiffEqConfig


# -- Main operational class: ---------------------------------------------------
class BaseDiffEq(torch.nn.Module, ABCParse.ABCParse):
    DIFFEQ_TYPE = ""
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        """
        Must call self.__config__(locals()) in the __init__ of theinheriting
        class.
        
        
        """

    # -- required methods in child classes: ------------------------------------
    @abstractmethod
    def drift(self):
        """Called by self.f"""
        ...

    @abstractmethod
    def diffusion(self):
        """Called by self.g"""
        ...

    def f(self, t: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Should return the output of self.drift"""
        return self.drift(y)

    def g(self, t: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Should return the output of self.diffusion"""
        return self.diffusion(y)
