import os.path
from abc import ABC, abstractmethod
from datetime import datetime

import numpy as np

from vidis_algorithms_api.core import settings


class Task(ABC):
    
    @classmethod
    @property
    @abstractmethod
    def name(cls):
        raise NotImplementedError
   
    def _save_task_result(self, layer_data: np.ndarray, hypespecter_path: str):
        path_to_save = os.path.join(settings.DATA_PATH, hypespecter_path,
                                    settings.CUSTOM_LAYER_FOLDER, f'{self.name}_{datetime.now()}.npy')
        os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
        np.save(path_to_save, layer_data)
        return os.path.dirname(path_to_save)
        

    def run(self, lname, hsi_id, _, hyperspecter_path, **kwargs):
        # Laye
        data = np.load(os.path.join(settings.DATA_PATH, hyperspecter_path, "hsi.npy"), mmap_mode="r")
        result = self.task(hyperspecter=data, **kwargs)
        assert result.ndim == 2, "Result should have two dimensions (height x width)"
        return self._save_task_result(result, hyperspecter_path)
    
    @abstractmethod
    def task(self, hyperspecter: np.ndarray, **kwargs) -> np.ndarray:
        pass
