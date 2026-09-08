# Backend - Visual Search API

FastAPI server for visual search using deep metric learning.

## Quick Start

```bash
cd backend
pip install -r requirements_onnx.txt
export DATABASE_URL="postgresql://user:password@ep-cool-db.neon.tech/neondb?sslmode=require"
uvicorn api_onnx:app --host 0.0.0.0 --port 7860 --reload
```

API: http://localhost:7860

## Project Structure

```
backend/
├── api_onnx.py            # Local FastAPI server
├── hf_app.py              # Hugging Face deployment script (Gradio wrapper)
├── requirements_onnx.txt  # Dependencies
├── model/
│   ├── model.py           # ResNet50 architecture
│   ├── save_embeddings.py # Generate embeddings
│   ├── weights/           # Pre-trained models (e.g., triplet_hard_model_best.onnx)
│   └── embeddings/        # Vector embeddings
```

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

## Machine Learning Architecture

- **Base Model**: ResNet50 (pretrained ImageNet weights)
- **Loss Function**: Triplet Loss (Hard mining)
- **Embedding Dimension**: 512
- **Distance Metric**: Cosine similarity

### Input
- Resolution: 224x224 pixels
- Format: RGB (3 channels)
- Normalization: ImageNet mean/std

## Database Schema (Neon PostgreSQL)

We use Neon Serverless PostgreSQL with the `pgvector` extension for high-performance vector search.

### Products Table
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

## Deployment (Hugging Face Spaces)

The backend is deployed on Hugging Face Spaces (ZeroGPU Free Tier).
To deploy:
1. Clone the Hugging Face space repo.
2. Push `hf_app.py` as `app.py`.
3. Add `DATABASE_URL` to Hugging Face Secrets.
4. (The system automatically wraps FastAPI into Gradio to satisfy HF SDK requirements and bypasses ZeroGPU constraints).
