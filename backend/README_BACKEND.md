# Backend - Visual Search API

FastAPI server for visual search using deep metric learning on e-commerce products.

## Quick Start

```bash
cd backend
pip install -r requirements_onnx.txt
export DATABASE_URL="postgresql://user:password@ep-cool-db.neon.tech/neondb?sslmode=require"
uvicorn api_onnx:app --host 0.0.0.0 --port 7860 --reload
```

API: http://localhost:7860
Docs: http://localhost:7860/docs

## Project Structure

```
backend/
├── api_onnx.py            # Local FastAPI server
├── hf_app.py              # Hugging Face deployment script (Gradio wrapper)
├── requirements_onnx.txt  # Dependencies
├── model/
│   ├── model.py           # ResNet50 architecture
│   ├── train.py           # Training logic
│   ├── loss.py            # Triplet/Contrastive loss
│   ├── dataset.py         # Data loading
│   ├── save_embeddings.py # Generate embeddings
│   ├── weights/           # Pre-trained models (e.g., triplet_hard_model_best.onnx)
│   └── embeddings/        # Vector embeddings (.npy files)
```

## Machine Learning Architecture

- **Base Model**: ResNet50 (pretrained ImageNet weights)
- **Loss Function**: Triplet Loss (Hard mining)
- **Embedding Dimension**: 512
- **Distance Metric**: Cosine similarity

### Input Format
- Resolution: 224x224 pixels
- Format: RGB (3 channels)
- Normalization: ImageNet mean/std

## Database Schema (Neon PostgreSQL)

We use Neon Serverless PostgreSQL with the `pgvector` extension for high-performance vector search.

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  gender TEXT,
  masterCategory TEXT,
  subCategory TEXT,
  articleType TEXT,
  baseColour TEXT,
  season TEXT,
  year INTEGER,
  usage TEXT,
  productDisplayName TEXT,
  image_link TEXT,
  price_pkr NUMERIC,
  embedding vector(512)
);

-- Index for fast cosine similarity search
CREATE INDEX ON products USING hnsw (embedding vector_cosine_ops);
```

## Model Training & Embeddings

### 1. Train a New Model
To train the ResNet50 model from scratch using PyTorch:
```bash
cd model
python main.py --epochs 30 --batch-size 64 --lr 0.001
```

### 2. Generate Embeddings
After training (or using a pretrained ONNX/PyTorch model), precompute the embeddings for all catalog images:
```bash
cd model
python save_embeddings.py --weights-dir weights --output-dir embeddings
```
*This generates `embeddings_all.npy`, `labels_all.npy`, and `paths_all.npy`.*

### 3. Evaluate Model
```bash
cd model
python evaluate.py --embeddings-dir embeddings --output-dir graphs
```

**Evaluation Metrics**
- **mAP (Mean Average Precision)**: 92-98% depending on loss function
- **Top-1 Accuracy**: 98%
- **Query Latency**: <50ms per retrieval

## API Endpoints

### Visual Search
```
POST /api/visual-search
Params: image (file upload)
Response: Array of similar products based on cosine similarity
```

### Products
```
GET /api/products?category=Apparel&limit=50&offset=0
GET /api/products/{id}
GET /api/categories
GET /api/health
```

## Deployment (Hugging Face Spaces)

The backend is deployed on Hugging Face Spaces (ZeroGPU Free Tier).
To deploy:
1. Clone the Hugging Face space repo.
2. Push `hf_app.py` as `app.py`.
3. Add `DATABASE_URL` to Hugging Face Secrets.
4. The system automatically wraps FastAPI into Gradio to satisfy HF SDK requirements and bypasses ZeroGPU constraints.

## Troubleshooting

- **`Invalid input type (tensor(double))`**: Numpy arrays convert to float64 automatically during division (`/255.0`). You must cast to `np.float32` before passing to the ONNX session.
- **`ONNX model not found`**: Ensure `triplet_hard_model_best.onnx` is tracked by Git LFS before pushing.
- **`ZeroGPU timeout/crash`**: Ensure `hf_app.py` includes the dummy `@spaces.GPU` wrapper to bypass Hugging Face environment checks.
