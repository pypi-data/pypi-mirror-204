from diffusers import UNet2DConditionModel, ControlNetModel
from hcpdiff.models.controlnet import ControlNetPlugin
from hcpdiff.utils.ckpt_manager import CkptManagerPKL

if __name__ == '__main__':
    unet = UNet2DConditionModel.from_pretrained(
            'runwayml/stable-diffusion-v1-5', subfolder="unet", revision=None
        )

    ctnet_0 = ControlNetModel()

    to_layers = [
        unet.down_blocks[0],
        unet.down_blocks[1],
        unet.down_blocks[2],
        unet.down_blocks[3],
        unet.mid_block,
    ]

    ckptmg = CkptManagerPKL()

    ctnet = ControlNetPlugin([unet], to_layers, unet)

    ctnet.load_state_dict(ckptmg.load_ckpt('ckpt/control/controlnet.ckpt'))