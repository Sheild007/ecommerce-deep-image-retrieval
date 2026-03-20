import torchvision.transforms as transforms

def get_transforms():
    # return data augmentation and normalization transforms
    return transforms.Compose([
        transforms.Resize((224, 224)), #resnet50 accept these dims
        transforms.RandomHorizontalFlip(p=0.5), # for augmentation
        transforms.RandomRotation(10),          #  for augmentation
        transforms.ToTensor(),                  # conversion to tensor
        transforms.Normalize(                   # offical normalize mean and std
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def get_val_transforms():
    #return normalization transforms
    return transforms.Compose([          
        transforms.Resize((224, 224)),  #resnet50 accept these dims
        transforms.ToTensor(),          # conversion to tensor
        transforms.Normalize(           # offical normalize mean and std
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

