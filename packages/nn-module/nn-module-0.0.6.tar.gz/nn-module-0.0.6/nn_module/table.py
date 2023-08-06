import torch
from torch import nn
from nn_module import Module

class Table(Module):
    def __init__(self, d1: int, d2: int):
        super().__init__()
        self.register_parameter("table", nn.Parameter(torch.empty(d1, d2)))
        self._reset_parameters()
    
    def _reset_parameters(self):
        nn.init.xavier_uniform_(self.table)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(d1={self.table.shape[0]}, d2={self.table.shape[1]})"
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        :param x: (n, d1)
        :return: (n, d1, d2)
        """
        assert len(x.shape) == 2
        assert x.shape[1] == self.table.shape[0]
        x_ = x.unsqueeze(2) # (n, d1, 1)
        t_ = self.table.unsqueeze(0) # (1, d1, d2)
        return x_ * t_


if __name__ == "__main__":
    t = Table(5, 3)
    print(t.table)
    x = torch.Tensor([
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
    ])
    print(t.forward(x))