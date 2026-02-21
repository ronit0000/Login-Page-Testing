# 🚀 Quick Start Guide

## Setup (First Time)

```bash
# 1. Navigate to project
cd "c:\Users\lenovo\Desktop\Login-page-testing"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment configuration
copy .env.example .env
```

## Running Tests

### 🎯 Quick Test Run
```bash
pytest -v
```

### 📊 Run with HTML Report
```bash
pytest --html=reports/report.html
```

### 🔍 Run Specific Category
```bash
# Boundary tests
pytest -m boundary -v

# Security tests
pytest -m security -v

# Functional tests
pytest -m functional -v

# Performance tests
pytest -m performance -v
```

### 🐛 Test Specific Bug
```bash
# BUG #1: Email Validation
pytest tests/test_boundary_values.py -k email -v

# BUG #2: Password Boundary
pytest tests/test_boundary_values.py -k password -v

# BUG #3: SQL Injection
pytest tests/test_security.py -k sql -v

# BUG #4: Empty Submission
pytest tests/test_functional.py::TestFunctionalRequirements::test_invalid_submission_blocked -v

# BUG #5: Rate Limiting
pytest tests/test_security.py::TestSecurityVulnerabilities::test_no_rate_limiting -v

# BUG #6: Insecure Storage
pytest tests/test_security.py::TestSecurityVulnerabilities::test_insecure_localstorage -v

# BUG #7: XSS
pytest tests/test_security.py -k xss -v
```

### ⚡ Fast Parallel Execution
```bash
pytest -n auto
```

### 🎬 Run in Headless Mode
```bash
set HEADLESS=true
pytest
```

## View Results

```bash
# Open HTML report
start reports\report.html

# View screenshots (if tests failed)
explorer screenshots
```

## Common Commands Cheat Sheet

```bash
# Run all tests with detailed output
pytest -vv

# Run tests and stop at first failure
pytest -x

# Run tests matching pattern
pytest -k "email or password"

# Run specific test file
pytest tests/test_security.py

# Run specific test
pytest tests/test_security.py::TestSecurityVulnerabilities::test_sql_injection_basic

# Show print statements
pytest -s

# Generate coverage report (if pytest-cov installed)
pytest --cov=pages --cov=config --cov-report=html

# List all available tests
pytest --collect-only

# List all markers
pytest --markers
```

## For Hackathon Demo

1. **Start with boundary tests**:
   ```bash
   pytest tests/test_boundary_values.py -v
   ```

2. **Show security vulnerabilities**:
   ```bash
   pytest tests/test_security.py -v
   ```

3. **Open HTML report**:
   ```bash
   start reports\report.html
   ```

4. **Show screenshots of failures**:
   ```bash
   explorer screenshots
   ```

## Troubleshooting

### WebDriver Issues
```bash
pip install --upgrade webdriver-manager selenium
```

### Browser Not Opening
```bash
# Try different browser
set BROWSER=firefox
pytest

# Or use headless mode
set HEADLESS=true
pytest
```

### Clear Cache
```bash
pytest --cache-clear
```

## Test Count
- **73+ total tests**
- Boundary: 20 tests
- Functional: 25 tests
- Security: 20 tests
- Performance: 8 tests

## Expected Results
- **~60% pass rate** (failures are intentional bugs!)
- All failures document security vulnerabilities and validation issues

---

**Happy Testing! 🧪**
