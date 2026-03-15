from typing import List, Tuple, Any, Optional
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import numpy as np
import os
import cv2
import random

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


def split_data(data_dir: str,train_ratio: float = 0.70, val_ratio: float = 0.15,test_ratio: float = 0.15,
    ) -> Tuple[Tuple[List[np.ndarray], List[str]],Tuple[List[mp.ndarray], List[str]],Tuple[List[np.ndarray], List[str]]]:
    
    images,labels=load_dataset(data_dir)
    n=len(images)
    indxes=List[range(n)]
    random.shuffle(indxes)
    train_end=int(train_ratio*n)
    val_end=train_end+int(val_ratio*n)
    
    train_indxes=indxes[:train_end]
    val_indxes=indxes[train_end:val_end]
    test_indxes=indxes[val_end:]

    train_images=[images[i]for i in train_indxes]
    train_labels=[labels[i]for i in train_indxes]

    val_images=[images[i]for i in val_indxes]
    val_labels=[labels[i]for i in val_indxes]

    test_images=[images[i]for i in test_indxes]
    test_labels=[labels[i]for i in test_indxes]

    return(
        (train_images,train_labels),
        (val_images,val_labels),
        (test_images,train_labels),

    )

    



