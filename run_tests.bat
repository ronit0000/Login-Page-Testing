@echo off
REM Quick test runner script for Windows

echo ============================================================
echo Login Page Testing - Quick Test Runner
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo ============================================================
echo Choose test suite to run:
echo ============================================================
echo 1. All Tests
echo 2. Boundary Value Tests
echo 3. Functional Tests
echo 4. Security Tests
echo 5. Performance Tests
echo 6. Quick Smoke Test (UI only)
echo 7. Specific Bug Tests
echo 8. Exit
echo ============================================================
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo Running ALL tests...
    pytest -v --html=reports/report.html
)
if "%choice%"=="2" (
    echo Running BOUNDARY VALUE tests...
    pytest -m boundary -v --html=reports/boundary_report.html
)
if "%choice%"=="3" (
    echo Running FUNCTIONAL tests...
    pytest -m functional -v --html=reports/functional_report.html
)
if "%choice%"=="4" (
    echo Running SECURITY tests...
    pytest -m security -v --html=reports/security_report.html
)
if "%choice%"=="5" (
    echo Running PERFORMANCE tests...
    pytest -m performance -v --html=reports/performance_report.html
)
if "%choice%"=="6" (
    echo Running QUICK SMOKE tests...
    pytest -m "functional and ui" -v
)
if "%choice%"=="7" (
    echo.
    echo Bug-Specific Tests:
    echo 1. BUG #1 - Email Validation
    echo 2. BUG #2 - Password Boundary
    echo 3. BUG #3 - SQL Injection
    echo 4. BUG #4 - Empty Submission
    echo 5. BUG #5 - Rate Limiting
    echo 6. BUG #6 - Insecure Storage
    echo 7. BUG #7 - XSS Vulnerability
    echo.
    set /p bug="Enter bug number (1-7): "
    
    if "!bug!"=="1" pytest tests/test_boundary_values.py -k email -v
    if "!bug!"=="2" pytest tests/test_boundary_values.py -k password -v
    if "!bug!"=="3" pytest tests/test_security.py -k sql -v
    if "!bug!"=="4" pytest tests/test_functional.py::TestFunctionalRequirements::test_invalid_submission_blocked -v
    if "!bug!"=="5" pytest tests/test_security.py::TestSecurityVulnerabilities::test_no_rate_limiting -v
    if "!bug!"=="6" pytest tests/test_security.py::TestSecurityVulnerabilities::test_insecure_localstorage -v
    if "!bug!"=="7" pytest tests/test_security.py -k xss -v
)
if "%choice%"=="8" (
    echo Exiting...
    exit /b
)

echo.
echo ============================================================
echo Test execution completed!
echo ============================================================
echo.
echo View reports:
echo - HTML Report: reports\report.html
echo - Screenshots: screenshots\
echo.

set /p openreport="Open HTML report? (y/n): "
if /i "%openreport%"=="y" (
    start reports\report.html
)

pause
