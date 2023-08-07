import torch
from torch import nn

class AA(nn.Module):
    def __init__(self):
        super().__init__()
        self.para_dict = nn.ParameterDict()
        self.emb_dict = {}

    def forward(self):
        return self.emb_dict[1]-1.

if __name__ == '__main__':
    pl = nn.ParameterList()
    p1 = nn.Parameter(torch.randn(4), requires_grad=True)
    p2 = nn.Parameter(torch.randn(4), requires_grad=False)
    pl.append(p1)
    pl.append(p2)
    print(sum(pl))


    layer = AA()
    p1 = nn.Parameter(torch.randn(4), requires_grad=True)
    p2 = nn.Parameter(torch.randn(4), requires_grad=False)
    layer.para_dict['1']=p1
    layer.emb_dict[1]=p1
    layer.emb_dict[2]=p2

    optimizer = torch.optim.AdamW(params=[p1], lr=0.1, weight_decay=1e-2)

    print(p1)

    layer().mean().backward()
    optimizer.step()

    print(layer.emb_dict[1])
    print(layer.para_dict['1'])