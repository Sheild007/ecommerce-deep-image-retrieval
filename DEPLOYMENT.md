# Deployment Guide

**Free production stack:**
```
Browser → Vercel (React) → Hugging Face Spaces (FastAPI + ONNX) → Neon PostgreSQL (pgvector)
```

---

## Prerequisites

- ✅ Neon account with data already migrated (pgvector + products table with embeddings)
- ✅ GitHub repo with this project
- ✅ Hugging Face account (free) — for the backend
- ✅ Vercel account (free) — for the frontend

> **Git LFS is required** — the ONNX model (98 MB) and embeddings (.npy files, ~98 MB) must be tracked with LFS.
> Install: https://git-lfs.github.com/

---

## Step 1 — Enable Git LFS (one-time setup)

```bash
# Install Git LFS (if not installed)
# Ubuntu/Debian:
sudo apt-get install git-lfs
# macOS: brew install git-lfs

# Enable LFS in this repo
git lfs install

# The .gitattributes already tracks *.onnx, *.npy, *.pt, *.db
# Just commit and push — LFS handles the rest
git add .
git commit -m "cleanup: remove junk files, add LFS tracking"
git push
```

---

## Step 2 — Test Locally

### 2a — Backend (requires DATABASE_URL from Neon)

```bash
cd backend

# Install dependencies
pip install -r requirements_onnx.txt

# Set your Neon connection string
export DATABASE_URL="postgresql://USER:PASSWORD@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require"

# Run API
uvicorn api_onnx:app --host 0.0.0.0 --port 7860 --reload

# Test health (in another terminal)
curl http://localhost:7860/api/health
```

Expected response:
```json
{
  "success": true,
  "status": "healthy",
  "model": "ONNX (triplet-hard)",
  "database": "Neon PostgreSQL",
  "total_products": 44446,
  "ml_ready": true
}
```

### 2b — Frontend

```bash
cd frontend
npm install

# Create local env pointing to local backend
echo 'VITE_API_URL=http://localhost:7860/api' > .env.local

npm run dev
# Open http://localhost:5173
```

Test:
1. Browse products → category filters work
2. Upload any fashion image → visual search returns similar items

---

## Step 3 — Deploy Backend on Hugging Face Spaces

### 3a — Create the Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Space name**: e.g. `ecommerce-visual-search`
   - **SDK**: **Docker**
   - **Visibility**: Public (required for free tier)
3. Click **Create Space**

### 3b — Push backend files

The Space needs **only these files** from `backend/`:
```
Dockerfile
api_onnx.py
requirements_onnx.txt
model/weights/triplet_hard_model_best.onnx   ← via Git LFS
```

**Option A — Push from this repo (recommended)**

HF Spaces can mirror a GitHub repo subfolder. Or you can create a separate HF repo:

```bash
# Clone the empty HF Space repo
git clone https://huggingface.co/spaces/YOUR-USERNAME/ecommerce-visual-search
cd ecommerce-visual-search

# Initialize LFS in the HF repo
git lfs install

# Copy needed files
cp /path/to/project/backend/Dockerfile .
cp /path/to/project/backend/api_onnx.py .
cp /path/to/project/backend/requirements_onnx.txt .
mkdir -p model/weights
cp /path/to/project/backend/model/weights/triplet_hard_model_best.onnx model/weights/

# Track ONNX with LFS
echo '*.onnx filter=lfs diff=lfs merge=lfs -text' > .gitattributes
git lfs track "model/weights/triplet_hard_model_best.onnx"

git add .
git commit -m "Deploy: FastAPI ONNX backend"
git push
```

### 3c — Add Neon secret

1. In your Space → **Settings** → **Variables and secrets** → **New secret**
2. Name: `DATABASE_URL`
3. Value: your Neon pooler connection string (e.g. `postgresql://...?sslmode=require`)

The Space will auto-rebuild. After build (~3-5 min), test:
```bash
curl https://YOUR-USERNAME-ecommerce-visual-search.hf.space/api/health
```

Your Space URL pattern: `https://USERNAME-SPACENAME.hf.space`

---

## Step 4 — Deploy Frontend on Vercel

1. Go to https://vercel.com → **Add New Project**
2. Import your GitHub repo
3. Set **Root Directory** → `frontend`
4. Under **Environment Variables**, add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://YOUR-USERNAME-ecommerce-visual-search.hf.space/api`
   - ⚠️ No trailing slash after `/api`
5. Click **Deploy**

Your frontend will be live at `https://your-project.vercel.app`

---

## Architecture

```
User Browser
    │
    ▼
Vercel (React + Vite)          — Free hobby plan
    │ REST API calls
    ▼
Hugging Face Spaces            — Free Docker Space (CPU)
    FastAPI + ONNX model
    ResNet50 triplet-hard
    512-dimensional embeddings
    │ pgvector similarity search
    ▼
Neon PostgreSQL                — Free tier (0.5 GB)
    products table
    embedding vector(512)
    HNSW index
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ONNX model not found` in HF Space | Check `model/weights/triplet_hard_model_best.onnx` is tracked by LFS and pushed |
| `DATABASE_URL is not set` | Add it in HF Space Settings → Secrets |
| Empty visual search results | Check Neon has embeddings: `SELECT COUNT(*) FROM products WHERE embedding IS NOT NULL` |
| CORS error in browser | `VITE_API_URL` must match exactly and end with `/api` (no trailing slash) |
| HF Space sleeping (cold start) | Free Spaces sleep after 48h of inactivity; first request may take 30-60s to wake |
| `psycopg2` SSL error | Ensure `?sslmode=require` is at the end of your `DATABASE_URL` |

---

## Security Checklist

- [ ] Never commit `.env` or `backend/.env` (gitignored ✅)
- [ ] Use HF Space **Secrets** (not Variables) for `DATABASE_URL`
- [ ] Use Vercel **Environment Variables** for `VITE_API_URL`
- [ ] Rotate Neon credentials if accidentally exposed in logs/chat
