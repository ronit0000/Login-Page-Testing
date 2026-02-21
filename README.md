# Login Form Testing - Selenium Automation

## 🎯 Project Overview

Comprehensive automated testing suite for the Login Page using Selenium WebDriver and Python. This project tests boundary values, functional requirements, security vulnerabilities, and performance metrics.

## 🐛 Bugs Being Tested

Based on `BUGS.md` from the Login-Page project:

1. **Email Validation Issues** (HIGH) - Weak validation accepting invalid formats
2. **Missing Boundary Checks** (HIGH) - No password length validation
3. **SQL Injection Vulnerability** (CRITICAL) - No input sanitization
4. **Empty Field Submission** (HIGH) - Form processes despite validation errors
5. **No Rate Limiting** (MEDIUM) - Brute force vulnerability
6. **Insecure Data Storage** (MEDIUM) - Plain text in localStorage
7. **XSS Vulnerability** (HIGH) - Raw input display

## 📁 Project Structure

```
Login-page-testing/
├── config.py                          # Test configuration
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── .env.example                       # Environment variables template
│
├── pages/                             # Page Object Model
│   ├── __init__.py
│   └── login_page.py                  # LoginPage class with all locators
│
├── tests/                             # Test suites
│   ├── __init__.py
│   ├── base_test.py                   # Base test class
│   ├── test_boundary_values.py        # Boundary value tests (20+ tests)
│   ├── test_functional.py             # Functional tests (25+ tests)
│   ├── test_security.py               # Security tests (20+ tests)
│   └── test_performance.py            # Performance tests (8+ tests)
│
├── screenshots/                       # Auto-generated screenshots on failure
├── reports/                           # Test reports (HTML, JSON)
└── README.md                          # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Chrome/Firefox/Edge browser installed
- Git

### 2. Clone and Navigate

```bash
cd "c:\Users\lenovo\Desktop\Login-page-testing"
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your settings (optional)
notepad .env
```

Default configuration:
- BASE_URL: `https://ronit0000.github.io/Login-Page/`
- BROWSER: `chrome`
- HEADLESS: `false`

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Boundary value tests only
pytest -m boundary

# Functional tests only
pytest -m functional

# Security tests only
pytest -m security

# Performance tests only
pytest -m performance
```

### Run Specific Test Files

```bash
# Run boundary tests
pytest tests/test_boundary_values.py

# Run functional tests
pytest tests/test_functional.py

# Run security tests
pytest tests/test_security.py

# Run performance tests
pytest tests/test_performance.py
```

### Run Specific Tests

```bash
# Run a specific test
pytest tests/test_security.py::TestSecurityVulnerabilities::test_sql_injection_basic

# Run tests matching pattern
pytest -k "email"

# Run tests matching multiple patterns
pytest -k "email or password"
```

### Run with Different Browsers

```bash
# Set browser in .env file or use environment variable
set BROWSER=firefox
pytest

# Or inline
pytest --browser=firefox
```

### Run in Headless Mode

```bash
# Set in .env
set HEADLESS=true
pytest
```

### Generate Detailed Report

```bash
# HTML report (auto-generated in reports/)
pytest --html=reports/detailed_report.html

# JSON report
pytest --json-report --json-report-file=reports/test_results.json
```

### Run with Verbose Output

```bash
pytest -v

# Extra verbose
pytest -vv
```

### Run in Parallel (faster)

```bash
# Install pytest-xdist (included in requirements.txt)
pytest -n auto
```

## 📊 Test Coverage

### Boundary Value Tests (20+ tests)

- **Email Validation**: Empty, single char, missing domain, missing username, multiple @, missing TLD, valid formats
- **Password Validation**: Empty, too short, at minimum, too long, spaces only, weak passwords

### Functional Tests (25+ tests)

- **UI Tests**: Page load, element visibility, responsive design, CSS styling
- **Validation Tests**: Empty form, valid data, error messages, error clearing
- **Submission Tests**: Valid flow, invalid blocking, form reset
- **Navigation Tests**: Links, keyboard navigation, tab order
- **Input Tests**: Text input, placeholders, password hiding

### Security Tests (20+ tests)

- **SQL Injection**: Basic, OR statements, UNION, comments
- **XSS**: Script tags, event handlers, javascript:, HTML injection
- **Authentication**: Rate limiting, password visibility, data exposure
- **Storage**: localStorage security
- **Sanitization**: Special chars, Unicode, null bytes
- **Advanced**: LDAP, command injection, path traversal

### Performance Tests (8+ tests)

- Page load time
- Form submission response time
- DOM ready state
- Resource loading
- Rapid submissions
- Console errors
- Memory usage
- Input responsiveness

## 📈 Test Results

After running tests, reports are generated in the `reports/` directory:

- **reports/report.html** - Interactive HTML report with pass/fail details
- **reports/report.json** - JSON format for integration
- **screenshots/** - Screenshots of failed tests

### Viewing Reports

```bash
# Open HTML report in browser
start reports/report.html

# Or manually open in browser:
# - Navigate to Login-page-testing/reports/
# - Open report.html
```

## 🔍 Expected Test Results

Based on the documented bugs, these tests are **EXPECTED TO FAIL**:

### Boundary Value Tests
- ❌ `test_email_missing_domain` - BUG #1
- ❌ `test_email_missing_username` - BUG #1
- ❌ `test_email_multiple_at_symbols` - BUG #1
- ❌ `test_email_missing_tld` - BUG #1
- ❌ `test_single_character_password` - BUG #2
- ❌ `test_password_below_minimum` - BUG #2
- ❌ `test_password_short_weak` - BUG #2
- ❌ `test_password_above_maximum` - BUG #2
- ❌ `test_password_only_spaces` - BUG #2

### Functional Tests
- ❌ `test_invalid_submission_blocked` - BUG #4

### Security Tests
- ❌ `test_sql_injection_basic` - BUG #3
- ❌ `test_sql_injection_or_statement` - BUG #3
- ❌ `test_sql_injection_union` - BUG #3
- ❌ `test_xss_script_tag_injection` - BUG #7
- ❌ `test_xss_event_handler_injection` - BUG #7
- ❌ `test_xss_html_injection` - BUG #7
- ❌ `test_no_rate_limiting` - BUG #5
- ❌ `test_console_data_exposure` - BUG #3
- ❌ `test_insecure_localstorage` - BUG #6

**These failures document the bugs for the hackathon presentation!**

## 🎓 Test Execution Examples

### Quick Smoke Test
```bash
pytest -m "functional and ui" -v
```

### Full Security Audit
```bash
pytest -m security -v --html=reports/security_audit.html
```

### Boundary Analysis
```bash
pytest -m boundary -v --html=reports/boundary_analysis.html
```

### Email Validation Tests Only
```bash
pytest -m email -v
```

### Password Validation Tests Only
```bash
pytest -m password -v
```

## 🛠️ Troubleshooting

### WebDriver Issues

```bash
# WebDriver Manager should auto-download drivers
# If issues occur, manually update:
pip install --upgrade webdriver-manager
```

### Browser Not Found

```bash
# Make sure browser is installed
# Try different browser:
set BROWSER=firefox
pytest
```

### Tests Timeout

```bash
# Increase wait times in config.py
IMPLICIT_WAIT = 20
EXPLICIT_WAIT = 30
```

### Screenshots Not Saving

```bash
# Check config.py
SCREENSHOT_ON_FAILURE = True

# Check screenshots/ directory exists
# It will be auto-created
```

## 📝 Writing New Tests

Follow the Page Object Model pattern:

```python
from tests.base_test import BaseTest
import pytest

class TestNewFeature(BaseTest):
    
    @pytest.mark.functional
    def test_my_new_test(self):
        """Test description"""
        # Use self.login_page for interactions
        self.login_page.enter_email("test@example.com")
        self.login_page.enter_password("password")
        self.login_page.click_login()
        
        # Add assertions
        assert self.login_page.is_welcome_message_displayed()
```

## 🎯 Hackathon Presentation Tips

### Demonstration Flow:

1. **Show the Login Page**: `https://ronit0000.github.io/Login-Page/`

2. **Explain the Bugs**: Reference `BUGS.md`

3. **Run Tests Live**:
   ```bash
   # Run boundary tests with verbose output
   pytest tests/test_boundary_values.py -v
   
   # Run security tests
   pytest tests/test_security.py -v
   ```

4. **Show Test Reports**: Open `reports/report.html`

5. **Show Screenshots**: Display failed test screenshots

6. **Demonstrate Specific Bugs**:
   ```bash
   # SQL Injection test
   pytest tests/test_security.py::TestSecurityVulnerabilities::test_sql_injection_basic -v
   
   # Email validation bug
   pytest tests/test_boundary_values.py::TestBoundaryValues::test_email_missing_domain -v
   ```

## 📊 Test Metrics

Total Tests: **73+**

- Boundary Value Tests: 20
- Functional Tests: 25
- Security Tests: 20
- Performance Tests: 8

Expected Pass Rate: ~60% (intentional bugs cause failures)

## 🤝 Contributing

To add more tests:

1. Create new test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Inherit from `BaseTest` class
4. Use appropriate pytest markers
5. Document expected behavior

## 📄 License

Educational project for testing hackathon.

## 👨‍💻 Author

Created for Testing Hackathon - February 2026

---

**Remember**: The test failures are INTENTIONAL and demonstrate the bugs planted in the login page for educational purposes!

**Happy Testing! 🧪🚀**
