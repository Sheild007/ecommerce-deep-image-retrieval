from typing import List, Tuple, Any, Optional
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import numpy as np
import os
import cv2


def load_dataset(data_dir: str) -> Tuple[List[np.ndarray], list[str]]:
    images: List[np.ndarray] = []
    labels: List[str] = []

    for label in os.listdir(data_dir):
        cls_path = os.path.join(data_dir, label)
        for file in os.listdir(cls_path):
            img = cv2.imread(os.path.join(cls_path, file))
            images.append(img)
            labels.append(label)
    return images, label



