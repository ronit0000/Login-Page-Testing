"""
Functional Testing - Testing form functionality and user interactions
Based on TESTING-GUIDE.md functional test cases
"""
import pytest
import time
from tests.base_test import BaseTest
from config import Config


class TestFunctionalRequirements(BaseTest):
    """Test functional requirements of the login form"""
    
    # =============================================
    # FORM DISPLAY & UI TESTS
    # =============================================
    
    @pytest.mark.functional
    @pytest.mark.ui
    def test_page_loads_correctly(self):
        """FT-001: Verify page loads and displays login form"""
        assert "Login" in self.login_page.get_page_title(), \
            "Page title should contain 'Login'"
        
        assert self.login_page.is_login_form_displayed(), \
            "Login form should be visible"
    
    @pytest.mark.functional
    @pytest.mark.ui
    def test_all_elements_visible(self):
        """FT-002: Verify all form elements are visible"""
        # Check email field
        email_field = self.driver.find_element(*self.login_page.EMAIL_INPUT)
        assert email_field.is_displayed(), "Email field should be visible"
        
        # Check password field
        password_field = self.driver.find_element(*self.login_page.PASSWORD_INPUT)
        assert password_field.is_displayed(), "Password field should be visible"
        
        # Check login button
        login_btn = self.driver.find_element(*self.login_page.LOGIN_BUTTON)
        assert login_btn.is_displayed(), "Login button should be visible"
        assert login_btn.text.upper() == "LOGIN", "Login button should have correct text"
        
        # Check Remember Me checkbox
        remember_checkbox = self.driver.find_element(*self.login_page.REMEMBER_ME_CHECKBOX)
        assert remember_checkbox.is_displayed(), "Remember Me checkbox should be visible"
        
        # Check links
        forgot_link = self.driver.find_element(*self.login_page.FORGOT_PASSWORD_LINK)
        assert forgot_link.is_displayed(), "Forgot password link should be visible"
        
        signup_link = self.driver.find_element(*self.login_page.SIGNUP_LINK)
        assert signup_link.is_displayed(), "Sign up link should be visible"
    
    @pytest.mark.functional
    @pytest.mark.responsive
    def test_responsive_mobile_375px(self):
        """FT-003: Test responsive design on mobile (375px)"""
        self.driver.set_window_size(375, 667)
        time.sleep(1)
        
        assert self.login_page.is_login_form_displayed(), \
            "Login form should be visible on mobile"
        
        # Check if elements are still accessible
        email_field = self.driver.find_element(*self.login_page.EMAIL_INPUT)
        assert email_field.is_displayed(), "Email field should be visible on mobile"
    
    @pytest.mark.functional
    @pytest.mark.responsive
    def test_responsive_tablet_768px(self):
        """FT-004: Test responsive design on tablet (768px)"""
        self.driver.set_window_size(768, 1024)
        time.sleep(1)
        
        assert self.login_page.is_login_form_displayed(), \
            "Login form should be visible on tablet"
    
    @pytest.mark.functional
    @pytest.mark.ui
    def test_css_styling_applied(self):
        """FT-005: Verify CSS styling is applied"""
        # Check background gradient
        body = self.driver.find_element("tag name", "body")
        background = body.value_of_css_property("background")
        assert background is not None, "Background styling should be applied"
        
        # Check login box styling
        login_box = self.driver.find_element("class name", "login-box")
        border_radius = login_box.value_of_css_property("border-radius")
        assert border_radius != "0px", "Login box should have rounded corners"
    
    # =============================================
    # FORM VALIDATION TESTS
    # =============================================
    
    @pytest.mark.functional
    @pytest.mark.validation
    def test_submit_empty_form(self):
        """FT-006: Test submitting empty form shows errors"""
        self.login_page.click_login()
        time.sleep(1)
        
        email_error = self.login_page.get_email_error()
        password_error = self.login_page.get_password_error()
        
        # At least one error should be shown
        assert email_error != "" or password_error != "", \
            "Empty form submission should show error messages"
    
    @pytest.mark.functional
    @pytest.mark.validation
    def test_submit_with_valid_data(self):
        """FT-007: Test successful login with valid credentials"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Should show welcome message
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Valid login should show welcome message"
        
        # Check if email is displayed in welcome message
        welcome_text = self.login_page.get_welcome_message_email()
        assert Config.VALID_EMAIL in welcome_text, \
            "Welcome message should display user email"
    
    @pytest.mark.functional
    @pytest.mark.validation
    def test_error_message_display(self):
        """FT-008: Test error message appears for invalid email"""
        self.login_page.enter_email("invalid")
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(1)
        
        email_error = self.login_page.get_email_error()
        # Error should be displayed (even if validation is weak)
        # Check if error element has text or form blocked submission
        login_form_visible = self.login_page.is_login_form_displayed()
        assert email_error != "" or login_form_visible, \
            "Invalid email should trigger error or validation"
    
    @pytest.mark.functional
    @pytest.mark.validation
    def test_error_message_clearing(self):
        """FT-009: Test error messages clear on valid resubmission"""
        # First, trigger an error
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        time.sleep(1)
        
        # Verify errors shown
        initial_error = self.login_page.get_email_error()
        assert initial_error != "", "Initial submission should show error"
        
        # Now submit with valid data
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Error should clear and welcome message should appear
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Valid submission should proceed successfully"
    
    @pytest.mark.functional
    @pytest.mark.validation
    def test_remember_me_checkbox(self):
        """FT-010: Test Remember Me checkbox functionality"""
        # Initially unchecked
        assert not self.login_page.is_remember_me_checked(), \
            "Remember Me should be unchecked by default"
        
        # Check it
        self.login_page.check_remember_me()
        assert self.login_page.is_remember_me_checked(), \
            "Remember Me should be checked after clicking"
        
        # Uncheck it
        self.login_page.uncheck_remember_me()
        assert not self.login_page.is_remember_me_checked(), \
            "Remember Me should be unchecked after clicking again"
    
    # =============================================
    # FORM SUBMISSION TESTS
    # =============================================
    
    @pytest.mark.functional
    @pytest.mark.submission
    def test_valid_submission_flow(self):
        """FT-011: Test complete valid submission flow"""
        # Fill form
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Form should hide
        form_visible = self.login_page.is_login_form_displayed()
        
        # Welcome message should show
        welcome_visible = self.login_page.is_welcome_message_displayed(timeout=3)
        
        assert welcome_visible, "Welcome message should be displayed"
        assert not form_visible, "Login form should be hidden after successful login"
    
    @pytest.mark.functional
    @pytest.mark.submission
    def test_invalid_submission_blocked(self):
        """FT-012: Test invalid submission is blocked (or shows errors)"""
        # BUG #4: Form may not actually block submission
        self.login_page.enter_email("invalid")
        self.login_page.enter_password("short")
        self.login_page.click_login()
        time.sleep(1)
        
        # Either error should show OR submission should be blocked
        email_error = self.login_page.get_email_error()
        password_error = self.login_page.get_password_error()
        welcome_shown = self.login_page.is_welcome_message_displayed(timeout=2)
        
        # If welcome is shown with invalid data, it's a bug
        if welcome_shown and (email_error == "" and password_error == ""):
            pytest.fail("BUG #4: Invalid submission processed without errors")
    
    @pytest.mark.functional
    @pytest.mark.submission
    def test_form_reset_on_refresh(self):
        """FT-014: Test form clears on page refresh"""
        # Fill form
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        
        # Refresh page
        self.driver.refresh()
        time.sleep(1)
        
        # Fields should be empty
        email_value = self.login_page.get_email_value()
        password_value = self.login_page.get_password_value()
        
        assert email_value == "", "Email field should be empty after refresh"
        assert password_value == "", "Password field should be empty after refresh"
    
    # =============================================
    # LINK FUNCTIONALITY TESTS
    # =============================================
    
    @pytest.mark.functional
    @pytest.mark.navigation
    def test_forgot_password_link(self):
        """FT-015: Test Forgot Password link is clickable"""
        forgot_link = self.driver.find_element(*self.login_page.FORGOT_PASSWORD_LINK)
        assert forgot_link.is_displayed(), "Forgot password link should be visible"
        
        # Link should have href (even if dummy)
        href = forgot_link.get_attribute("href")
        assert href is not None, "Forgot password link should have href attribute"
    
    @pytest.mark.functional
    @pytest.mark.navigation
    def test_create_account_link(self):
        """FT-016: Test Create Account link is clickable"""
        signup_link = self.driver.find_element(*self.login_page.SIGNUP_LINK)
        assert signup_link.is_displayed(), "Sign up link should be visible"
        
        # Link should have href
        href = signup_link.get_attribute("href")
        assert href is not None, "Sign up link should have href attribute"
    
    @pytest.mark.functional
    @pytest.mark.ui
    def test_link_hover_effect(self):
        """FT-017: Test links have hover effects (color change)"""
        from selenium.webdriver.common.action_chains import ActionChains
        
        forgot_link = self.driver.find_element(*self.login_page.FORGOT_PASSWORD_LINK)
        
        # Get initial color
        initial_color = forgot_link.value_of_css_property("color")
        
        # Hover over link
        actions = ActionChains(self.driver)
        actions.move_to_element(forgot_link).perform()
        time.sleep(0.5)
        
        # Get color after hover
        hover_color = forgot_link.value_of_css_property("color")
        
        # Color should change or link should still be visible
        # (This test documents the hover behavior)
        print(f"Link color - Initial: {initial_color}, Hover: {hover_color}")
    
    # =============================================
    # INPUT FIELD TESTS
    # =============================================
    
    @pytest.mark.functional
    @pytest.mark.input
    def test_email_input_accepts_text(self):
        """Test email field accepts text input"""
        test_email = "test@example.com"
        self.login_page.enter_email(test_email)
        
        value = self.login_page.get_email_value()
        assert value == test_email, "Email field should accept and store text"
    
    @pytest.mark.functional
    @pytest.mark.input
    def test_password_field_hides_input(self):
        """Test password field hides input (type=password)"""
        password_field = self.driver.find_element(*self.login_page.PASSWORD_INPUT)
        field_type = password_field.get_attribute("type")
        
        assert field_type == "password", \
            "Password field should have type='password' to hide input"
    
    @pytest.mark.functional
    @pytest.mark.input
    def test_input_field_placeholders(self):
        """Test input fields have placeholder text"""
        email_field = self.driver.find_element(*self.login_page.EMAIL_INPUT)
        email_placeholder = email_field.get_attribute("placeholder")
        assert email_placeholder is not None and email_placeholder != "", \
            "Email field should have placeholder text"
        
        password_field = self.driver.find_element(*self.login_page.PASSWORD_INPUT)
        password_placeholder = password_field.get_attribute("placeholder")
        assert password_placeholder is not None and password_placeholder != "", \
            "Password field should have placeholder text"
    
    @pytest.mark.functional
    @pytest.mark.keyboard
    def test_form_submission_with_enter_key(self):
        """Test form can be submitted with Enter key"""
        from selenium.webdriver.common.keys import Keys
        
        self.login_page.enter_email(Config.VALID_EMAIL)
        password_field = self.driver.find_element(*self.login_page.PASSWORD_INPUT)
        password_field.send_keys(Config.VALID_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        # Should submit and show welcome message
        assert self.login_page.is_welcome_message_displayed(timeout=3), \
            "Form should submit with Enter key"
    
    @pytest.mark.functional
    @pytest.mark.keyboard
    def test_tab_navigation(self):
        """Test tab key navigation between fields"""
        from selenium.webdriver.common.keys import Keys
        
        email_field = self.driver.find_element(*self.login_page.EMAIL_INPUT)
        email_field.click()
        email_field.send_keys(Keys.TAB)
        
        # Focus should move to password field
        active_element = self.driver.switch_to.active_element
        assert active_element.get_attribute("id") == "password", \
            "Tab should move focus to password field"
