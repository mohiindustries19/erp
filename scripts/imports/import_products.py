"""
Import Products - Mohi Industries Bakery Items
Run this script to add all bakery products to the database
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models import Product, ProductCategory

# Product data from Mohi Industries catalog
products_data = [
    # Bread Products - White
    {"name": "Bread White 175g", "category": "Bread", "pack_size": "175g", "unit": "pcs", "sku": "BRD-WHT-175"},
    {"name": "Bread White 200g", "category": "Bread", "pack_size": "200g", "unit": "pcs", "sku": "BRD-WHT-200"},
    {"name": "Bread White 350g", "category": "Bread", "pack_size": "350g", "unit": "pcs", "sku": "BRD-WHT-350"},
    {"name": "Bread White 400g", "category": "Bread", "pack_size": "400g", "unit": "pcs", "sku": "BRD-WHT-400"},
    {"name": "Bread White 600g", "category": "Bread", "pack_size": "600g", "unit": "pcs", "sku": "BRD-WHT-600"},
    {"name": "Bread White 800g", "category": "Bread", "pack_size": "800g", "unit": "pcs", "sku": "BRD-WHT-800"},
    
    # Bread Products - Atta
    {"name": "Bread Atta 450g", "category": "Bread", "pack_size": "450g", "unit": "pcs", "sku": "BRD-ATA-450"},
    
    # Bread Products - Fruits
    {"name": "Bread Fruits 200g", "category": "Bread", "pack_size": "200g", "unit": "pcs", "sku": "BRD-FRT-200"},
    
    # Bread Products - Makhan
    {"name": "Bread Makhan 400g", "category": "Bread", "pack_size": "400g", "unit": "pcs", "sku": "BRD-MKN-400"},
    
    # Bread Products - Milk
    {"name": "Bread Milk 400g", "category": "Bread", "pack_size": "400g", "unit": "pcs", "sku": "BRD-MLK-400"},
    
    # Cookies
    {"name": "Cookies", "category": "Cookies & Biscuits", "pack_size": "pack", "unit": "pcs", "sku": "CKI-STD-001"},
    
    # Bakery Items
    {"name": "Paw", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-PAW-001"},
    {"name": "Bun", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-BUN-001"},
    {"name": "Papa", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-PAP-001"},
    {"name": "Cream Roll", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-CRL-001"},
    {"name": "Cake", "category": "Cakes", "pack_size": "pcs", "unit": "pcs", "sku": "CAK-STD-001"},
    {"name": "Rusk", "category": "Rusk", "pack_size": "pack", "unit": "pcs", "sku": "RSK-STD-001"},
    {"name": "Namak Pare", "category": "Snacks", "pack_size": "pack", "unit": "pcs", "sku": "SNK-NMP-001"},
    {"name": "Cream Bun", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-CBN-001"},
    {"name": "Rosted Nimki", "category": "Snacks", "pack_size": "pack", "unit": "pcs", "sku": "SNK-RNM-001"},
    {"name": "Pizza Base", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-PZB-001"},
    {"name": "Cup Cake", "category": "Cakes", "pack_size": "pcs", "unit": "pcs", "sku": "CAK-CUP-001"},
    {"name": "Ring Bun", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-RBN-001"},
    {"name": "Rosted Roll", "category": "Bakery", "pack_size": "pcs", "unit": "pcs", "sku": "BAK-RRL-001"},
]

# Default pricing (you can adjust these)
default_prices = {
    "Bread": {"mrp": 30, "base_price": 25, "cost_price": 20},
    "Cookies & Biscuits": {"mrp": 20, "base_price": 17, "cost_price": 14},
    "Bakery": {"mrp": 15, "base_price": 12, "cost_price": 10},
    "Cakes": {"mrp": 50, "base_price": 42, "cost_price": 35},
    "Rusk": {"mrp": 40, "base_price": 34, "cost_price": 28},
    "Snacks": {"mrp": 25, "base_price": 21, "cost_price": 17},
}

def get_or_create_category(name):
    """Get existing category or create new one"""
    category = ProductCategory.query.filter_by(name=name).first()
    if not category:
        # Generate category code
        code = ''.join([c[0].upper() for c in name.split()[:3]])
        if len(code) < 3:
            code = name[:3].upper()
        
        # Check if code exists, make it unique
        counter = 1
        base_code = code
        while ProductCategory.query.filter_by(code=code).first():
            code = f"{base_code}{counter}"
            counter += 1
        
        category = ProductCategory(
            name=name,
            code=code,
            description=f"{name} products manufactured by Mohi Industries",
            hsn_code="1905",  # Default HSN for bakery
            gst_rate=5.0
        )
        db.session.add(category)
        db.session.flush()
    return category

def import_products():
    """Import all products into the database"""
    app = create_app()
    
    with app.app_context():
        print("Starting product import...")
        print(f"Total products to import: {len(products_data)}")
        print("="*60)
        
        added = 0
        skipped = 0
        updated = 0
        
        for idx, data in enumerate(products_data, 1):
            try:
                # Check if product already exists by SKU
                existing = Product.query.filter_by(sku=data['sku']).first()
                
                if existing:
                    # Update existing product
                    existing.name = data['name']
                    existing.pack_size = data['pack_size']
                    existing.unit = data['unit']
                    updated += 1
                    print(f"{idx}. Updated: {data['sku']} - {data['name']}")
                else:
                    # Get or create category
                    category = get_or_create_category(data['category'])
                    
                    # Get default prices for category
                    prices = default_prices.get(data['category'], {"mrp": 20, "base_price": 17, "cost_price": 14})
                    
                    # Adjust prices based on pack size (larger packs = higher price)
                    pack_size = data['pack_size']
                    price_multiplier = 1.0
                    
                    if 'g' in pack_size:
                        weight = int(''.join(filter(str.isdigit, pack_size)))
                        if weight >= 800:
                            price_multiplier = 2.5
                        elif weight >= 600:
                            price_multiplier = 2.0
                        elif weight >= 400:
                            price_multiplier = 1.5
                        elif weight >= 350:
                            price_multiplier = 1.3
                        elif weight >= 200:
                            price_multiplier = 1.0
                        elif weight >= 175:
                            price_multiplier = 0.9
                    
                    # Create new product
                    product = Product(
                        sku=data['sku'],
                        name=data['name'],
                        category_id=category.id,
                        description=f"{data['name']} - Fresh bakery product from Mohi Industries",
                        unit=data['unit'],
                        pack_size=data['pack_size'],
                        hsn_code="1905",  # HSN code for bread, pastry, cakes, biscuits
                        gst_rate=5.0,  # 5% GST for bakery products
                        shelf_life_days=7,  # 7 days shelf life for bakery
                        mrp=round(prices['mrp'] * price_multiplier, 2),
                        base_price=round(prices['base_price'] * price_multiplier, 2),
                        cost_price=round(prices['cost_price'] * price_multiplier, 2),
                        min_stock_level=50,
                        reorder_level=100,
                        requires_batch_tracking=True,
                        is_active=True
                    )
                    
                    db.session.add(product)
                    added += 1
                    print(f"{idx}. Added: {data['sku']} - {data['name']} (₹{product.mrp})")
                
            except Exception as e:
                print(f"{idx}. ERROR: {data['name']} - {str(e)}")
                skipped += 1
                continue
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("IMPORT COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"✅ Added: {added} products")
            print(f"🔄 Updated: {updated} products")
            print(f"⚠️  Skipped: {skipped} products")
            print(f"📊 Total: {added + updated} products in database")
            print("="*60)
            
            # Show category summary
            print("\nCATEGORY SUMMARY:")
            print("-"*60)
            categories = ProductCategory.query.all()
            for cat in categories:
                count = Product.query.filter_by(category_id=cat.id).count()
                print(f"  {cat.name}: {count} products")
            print("="*60)
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR committing to database: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    success = import_products()
    sys.exit(0 if success else 1)
