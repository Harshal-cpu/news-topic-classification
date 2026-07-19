@echo off
REM News Classification Project - Quick Run Script
REM This script helps you run the project easily on Windows

echo ====================================================================
echo NEWS TOPIC CLASSIFICATION - QUICK RUN MENU
echo ====================================================================
echo.

:menu
echo Please select an option:
echo.
echo 1. Test Setup (Verify installation)
echo 2. Run Main Project (Full pipeline)
echo 3. Open Jupyter Notebook
echo 4. Start Flask API
echo 5. Start Streamlit Demo App (For Developers)
echo 6. Start User-Friendly Web App (For Everyone)
echo 7. Install Dependencies
echo 8. Download NLTK Data
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto main
if "%choice%"=="3" goto notebook
if "%choice%"=="4" goto api
if "%choice%"=="5" goto streamlit
if "%choice%"=="6" goto webapp
if "%choice%"=="7" goto install
if "%choice%"=="8" goto nltk
if "%choice%"=="9" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:test
echo.
echo ====================================================================
echo Running Setup Tests...
echo ====================================================================
python test_setup.py
echo.
pause
goto menu

:main
echo.
echo ====================================================================
echo Running Main Project...
echo This will take 5-10 minutes. Please wait...
echo ====================================================================
python news_classification.py
echo.
echo ====================================================================
echo Project completed! Check the 'outputs' folder for visualizations.
echo ====================================================================
pause
goto menu

:notebook
echo.
echo ====================================================================
echo Starting Jupyter Notebook...
echo ====================================================================
jupyter notebook news_classification.ipynb
pause
goto menu

:api
echo.
echo ====================================================================
echo Starting Flask API...
echo API will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ====================================================================
python api.py
pause
goto menu

:streamlit
echo.
echo ====================================================================
echo Starting Streamlit Demo Application...
echo App will open in your browser automatically
echo URL: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ====================================================================
streamlit run streamlit_app.py
pause
goto menu

:webapp
echo.
echo ====================================================================
echo Starting User-Friendly Web Application...
echo.
echo This is the PRODUCTION-READY version for end users!
echo Beautiful interface, easy to use, no technical knowledge needed.
echo.
echo App will open in your browser automatically
echo URL: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ====================================================================
streamlit run app.py
pause
goto menu

:install
echo.
echo ====================================================================
echo Installing Dependencies...
echo ====================================================================
pip install -r requirements.txt
echo.
echo ====================================================================
echo Installation completed!
echo ====================================================================
pause
goto menu

:nltk
echo.
echo ====================================================================
echo Downloading NLTK Data...
echo ====================================================================
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')"
echo.
echo ====================================================================
echo NLTK data downloaded!
echo ====================================================================
pause
goto menu

:end
echo.
echo Thank you for using News Classification Project!
echo.
exit
