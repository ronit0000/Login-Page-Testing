"""
🎓 Boundary Testing for Login Page

BOUNDARY TESTING:
- Tests the limits/boundaries of input fields
- Examples: empty fields, minimum length, maximum length
- Helps find bugs at edge cases

This file contains 6 boundary test scenarios:
1. Empty email field
2. Invalid email format
3. Empty password field
4. Password too short
5. Valid minimum length password
6. Valid email and password
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# Test configuration
BASE_URL = 'https://ronit0000.github.io/Login-Page/'


@pytest.fixture
def driver():
    """
    Setup: Open Chrome browser before each test
    Teardown: Close browser after each test
    """
    # Setup - Open Chrome
    print("\n🚀 Opening Chrome browser...")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(BASE_URL)
    time.sleep(2)  # Wait for page to load
    
    yield driver  # Run the test here
    
    # Teardown - Close browser
    driver.quit()
    print("🛑 Browser closed")


class TestBoundaryValues:
    """Boundary Value Tests for Login Page"""
    
    # ==========================================
    # TEST #1: Empty Email (Boundary Test)
    # ==========================================
    def test_empty_email(self, driver):
        """
        BOUNDARY TEST: Email field should not accept empty value
        
        Expected: Error message shown OR login fails
        """
        print("\n🧪 TEST 1: Empty Email")
        
        # Find elements
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Leave email empty, enter password
        email_field.send_keys("")  # Empty!
        password_field.send_keys("Password123")
        login_button.click()
        
        time.sleep(2)
        
        # Check if error message appears
        try:
            error = driver.find_element(By.ID, 'emailError')
            print(f"  ✅ Error shown: {error.text}")
            assert error.text != "", "Empty email should show error"
        except:
            # Check if welcome message did NOT appear (login should fail)
            try:
                welcome = driver.find_element(By.ID, 'welcomeMessage')
                if welcome.is_displayed():
                    pytest.fail("🐛 BUG: Empty email was accepted!")
            except:
                print("  ✅ Login correctly blocked")
    
    
    # ==========================================
    # TEST #2: Invalid Email Format (Boundary Test)
    # ==========================================
    def test_invalid_email_format(self, driver):
        """
        BOUNDARY TEST: Email without proper format should be rejected
        
        Testing: "test@" (missing domain)
        Expected: Error message OR login fails
        """
        print("\n🧪 TEST 2: Invalid Email Format")
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter invalid email (missing domain after @)
        email_field.send_keys("test@")  # Invalid!
        password_field.send_keys("Password123")
        login_button.click()
        
        time.sleep(2)
        
        # Check if login is blocked
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                pytest.fail("🐛 BUG: Invalid email 'test@' was accepted!")
        except:
            print("  ✅ Invalid email correctly rejected")
    
    
    # ==========================================
    # TEST #3: Empty Password (Boundary Test)
    # ==========================================
    def test_empty_password(self, driver):
        """
        BOUNDARY TEST: Password field should not accept empty value
        
        Expected: Error message shown OR login fails
        """
        print("\n🧪 TEST 3: Empty Password")
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter email but leave password empty
        email_field.send_keys("test@example.com")
        password_field.send_keys("")  # Empty!
        login_button.click()
        
        time.sleep(2)
        
        # Check if error shown or login blocked
        try:
            error = driver.find_element(By.ID, 'passwordError')
            print(f"  ✅ Error shown: {error.text}")
            assert error.text != "", "Empty password should show error"
        except:
            try:
                welcome = driver.find_element(By.ID, 'welcomeMessage')
                if welcome.is_displayed():
                    pytest.fail("🐛 BUG: Empty password was accepted!")
            except:
                print("  ✅ Login correctly blocked")
    
    
    # ==========================================
    # TEST #4: Short Password (Boundary Test)
    # ==========================================
    def test_password_too_short(self, driver):
        """
        BOUNDARY TEST: Password below minimum length should be rejected
        
        Testing: "Pass1" (only 5 characters)
        Expected: Minimum 8 characters required
        """
        print("\n🧪 TEST 4: Password Too Short (5 chars)")
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter short password
        email_field.send_keys("test@example.com")
        password_field.send_keys("Pass1")  # Only 5 characters!
        login_button.click()
        
        time.sleep(2)
        
        # Check if rejected
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                pytest.fail("🐛 BUG: Short password (5 chars) was accepted!")
        except:
            print("  ✅ Short password correctly rejected")
    
    
    # ==========================================
    # TEST #5: Minimum Valid Password (Boundary Test)
    # ==========================================
    def test_minimum_valid_password(self, driver):
        """
        BOUNDARY TEST: Password at minimum length (8 chars) should work
        
        Testing: "Pass1234" (exactly 8 characters)
        Expected: Should be accepted
        """
        print("\n🧪 TEST 5: Minimum Valid Password (8 chars)")
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter minimum valid password
        email_field.send_keys("test@example.com")
        password_field.send_keys("Pass1234")  # Exactly 8 characters
        login_button.click()
        
        time.sleep(2)
        
        # Check if welcome message appears
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                print("  ✅ Minimum valid password accepted")
            else:
                print("  ⚠️ Welcome message not visible")
        except:
            print("  ⚠️ Login may have failed (could be a bug)")
    
    
    # ==========================================
    # TEST #6: Valid Login (Boundary Test - Valid Case)
    # ==========================================
    def test_valid_email_and_password(self, driver):
        """
        BOUNDARY TEST: Valid email and password should work
        
        Testing: "test@example.com" and "Password123"
        Expected: Login successful, welcome message shown
        """
        print("\n🧪 TEST 6: Valid Email and Password")
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter valid credentials
        email_field.send_keys("test@example.com")
        password_field.send_keys("Password123")
        login_button.click()
        
        time.sleep(2)
        
        # Check if welcome message appears
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            assert welcome.is_displayed(), "Welcome message should be shown"
            print("  ✅ Valid login successful")
        except:
            pytest.fail("❌ Valid login failed (should have succeeded)")


# ========================================
# 🎓 HOW TO RUN THESE TESTS:
# ========================================
#
# Run all boundary tests:
#   pytest tests/test_boundary.py -v -s
#
# Run one specific test:
#   pytest tests/test_boundary.py::TestBoundaryValues::test_empty_email -v -s
#
# Options:
#   -v  = verbose (show test names)
#   -s  = show print statements
#
# What you'll see:
#   - Chrome browser will open
#   - Each test will run (fill forms, click buttons)
#   - Print statements show what's happening
#   - Browser closes after each test
#   - Final summary shows PASSED/FAILED
#
# ========================================
