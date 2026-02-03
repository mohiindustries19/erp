@echo off
echo ============================================================
echo Installing Export & Email Features
echo Mohi Industries ERP
echo ============================================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate

echo.
echo Installing required packages...
echo.

echo [1/1] Installing openpyxl (for Excel export)...
pip install openpyxl==3.1.2

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Features installed:
echo   - PDF Export (browser print-to-PDF, no extra install needed)
echo   - Excel Export (openpyxl)
echo   - Email sending (already configured)
echo.
echo Next steps:
echo   1. Make sure distributors have email addresses
echo   2. Go to Orders - View any order
echo   3. Try the new buttons:
echo      - Export PDF (opens print dialog)
echo      - Export Excel (downloads Excel file)
echo      - Send Email (sends invoice via email)
echo.
echo ============================================================
pause
