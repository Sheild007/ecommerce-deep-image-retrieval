"""
Migrate product metadata + embeddings from local files to Neon PostgreSQL (pgvector).

Usage:
  export DATABASE_URL="postgresql://..."
  python migrate_to_neon.py
"""
import os
import sqlite3
import sys
from pathlib import Path

import numpy as np
import psycopg2
from psycopg2.extras import execute_values

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / 'model'
EMBEDDINGS_DIR = MODEL_DIR / 'embeddings'
DB_PATH = BASE_DIR / 'products.db'
EMBEDDING_DIM = 512
BATCH_SIZE = 200


def get_database_url() -> str:
    url = os.environ.get('DATABASE_URL')
    if not url:
        print('ERROR: Set DATABASE_URL before running migration.')
        print('  export DATABASE_URL="postgresql://user:pass@host/neondb?sslmode=require"')
        sys.exit(1)
    return url


def setup_pgvector(conn):
    cur = conn.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    conn.commit()
    cur.close()
    print('pgvector extension enabled')


def create_products_table(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS products CASCADE;')
    cur.execute(f'''
        CREATE TABLE products (
            id BIGINT PRIMARY KEY,
            gender VARCHAR(50),
            masterCategory VARCHAR(100),
            subCategory VARCHAR(100),
            articleType VARCHAR(100),
            baseColour VARCHAR(100),
            season VARCHAR(50),
            year INT,
            usage VARCHAR(100),
            productDisplayName TEXT,
            image_link TEXT,
            price_pkr FLOAT,
            embedding vector({EMBEDDING_DIM})
        );
    ''')
    conn.commit()
    cur.close()
    print('Products table created')


def create_vector_index(conn):
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM products WHERE embedding IS NOT NULL;')
    count = cur.fetchone()[0]
    if count < 100:
        print(f'Skipping vector index ({count} rows; need more data)')
        cur.close()
        return

    try:
        cur.execute('DROP INDEX IF EXISTS products_embedding_idx;')
        cur.execute('''
            CREATE INDEX products_embedding_idx ON products
            USING hnsw (embedding vector_cosine_ops);
        ''')
        conn.commit()
        print('HNSW vector index created')
    except Exception as e:
        print(f'HNSW index failed ({e}), trying IVFFlat...')
        conn.rollback()
        cur.execute('DROP INDEX IF EXISTS products_embedding_idx;')
        lists = max(10, min(100, count // 100))
        cur.execute(f'''
            CREATE INDEX products_embedding_idx ON products
            USING ivfflat (embedding vector_cosine_ops) WITH (lists = {lists});
        ''')
        conn.commit()
        print(f'IVFFlat index created (lists={lists})')
    cur.close()


def load_sqlite_products():
    if not DB_PATH.exists():
        print(f'ERROR: {DB_PATH} not found. Run: python db_setup.py')
        sys.exit(1)

    products = {}
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        SELECT id, gender, masterCategory, subCategory, articleType,
               baseColour, season, year, usage, productDisplayName,
               image_link, price_pkr
        FROM products
    ''')
    for row in cur.fetchall():
        products[row[0]] = row
    conn.close()
    print(f'Loaded {len(products)} products from SQLite')
    return products


def migrate_embeddings(conn, sqlite_products):
    emb_path = EMBEDDINGS_DIR / 'embeddings_all.npy'
    paths_path = EMBEDDINGS_DIR / 'paths_all.npy'

    if not emb_path.exists():
        print(f'ERROR: {emb_path} not found. Run: cd model && python save_embeddings.py')
        sys.exit(1)

    embeddings = np.load(emb_path)
    paths = np.load(paths_path, allow_pickle=True)
    print(f'Embeddings shape: {embeddings.shape}', flush=True)

    rows = []
    failed = 0

    for i, (embedding, path) in enumerate(zip(embeddings, paths)):
        try:
            filename = str(Path(path).name)
            product_id = int(filename.split('.')[0])
            if product_id not in sqlite_products:
                failed += 1
                continue

            prod = sqlite_products[product_id]
            embedding_str = '[' + ','.join(map(str, embedding.tolist())) + ']'
            rows.append((
                product_id, prod[1], prod[2], prod[3], prod[4],
                prod[5], prod[6], prod[7], prod[8], prod[9],
                prod[10], prod[11], embedding_str,
            ))
        except Exception as e:
            failed += 1
            if failed <= 5:
                print(f'  Error at index {i}: {e}', flush=True)

    print(f'Prepared {len(rows)} rows for bulk insert...', flush=True)
    cur = conn.cursor()
    insert_sql = '''
        INSERT INTO products (
            id, gender, masterCategory, subCategory, articleType,
            baseColour, season, year, usage, productDisplayName,
            image_link, price_pkr, embedding
        ) VALUES %s
    '''

    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]
        execute_values(cur, insert_sql, batch, page_size=BATCH_SIZE)
        conn.commit()
        print(f'  Inserted {min(start + BATCH_SIZE, len(rows))}/{len(rows)}', flush=True)

    cur.close()
    print(f'Migration complete: {len(rows)} inserted, {failed} skipped/failed', flush=True)
    return len(rows)


def verify_migration(conn):
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM products;')
    count = cur.fetchone()[0]
    cur.execute(
        'SELECT id, productDisplayName, price_pkr FROM products LIMIT 3;'
    )
    samples = cur.fetchall()
    cur.close()
    print(f'\nVerification: {count} products in Neon')
    for row in samples:
        print(f'  ID {row[0]}: {row[1][:50]}... PKR {row[2]}')


def test_vector_search(conn):
    cur = conn.cursor()
    cur.execute('SELECT embedding FROM products WHERE embedding IS NOT NULL LIMIT 1;')
    row = cur.fetchone()
    if not row:
        return
    query_vector = row[0]
    cur.execute('''
        SELECT id, productDisplayName, embedding <=> %s AS distance
        FROM products
        ORDER BY embedding <=> %s
        LIMIT 5;
    ''', (query_vector, query_vector))
    results = cur.fetchall()
    cur.close()
    print('\nVector search test (top 5):')
    for r in results:
        print(f'  ID {r[0]}: dist={r[2]:.4f} — {r[1][:40]}')


def main():
    database_url = get_database_url()
    print('Connecting to Neon...', flush=True)
    conn = psycopg2.connect(database_url)
    print('Connected')

    setup_pgvector(conn)
    create_products_table(conn)
    sqlite_products = load_sqlite_products()
    migrate_embeddings(conn, sqlite_products)
    create_vector_index(conn)
    verify_migration(conn)
    test_vector_search(conn)
    conn.close()
    print('\nMigration successful!')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'\nMigration failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
