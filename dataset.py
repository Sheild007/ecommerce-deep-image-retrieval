from typing import List, Tuple, Any, Optional
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import os
import random

def load_dataset(data_dir: str) -> Tuple[List[str], List[int]]:
    
    image_paths: List[str] = []
    labels: List[int] = []
    
    
    valid_folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    valid_folders.sort() 
    class_to_idx = {cls_name: idx for idx, cls_name in enumerate(valid_folders)}

    for label_name in valid_folders:
        cls_path = os.path.join(data_dir, label_name)
        for file in os.listdir(cls_path):
            full_path = os.path.join(cls_path, file)
            image_paths.append(full_path)
            
            
            labels.append(class_to_idx[label_name])
            
    
    return image_paths, labels


def split_data(
    data_dir: str,
    train_ratio: float = 0.70, 
    val_ratio: float = 0.15,
    test_ratio: float = 0.15
) -> Tuple[Tuple[List[str], List[int]], Tuple[List[str], List[int]], Tuple[List[str], List[int]]]:
   
    image_paths, labels = load_dataset(data_dir)
    n = len(image_paths)
    
    
    indxes = list(range(n))
    random.shuffle(indxes)
    
    train_end = int(train_ratio * n)
    val_end = train_end + int(val_ratio * n)
    
    train_indxes = indxes[:train_end]
    val_indxes = indxes[train_end:val_end]
    test_indxes = indxes[val_end:]

    train_paths = [image_paths[i] for i in train_indxes]
    train_labels = [labels[i] for i in train_indxes]

    val_paths = [image_paths[i] for i in val_indxes]
    val_labels = [labels[i] for i in val_indxes]

    test_paths = [image_paths[i] for i in test_indxes]
    test_labels = [labels[i] for i in test_indxes]

    return (
        (train_paths, train_labels),
        (val_paths, val_labels),
        (test_paths, test_labels), 
    )
