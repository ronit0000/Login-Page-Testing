"""
🎓 BEGINNER-FRIENDLY: Test Configuration

WHAT IS THIS FILE?
- This file stores all settings in ONE place
- Instead of writing the URL 50 times, we write it once here!
- When URL changes, update it here and ALL tests automatically use the new URL

This is called a "Configuration Class" or "Config"
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()


class Config:
    """
    Configuration settings for all tests
    
    All values can be changed here without touching test files!
    """
    
    # ========================================
    # 🌐 Website URL
    # ========================================
    # The login page we're testing
    BASE_URL = os.getenv('BASE_URL', 'https://ronit0000.github.io/Login-Page/')
    
    # ========================================
    # 🌐 Browser Settings
    # ========================================
    # Which browser to use? Options: 'chrome', 'firefox', 'edge'
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    
    # Run tests without showing browser window? (faster but can't watch)
    # False = Show browser (good for learning!)
    # True = Hide browser (good for speed)
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    # ========================================
    # ⏱️ Wait Times (in seconds)
    # ========================================
    # How long to wait for elements to appear
    # If page is slow, increase these numbers
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))   # Default wait
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 20))   # Longer wait for slow elements
    
    # ========================================
    # 📸 Screenshot Settings
    # ========================================
    # Take screenshot when test fails? (helps debugging!)
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    
    # Where to save screenshots
    SCREENSHOT_DIR = 'screenshots'
    
    # ========================================
    # 📊 Report Settings
    # ========================================
    # Where to save test reports
    REPORT_DIR = 'reports'
    
    # ========================================
    # 🧪 Test Data (Default values for testing)
    # ========================================
    # Valid credentials that should work
    VALID_EMAIL = 'test@example.com'
    VALID_PASSWORD = 'ValidPass123!'
    
    # Password length rules
    PASSWORD_MIN_LENGTH = 8       # Minimum 8 characters
    PASSWORD_MAX_LENGTH = 128     # Maximum 128 characters
    
    # ========================================
    # ⚡ Performance Thresholds
    # ========================================
    # How fast should the page be? (in seconds)
    PAGE_LOAD_THRESHOLD = 3       # Page should load in under 3 seconds
    FORM_SUBMIT_THRESHOLD = 2     # Form should submit in under 2 seconds


# ========================================
# 🎓 LEARNING NOTES:
# ========================================
#
# How to use Config in tests?
#   from config import Config
#   print(Config.BASE_URL)          # Access setting like this
#
# Why use os.getenv()?
#   - Allows overriding settings without changing code
#   - Create a .env file with: BASE_URL=http://localhost:3000
#   - Useful for different environments (dev, staging, production)
#
# How to change settings?
#   Option 1: Edit this file directly
#   Option 2: Create a .env file (see .env.example)
#
# Common changes beginners make:
#   - Change BASE_URL to test different website
#   - Set HEADLESS = True to run tests faster (but not see browser)
#   - Increase IMPLICIT_WAIT if page is slow
#
# ========================================
