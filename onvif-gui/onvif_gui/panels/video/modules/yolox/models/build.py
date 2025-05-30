#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#******************************************************************************/

import torch
from torch import nn
from torch.hub import load_state_dict_from_url

__all__ = [
    "create_yolox_model",
    "yolox_nano",
    "yolox_tiny",
    "yolox_s",
    "yolox_m",
    "yolox_l",
    "yolox_x",
    "yolov3",
    "yolox_custom"
]

_CKPT_ROOT_URL = "https://github.com/Megvii-BaseDetection/YOLOX/releases/download"
_CKPT_FULL_PATH = {
    "yolox-nano": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_nano.pth",
    "yolox-tiny": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_tiny.pth",
    "yolox-s": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_s.pth",
    "yolox-m": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_m.pth",
    "yolox-l": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_l.pth",
    "yolox-x": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_x.pth",
    "yolov3": f"{_CKPT_ROOT_URL}/0.1.1rc0/yolox_darknet.pth",
}


def create_yolox_model(name: str, pretrained: bool = True, num_classes: int = 80, device=None,
                       exp_path: str = None, ckpt_path: str = None) -> nn.Module:
    """creates and loads a YOLOX model

    Args:
        name (str): name of model. for example, "yolox-s", "yolox-tiny" or "yolox_custom"
        if you want to load your own model.
        pretrained (bool): load pretrained weights into the model. Default to True.
        device (str): default device to for model. Default to None.
        num_classes (int): number of model classes. Default to 80.
        exp_path (str): path to your own experiment file. Required if name="yolox_custom"
        ckpt_path (str): path to your own ckpt. Required if name="yolox_custom" and you want to
            load a pretrained model


    Returns:
        YOLOX model (nn.Module)
    """
    from yolox.exp import get_exp, Exp

    if device is None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
    device = torch.device(device)

    assert name in _CKPT_FULL_PATH or name == "yolox_custom", \
        f"user should use one of value in {_CKPT_FULL_PATH.keys()} or \"yolox_custom\""
    if name in _CKPT_FULL_PATH:
        exp: Exp = get_exp(exp_name=name)
        exp.num_classes = num_classes
        yolox_model = exp.get_model()
        if pretrained and num_classes == 80:
            weights_url = _CKPT_FULL_PATH[name]
            ckpt = load_state_dict_from_url(weights_url, map_location="cpu")
            if "model" in ckpt:
                ckpt = ckpt["model"]
            yolox_model.load_state_dict(ckpt)
    else:
        assert exp_path is not None, "for a \"yolox_custom\" model exp_path must be provided"
        exp: Exp = get_exp(exp_file=exp_path)
        yolox_model = exp.get_model()
        if ckpt_path:
            ckpt = torch.load(ckpt_path, map_location="cpu")
            if "model" in ckpt:
                ckpt = ckpt["model"]
            yolox_model.load_state_dict(ckpt)

    yolox_model.to(device)
    return yolox_model


def yolox_nano(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolox-nano", pretrained, num_classes, device)


def yolox_tiny(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolox-tiny", pretrained, num_classes, device)


def yolox_s(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolox-s", pretrained, num_classes, device)


def yolox_m(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolox-m", pretrained, num_classes, device)


def yolox_l(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolox-l", pretrained, num_classes, device)


def yolox_x(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolox-x", pretrained, num_classes, device)


def yolov3(pretrained: bool = True, num_classes: int = 80, device: str = None) -> nn.Module:
    return create_yolox_model("yolov3", pretrained, num_classes, device)


def yolox_custom(ckpt_path: str = None, exp_path: str = None, device: str = None) -> nn.Module:
    return create_yolox_model("yolox_custom", ckpt_path=ckpt_path, exp_path=exp_path, device=device)
