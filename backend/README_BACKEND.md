# Backend - Visual Search API

FastAPI server for visual search using deep metric learning on 44,000+ products.

## Quick Start

```bash
cd backend
pip install -r requirements_api.txt
python db_setup.py
cd model && python save_embeddings.py && cd ..
uvicorn api:app --host 0.0.0.0 --port 5000 --reload
```

API: http://localhost:5000
Docs: http://localhost:5000/docs

## Project Structure

```
backend/
├── api.py                 # FastAPI server
├── db_setup.py            # Initialize database
├── model/
│   ├── model.py          # ResNet50 architecture
│   ├── train.py          # Training logic
│   ├── loss.py           # Triplet/Contrastive loss
│   ├── dataset.py        # Data loading
│   ├── save_embeddings.py # Generate embeddings
│   ├── weights/          # Pre-trained models
│   └── embeddings/       # Vector embeddings
└── products.db           # SQLite database
```

## API Endpoints

### Visual Search
```
POST /api/visual-search
Params: image (file), limit (10), offset (0)
Response: Array of similar products
```

### Products
```
GET /api/products?category=Apparel&limit=20
GET /api/products/{id}
GET /api/categories
GET /api/health
```

## Setup Steps

### 1. Dependencies
```bash
pip install -r requirements_api.txt
```

### 2. Database
```bash
python db_setup.py
# Creates products.db from styles.csv & images.csv (44,000 products)
```

### 3. Embeddings
```bash
cd model
python save_embeddings.py
# Generates embeddings_all.npy, labels_all.npy, paths_all.npy
cd ..
```

### 4. Start Server
```bash
uvicorn api:app --host 0.0.0.0 --port 5000 --reload
```

## Database Schema

```
products table:
- id: Product ID
- title: Product name
- category: Category
- gender: Gender (Men/Women/Unisex)
- price: Price in PKR
- image_url: Image URL
- currency: Currency
```

## ML Model

**Architecture**: ResNet50 (ImageNet pretrained)
- Input: 224x224 RGB
- Embedding: 256-dimensional
- Distance: Cosine similarity

**Training**:
- Loss: Triplet (Hard/Random) or Contrastive
- Optimizer: SGD with momentum
- Epochs: 30
- Batch: 64

**Performance**:
- mAP@1: 98%
- Query time: <5ms
- Inference: 200-500ms/batch

## Running

### Development
```bash
uvicorn api:app --reload
```

### Production
```bash
uvicorn api:app --workers 4
```

### Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

## Configuration

### Environment
```bash
API_HOST=0.0.0.0
API_PORT=5000
DATABASE_URL=            # Optional remote DB
```

### Paths
Edit `api.py`:
```python
WEIGHTS_PATH = BASE_DIR / 'model' / 'weights' / 'triplet_hard_model_best.pt'
EMBEDDINGS_DIR = BASE_DIR / 'model' / 'embeddings'
```

## Training

### Train New Model
```bash
cd model
python main.py --epochs 30 --batch-size 64 --lr 0.001
```

### Evaluate
```bash
cd model
python evaluate.py --embeddings-dir embeddings
```

## Docker

### Build
```bash
docker build -t ecommerce-api .
```

### Run
```bash
docker run -p 5000:5000 -e API_HOST=0.0.0.0 ecommerce-api
```

## Technologies

- FastAPI: Web framework
- PyTorch: Deep learning
- scikit-learn: NearestNeighbors search
- SQLite: Database
- NumPy: Numerical computing
- Pillow: Image processing

## Error Handling

**Embeddings not loaded**: Run `python model/save_embeddings.py`

**Database locked**: Kill process on port 5000

**Out of memory**: Reduce batch size in save_embeddings.py

## Testing

```bash
# Health check
curl http://localhost:5000/api/health

# Visual search
curl -X POST -F "image=@test.jpg" \
  http://localhost:5000/api/visual-search?limit=5

# Products
curl http://localhost:5000/api/products?limit=5
```

## Security

- Validate file uploads
- Set size limits (50MB)
- Sanitize inputs
- Use HTTPS in production
- Don't expose sensitive paths

## Dependencies

See `requirements_api.txt` for complete list

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [PyTorch Docs](https://pytorch.org)
- [scikit-learn](https://scikit-learn.org)

## Technologies

- **FastAPI** - Modern Python web framework with auto documentation
- **PyTorch** - Deep learning framework for model inference
- **scikit-learn** - Machine learning utilities (NearestNeighbors)
- **SQLite** - Lightweight database for product catalog
- **NumPy** - Numerical computing
- **Pillow** - Image processing
- **CORS Middleware** - Cross-origin resource sharing for frontend

## Project Structure

```
backend/
├── api.py                          # Main FastAPI application
├── db_setup.py                     # Database initialization
├── requirements_api.txt            # API dependencies
├── requirements_onnx.txt           # ONNX dependencies
├── Dockerfile                      # Docker configuration
├── products.db                     # SQLite database (generated)
│
├── model/                          # Deep learning components
│   ├── main.py                    # Training orchestrator
│   ├── model.py                   # Neural network architecture
│   ├── train.py                   # Training logic
│   ├── inference.py               # Inference utilities
│   ├── dataset.py                 # Data loading and preprocessing
│   ├── loss.py                    # Loss functions (triplet, contrastive)
│   ├── evaluate.py                # Evaluation metrics and analysis
│   ├── retrieval.py               # Retrieval pipeline
│   ├── save_embeddings.py         # Embedding generation script
│   ├── requirements.txt           # Model dependencies
│   ├── README.md                  # Model documentation
│   │
│   ├── weights/                   # Pre-trained model weights
│   │   ├── triplet_hard_model_best.pt
│   │   ├── triplet_random_model_best.pt
│   │   └── contrastive_model_best.pt
│   │
│   ├── embeddings/                # Pre-computed embeddings
│   │   ├── embeddings_all.npy    # Vector embeddings
│   │   ├── labels_all.npy        # Product labels
│   │   └── paths_all.npy         # Image paths
│   │
│   └── graphs/                    # Evaluation visualizations
│       ├── contrastive/
│       ├── triplet_hard/
│       └── triplet_random/
│
└── README_BACKEND.md              # This file
```

## Quick Start

### Prerequisites
- Python 3.8+
- 4GB+ RAM (for embeddings)
- Disk space for models and embeddings (~2GB)

### Installation

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements_api.txt

# 4. Setup database from CSV files
python db_setup.py
# This creates: products.db with 44,000+ products

# 5. Generate embeddings for visual search
cd model
python save_embeddings.py
cd ..
# This creates: model/embeddings/(embeddings_all.npy, labels_all.npy, paths_all.npy)

# 6. Start API server
uvicorn api:app --host 0.0.0.0 --port 5000 --reload
```

Server will start at `http://localhost:5000`

Visit `http://localhost:5000/docs` for interactive API documentation.

## API Endpoints

### 1. Visual Search (Core Feature)
```
POST /api/visual-search
Content-Type: multipart/form-data

Parameters:
  - image: Image file (JPEG, PNG, WebP, GIF)
  - limit: Number of results (default: 10, max: 100)
  - offset: Pagination offset (default: 0)

Response (200 OK):
{
  "success": true,
  "results": [
    {
      "id": "product_id",
      "title": "Product Title",
      "price": 2999.00,
      "currency": "PKR",
      "category": "Apparel",
      "gender": "Men",
      "similarity": 0.95,
      "image_url": "https://...",
      "rank": 1
    },
    ...
  ],
  "query_time_ms": 245,
  "total_results": 10
}
```

### 2. Get All Products
```
GET /api/products

Query Parameters:
  - category: Filter by category (optional)
  - gender: Filter by gender (Men/Women/Unisex) (optional)
  - search: Search in product titles (optional)
  - limit: Results per page (default: 20, max: 100)
  - offset: Pagination offset (default: 0)

Response (200 OK):
{
  "success": true,
  "products": [
    {
      "id": "product_id",
      "title": "Product Title",
      "category": "Apparel",
      "gender": "Men",
      "price": 2999.00,
      "currency": "PKR",
      "image_url": "https://..."
    },
    ...
  ],
  "total": 44000,
  "limit": 20,
  "offset": 0
}
```

### 3. Get Product Details
```
GET /api/products/{product_id}

Response (200 OK):
{
  "success": true,
  "product": {
    "id": "product_id",
    "title": "Full Product Title",
    "category": "Apparel",
    "gender": "Men",
    "price": 2999.00,
    "currency": "PKR",
    "image_url": "https://...",
    "description": "Product description"
  }
}

Response (404 Not Found):
{
  "success": false,
  "error": "Product not found"
}
```

### 4. Get Categories and Filters
```
GET /api/categories

Response (200 OK):
{
  "success": true,
  "categories": [
    "Apparel",
    "Footwear",
    "Accessories",
    "Watches",
    ...
  ],
  "genders": ["Men", "Women", "Unisex"],
  "total_products": 44000
}
```

### 5. Health Check
```
GET /api/health

Response (200 OK):
{
  "status": "healthy",
  "model_loaded": true,
  "embeddings_loaded": true,
  "database_connected": true
}
```

## Database Schema

### Products Table
```sql
CREATE TABLE products (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT,
  gender TEXT,
  price REAL,
  currency TEXT,
  image_url TEXT,
  created_at TIMESTAMP
);

CREATE INDEX idx_category ON products(category);
CREATE INDEX idx_gender ON products(gender);
CREATE INDEX idx_title ON products(title);
```

## Deep Learning Model

### Architecture
```
ResNet50 (ImageNet Pretrained)
  ↓
Global Average Pooling
  ↓
FC Layer (256-dim embedding)
  ↓
Embedding Vector (256D)
```

### Input
- Resolution: 224×224 pixels
- Format: RGB (3 channels)
- Normalization: ImageNet mean/std

### Output
- Embedding Dimension: 256
- Distance Metric: Cosine similarity
- Range: [-1, 1]

### Training Details
- **Base Model**: ResNet50 (pretrained ImageNet weights)
- **Loss Functions**: 
  - Triplet Loss (Hard/Random mining)
  - Contrastive Loss
- **Optimizer**: SGD with momentum
- **Learning Rate**: 0.001
- **Batch Size**: 64
- **Epochs**: 30

### Performance Metrics
- **mAP@1**: 98%
- **mAP@10**: 92%
- **Query Speed**: <5ms per query
- **Inference Time**: ~200-500ms (batch)

## Embeddings

### Pre-computed Embeddings
Located in `model/embeddings/`:
- `embeddings_all.npy`: (44000, 256) float32 array
- `labels_all.npy`: (44000,) integer array
- `paths_all.npy`: (44000,) object array with image paths

### Memory Usage
- Embeddings: ~45MB
- Loaded in RAM for fast search

### Retrieval Method
- **Algorithm**: NearestNeighbors (sklearn)
- **Metric**: Cosine similarity
- **Search Time**: <5ms per query

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=           # Remote database connection (optional)
DB_PATH=./products.db   # Local database path

# Model
MODEL_WEIGHTS=./model/weights/triplet_hard_model_best.pt
EMBEDDINGS_DIR=./model/embeddings

# API
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=false

# CORS
ALLOWED_ORIGINS=*
```

### Configuration File
Edit [api.py](api.py):
```python
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'products.db'
EMBEDDINGS_DIR = BASE_DIR / 'model' / 'embeddings'
WEIGHTS_PATH = BASE_DIR / 'model' / 'weights' / 'triplet_hard_model_best.pt'
```

## Data Files

### CSV Files (Input)
```
styles.csv
├── product_id
├── title
├── category
├── gender
├── price
└── ...

images.csv
├── image_id
├── product_id
├── image_url
└── ...
```

### Database (Generated)
```
products.db
└── products table (44,000 rows)
```

### Embeddings (Generated)
```
model/embeddings/
├── embeddings_all.npy (44000, 256)
├── labels_all.npy     (44000,)
└── paths_all.npy      (44000,)
```

## Running the Server

### Development Mode
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 5000
```
- Auto-reload on code changes
- Debug mode enabled
- Detailed error messages

### Production Mode
```bash
uvicorn api:app --host 0.0.0.0 --port 5000 --workers 4
```
- Multiple worker processes
- No auto-reload
- Better performance

### With Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

## Docker Deployment

### Build Image
```bash
docker build -t ecommerce-api:latest .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -v /path/to/embeddings:/app/model/embeddings \
  ecommerce-api:latest
```

### Docker Compose (with Frontend)
```yaml
version: '3.8'
services:
  api:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=5000
    volumes:
      - ./backend/model/embeddings:/app/model/embeddings

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:5000/api
```

Run with: `docker-compose up`

## Model Training (Advanced)

### Training New Model
```bash
cd model
python main.py --epochs 30 --batch-size 64 --lr 0.001
```

### Generating New Embeddings
```bash
cd model
python save_embeddings.py --weights-dir weights --output-dir embeddings
```

### Evaluating Model
```bash
cd model
python evaluate.py --embeddings-dir embeddings --output-dir graphs
```

See [model/README.md](model/README.md) for detailed instructions.

## Testing

### Test Visual Search
```python
import requests
from pathlib import Path

# Upload test image
with open('test_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post(
        'http://localhost:5000/api/visual-search',
        files=files,
        params={'limit': 5}
    )
    
print(response.json())
```

### Test Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get products
curl http://localhost:5000/api/products?limit=5

# Get categories
curl http://localhost:5000/api/categories

# Get single product
curl http://localhost:5000/api/products/product_id
```

## Performance Optimization

### Caching
- Embeddings cached in memory on startup
- HTTP caching headers for consistent responses
- Database query optimization with indexes

### Async Operations
- FastAPI async endpoints
- Non-blocking I/O
- Multiple worker support

### Batch Processing
- Batch image loading
- Vectorized embedding operations
- Efficient memory usage

## Debugging

### Enable Debug Mode
```python
# In api.py
app = FastAPI(debug=True)
```

### View Logs
```bash
# Watch server logs
tail -f server.log

# Filter errors
grep ERROR server.log
```

### API Documentation
Visit `http://localhost:5000/docs` for interactive Swagger UI.

## Error Handling

### Common Errors

**400 Bad Request**
```json
{
  "detail": "No image file provided"
}
```
**Solution**: Ensure image file in request

**404 Not Found**
```json
{
  "detail": "Product not found"
}
```
**Solution**: Verify product ID exists

**413 Payload Too Large**
```json
{
  "detail": "File too large"
}
```
**Solution**: Upload image < 50MB

**500 Internal Server Error**
```json
{
  "detail": "Error loading embeddings"
}
```
**Solution**: Ensure embeddings are generated

## Additional Resources

### Documentation Files
- [API_SETUP.md](API_SETUP.md) - Database and API setup
- [VISUAL_SEARCH.md](VISUAL_SEARCH.md) - Visual search feature details
- [README_ONNX_DEPLOYMENT.md](README_ONNX_DEPLOYMENT.md) - ONNX deployment guide
- [model/README.md](model/README.md) - Model training documentation

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [PyTorch Documentation](https://pytorch.org/docs)
- [scikit-learn Documentation](https://scikit-learn.org)
- [SQLite Documentation](https://sqlite.org/docs.html)

## Scaling Considerations

### For 1M+ Products
1. Replace SQLite with PostgreSQL/Neon
2. Add pgvector for direct vector search
3. Implement distributed embeddings
4. Use Redis for caching
5. Deploy with load balancer

### For Real-time Updates
1. Implement embedding queue system
2. Add async processing
3. Use message brokers (RabbitMQ, Kafka)
4. Implement incremental index updates

## Security Best Practices

- Validate file uploads
- Sanitize user inputs
- Set file size limits (50MB)
- Use HTTPS in production
- Implement rate limiting
- Add authentication/authorization
- Secure database credentials
- Don't expose sensitive paths
- Don't enable debug in production
- Don't log sensitive data

## Dependencies

### Core Dependencies
```
fastapi         - Web framework
uvicorn         - ASGI server
torch           - Deep learning
numpy           - Numerical computing
scikit-learn    - ML utilities
pillow          - Image processing
```

### Full List
See [requirements_api.txt](requirements_api.txt)

## Maintenance

### Cleanup
```bash
# Remove cache
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf .venv

# Clean database (regenerate)
rm products.db
python db_setup.py
```

### Backup
```bash
# Backup database
cp products.db products.db.backup

# Backup embeddings
cp -r model/embeddings model/embeddings.backup
```

## Development Workflow

### 1. Create New Endpoint
Edit [api.py](api.py):
```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"message": "Hello"}
```

### 2. Test Endpoint
```bash
curl http://localhost:5000/api/new-endpoint
```

### 3. Update Documentation
Add docstring:
```python
"""
Short description.

Returns:
    dict: Response structure
"""
```

## Support & Troubleshooting

### Common Issues

**Issue: "Embeddings not loaded"**
```bash
# Solution: Generate embeddings
cd model
python save_embeddings.py
```

**Issue: "Database locked"**
```bash
# Solution: Ensure only one instance running
# Kill other processes using port 5000
lsof -i :5000
kill -9 <PID>
```

**Issue: "Out of memory"**
```bash
# Solution: Reduce batch size, close other apps
# Check available RAM
free -h
```

---

**Happy coding!**
