from typing import Optional, Union, Tuple

import re
import torch
from omegaconf import OmegaConf

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def low_rank_approximate(weight, rank, clamp_quantile=0.99):
    if len(weight.shape)==4: # conv
        weight=weight.flatten(1)
        out_ch, in_ch, k1, k2 = weight.shape

    U, S, Vh = torch.linalg.svd(weight)
    U = U[:, :rank]
    S = S[:rank]
    U = U @ torch.diag(S)

    Vh = Vh[:rank, :]

    dist = torch.cat([U.flatten(), Vh.flatten()])
    hi_val = torch.quantile(dist, clamp_quantile)
    low_val = -hi_val

    U = U.clamp(low_val, hi_val)
    Vh = Vh.clamp(low_val, hi_val)

    if len(weight.shape) == 4:
        # U is (out_channels, rank) with 1x1 conv.
        U = U.reshape(U.shape[0], U.shape[1], 1, 1)
        # V is (rank, in_channels * kernel_size1 * kernel_size2)
        Vh = Vh.reshape(Vh.shape[0], in_ch, k1, k2)
    return U, Vh

def load_config(path):
    cfg = OmegaConf.load(path)
    if '_base_' in cfg:
        for base in cfg['_base_']:
            cfg = OmegaConf.merge(load_config(base), cfg)
        del cfg['_base_']
    return cfg

def load_config_with_cli(path, args_list=None):
    cfg = load_config(path)
    cfg_cli = OmegaConf.from_cli(args_list)
    cfg = OmegaConf.merge(cfg, cfg_cli)
    return cfg

def _default(v, default):
    return default if v is None else v

def dict_get(data, key, default):
    return data[key] if key in data else default

def cycle_data(data_loader, arb=False):
    epoch=0
    while True:
        if arb:
            data_loader.dataset.bucket.rest(epoch)
        for data in data_loader:
            yield data
        epoch+=1

def get_cfg_range(cfg_text:str):
    dy_cfg_f='ln'
    if cfg_text.find(':')!=-1:
        cfg_text, dy_cfg_f = cfg_text.split(':')

    if cfg_text.find('-')!=-1:
        l, h = cfg_text.split('-')
        return float(l), float(h), dy_cfg_f
    else:
        return float(cfg_text), float(cfg_text), dy_cfg_f

def to_validate_file(name):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", name)  # 替换为下划线
    return new_title

def make_mask(start, end, length):
    mask=torch.zeros(length)
    mask[int(length*start):int(length*end)]=1
    return mask.bool()

def get_file_name(file: str):
    return file.rsplit('.',1)[0]

def get_file_ext(file: str):
    return file.rsplit('.',1)[1].lower()

def factorization(dimension: int, factor:int=-1) -> Tuple[int, int]:
    find_one = lambda x: len(x) - (x.rfind('1') + 1)
    dim_bin = bin(dimension)
    num = find_one(dim_bin)
    f_max = (len(dim_bin)-3)>>1 if factor<0 else find_one(bin(factor))
    num = min(num, f_max)
    return dimension>>num, 1<<num