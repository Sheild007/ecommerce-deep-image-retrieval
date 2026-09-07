"""
FastAPI backend: ONNX inference + Neon PostgreSQL (pgvector).
Deploy on Hugging Face Spaces (Docker, port 7860).
"""
import io
import os
from pathlib import Path
from typing import Any

import numpy as np
import onnxruntime as ort
import psycopg2
import psycopg2.extras
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / 'model' / 'weights' / 'triplet_hard_model_best.onnx'
DATABASE_URL = os.environ.get('DATABASE_URL')

app = FastAPI(title='E-commerce Visual Search', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

ort_session = None


def get_db_connection():
    if not DATABASE_URL:
        raise HTTPException(
            status_code=503,
            detail='DATABASE_URL is not set. Add it in Hugging Face Space secrets.',
        )
    return psycopg2.connect(DATABASE_URL)


@app.on_event('startup')
def load_onnx_model():
    global ort_session
    try:
        print('Loading ONNX model...')
        candidates = [
            MODEL_PATH,
            Path('model/weights/triplet_hard_model_best.onnx'),
            Path('triplet_hard_model_best.onnx'),
        ]
        model_file = next((p for p in candidates if p.exists()), None)
        if not model_file:
            raise FileNotFoundError(f'ONNX model not found. Checked: {candidates}')

        ort_session = ort.InferenceSession(
            str(model_file),
            providers=['CPUExecutionProvider'],
        )
        print(f'ONNX model loaded from {model_file}')
    except Exception as e:
        print(f'Warning: Could not load ONNX model: {e}')


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_array = (img_array - mean) / std
    img_array = np.transpose(img_array, (2, 0, 1))
    return np.expand_dims(img_array, axis=0)


def normalize_product(row: dict) -> dict[str, Any]:
    """Map PostgreSQL lowercase keys to frontend camelCase."""
    key_map = {
        'mastercategory': 'masterCategory',
        'subcategory': 'subCategory',
        'articletype': 'articleType',
        'basecolour': 'baseColour',
        'productdisplayname': 'productDisplayName',
        'image_link': 'image_link',
        'price_pkr': 'price_pkr',
    }
    out: dict[str, Any] = {}
    for key, value in row.items():
        mapped = key_map.get(key.lower(), key)
        if mapped not in out:
            out[mapped] = value
    out.pop('embedding', None)
    return out


def row_to_product(row: dict) -> dict[str, Any]:
    product = normalize_product(dict(row))
    product.pop('distance', None)
    return product


@app.get('/api/health')
async def health_check():
    db_ok = False
    product_count = 0
    if DATABASE_URL:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM products')
            product_count = cur.fetchone()[0]
            cur.close()
            conn.close()
            db_ok = True
        except Exception as e:
            print(f'DB health check failed: {e}')

    return {
        'success': True,
        'status': 'healthy' if db_ok and ort_session else 'degraded',
        'model': 'ONNX (triplet-hard)',
        'database': 'Neon PostgreSQL' if db_ok else 'unavailable',
        'total_products': product_count,
        'ml_ready': ort_session is not None,
    }


@app.get('/api/products')
async def get_products(
    category: str = Query(default='All'),
    search: str = Query(default=''),
    limit: int = Query(default=100, ge=1, le=100000),
    offset: int = Query(default=0, ge=0),
):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''
            SELECT id, gender, masterCategory, subCategory, articleType,
                   baseColour, season, year, usage, productDisplayName,
                   image_link, price_pkr
            FROM products WHERE 1=1
        '''
        params: list[Any] = []

        if category and category != 'All':
            query += ' AND (masterCategory = %s OR gender = %s)'
            params.extend([category, category])

        if search:
            query += '''
                AND (productDisplayName ILIKE %s OR baseColour ILIKE %s
                     OR articleType ILIKE %s)
            '''
            term = f'%{search}%'
            params.extend([term, term, term])

        count_query = query.replace(
            'SELECT id, gender, masterCategory, subCategory, articleType,\n'
            '                   baseColour, season, year, usage, productDisplayName,\n'
            '                   image_link, price_pkr',
            'SELECT COUNT(*)',
        )
        cur.execute(count_query, params)
        total = cur.fetchone()['count']

        query += ' ORDER BY id LIMIT %s OFFSET %s'
        params.extend([limit, offset])
        cur.execute(query, params)
        products = [normalize_product(dict(row)) for row in cur.fetchall()]

        cur.close()
        conn.close()

        return {
            'success': True,
            'products': products,
            'total': total,
            'limit': limit,
            'offset': offset,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get('/api/products/{product_id}')
async def get_product(product_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            '''
            SELECT id, gender, masterCategory, subCategory, articleType,
                   baseColour, season, year, usage, productDisplayName,
                   image_link, price_pkr
            FROM products WHERE id = %s
            ''',
            (product_id,),
        )
        product = cur.fetchone()
        cur.close()
        conn.close()

        if not product:
            raise HTTPException(status_code=404, detail='Product not found')

        return {'success': True, 'product': normalize_product(dict(product))}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get('/api/categories')
async def get_categories():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            'SELECT DISTINCT masterCategory FROM products '
            'WHERE masterCategory IS NOT NULL ORDER BY masterCategory'
        )
        categories = [
            r.get('mastercategory') or r.get('masterCategory')
            for r in cur.fetchall()
        ]

        cur.execute(
            'SELECT DISTINCT gender FROM products '
            'WHERE gender IS NOT NULL ORDER BY gender'
        )
        genders = [r['gender'] for r in cur.fetchall()]

        cur.close()
        conn.close()

        return {
            'success': True,
            'categories': categories,
            'genders': genders,
            'all': ['All'] + categories + genders,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post('/api/visual-search')
async def visual_search(image: UploadFile = File(...)):
    if not ort_session:
        raise HTTPException(status_code=503, detail='ONNX model not loaded')

    try:
        if not image.filename:
            raise HTTPException(status_code=400, detail='No image file provided')

        image_bytes = await image.read()
        input_tensor = preprocess_image(image_bytes)

        ort_inputs = {ort_session.get_inputs()[0].name: input_tensor}
        query_embedding = ort_session.run(None, ort_inputs)[0][0]
        query_vector_str = '[' + ','.join(map(str, query_embedding.tolist())) + ']'

        K_FETCH = 48
        DISTANCE_THRESHOLD = 1.2

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            '''
            SELECT id, gender, masterCategory, subCategory, articleType,
                   baseColour, season, year, usage, productDisplayName,
                   image_link, price_pkr,
                   embedding <=> %s::vector AS distance
            FROM products
            WHERE embedding <=> %s::vector <= %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            ''',
            (
                query_vector_str,
                query_vector_str,
                DISTANCE_THRESHOLD,
                query_vector_str,
                K_FETCH,
            ),
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        products = []
        for rank, row in enumerate(rows, start=1):
            product = row_to_product(dict(row))
            product['similarity_rank'] = rank
            product['distance'] = float(row['distance'])
            products.append(product)

        return {
            'success': True,
            'products': products,
            'total_results': len(products),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == '__main__':
    import uvicorn

    port = int(os.environ.get('PORT', 7860))
    uvicorn.run(app, host='0.0.0.0', port=port)
