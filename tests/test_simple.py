"""
🎓 BEGINNER-FRIENDLY: Simple Login Page Tests

This file contains easy-to-understand tests for the login page.
Each test checks ONE specific thing about the login functionality.

WHAT IS A TEST?
- A test is a function that checks if something works correctly
- If the check passes ✅ = test passes
- If the check fails ❌ = test fails (we found a bug!)

HOW TO READ A TEST:
1. Look at the function name - it tells you what's being tested
2. Read the comments - they explain each step
3. Look at assert statements - these are the actual checks
"""

import pytest
import time
from tests.base_test import BaseTest


class TestLoginPage(BaseTest):
    """
    A collection of tests for the Login Page
    Each method (function) starting with 'test_' is one test
    """
    
    # ==========================================
    # TEST #1: Check if the page loads
    # ==========================================
    def test_page_loads_successfully(self):
        """
        Test that the login page opens without errors
        
        Steps:
        1. Open the page (already done by BaseTest setup)
        2. Check if the page title is correct
        
        If this fails, something is very wrong with the page!
        """
        # Get the page title from browser
        title = self.login_page.get_page_title()
        
        # Check if "Login" is in the title
        # assert means "this MUST be True, or the test fails"
        assert "Login" in title, f"Expected 'Login' in title, but got: {title}"
        
        print("✅ Page loaded successfully!")
    
    
    # ==========================================
    # TEST #2: Valid login should work
    # ==========================================
    def test_valid_login(self):
        """
        Test that login works with correct email and password
        
        Steps:
        1. Enter valid email
        2. Enter valid password
        3. Click login button
        4. Check if welcome message appears
        """
        # Perform login with valid credentials
        self.login_page.do_login("test@example.com", "Password123")
        
        # Wait a moment for welcome message to appear
        time.sleep(2)
        
        # Check if welcome message is shown (means login succeeded)
        is_welcome_shown = self.login_page.is_welcome_message_shown()
        
        assert is_welcome_shown, "Login failed! Welcome message not shown"
        print("✅ Valid login works correctly!")
    
    
    # ==========================================
    # TEST #3: Empty email should show error
    # ==========================================
    def test_empty_email_shows_error(self):
        """
        🐛 BUG TEST: Empty email should be rejected
        
        This tests BUG #1 (Email Validation Issues)
        
        Steps:
        1. Leave email empty
        2. Enter password
        3. Click login
        4. Check if error message appears
        """
        # Try to login with empty email
        self.login_page.enter_email("")  # Empty!
        self.login_page.enter_password("Password123")
        self.login_page.click_login_button()
        
        # Wait for validation
        time.sleep(1)
        
        # Get the error message
        error = self.login_page.get_email_error_message()
        
        # Check if error message exists
        # The bug is: email validation is too weak, so it might not show error!
        assert error != "", "BUG FOUND: No error shown for empty email!"
        assert "required" in error.lower(), f"Expected 'required' in error, got: {error}"
        
        print(f"✅ Error message shown: {error}")
    
    
    # ==========================================
    # TEST #4: Invalid email format should fail
    # ==========================================
    def test_invalid_email_format(self):
        """
        🐛 BUG TEST: Email without @ symbol should be rejected
        
        This tests BUG #1 (Email Validation Issues)
        
        The bug: Our validation only checks for @ symbol
        So "test@" is accepted (missing domain)
        """
        # Try to login with incomplete email (missing domain)
        self.login_page.enter_email("test@")  # Invalid: missing domain after @
        self.login_page.enter_password("Password123")
        self.login_page.click_login_button()
        
        time.sleep(1)
        
        # Check if error is shown OR welcome message is NOT shown
        error = self.login_page.get_email_error_message()
        welcome_shown = self.login_page.is_welcome_message_shown()
        
        # At least ONE of these should be true:
        # - Error message exists
        # - Welcome message is NOT shown
        if welcome_shown and error == "":
            pytest.fail("🐛 BUG FOUND: Invalid email 'test@' was accepted!")
        
        print("✅ Invalid email rejected correctly")
    
    
    # ==========================================
    # TEST #5: Empty password should show error
    # ==========================================
    def test_empty_password_shows_error(self):
        """
        🐛 BUG TEST: Empty password should be rejected
        
        This tests BUG #2 (Password Validation Issues)
        
        The bug: validatePassword() always returns true
        So empty passwords are accepted!
        """
        # Try to login with empty password
        self.login_page.enter_email("test@example.com")
        self.login_page.enter_password("")  # Empty password!
        self.login_page.click_login_button()
        
        time.sleep(1)
        
        # Check for error message
        error = self.login_page.get_password_error_message()
        welcome_shown = self.login_page.is_welcome_message_shown()
        
        # Should show error OR not show welcome
        if welcome_shown:
            pytest.fail("🐛 BUG FOUND: Empty password was accepted!")
        
        if error == "":
            pytest.fail("🐛 BUG FOUND: No error message for empty password!")
        
        print(f"✅ Password error shown: {error}")
    
    
    # ==========================================
    # TEST #6: Short password should be rejected
    # ==========================================
    def test_short_password_rejected(self):
        """
        🐛 BUG TEST: Password shorter than 8 characters should fail
        
        This tests BUG #2 (Password Validation Issues)
        """
        # Try password with only 5 characters (too short)
        self.login_page.enter_email("test@example.com")
        self.login_page.enter_password("Pass1")  # Only 5 chars!
        self.login_page.click_login_button()
        
        time.sleep(1)
        
        error = self.login_page.get_password_error_message()
        welcome_shown = self.login_page.is_welcome_message_shown()
        
        if welcome_shown:
            pytest.fail("🐛 BUG FOUND: Short password (5 chars) was accepted!")
        
        print("✅ Short password rejected correctly")
    
    
    # ==========================================
    # TEST #7: SQL Injection attempt
    # ==========================================
    def test_sql_injection_blocked(self):
        """
        🐛 SECURITY TEST: SQL injection should be blocked
        
        This tests BUG #3 (No Input Sanitization)
        
        SQL Injection is a hacking technique where attacker puts
        SQL code in input fields to break the application
        
        Example: admin'-- tries to bypass login
        """
        # Try a common SQL injection attack
        self.login_page.enter_email("admin'--")  # SQL injection attempt!
        self.login_page.enter_password("anything")
        self.login_page.click_login_button()
        
        time.sleep(1)
        
        # Login should NOT succeed with SQL injection
        welcome_shown = self.login_page.is_welcome_message_shown()
        
        if welcome_shown:
            pytest.fail("🐛 SECURITY BUG: SQL injection was not blocked!")
        
        print("✅ SQL injection blocked successfully")


# ========================================
# 🎓 LEARNING NOTES - HOW TO RUN TESTS:
# ========================================
#
# Run ALL tests in this file:
#   pytest tests/test_simple.py -v
#
# Run ONE specific test:
#   pytest tests/test_simple.py::TestLoginPage::test_page_loads_successfully -v
#
# What does -v mean?
#   -v = verbose (shows more details about what's running)
#
# Understanding test results:
#   PASSED = ✅ Test succeeded (feature works correctly)
#   FAILED = ❌ Test failed (BUG FOUND!)
#
# Common pytest commands:
#   pytest tests/test_simple.py -v                    # Run all tests, verbose output
#   pytest tests/test_simple.py -k "email"            # Run only tests with "email" in name
#   pytest tests/test_simple.py --tb=short            # Show shorter error messages
#   pytest tests/test_simple.py -s                    # Show print statements
#   pytest tests/test_simple.py -x                    # Stop after first failure
#
# ========================================
# 🎯 WHAT YOU LEARNED:
# ========================================
# 1. How to write a test function
# 2. How to use the LoginPage class in tests
# 3. What assert statements do
# 4. How to check for bugs with pytest.fail()
# 5. Basic Selenium actions (enter text, click button)
#
# Next step: Try modifying these tests or writing your own!
# ========================================
