from hcpdiff.models.plugin import SinglePluginParameter
import torch
from torch import nn

class PTest(SinglePluginParameter):
    def __init__(self, layer: nn.Module):
        super().__init__(layer)
        self.w2 = nn.Parameter(torch.randn(4,8), requires_grad=True)

    def forward(self, host_param: nn.Parameter):
        return host_param+self.w2

if __name__ == '__main__':
    layer = nn.Linear(8,4)
    x = torch.randn(1,8)

    pl = PTest(layer)

    y = layer(x)
    y.mean().backward()

    print(y.shape)
    print(layer.weight.grad)
    print(pl.w2.grad)