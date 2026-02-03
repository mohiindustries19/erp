@echo off
echo ========================================
echo Barcode System Installation
echo ========================================
echo.

echo Step 1: Installing Python packages...
call .venv\Scripts\activate
pip install python-barcode[images]==0.15.1 reportlab==4.0.7 Pillow==10.1.0

echo.
echo Step 2: Running database migration...
flask db upgrade

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Update company prefix in app/utils/barcode_generator.py
echo 2. Register with GS1 India: https://www.gs1india.org
echo 3. Access barcode features from Products page
echo.
echo Press any key to exit...
pause >nul
