# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:28
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["BaseDataLoader", "BaseExp"]

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import logging
from pathlib import Path
import re
from typing import Union, Optional, Tuple

import numpy as np
import pandas as pd
import torch
from torch import nn, Tensor
from torch.utils.data import Dataset as TorchDataset

from .config import NetConfig


class BaseDataLoader(TorchDataset, metaclass=ABCMeta):
    """ Base data loader for network.

    Args:
        samples: The list of the samples.
        mode: default `train`, Optional in `train`, `test` and `eval`. The mode of the DataLoader.
    """

    def __init__(self,
                 samples: Union[list, np.ndarray, pd.DataFrame],
                 mode: str = "train"
                 ) -> None:
        super(BaseDataLoader, self).__init__()
        self.samples = samples
        if mode in ["train", "test", "eval"]:
            self.mode = mode
        else:
            raise ValueError(f"Unexpected input of the \"mode\": {mode}, please check it!")

    @abstractmethod
    def __getitem__(self,
                    index: int):
        pass

    def __len__(self) -> int:
        return len(self.samples)

    @staticmethod
    def merge_file(time: datetime,
                   lead_time: Optional[timedelta],
                   file: str
                   ) -> str:
        """ Merge the file with time and lead time.

        The time is report time while the lead time is not None. On the contrary, the time is live time while the lead
        time is None.

        Args:
            time: The report time or the live time
            lead_time: The lead time for forecast data.
            file: The string rule of the file.

        Returns:
            The file path.
        """
        if lead_time is None:
            # the time is live time while the lead time is None.
            return time.strftime(file)
        else:
            # the time is report time while the lead time is not None
            file_split_1 = time.strftime("_".join(file.split("_")[:-1]))
            file_split_2 = (time + lead_time).strftime(file.split("_")[-1])
            file = file_split_1 + "_" + file_split_2
            return file


class BaseExp(metaclass=ABCMeta):
    """ Base experiment.

    Args:
        net: The optimizer of the neural network
        cost_func: The cost functions for training
        config: The configurations of the neural network
        net_dir: The directory of the pretrained neural network or the saving
        log_dir: The directory of the logger
    """

    def __init__(self,
                 net: nn.Module,
                 cost_func: dict,
                 config: NetConfig = NetConfig,
                 net_dir: str = "./model/",
                 log_dir: str = "./logs/"
                 ) -> None:
        self.net = net
        self.name = self.net.__name__
        self.optimizer = None
        self.cost_func = cost_func
        self.config = config
        self.net_dir = Path(net_dir)
        self.net_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir = log_dir
        self.logger = self._set_logger()

    def _set_logger(self) -> logging.Logger:
        """ Set Logger

        Returns:
            The logger for neural network.
        """
        Path(f"{self.log_dir}/{self.name}").mkdir(parents=True, exist_ok=True)
        logger = logging.Logger(self.name)
        log_path = Path(f"{self.log_dir}/{self.name}/logs.log")
        i = 1
        while log_path.exists():
            log_path = log_path.parent.joinpath(f"logs_{i}.log")
            i += 1
        logger.addHandler(logging.FileHandler(str(log_path), mode="w"))
        logger.setLevel(level=logging.INFO)
        return logger

    def calc_loss(self,
                  target: torch.Tensor,
                  input: torch.Tensor,
                  keys: list = None
                  ) -> Tuple[dict, Tensor]:
        """Calculate loss for training.

        Args:
            target: the target, which is label value.
            input: the result from neural network.
            keys: keys of cost function.
        """
        if keys is None:
            keys = self.cost_func.keys()

        loss_item, loss = dict(), torch.Tensor(0)
        for key, func in self.cost_func.items():
            if key in keys:
                tmp = func[0](input=input, target=target)
                loss += tmp * func[1]
                loss_item[key] = tmp
        return loss_item, loss

    def load_net(self,
                 reload: bool = False,
                 idx: Optional[int] = None
                 ) -> int:
        """ Load the neural network

        Args:
            reload: default ``False``. Whether reload the neural network parameters, or not.
            idx:  default ``None``. The ID of the pretrained neural network

        Returns:

        """

        def _load(model_dir: Union[str, Path]) -> tuple:
            files = Path(model_dir).iterdir()
            files = sorted(files, key=lambda x: int(re.findall("_(\d{3}).pkl", x.name)[0]), reverse=True)
            i = int(re.findall("_(\d{3}).pkl", files[0].name)[0])
            return torch.load(files[0]), i

        if reload:
            if isinstance(idx, int):
                path = Path(f"{self.net_dir}/model_{idx:03d}.pkl")
                if path.exists():
                    # point = torch.load(path)
                    point = torch.load(path)
                else:
                    point, idx = _load(self.net_dir)
            else:
                point, idx = _load(self.net_dir)
            self.logger.info("-" * 15 + f">Reload No.{idx:03d} epoch network...")
            self.net.load_state_dict(point["model_states"])
        else:
            self.logger.info("-" * 15 + ">Initiating new network...")
            idx = 0
            point = dict()
        # todo: change into DistributedDataParallel
        self.net = nn.DataParallel(self.net, device_ids=self.config.DEVICES_IDS)
        _parameters = [p for p in self.net.parameters() if p.requires_grad]
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=self.config.LR, weight_decay=1e-5)
        if reload:
            self.optimizer.load_state_dict(point["optimizer_states"])
        self.logger.info(f">>>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Net has been loaded!\n")
        return idx

    def save_net(self,
                 epoch: int,
                 **kwargs
                 ) -> None:
        """Saving states of the neural network

        Args:
            epoch: epoch number of training.

        """
        path = self.net_dir.joinpath(f"model_{epoch:03d}.pkl")
        # Saving states of the network.
        torch.save(dict(epoch=epoch, **kwargs), path)
        self.logger.info(f">>>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | save path: {path}\n")