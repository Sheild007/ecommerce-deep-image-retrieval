# E-Commerce Deep Image Retrieval

Visual search for e-commerce using deep metric learning. Upload product images to find similar items in 44,000+ products.

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements_api.txt
python db_setup.py
cd model && python save_embeddings.py && cd ..
uvicorn api:app --host 0.0.0.0 --port 5000 --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Access at http://localhost:5173

## Features

- **Visual Search**: Upload images to find similar products
- **Fast Retrieval**: <5ms queries with pre-computed embeddings
- **44K Products**: Browse with category/gender filters
- **Lazy Loading**: Optimized image rendering
- **Responsive**: Desktop and mobile support

## Project Structure

```
├── frontend/          # React + Vite UI
│   └── src/
│       ├── components/   # UI components
│       └── styles/       # CSS
│
├── backend/           # FastAPI server
│   └── model/
│       ├── weights/      # Pre-trained models
│       └── embeddings/   # Vector embeddings
│
├── styles.csv         # Product data
└── images.csv         # Image data
```

## API Endpoints

```bash
POST /api/visual-search       # Upload image to search
GET /api/products              # Browse products
GET /api/products/{id}         # Product details
GET /api/categories            # Available filters
GET /api/health                # API status
```

## Technologies

- **Frontend**: React 19, Vite, JavaScript
- **Backend**: FastAPI, PyTorch, SQLite
- **ML**: ResNet50, Triplet/Contrastive Loss
- **Query**: scikit-learn NearestNeighbors

## Configuration

### Backend Environment
```bash
API_HOST=0.0.0.0
API_PORT=5000
```

### Frontend API
Edit `frontend/src/App.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## Docker Deployment

```bash
cd backend
docker build -t ecommerce-api .
docker run -p 5000:5000 ecommerce-api
```

## Details

- [Frontend Docs](frontend/README_FRONTEND.md)
- [Backend Docs](backend/README_BACKEND.md)
