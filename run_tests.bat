@echo off
echo ============================================================
echo Boundary Testing - Login Page
echo ============================================================
echo.
echo Running 6 boundary tests...
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
)

REM Run boundary tests with text output only
pytest tests/test_boundary.py -v -s

echo.
echo ============================================================
echo Tests completed!
echo ============================================================
pause
