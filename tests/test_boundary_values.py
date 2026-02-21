"""
Boundary Value Testing - Testing edge cases and limits
Based on BUGS.md - BUG #1 (Email Validation) and BUG #2 (Password Boundary Checks)
"""
import pytest
import time
from tests.base_test import BaseTest
from config import Config


class TestBoundaryValues(BaseTest):
    """Test boundary values for email and password fields"""
    
    # =============================================
    # EMAIL BOUNDARY TESTS - BUG #1
    # =============================================
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_empty_email(self):
        """BVT-001: Test empty email submission"""
        self.login_page.enter_email("")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        error = self.login_page.get_email_error()
        assert "required" in error.lower() or error != "", \
            "Empty email should show error message"
        
        # BUG #4: Check if form actually blocked submission
        # Due to bug, welcome message may appear even with error
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Empty email accepted - Form submitted despite validation error")
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_single_character_email(self):
        """BVT-002: Test single character as email"""
        self.login_page.enter_email("a")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        error = self.login_page.get_email_error()
        # BUG: Weak validation may not catch this
        assert error != "" or not self.login_page.is_welcome_message_displayed(timeout=2), \
            "Single character email should be rejected"
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_missing_domain(self):
        """BVT-003: Test email with @ but no domain (test@)"""
        self.login_page.enter_email("test@")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #1: Weak validation only checks for @ symbol
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Email 'test@' accepted - Invalid format should be rejected")
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_missing_username(self):
        """BVT-004: Test email with @ but no username (@domain.com)"""
        self.login_page.enter_email("@domain.com")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #1: Weak validation may accept this
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Email '@domain.com' accepted - Missing username should be rejected")
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_multiple_at_symbols(self):
        """BVT-005: Test email with multiple @ symbols"""
        self.login_page.enter_email("test@@example.com")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #1: May accept multiple @ symbols
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Email 'test@@example.com' accepted - Multiple @ symbols should be rejected")
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_missing_tld(self):
        """BVT-006: Test email without TLD (user@domain)"""
        self.login_page.enter_email("user@domain")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #1: Weak validation may accept this
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Email 'user@domain' accepted - Missing TLD should be rejected")
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_valid_email_format(self):
        """BVT-007: Test valid email format"""
        self.login_page.enter_email("valid@example.com")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Valid email should be accepted
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Valid email should be accepted"
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_with_subdomain(self):
        """BVT-008: Test email with subdomain"""
        self.login_page.enter_email("user.name@subdomain.example.co.uk")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Complex but valid email should work
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Valid complex email should be accepted"
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_with_plus_sign(self):
        """BVT-009: Test email with + sign (valid character)"""
        self.login_page.enter_email("user+tag@example.com")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Plus sign is valid in email
        is_accepted = self.login_page.is_welcome_message_displayed(timeout=3)
        # May fail if validation rejects it (acceptable behavior)
        assert is_accepted, "Email with + sign should be accepted (valid per RFC)"
    
    @pytest.mark.boundary
    @pytest.mark.email
    def test_email_with_special_characters(self):
        """BVT-010: Test email with special characters"""
        special_emails = [
            "user!#$%@domain.com",
            "user..name@domain.com",
            ".user@domain.com"
        ]
        
        for email in special_emails:
            self.driver.refresh()
            time.sleep(1)
            
            self.login_page.enter_email(email)
            self.login_page.enter_password(Config.VALID_PASSWORD)
            self.login_page.click_login()
            time.sleep(1)
            
            # Most of these should be rejected
            # Documenting behavior
            is_accepted = self.login_page.is_welcome_message_displayed(timeout=2)
            print(f"Email '{email}' - Accepted: {is_accepted}")
    
    # =============================================
    # PASSWORD BOUNDARY TESTS - BUG #2
    # =============================================
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_empty_password(self):
        """BVT-011: Test empty password submission"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("")
        self.login_page.click_login()
        time.sleep(1)
        
        error = self.login_page.get_password_error()
        assert "required" in error.lower() or error != "", \
            "Empty password should show error message"
        
        # BUG #4: Check if form actually blocked submission
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Empty password accepted - Form submitted despite validation error")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_single_character_password(self):
        """BVT-012: Test single character password"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("a")
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #2: No length validation, may accept
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Single character password accepted - Should require minimum length")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_below_minimum(self):
        """BVT-013: Test password with 7 characters (below minimum of 8)"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("1234567")  # 7 characters
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #2: No minimum length check
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Password with 7 chars accepted - Should require minimum 8 characters")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_at_minimum_boundary(self):
        """BVT-014: Test password with exactly 8 characters (minimum boundary)"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("12345678")  # Exactly 8
        self.login_page.click_login()
        time.sleep(2)
        
        # Should be accepted (at minimum)
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Password with 8 characters should be accepted (minimum boundary)"
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_normal_length(self):
        """BVT-015: Test password with normal length"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("ValidPass123")  # 12 characters
        self.login_page.click_login()
        time.sleep(2)
        
        # Should be accepted
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Normal length password should be accepted"
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_short_weak(self):
        """BVT-016: Test short weak password"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("Pass1!")  # 6 characters
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #2: No length validation
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Short password (6 chars) accepted - Should require minimum 8")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_above_maximum(self):
        """BVT-017: Test password exceeding maximum length (129+ characters)"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        long_password = "A" * 129  # 129 characters
        self.login_page.enter_password(long_password)
        self.login_page.click_login()
        time.sleep(1)
        
        # BUG #2: No maximum length check
        # May accept or have browser/system limits
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Extremely long password accepted - Should have maximum limit")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_only_spaces(self):
        """BVT-018: Test password with only spaces"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("        ")  # 8 spaces
        self.login_page.click_login()
        time.sleep(1)
        
        # Should be rejected (invalid password)
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_welcome_shown:
            pytest.fail("BUG FOUND: Password with only spaces accepted - Should be rejected")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_no_numbers(self):
        """BVT-019: Test password without numbers"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password("NoNumbers!")  # 11 chars, no digits
        self.login_page.click_login()
        time.sleep(2)
        
        # BUG #2: No complexity validation
        # This will likely be accepted (bug), but depends on requirements
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=3)
        # Document the behavior
        print(f"Password without numbers - Accepted: {is_welcome_shown}")
    
    @pytest.mark.boundary
    @pytest.mark.password
    def test_password_weak_common(self):
        """BVT-020: Test weak common password"""
        weak_passwords = ["12345678", "password", "qwerty123"]
        
        for pwd in weak_passwords:
            self.driver.refresh()
            time.sleep(1)
            
            self.login_page.enter_email(Config.VALID_EMAIL)
            self.login_page.enter_password(pwd)
            self.login_page.click_login()
            time.sleep(1)
            
            # BUG #2: No strength check, will accept
            is_accepted = self.login_page.is_welcome_message_displayed(timeout=2)
            if is_accepted:
                print(f"WEAK PASSWORD ACCEPTED: '{pwd}'")
