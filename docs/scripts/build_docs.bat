@echo off
REM Documentation Build Script for Hephaestus
REM This script provides an easy way to run the various documentation scripts

echo Hephaestus Documentation Tools
echo ------------------------------
echo.

:menu
echo Please select an option:
echo 1. Set up documentation structure
echo 2. Migrate existing documentation
echo 3. Generate component documentation
echo 4. Run MkDocs server (preview)
echo 5. Build documentation site
echo 6. Run complete documentation pipeline
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto generate
if "%choice%"=="4" goto serve
if "%choice%"=="5" goto build
if "%choice%"=="6" goto pipeline
if "%choice%"=="7" goto end

echo Invalid choice. Please try again.
goto menu

:setup
echo.
echo Running documentation setup script...
python docs/scripts/setup_docs.py
echo.
pause
goto menu

:migrate
echo.
echo Running documentation migration script...
python docs/scripts/migrate_docs.py
echo.
pause
goto menu

:generate
echo.
echo Running component documentation generator...
python docs/scripts/generate_component_docs.py
echo.
pause
goto menu

:serve
echo.
echo Starting MkDocs server for preview...
echo The documentation will be available at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server.
echo.
mkdocs serve
goto menu

:build
echo.
echo Building documentation site...
mkdocs build --clean
echo.
echo Documentation site built in the 'site' directory.
pause
goto menu

:pipeline
echo.
echo Running complete documentation pipeline...
echo.
echo Step 1: Setting up documentation structure...
python docs/scripts/setup_docs.py
echo.
echo Step 2: Migrating existing documentation...
python docs/scripts/migrate_docs.py
echo.
echo Step 3: Generating component documentation...
python docs/scripts/generate_component_docs.py
echo.
echo Step 4: Building documentation site...
mkdocs build --clean
echo.
echo Documentation pipeline completed.
echo The built site is available in the 'site' directory.
pause
goto menu

:end
echo.
echo Exiting documentation tools.
exit /b 0 