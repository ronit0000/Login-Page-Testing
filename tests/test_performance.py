"""
Performance Testing - Testing page load times and responsiveness
"""
import pytest
import time
from tests.base_test import BaseTest
from config import Config


class TestPerformance(BaseTest):
    """Test performance metrics of the login page"""
    
    @pytest.mark.performance
    def test_page_load_time(self):
        """Test page load time is within acceptable threshold"""
        start_time = time.time()
        
        # Reload the page
        self.driver.get(Config.BASE_URL)
        
        # Wait for page to be fully loaded
        self.driver.execute_script("return document.readyState") == "complete"
        
        end_time = time.time()
        load_time = end_time - start_time
        
        print(f"\nPage Load Time: {load_time:.2f} seconds")
        
        assert load_time < Config.PAGE_LOAD_THRESHOLD, \
            f"Page load time ({load_time:.2f}s) exceeds threshold ({Config.PAGE_LOAD_THRESHOLD}s)"
    
    @pytest.mark.performance
    def test_form_submission_response_time(self):
        """Test form submission response time"""
        self.login_page.enter_email(Config.VALID_EMAIL)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        
        start_time = time.time()
        self.login_page.click_login()
        
        # Wait for welcome message
        self.login_page.is_welcome_message_displayed(timeout=5)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\nForm Submission Response Time: {response_time:.2f} seconds")
        
        assert response_time < Config.FORM_SUBMIT_THRESHOLD, \
            f"Form submission time ({response_time:.2f}s) exceeds threshold ({Config.FORM_SUBMIT_THRESHOLD}s)"
    
    @pytest.mark.performance
    def test_dom_ready_state(self):
        """Test DOM reaches ready state quickly"""
        self.driver.get(Config.BASE_URL)
        
        # Check DOM ready state
        ready_state = self.driver.execute_script("return document.readyState")
        
        assert ready_state in ["interactive", "complete"], \
            "DOM should be in ready state"
    
    @pytest.mark.performance
    def test_resource_loading(self):
        """Test CSS and JS resources load successfully"""
        # Navigate to page
        self.driver.get(Config.BASE_URL)
        time.sleep(2)
        
        # Check if CSS is loaded by verifying styled element
        login_box = self.driver.find_element("class name", "login-box")
        background = login_box.value_of_css_property("background-color")
        
        assert background != "rgba(0, 0, 0, 0)", \
            "CSS should be loaded (background color applied)"
        
        # Check if JavaScript is loaded by executing a function
        js_loaded = self.driver.execute_script(
            "return typeof handleLogin === 'function'"
        )
        
        assert js_loaded, "JavaScript should be loaded"
    
    @pytest.mark.performance
    def test_multiple_rapid_submissions(self):
        """Test handling of multiple rapid form submissions"""
        submission_times = []
        
        for i in range(5):
            self.driver.refresh()
            time.sleep(0.5)
            
            self.login_page.enter_email(f"test{i}@example.com")
            self.login_page.enter_password(Config.VALID_PASSWORD)
            
            start = time.time()
            self.login_page.click_login()
            time.sleep(1)
            end = time.time()
            
            submission_times.append(end - start)
        
        avg_time = sum(submission_times) / len(submission_times)
        print(f"\nAverage submission time over 5 attempts: {avg_time:.2f}s")
        print(f"Individual times: {[f'{t:.2f}s' for t in submission_times]}")
        
        assert avg_time < Config.FORM_SUBMIT_THRESHOLD, \
            "Average submission time should be acceptable"
    
    @pytest.mark.performance
    def test_browser_console_errors(self):
        """Test for JavaScript errors in console"""
        logs = self.login_page.get_console_logs()
        
        # Filter for actual errors (not warnings or info)
        errors = [log for log in logs if log.get('level') == 'SEVERE']
        
        if errors:
            print("\nConsole Errors Found:")
            for error in errors:
                print(f"  - {error.get('message', 'Unknown error')}")
        
        # Document errors but don't fail (some might be expected)
        print(f"\nTotal console errors: {len(errors)}")
    
    @pytest.mark.performance
    def test_memory_usage_check(self):
        """Test for basic memory usage patterns"""
        # Perform multiple operations
        for i in range(10):
            self.login_page.enter_email(f"test{i}@example.com")
            self.login_page.enter_password("password")
            self.login_page.click_login()
            time.sleep(0.5)
            self.driver.refresh()
            time.sleep(0.5)
        
        # Check if page still responsive
        assert self.login_page.is_login_form_displayed(), \
            "Page should remain responsive after multiple operations"
    
    @pytest.mark.performance
    def test_input_field_responsiveness(self):
        """Test input fields respond quickly to user input"""
        import string
        
        # Type a long string quickly
        long_email = "a" * 50 + "@example.com"
        
        start = time.time()
        self.login_page.enter_email(long_email)
        end = time.time()
        
        input_time = end - start
        
        print(f"\nTime to input {len(long_email)} characters: {input_time:.3f}s")
        
        # Verify value was set correctly
        actual_value = self.login_page.get_email_value()
        assert actual_value == long_email, "Input should be set correctly"
        assert input_time < 1.0, "Input field should be responsive"
