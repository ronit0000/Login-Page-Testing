# 🧪 Boundary Testing - Login Page

Simple boundary testing project using **Selenium WebDriver** and **Python pytest**.

## 🎯 What This Tests

Tests boundary conditions for a login form at: https://ronit0000.github.io/Login-Page/

**6 Test Scenarios:**
1. ✅ Empty email field
2. ✅ Invalid email format (test@)
3. ✅ Empty password field
4. ✅ Password too short (5 chars)
5. ✅ Minimum valid password (8 chars)
6. ✅ Valid email and password

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
**Windows:**
```bash
run_tests.bat
```

**Mac/Linux:**
```bash
pytest tests/test_boundary.py -v -s
```

## 📁 Project Structure

```
Login-page-testing/
├── tests/
│   ├── __init__.py
│   └── test_boundary.py       # 6 boundary tests
├── requirements.txt           # selenium, pytest, webdriver-manager
├── run_tests.bat             # Easy test runner (Windows)
└── README.md                 # This file
```

## 💻 Test Output

Tests show **text output only** - no HTML reports!

```
🧪 TEST 1: Empty Email
  ✅ Error shown: Email is required

🧪 TEST 2: Invalid Email Format
  ✅ Invalid email correctly rejected

...

============== 6 passed in 45.23s ==============
```

## 📖 What You'll Learn

- Selenium WebDriver basics
- Finding elements (By.ID, By.CSS_SELECTOR)
- Boundary testing concepts
- pytest fixtures (setup/teardown)
- Text-based test reporting

## 🛠️ Technologies

- **Python 3.x** - Programming language
- **Selenium** - Browser automation
- **pytest** - Testing framework
- **webdriver-manager** - Auto-downloads ChromeDriver
- **Chrome** - Browser for testing

## 🎓 For Beginners

This is a minimal, easy-to-understand testing project:
- ✅ Only 6 test cases
- ✅ Direct Selenium WebDriver (no Page Object Model)
- ✅ Text output only (no complex HTML reports)
- ✅ Clear comments explaining everything

Perfect for learning boundary testing basics!

## 📝 License

Free to use for learning!

---

**Simple** ✨ **Easy to understand** 📚 **Boundary testing** 🎯
