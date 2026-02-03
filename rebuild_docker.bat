@echo off
echo ========================================
echo Rebuilding Docker Container with Barcode Support
echo ========================================
echo.

echo Stopping containers...
docker-compose down

echo.
echo Rebuilding with new packages...
docker-compose build --no-cache

echo.
echo Starting containers...
docker-compose up -d

echo.
echo Checking status...
docker-compose ps

echo.
echo ========================================
echo Rebuild Complete!
echo ========================================
echo.
echo Check logs: docker-compose logs -f mohi_web
echo.
pause
