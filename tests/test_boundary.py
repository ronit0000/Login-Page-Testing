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
        print("\n" + "="*60)
        print("🧪 TEST 1: Empty Email (Boundary Test)")
        print("="*60)
        print("  📝 Input: Email = '' (empty), Password = 'Password123'")
        print("  ⚠️  Expected: Should show error OR block login")
        print()
        
        # Find elements
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Leave email empty, enter password
        email_field.send_keys("")  # Empty!
        password_field.send_keys("Password123")
        login_button.click()
        
        time.sleep(2)
        
        # Check what actually happened
        error_shown = False
        error_text = ""
        login_succeeded = False
        welcome_text = ""
        
        # Check for error message
        try:
            error = driver.find_element(By.ID, 'emailError')
            error_text = error.text.strip()
            if error_text:
                error_shown = True
        except:
            pass
        
        # Check if login succeeded
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                welcome_text = welcome.text.strip()
                login_succeeded = True
        except:
            pass
        
        # Report what happened
        print("  📊 ACTUAL RESULT:")
        if error_shown:
            print(f"     ├─ Error Message: '{error_text}'")
        else:
            print(f"     ├─ Error Message: (none)")
        
        if login_succeeded:
            print(f"     └─ Login Status: ✅ SUCCESS - '{welcome_text}'")
        else:
            print(f"     └─ Login Status: ❌ BLOCKED")
        
        print()
        
        # Determine if behavior is correct
        if login_succeeded:
            print("  🐛 BUG DETECTED: Empty email was accepted and login succeeded!")
            print("  ❌ TEST RESULT: FAIL - Boundary not enforced")
            pytest.fail("🐛 BUG: Empty email should be rejected but login succeeded!")
        elif error_shown:
            print(f"  ✅ CORRECT: Error message shown and login blocked")
            print("  ✅ TEST RESULT: PASS - Boundary properly enforced")
        else:
            print(f"  ⚠️  WARNING: Login blocked but no error message shown")
            print("  ✅ TEST RESULT: PASS - Boundary enforced (but UX could be better)")
    
    
    # ==========================================
    # TEST #2: Invalid Email Format (Boundary Test)
    # ==========================================
    def test_invalid_email_format(self, driver):
        """
        BOUNDARY TEST: Email without proper format should be rejected
        
        Testing: "test@" (missing domain)
        Expected: Error message OR login fails
        """
        print("\n" + "="*60)
        print("🧪 TEST 2: Invalid Email Format (Boundary Test)")
        print("="*60)
        print("  📝 Input: Email = 'test@' (missing domain), Password = 'Password123'")
        print("  ⚠️  Expected: Should show error OR block login")
        print()
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter invalid email
        email_field.send_keys("test@")
        password_field.send_keys("Password123")
        login_button.click()
        
        time.sleep(2)
        
        # Check what actually happened
        error_shown = False
        error_text = ""
        login_succeeded = False
        welcome_text = ""
        
        try:
            error = driver.find_element(By.ID, 'emailError')
            error_text = error.text.strip()
            if error_text:
                error_shown = True
        except:
            pass
        
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                welcome_text = welcome.text.strip()
                login_succeeded = True
        except:
            pass
        
        # Report results
        print("  " + "="*60)
        print("🧪 TEST 3: Empty Password (Boundary Test)")
        print("="*60)
        print("  📝 Input: Email = 'test@example.com', Password = '' (empty)")
        print("  ⚠️  Expected: Should show error OR block login")
        print()
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter email but leave password empty
        email_field.send_keys("test@example.com")
        password_field.send_keys("")
        login_button.click()
        
        time.sleep(2)
        
        # Check what actually happened
        error_shown = False
        error_text = ""
        login_succeeded = False
        welcome_text = ""
        
        try:
            error = driver.find_element(By.ID, 'passwordError')
            error_text = error.text.strip()
            if error_text:
                error_shown = True
        except:
            pass
        
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                welcome_text = welcome.text.strip()
                login_succeeded = True
        except:
            pass
        
        # Report results
        print("  📊 ACTUAL RESULT:")
        if error_shown:
            print(f"     ├─ Error Message: '{error_text}'")
        else:
            print(f"     ├─ Error Message: (none)")
        
        if login_succeeded:
            print(f"     └─ Login Status: ✅ SUCCESS - '{welcome_text}'")
        else:
            print(f"     └─ Login Status: ❌ BLOCKED")
        
        print()
        
        if login_succeeded:
            print("  🐛 BUG DETECTED: Empty password was accepted and login succeeded!")
            print("  ❌ TEST RESULT: FAIL - Boundary not enforced")
            pytest.fail("🐛 BUG: Empty password should be rejected!")
        elif error_shown:
            print(f"  ✅ CORRECT: Error message shown and login blocked")
            print("  ✅ TEST RESULT: PASS - Boundary properly enforced")
        else:
            print(f"  ⚠️  WARNING: Login blocked but no error message shown")
            print("  ✅ TEST RESULT: PASS - Boundary enforced (but UX could be better)
        print("  📝 Testing: Submitting form with empty password field")
        
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
            error_text = error.text
            print" + "="*60)
        print("🧪 TEST 4: Password Too Short (Boundary Test)")
        print("="*60)
        print("  📝 Input: Email = 'test@example.com', Password = 'Pass1' (5 chars)")
        print("  ⚠️  Expected: Should reject (minimum 8 characters)")
        print()
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter short password
        email_field.send_keys("test@example.com")
        password_field.send_keys("Pass1")
        login_button.click()
        
        time.sleep(2)
        
        # Check what actually happened
        error_shown = False
        error_text = ""
        login_succeeded = False
        welcome_text = ""
        
        try:
            error = driver.find_element(By.ID, 'passwordError')
            error_text = error.text.strip()
            if error_text:
                error_shown = True
        except:
            pass
        
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                welcome_text = welcome.text.strip()
                login_succeeded = True
        except:
            pass
        
        # Report results
        print("  📊 ACTUAL RESULT:")
        if error_" + "="*60)
        print("🧪 TEST 5: Minimum Valid Password (Boundary Test)")
        print("="*60)
        print("  📝 Input: Email = 'test@example.com', Password = 'Pass1234' (8 chars)")
        print("  ✅ Expected: Should ACCEPT (minimum valid length)")
        print()
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter minimum valid password
        email_field.send_keys("test@example.com")
        password_field.send_keys("Pass1234")
        login_button.click()
        
        time.sleep(2)
        
        # Check what actually happened
        error_shown = False
        error_text = ""
        login_succeeded = False
        welcome_text = ""
        
        try:
            error = driver.find_element(By.ID, 'passwordError')
            error_text = error.text.strip()
            if error_text:
                error_shown = True
        except:
            pass
        
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                welcome_text = welcome.text.strip()
                login_succeeded = True
        except:
            pass
        
        # Report results
        print("  📊 ACTUAL RESULT:")
        if error_shown:
            print(f"     ├─ Error Message: '{error_text}'")
        else:
            print(f"     ├─ Error Message: (none)")
        
        if login_succeeded:
            print(f"     └─ Login Status: ✅ SUCCESS - '{welcome_text}'")
        else:
            print(f"     └─ Login Status: ❌ BLOCKED")
        
        print()
        
        if login_succeeded and not error_shown:
            print("  ✅ CORRECT: 8-character password accepted (minimum valid)")
            print("  ✅ TEST RESULT: PASS - Boundary properly enforced")
        elif not login_succeeded:
            print("  🐛 BUG DETECTED: Valid 8-character password was rejected!")
            print("  ❌ TEST RESULT: FAIL - Valid input rejected")
            pytest.fail("🐛 BUG: 8-character password should be accepted!")
        else:
            print("  ⚠️  WARNING: Login succeeded but error shown?")
            print("  ✅ TEST RESULT: PASS - But UX is confusing
        # Enter short password
        email_field.send_keys("test@example.com")
        password_field.send_keys("Pass1")  # Only 5 characters!
        login_button.click()
        
        time.slee" + "="*60)
        print("🧪 TEST 6: Valid Email and Password (Control Test)")
        print("="*60)
        print("  📝 Input: Email = 'test@example.com', Password = 'Password123'")
        print("  ✅ Expected: Should ACCEPT (all requirements met)")
        print()
        
        email_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        
        # Enter valid credentials
        email_field.send_keys("test@example.com")
        password_field.send_keys("Password123")
        login_button.click()
        
        time.sleep(2)
        
        # Check what actually happened
        error_shown = False
        error_text = ""
        login_succeeded = False
        welcome_text = ""
        
        try:
            error = driver.find_element(By.ID, 'emailError')
            error_text = error.text.strip()
            if error_text:
                error_shown = True
        except:
            pass
        
        if not error_shown:
            try:
                error = driver.find_element(By.ID, 'passwordError')
                error_text = error.text.strip()
                if error_text:
                    error_shown = True
            except:
                pass
        
        try:
            welcome = driver.find_element(By.ID, 'welcomeMessage')
            if welcome.is_displayed():
                welcome_text = welcome.text.strip()
                login_succeeded = True
        except:
            pass
        
        # Report results
        print("  📊 ACTUAL RESULT:")
        if error_shown:
            print(f"     ├─ Error Message: '{error_text}'")
        else:
            print(f"     ├─ Error Message: (none)")
        
        if login_succeeded:
            print(f"     └─ Login Status: ✅ SUCCESS - '{welcome_text}'")
        else:
            print(f"     └─ Login Status: ❌ BLOCKED")
        
        print()
        
        if login_succeeded and not error_shown:
            print("  ✅ CORRECT: Valid credentials accepted")
            print("  ✅ TEST RESULT: PASS - System working properly")
        elif not login_succeeded:
            print("  🐛 BUG DETECTED: Valid credentials were rejected!")
            print("  ❌ TEST RESULT: FAIL - Valid login blocked")
            pytest.fail("🐛 BUG: Valid credentials should be accepted!")
        else:
            print("  ⚠️  WARNING: Login succeeded but error also shown?")
            print("  ⚠️  TEST RESULT: PASS - But UX is confusing
        Expected: Should be accepted
        """
        print("\n🧪 TEST 5: Minimum Valid Password (8 chars)")
        print("  📝 Testing: Submitting 'Pass1234' (exactly 8 characters)")
        
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
                welcome_text = welcome.text
                print(f"  📌 Welcome Message: '{welcome_text}'")
                print("  ✅ PASS: Minimum valid password accepted")
                assert True
            else:
                print("  ⚠️ Welcome message element found but not visible")
                pytest.fail("Welcome message not visible")
        except:
            print("  ❌ Login failed - welcome message not found")
            pytest.fail("Login should have succeeded with 8-char password")
    
    
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
        print("  📝 Testing: Submitting valid credentials")
        
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
            welcome_text = welcome.text
            print(f"  📌 Welcome Message: '{welcome_text}'")
            
            if welcome.is_displayed():
                print("  ✅ PASS: Valid login successful")
                assert True
            else:
                pytest.fail("Welcome message found but not visible")
        except Exception as e:
            print("  ❌ Login failed - welcome message not found")
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
