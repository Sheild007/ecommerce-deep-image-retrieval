import torch
import torch.nn as nn 
import torch.nn.functional as F 
import torchvision.models as models 


class EmbeddingNet(nn.Module):
    def __init__(self, embedding_dim: int = 512) -> None:
        super().__init__()
        # Resnet50 with pretrained weights as backbone feature_extractor
        backbone = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        input_dim = backbone.fc.in_features 
        # Strip final fc layer from backbone 
        backbone.fc = nn.Identity()
        self.feature_extractor = backbone
        
        # Added Dropout for better generalization in Metric Learning
        self.fc = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(input_dim, embedding_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # step1: extract features using Resnet50
        features = self.feature_extractor(x)
        # step2: project features to 512 embedding vector 
        embeddings = self.fc(features)
        # step3: L2 normalization (ensure strictly along the feature dimension)
        embeddings = F.normalize(embeddings, p=2, dim=1) 
        return embeddings
        

