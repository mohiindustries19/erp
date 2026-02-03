"""
Barcode Generation Utilities - EAN-13 for Retail
"""
import barcode
from barcode.writer import ImageWriter, SVGWriter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os


class BarcodeGenerator:
    """Generate EAN-13 barcodes for retail products"""
    
    # Default company prefix (update with your GS1 India registered prefix)
    DEFAULT_COMPANY_PREFIX = "890"  # India country code
    
    @staticmethod
    def calculate_check_digit(barcode_12):
        """
        Calculate EAN-13 check digit
        Formula: (10 - ((sum of odd position digits * 1 + sum of even position digits * 3) % 10)) % 10
        """
        if len(barcode_12) != 12:
            raise ValueError("Barcode must be 12 digits for check digit calculation")
        
        odd_sum = sum(int(barcode_12[i]) for i in range(0, 12, 2))
        even_sum = sum(int(barcode_12[i]) for i in range(1, 12, 2))
        
        total = odd_sum + (even_sum * 3)
        check_digit = (10 - (total % 10)) % 10
        
        return str(check_digit)
    
    @staticmethod
    def generate_ean13(company_prefix, product_code):
        """
        Generate EAN-13 barcode number
        
        Args:
            company_prefix: Your GS1 company prefix (7-9 digits)
            product_code: Your product code (3-5 digits)
        
        Returns:
            13-digit EAN-13 barcode string
        """
        # Combine prefix and product code
        combined = f"{company_prefix}{product_code}"
        
        # Ensure total is 12 digits before check digit
        if len(combined) > 12:
            # Truncate product code if combined is too long
            product_code = product_code[:12 - len(company_prefix)]
            combined = f"{company_prefix}{product_code}"
        
        barcode_12 = combined.zfill(12)
        
        if len(barcode_12) != 12:
            raise ValueError(f"Company prefix + product code must total 12 digits, got {len(barcode_12)}")
        
        check_digit = BarcodeGenerator.calculate_check_digit(barcode_12)
        return barcode_12 + check_digit
    
    @staticmethod
    def validate_ean13(ean_code):
        """Validate EAN-13 barcode"""
        if not ean_code or len(ean_code) != 13:
            return False
        
        if not ean_code.isdigit():
            return False
        
        # Validate check digit
        calculated_check = BarcodeGenerator.calculate_check_digit(ean_code[:12])
        return calculated_check == ean_code[12]
    
    @staticmethod
    def generate_barcode_image(ean_code, format='png'):
        """
        Generate barcode image
        
        Args:
            ean_code: 13-digit EAN code
            format: 'png' or 'svg'
        
        Returns:
            BytesIO object containing image data
        """
        if not BarcodeGenerator.validate_ean13(ean_code):
            raise ValueError(f"Invalid EAN-13 code: {ean_code}")
        
        # Create barcode
        writer = ImageWriter() if format == 'png' else SVGWriter()
        ean = barcode.get('ean13', ean_code, writer=writer)
        
        # Generate to BytesIO
        output = BytesIO()
        ean.write(output, options={
            'module_width': 0.3,
            'module_height': 15.0,
            'quiet_zone': 6.5,
            'font_size': 10,
            'text_distance': 5.0,
            'write_text': True
        })
        output.seek(0)
        
        return output
    
    @staticmethod
    def generate_product_label(product, batch=None, label_size=(400, 600)):
        """
        Generate professional retail product label with barcode, MRP, batch info
        Meets Indian retail standards (FSSAI, Legal Metrology Act)
        
        Args:
            product: Product model instance
            batch: Optional Batch model instance
            label_size: Tuple (width, height) in pixels (default: 400x600 for 50x75mm at 203dpi)
        
        Returns:
            PIL Image object
        """
        width, height = label_size
        
        # Create white background
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts with fallback
        try:
            # Professional fonts for retail labels
            company_font = ImageFont.truetype("arialbd.ttf", 20)  # Bold for company
            title_font = ImageFont.truetype("arialbd.ttf", 24)    # Bold for product
            mrp_font = ImageFont.truetype("arialbd.ttf", 32)      # Large bold for MRP
            normal_font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
            tiny_font = ImageFont.truetype("arial.ttf", 10)
        except:
            # Fallback to default
            company_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            mrp_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            tiny_font = ImageFont.load_default()
        
        y_offset = 15
        center_x = width // 2
        
        # === COMPANY HEADER ===
        company_name = "MOHI INDUSTRIES"
        bbox = draw.textbbox((0, 0), company_name, font=company_font)
        text_width = bbox[2] - bbox[0]
        draw.text((center_x - text_width//2, y_offset), company_name, fill='black', font=company_font)
        y_offset += 30
        
        # Separator line
        draw.line([(20, y_offset), (width-20, y_offset)], fill='#d00000', width=2)
        y_offset += 15
        
        # === PRODUCT NAME ===
        product_name = product.name
        # Wrap long product names
        if len(product_name) > 25:
            words = product_name.split()
            line1 = ""
            line2 = ""
            for word in words:
                if len(line1 + word) < 25:
                    line1 += word + " "
                else:
                    line2 += word + " "
            
            bbox = draw.textbbox((0, 0), line1.strip(), font=title_font)
            text_width = bbox[2] - bbox[0]
            draw.text((center_x - text_width//2, y_offset), line1.strip(), fill='black', font=title_font)
            y_offset += 28
            
            if line2:
                bbox = draw.textbbox((0, 0), line2.strip(), font=title_font)
                text_width = bbox[2] - bbox[0]
                draw.text((center_x - text_width//2, y_offset), line2.strip(), fill='black', font=title_font)
                y_offset += 28
        else:
            bbox = draw.textbbox((0, 0), product_name, font=title_font)
            text_width = bbox[2] - bbox[0]
            draw.text((center_x - text_width//2, y_offset), product_name, fill='black', font=title_font)
            y_offset += 30
        
        # === PACK SIZE ===
        if product.pack_size:
            pack_text = f"Net Wt: {product.pack_size}"
            bbox = draw.textbbox((0, 0), pack_text, font=normal_font)
            text_width = bbox[2] - bbox[0]
            draw.text((center_x - text_width//2, y_offset), pack_text, fill='black', font=normal_font)
            y_offset += 25
        
        y_offset += 10
        
        # === MRP (PROMINENT) ===
        mrp_text = f"MRP: ₹{product.mrp:.2f}"
        bbox = draw.textbbox((0, 0), mrp_text, font=mrp_font)
        text_width = bbox[2] - bbox[0]
        # MRP box with border
        mrp_box_padding = 10
        mrp_box = [
            center_x - text_width//2 - mrp_box_padding,
            y_offset - 5,
            center_x + text_width//2 + mrp_box_padding,
            y_offset + 35
        ]
        draw.rectangle(mrp_box, outline='#d00000', width=3)
        draw.text((center_x - text_width//2, y_offset), mrp_text, fill='#d00000', font=mrp_font)
        y_offset += 45
        
        # Legal requirement
        incl_text = "(Incl. of all taxes)"
        bbox = draw.textbbox((0, 0), incl_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        draw.text((center_x - text_width//2, y_offset), incl_text, fill='gray', font=small_font)
        y_offset += 25
        
        # === BARCODE ===
        if product.ean_barcode:
            try:
                barcode_img_io = BarcodeGenerator.generate_barcode_image(product.ean_barcode)
                barcode_img = Image.open(barcode_img_io)
                
                # Resize barcode to fit label (standard size)
                barcode_width = width - 40
                barcode_height = int(barcode_img.height * (barcode_width / barcode_img.width))
                barcode_img = barcode_img.resize((barcode_width, barcode_height), Image.Resampling.LANCZOS)
                
                # Center barcode
                barcode_x = (width - barcode_width) // 2
                img.paste(barcode_img, (barcode_x, y_offset))
                y_offset += barcode_height + 10
            except Exception as e:
                draw.text((20, y_offset), f"Barcode error: {str(e)}", fill='red', font=small_font)
                y_offset += 20
        else:
            draw.text((20, y_offset), "No barcode assigned", fill='gray', font=small_font)
            y_offset += 20
        
        y_offset += 10
        
        # === BATCH INFORMATION ===
        if batch:
            # Batch box
            batch_y_start = y_offset
            draw.rectangle([(15, y_offset), (width-15, y_offset + 75)], outline='#333', width=1)
            y_offset += 8
            
            batch_info = [
                f"Batch No: {batch.batch_number}",
                f"Mfg Date: {batch.manufacturing_date.strftime('%d/%m/%Y')}",
                f"Best Before: {batch.expiry_date.strftime('%d/%m/%Y')}"
            ]
            
            for info in batch_info:
                draw.text((25, y_offset), info, fill='black', font=small_font)
                y_offset += 20
            
            y_offset += 10
        
        # === COMPANY DETAILS (Footer) ===
        y_offset = height - 120  # Fixed position from bottom
        
        company_details = [
            "FSSAI Lic: 12345678901234",
            "Mfd by: Mohi Industries",
            "B-61, P-1, BIADA, Hajipur,",
            "Vaishali, Bihar - 844102",
            "Customer Care: 1800-XXX-XXXX"
        ]
        
        for detail in company_details:
            bbox = draw.textbbox((0, 0), detail, font=tiny_font)
            text_width = bbox[2] - bbox[0]
            draw.text((center_x - text_width//2, y_offset), detail, fill='#333', font=tiny_font)
            y_offset += 12
        
        return img
    
    @staticmethod
    def generate_next_product_code(company_prefix, last_product_code=None):
        """
        Generate next sequential product code
        
        Args:
            company_prefix: Your company prefix (7-9 digits)
            last_product_code: Last used product code (optional)
        
        Returns:
            Next product code string
        """
        # Calculate how many digits we need for product code
        prefix_len = len(company_prefix)
        product_code_len = 12 - prefix_len
        
        if last_product_code:
            next_code = int(last_product_code) + 1
        else:
            next_code = 1
        
        # Format with leading zeros
        return str(next_code).zfill(product_code_len)
