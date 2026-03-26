import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors

def recall_at_k(embeddings:np.ndarray,labels:np.ndarray,k:int=1)->float:
    
    # fining k neibioours of all embeddings
    neighbours=NearestNeighbors(n_neighbors=k + 1,algorithm='brute',metric='euclidean')
    neighbours.fit(embeddings)
    distances, indices=neighbours.kneighbors(embeddings)
    
    # Exclude query itself 
    indices=indices[:, 1:k + 1]
    retrieved_labels=labels[indices]
    query_labels=labels.reshape(-1, 1)

    # Check if correct class appears in top-k
    matches=(retrieved_labels==query_labels).any(axis=1)
    # taking avearage of all correct and wrong answers
    return np.mean(matches)
