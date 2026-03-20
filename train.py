import os
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import torchvision.transforms as transforms

from model import EmbeddingNet
from dataset import split_data, ContrastiveDataset
from loss import ContrastiveLoss

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

def train_contrastive(data_dir:str ='caltech-101',output_dir:str ='checkpoints',
    epochs:int =30,batch_size:int=32,lr:float=0.001,margin:float=1.0,device:str= None) -> None:
   
    if device is None:
       if torch.cuda.is_available():
             device = 'cuda'  
       else:
            device = 'cpu' 
    
    #spliting data with default 70 15 15 ratio
    train_data, val_data, _ = split_data(data_dir)
    
    train_transforms=get_transforms()
    val_transforms=get_val_transforms()
    
    #making dataset and data loaders
    train_dataset=ContrastiveDataset(train_data[0],train_data[1],transforms=train_transforms,prob=0.5)
    val_dataset=ContrastiveDataset(val_data[0],val_data[1],transforms=val_transforms,prob=0.5)
    
    train_loader=DataLoader(train_dataset,batch_size=batch_size,shuffle=True,num_workers=4)
    val_loader=DataLoader(val_dataset,batch_size=batch_size,shuffle=False,num_workers=4)
    
    #loading the model
    model=EmbeddingNet().to(device)
    optimizer=optim.Adam(model.parameters(),lr=lr)
    criterion=ContrastiveLoss(margin=margin)
    
    os.makedirs(output_dir, exist_ok=True)
    checkpoint = os.path.join(output_dir, 'contrastive_model_best.pt')
    best_val_loss = float('inf')
    
    print(f"Contrastive Learning:Training for {epochs} epochs...")
    for epoch in range(epochs):
        model.train() # swtich model to train phase
        train_loss = 0.0
        for img1,img2,label in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
            img1=img1.to(device)
            img2=img2.to(device)
            label=label.to(device)
            
            optimizer.zero_grad() # zeroing gradients
            emb1=model(img1)      # embeddings of img1
            emb2=model(img2)      # embeddings of img2

            loss=criterion(emb1, emb2, label)  # computing contrastive loss
            
            loss.backward() # back prop
            optimizer.step() # updating weights
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        
        # Validation
        model.eval() # switch back to eval mode
        val_loss = 0.0
        with torch.no_grad():
            for img1, img2, label in val_loader:
                img1 = img1.to(device)
                img2 = img2.to(device)
                label = label.to(device)
                
                emb1 = model(img1)
                emb2 = model(img2)
                loss = criterion(emb1, emb2, label)
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), checkpoint)
            print(f"Best model saved with val_loss={val_loss:.6f}")

        print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}")
    
    return checkpoint
