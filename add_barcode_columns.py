"""
Add barcode columns to products table
Run this script to add barcode support
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file")
    exit(1)

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("🔄 Adding barcode columns to products table...")
    
    # Add columns
    cur.execute("""
        ALTER TABLE products 
        ADD COLUMN IF NOT EXISTS ean_barcode VARCHAR(13),
        ADD COLUMN IF NOT EXISTS barcode_source VARCHAR(32),
        ADD COLUMN IF NOT EXISTS barcode_registered_date DATE;
    """)
    
    print("✅ Columns added")
    
    # Create unique index
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ix_products_ean_barcode 
        ON products(ean_barcode);
    """)
    
    print("✅ Index created")
    
    # Commit changes
    conn.commit()
    
    print("\n✅ Barcode system installed successfully!")
    print("\nNext steps:")
    print("1. Update company prefix in app/utils/barcode_generator.py")
    print("2. Go to Products page and click '📊 Barcode' button")
    print("3. Generate barcodes for your products")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    conn.rollback()
finally:
    cur.close()
    conn.close()
