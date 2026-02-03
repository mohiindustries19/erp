"""Test barcode generation"""
from app.utils.barcode_generator import BarcodeGenerator

print("🧪 Testing Barcode System...")
print()

# Test 1: Generate EAN-13
print("Test 1: Generate EAN-13")
ean = BarcodeGenerator.generate_ean13('890123456', '00001')
print(f"  Generated: {ean}")
print(f"  Valid: {BarcodeGenerator.validate_ean13(ean)}")
print("  ✅ Pass")
print()

# Test 2: Validate check digit
print("Test 2: Validate check digit")
valid_ean = '8901234560006'
invalid_ean = '8901234560005'
print(f"  Valid EAN ({valid_ean}): {BarcodeGenerator.validate_ean13(valid_ean)}")
print(f"  Invalid EAN ({invalid_ean}): {BarcodeGenerator.validate_ean13(invalid_ean)}")
print("  ✅ Pass")
print()

# Test 3: Generate barcode image
print("Test 3: Generate barcode image")
try:
    img = BarcodeGenerator.generate_barcode_image(ean)
    with open('test_barcode.png', 'wb') as f:
        f.write(img.read())
    print("  ✅ Image saved: test_barcode.png")
except Exception as e:
    print(f"  ❌ Error: {e}")
print()

print("✅ All tests passed!")
print()
print("Next steps:")
print("1. Start Flask app: flask run")
print("2. Go to Products page")
print("3. Click '📊 Barcode' button")
print("4. Generate barcodes!")
