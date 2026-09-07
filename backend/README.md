# Backend — Ecommerce Visual Search API

FastAPI backend with ONNX inference and Neon PostgreSQL (pgvector).

## Stack

| Component | Details |
|-----------|---------|
| **API** | FastAPI 0.115 |
| **Model** | ResNet50, triplet-hard loss, 512-d embeddings (ONNX) |
| **DB** | Neon PostgreSQL + pgvector (cosine similarity) |
| **Deploy** | Hugging Face Spaces (Docker, port 7860) |

## Local Development

```bash
pip install -r requirements_onnx.txt
export DATABASE_URL="postgresql://..."
uvicorn api_onnx:app --host 0.0.0.0 --port 7860 --reload
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check + DB/model status |
| GET | `/api/products` | List products (filter by category, search, paginate) |
| GET | `/api/products/{id}` | Get single product |
| GET | `/api/categories` | List all categories and genders |
| POST | `/api/visual-search` | Upload image → get similar products |

## Files

```
backend/
├── api_onnx.py              # Main API (production)
├── Dockerfile               # HF Spaces Docker config
├── requirements_onnx.txt    # Python dependencies
├── db_setup.py              # Rebuild SQLite from CSVs (dev utility)
├── migrate_to_neon.py       # One-time migration: SQLite + embeddings → Neon
├── products.db              # SQLite source (used by migrate_to_neon.py)
└── model/
    ├── model.py             # EmbeddingNet architecture
    ├── weights/
    │   └── triplet_hard_model_best.onnx   # Production model (98 MB, Git LFS)
    └── embeddings/
        ├── embeddings_all.npy   # Precomputed vectors (91 MB, Git LFS)
        └── paths_all.npy        # Image path index (7 MB, Git LFS)
```

## Model Architecture

- **Base**: ResNet50 (ImageNet pretrained)
- **Loss**: Triplet loss with hard negative mining
- **Embedding dim**: 512
- **Input**: 224×224 RGB, ImageNet normalization
- **Search**: pgvector cosine similarity (HNSW index)
