@echo off
echo ============================================================
echo Running ALL Tests - This will take 5-10 minutes
echo ============================================================
echo.
echo Tests will check:
echo - Email Validation (BUG #1)
echo - Password Boundaries (BUG #2)
echo - SQL Injection (BUG #3)
echo - Empty Submission (BUG #4)
echo - Rate Limiting (BUG #5)
echo - Insecure Storage (BUG #6)
echo - XSS Vulnerabilities (BUG #7)
echo.
pause

pytest -v --html=reports/full_report.html --self-contained-html

echo.
echo ============================================================
echo Test execution completed!
echo ============================================================
echo.
echo Opening HTML report...
start reports\full_report.html
echo.
pause
