# E-Commerce Deep Image Retrieval

**Frontend Live Demo**: [https://ecommerce-deep-image-retrieval.vercel.app](https://ecommerce-deep-image-retrieval.vercel.app)

Visual search for e-commerce using deep metric learning. Upload product images to find similar items in 44,000+ products.

## Overview

This project implements content-based image retrieval using deep metric learning for e-commerce product discovery. Instead of text-based search, users can upload a product image and find visually similar items from a catalog of 44,000+ products.

## Core Deep Learning Approach

**Metric Learning Framework**: Train a ResNet50 neural network to map product images into a learned embedding space where semantically similar products are positioned close together.

**Three Loss Functions Implemented**:

- **Triplet Loss (Hard Mining)**: Selects hardest negative examples per batch - achieves 98% mAP (best performance)
- **Triplet Loss (Random)**: Randomly samples negatives - balanced training/performance
- **Contrastive Loss**: Binary similarity learning - alternative approach

**Model Architecture**:

- Base: ResNet50 pretrained on ImageNet
- Output: 256-dimensional embedding vectors
- Optimization: SGD with momentum, trained for 30 epochs
- Batch size: 64 | Learning rate: 0.001

## Image Retrieval Pipeline

- **Training Phase**: Train model on product images using metric learning losses
- **Embedding Generation**: Pre-compute embeddings for all 44,000 catalog images
- **Indexing**: Store embeddings with scikit-learn NearestNeighbors (cosine similarity)
- **Query**: User uploads image → compute embedding → find K-nearest neighbors in embedding space
- **Results**: Return top-10 most similar products with similarity scores

## Performance Results

| Metric | Value |
| -------- | ------- |
| mAP@1 | 98% |
| mAP@10 | 92% |
| Query Time | <5ms |
| Inference Time | 200-500ms per batch |
| Embedding Dimension | 256D |
| Dataset Size | 44,000 products |

## Key Features

- **Fast Inference**: Pre-computed embeddings cached in memory enable <5ms retrieval
- **Production Ready**: FastAPI backend with CORS support
- **Scalable**: Pre-trained weights provided, easy to retrain on new datasets
- **End-to-End**: Training, validation, evaluation, and deployment scripts included

## Quick Start

**Backend Setup**

```bash
cd backend
pip install -r requirements_api.txt
python db_setup.py
cd model && python save_embeddings.py && cd ..
uvicorn api:app --host 0.0.0.0 --port 5000 --reload
```

**Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

Access at [http://localhost:5173](http://localhost:5173/)

## Features

- **Visual Search**: Upload images to find similar products
- **Fast Retrieval**: <5ms queries with pre-computed embeddings
- **44K Products**: Browse with category/gender filters
- **Lazy Loading**: Optimized image rendering
- **Responsive**: Desktop and mobile support

## Project Structure

```text
├── frontend/             # React + Vite UI
│   └── src/
│       ├── components/   # UI components
│       └── styles/       # CSS
├── backend/              # FastAPI server
│   └── model/
│       ├── weights/      # Pre-trained models
│       └── embeddings/   # Vector embeddings
├── styles.csv            # Product data
└── images.csv            # Image data
```

## API Endpoints

**Visual Search (Primary Feature)**

- `POST /api/visual-search`
- Input: Image file + limit (default: 10)
- Output: Top-K similar products with cosine similarity scores
- Process: Compute query embedding → Search nearest neighbors → Return results

**Product Management**

- `GET /api/products` # Browse all products with filters
- `GET /api/products/{id}` # Get product details
- `GET /api/categories` # Available categories
- `GET /api/health` # API health check

## Technologies

**Deep Learning & ML**

- PyTorch: Model training and inference
- ResNet50: CNN backbone for feature extraction
- scikit-learn: Efficient nearest neighbor search (with cosine similarity)
- NumPy: Vectorized embedding operations

**Backend Infrastructure**

- FastAPI: Modern async Python framework with auto docs
- Uvicorn: ASGI server
- SQLite: Product catalog database
- CORS Middleware: Enable cross-origin requests

**Frontend**

- React 19: UI components and state management
- Vite: Fast build tool with HMR
- JavaScript ES6+: Modern language features

## Training & Results

**How to Train**

1. **Prepare Dataset**: Organize images by class
2. **Configure Loss**: Choose Triplet (Hard/Random) or Contrastive
3. **Train Model**:

   ```bash
   cd backend/model
   python main.py --epochs 30 --batch-size 64 --lr 0.001
   ```

4. **Generate Embeddings**: Pre-compute for all images

   ```bash
   python save_embeddings.py
   ```

5. **Evaluate**: Compute metrics

   ```bash
   python evaluate.py
   ```

**Evaluation Metrics**

- mAP (Mean Average Precision): 92-98% depending on loss function
- Top-1 Accuracy: 98%
- Query Latency: <5ms per retrieval
- Model Size: ~100MB (ResNet50 weights)

![Loss Plot — Triplet Hard](loss_plot.png)

**Loss Functions Comparison**

| Loss | mAP@1 | mAP@10 | Training Speed | Notes |
| --- | --- | --- | --- | --- |
| Triplet Hard | 98% | 92% | Slower | Best quality |
| Triplet Random | 96% | 89% | Faster | Balanced |
| Contrastive | 94% | 87% | Fast | Binary approach |

## Configuration

**Backend Environment**

```env
API_HOST=0.0.0.0
API_PORT=5000
```

**Frontend API**
Edit `frontend/src/App.jsx`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

**Docker Deployment**

```yaml
version: '3.8'
services:
  api:
    build: ./backend
    ports:
      - "5000:5000"
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
```
