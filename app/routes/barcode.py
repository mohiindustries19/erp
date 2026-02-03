"""Barcode Routes - EAN-13 Generation and Label Printing"""

from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Batch
from datetime import datetime, date
from io import BytesIO
from urllib.parse import urlparse
from typing import Optional

# Try to import barcode libraries, make them optional
try:
    from app.utils.barcode_generator import BarcodeGenerator
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False
    BarcodeGenerator = None

# Try to import PDF libraries
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from PIL import Image
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

bp = Blueprint('barcode', __name__, url_prefix='/barcode')


def _default_company_prefix() -> str:
    return str(current_app.config.get('BARCODE_COMPANY_PREFIX', '890123456'))


def _extract_product_code_from_ean(company_prefix: str, ean_barcode: str) -> Optional[str]:
    if not ean_barcode or not company_prefix:
        return None
    if not ean_barcode.startswith(company_prefix) or len(ean_barcode) != 13:
        return None
    # strip prefix and check digit
    product_code = ean_barcode[len(company_prefix):-1]
    if not product_code.isdigit():
        return None
    return product_code


def _get_last_product_code_for_prefix(company_prefix: str) -> Optional[str]:
    if not company_prefix:
        return None
    last_product = (
        Product.query
        .filter(Product.ean_barcode.isnot(None), Product.ean_barcode.startswith(company_prefix))
        .order_by(Product.ean_barcode.desc())
        .first()
    )
    if not last_product or not last_product.ean_barcode:
        return None
    return _extract_product_code_from_ean(company_prefix, last_product.ean_barcode)


def _safe_next_url() -> Optional[str]:
    """Return a safe local redirect target if provided via request."""
    next_url = request.values.get('next')
    if not next_url:
        return None

    parsed = urlparse(next_url)
    # Only allow relative paths (no scheme/host)
    if parsed.scheme or parsed.netloc:
        return None
    if not next_url.startswith('/') or next_url.startswith('//'):
        return None
    return next_url


def check_barcode_available():
    """Check if barcode functionality is available"""
    if not BARCODE_AVAILABLE:
        flash('⚠️ Barcode functionality not available. Please install: pip install python-barcode[images] reportlab pillow', 'warning')
        return False
    return True


@bp.route('/product/<int:product_id>')
@login_required
def view_product_barcode(product_id):
    """View product barcode"""
    product = Product.query.get_or_404(product_id)
    return render_template('barcode/product_barcode.html', 
                         product=product, 
                         barcode_available=BARCODE_AVAILABLE,
                         default_company_prefix=_default_company_prefix())


@bp.route('/product/<int:product_id>/generate', methods=['POST'])
@login_required
def generate_product_barcode(product_id):
    """Generate EAN-13 barcode for product"""
    if not check_barcode_available():
        return redirect(url_for('barcode.view_product_barcode', product_id=product_id))
    
    product = Product.query.get_or_404(product_id)
    
    try:
        # Block accidental changes unless explicitly requested
        allow_replace = request.form.get('replace_existing') == 'on'
        if product.ean_barcode and not allow_replace:
            flash(
                f"ℹ️ This product already has barcode {product.ean_barcode}. "
                "Use the 'Replace existing barcode' option to change it.",
                'error'
            )
            next_url = _safe_next_url()
            return redirect(next_url or url_for('barcode.view_product_barcode', product_id=product_id))

        # Get company prefix from form or use default
        company_prefix = request.form.get('company_prefix') or _default_company_prefix()

        # Find last used code *for this prefix* and generate next.
        last_code = _get_last_product_code_for_prefix(company_prefix)
        product_code = BarcodeGenerator.generate_next_product_code(company_prefix, last_code)

        # Generate EAN-13 (skip duplicates if any exist)
        ean_code = None
        for _ in range(2000):
            candidate = BarcodeGenerator.generate_ean13(company_prefix, product_code)
            existing = Product.query.filter_by(ean_barcode=candidate).first()
            if not existing:
                ean_code = candidate
                break
            product_code = BarcodeGenerator.generate_next_product_code(company_prefix, product_code)

        if not ean_code:
            flash('❌ Could not find an available barcode number. Please check your prefix or existing barcodes.', 'error')
            next_url = _safe_next_url()
            return redirect(next_url or url_for('barcode.view_product_barcode', product_id=product_id))
        
        # Validate
        if not BarcodeGenerator.validate_ean13(ean_code):
            flash('❌ Generated barcode is invalid!', 'error')
            return redirect(url_for('barcode.view_product_barcode', product_id=product_id))
        
        # Defensive check (should be prevented by loop)
        existing = Product.query.filter_by(ean_barcode=ean_code).first()
        if existing:
            flash(f"❌ Barcode already exists (assigned to {existing.sku} - {existing.name}).", 'error')
            next_url = _safe_next_url()
            return redirect(next_url or url_for('barcode.view_product_barcode', product_id=product_id))
        
        # Save to product
        product.ean_barcode = ean_code
        product.barcode_source = request.form.get('barcode_source', 'internal')
        product.barcode_registered_date = date.today()
        
        db.session.commit()
        
        flash(f'✅ Barcode {ean_code} generated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error generating barcode: {str(e)}', 'error')

    next_url = _safe_next_url()
    return redirect(next_url or url_for('barcode.view_product_barcode', product_id=product_id))


@bp.route('/product/<int:product_id>/update', methods=['POST'])
@login_required
def update_product_barcode(product_id):
    """Manually update product barcode"""
    product = Product.query.get_or_404(product_id)
    
    try:
        ean_code = request.form.get('ean_barcode', '').strip()
        
        if not ean_code:
            product.ean_barcode = None
            product.barcode_source = None
            product.barcode_registered_date = None
            db.session.commit()
            flash('✅ Barcode removed', 'success')
            next_url = _safe_next_url()
            return redirect(next_url or url_for('barcode.view_product_barcode', product_id=product_id))
        
        # Validate
        if not BarcodeGenerator.validate_ean13(ean_code):
            flash('❌ Invalid EAN-13 barcode! Must be 13 digits with valid check digit.', 'error')
            return redirect(url_for('barcode.view_product_barcode', product_id=product_id))
        
        # Check duplicates
        existing = Product.query.filter(
            Product.ean_barcode == ean_code,
            Product.id != product_id
        ).first()
        
        if existing:
            flash(f'❌ Barcode already assigned to {existing.sku} - {existing.name}!', 'error')
            return redirect(url_for('barcode.view_product_barcode', product_id=product_id))
        
        # Update
        product.ean_barcode = ean_code
        product.barcode_source = request.form.get('barcode_source', 'gs1')
        product.barcode_registered_date = date.today()
        
        db.session.commit()
        flash(f'✅ Barcode {ean_code} saved successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error updating barcode: {str(e)}', 'error')

    next_url = _safe_next_url()
    return redirect(next_url or url_for('barcode.view_product_barcode', product_id=product_id))


@bp.route('/product/<int:product_id>/image')
@login_required
def get_barcode_image(product_id):
    """Get barcode image for product"""
    if not check_barcode_available():
        return "Barcode library not installed", 503
    
    product = Product.query.get_or_404(product_id)
    
    if not product.ean_barcode:
        return "No barcode", 404
    
    try:
        img_io = BarcodeGenerator.generate_barcode_image(product.ean_barcode)
        return send_file(img_io, mimetype='image/png', download_name=f'{product.sku}_barcode.png')
    except Exception as e:
        return f"Error: {str(e)}", 500


@bp.route('/product/<int:product_id>/label')
@login_required
def get_product_label(product_id):
    """Get product label with barcode"""
    if not check_barcode_available():
        return "Barcode library not installed", 503
    
    product = Product.query.get_or_404(product_id)
    batch_id = request.args.get('batch_id', type=int)
    
    batch = None
    if batch_id:
        batch = Batch.query.get(batch_id)
    
    try:
        label_img = BarcodeGenerator.generate_product_label(product, batch)
        
        # Convert to BytesIO
        img_io = BytesIO()
        label_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', download_name=f'{product.sku}_label.png')
    except Exception as e:
        return f"Error: {str(e)}", 500


@bp.route('/product/<int:product_id>/print-labels')
@login_required
def print_product_labels(product_id):
    """Print multiple labels on A4 sheet"""
    if not check_barcode_available() or not PDF_AVAILABLE:
        flash('⚠️ PDF generation not available. Please install reportlab.', 'warning')
        return redirect(url_for('barcode.view_product_barcode', product_id=product_id))
    
    product = Product.query.get_or_404(product_id)
    count = request.args.get('count', 10, type=int)
    batch_id = request.args.get('batch_id', type=int)
    
    batch = None
    if batch_id:
        batch = Batch.query.get(batch_id)
    
    try:
        # Create PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        page_width, page_height = A4
        
        # Label dimensions (40mm x 25mm)
        label_width = 40 * mm
        label_height = 25 * mm
        
        # Margins
        margin_x = 10 * mm
        margin_y = 10 * mm
        
        # Calculate labels per row and column
        labels_per_row = int((page_width - 2 * margin_x) / label_width)
        labels_per_col = int((page_height - 2 * margin_y) / label_height)
        
        # Generate label image
        label_img = BarcodeGenerator.generate_product_label(product, batch, label_size=(int(label_width * 2.83), int(label_height * 2.83)))
        
        # Convert PIL image to ReportLab ImageReader
        img_buffer = BytesIO()
        label_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_reader = ImageReader(img_buffer)
        
        # Draw labels
        label_count = 0
        for page in range((count // (labels_per_row * labels_per_col)) + 1):
            for row in range(labels_per_col):
                for col in range(labels_per_row):
                    if label_count >= count:
                        break
                    
                    x = margin_x + col * label_width
                    y = page_height - margin_y - (row + 1) * label_height
                    
                    c.drawImage(img_reader, x, y, width=label_width, height=label_height)
                    label_count += 1
                
                if label_count >= count:
                    break
            
            if label_count < count:
                c.showPage()
        
        c.save()
        buffer.seek(0)
        
        filename = f'{product.sku}_labels_{count}pcs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        return send_file(buffer, mimetype='application/pdf', download_name=filename, as_attachment=True)
        
    except Exception as e:
        flash(f'❌ Error generating labels: {str(e)}', 'error')
        return redirect(url_for('barcode.view_product_barcode', product_id=product_id))


@bp.route('/bulk-generate')
@login_required
def bulk_generate_page():
    """Bulk barcode generation page"""
    if not check_barcode_available():
        flash('⚠️ Barcode functionality not available. Install packages first.', 'warning')
    
    products = Product.query.filter_by(ean_barcode=None).order_by(Product.name).all()
    return render_template('barcode/bulk_generate.html', 
                         products=products,
                         barcode_available=BARCODE_AVAILABLE,
                         default_company_prefix=_default_company_prefix())


@bp.route('/bulk-generate', methods=['POST'])
@login_required
def bulk_generate_barcodes():
    """Generate barcodes for multiple products"""
    if not check_barcode_available():
        return redirect(url_for('barcode.bulk_generate_page'))
    try:
        product_ids = request.form.getlist('product_ids[]')
        company_prefix = request.form.get('company_prefix') or _default_company_prefix()
        
        if not product_ids:
            flash('❌ No products selected!', 'error')
            return redirect(url_for('barcode.bulk_generate_page'))
        
        success_count = 0
        error_count = 0

        # Start from last used code for this prefix, then increment sequentially.
        current_code = BarcodeGenerator.generate_next_product_code(
            company_prefix,
            _get_last_product_code_for_prefix(company_prefix)
        )
        
        for product_id in product_ids:
            try:
                product = Product.query.get(int(product_id))
                if not product or product.ean_barcode:
                    continue

                # Generate EAN-13 and skip duplicates if necessary
                ean_code = None
                for _ in range(2000):
                    candidate = BarcodeGenerator.generate_ean13(company_prefix, current_code)
                    if not Product.query.filter_by(ean_barcode=candidate).first():
                        ean_code = candidate
                        break
                    current_code = BarcodeGenerator.generate_next_product_code(company_prefix, current_code)

                if not ean_code:
                    raise ValueError('Unable to find available barcode number')
                
                # Save
                product.ean_barcode = ean_code
                product.barcode_source = 'internal'
                product.barcode_registered_date = date.today()
                
                db.session.commit()
                success_count += 1

                # Prepare next code for next product
                current_code = BarcodeGenerator.generate_next_product_code(company_prefix, current_code)
                
            except Exception as e:
                error_count += 1
                print(f"Error generating barcode for product {product_id}: {str(e)}")
                continue
        
        if success_count > 0:
            flash(f'✅ Generated {success_count} barcodes successfully!', 'success')
        if error_count > 0:
            flash(f'⚠️ {error_count} products failed', 'warning')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('barcode.bulk_generate_page'))


@bp.route('/validate', methods=['POST'])
@login_required
def validate_barcode():
    """AJAX endpoint to validate barcode"""
    if not BARCODE_AVAILABLE:
        return jsonify({'valid': False, 'error': 'Barcode library not available'})
    
    ean_code = request.json.get('ean_code', '')
    
    is_valid = BarcodeGenerator.validate_ean13(ean_code)
    
    # Check if already exists
    existing = None
    if is_valid:
        existing = Product.query.filter_by(ean_barcode=ean_code).first()
    
    return jsonify({
        'valid': is_valid,
        'exists': existing is not None,
        'product': existing.name if existing else None
    })
