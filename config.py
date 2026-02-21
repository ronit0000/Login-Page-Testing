"""
Configuration file for test settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Test configuration settings"""
    
    # Base URL
    BASE_URL = os.getenv('BASE_URL', 'https://ronit0000.github.io/Login-Page/')
    
    # Browser settings
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    # Wait times
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 20))
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    SCREENSHOT_DIR = 'screenshots'
    
    # Report settings
    REPORT_DIR = 'reports'
    
    # Test data
    VALID_EMAIL = 'test@example.com'
    VALID_PASSWORD = 'ValidPass123!'
    
    # Boundary values
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 128
    
    # Performance thresholds
    PAGE_LOAD_THRESHOLD = 3  # seconds
    FORM_SUBMIT_THRESHOLD = 2  # seconds
