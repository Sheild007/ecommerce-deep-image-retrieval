import csv
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
STYLES_CSV = PROJECT_ROOT / 'styles.csv'
IMAGES_CSV = PROJECT_ROOT / 'images.csv'
DB_PATH = BASE_DIR / 'products.db'


def create_database():
    """Convert CSV files to SQLite database."""

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print('Reading images.csv...')
    image_map = {}
    with open(IMAGES_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row['filename'].replace('.jpg', '')
            image_map[filename] = row['link']

    print(f'Loaded {len(image_map)} image URLs')

    print('Creating products table...')
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
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
            price_pkr INTEGER
        )
    ''')

    print('Reading and inserting from styles.csv...')
    count = 0
    with open(STYLES_CSV, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                product_id = row['id']
                image_url = image_map.get(product_id, '')

                base_price_pkr = 1799
                price_variation = 0.7 + (int(product_id) % 100) / 100
                price_pkr = int(base_price_pkr * price_variation)

                cursor.execute('''
                    INSERT INTO products
                    (id, gender, masterCategory, subCategory, articleType, baseColour,
                     season, year, usage, productDisplayName, image_link, price_pkr)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    product_id,
                    row.get('gender', 'Unisex'),
                    row.get('masterCategory', 'Unknown'),
                    row.get('subCategory', 'Unknown'),
                    row.get('articleType', 'Unknown'),
                    row.get('baseColour', 'Black'),
                    row.get('season', 'Summer'),
                    int(row.get('year', 2012)),
                    row.get('usage', 'Casual'),
                    row.get('productDisplayName', 'Product'),
                    image_url,
                    price_pkr,
                ))

                count += 1
                if count % 5000 == 0:
                    print(f'  Inserted {count} products...')
            except Exception as e:
                print(f'Error on row {count}: {e}')
                continue

    conn.commit()

    print('Creating indexes...')
    cursor.execute('CREATE INDEX idx_category ON products(masterCategory)')
    cursor.execute('CREATE INDEX idx_gender ON products(gender)')
    cursor.execute('CREATE INDEX idx_name ON products(productDisplayName)')
    conn.commit()

    print('\nDatabase created successfully!')
    print(f'Location: {DB_PATH}')
    print(f'Total products: {count}')
    conn.close()


if __name__ == '__main__':
    create_database()
