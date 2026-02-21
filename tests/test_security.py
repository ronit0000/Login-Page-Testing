"""
Security Testing - Testing for vulnerabilities
Based on BUGS.md - BUG #3 (SQL Injection), BUG #5 (Rate Limiting), 
BUG #6 (Insecure Storage), BUG #7 (XSS)
"""
import pytest
import time
from tests.base_test import BaseTest
from config import Config


class TestSecurityVulnerabilities(BaseTest):
    """Test security vulnerabilities and attack vectors"""
    
    # =============================================
    # SQL INJECTION TESTS - BUG #3
    # =============================================
    
    @pytest.mark.security
    @pytest.mark.sql_injection
    def test_sql_injection_basic(self):
        """ST-001: Test basic SQL injection in email field"""
        sql_injection = "admin'--"
        
        self.login_page.enter_email(sql_injection)
        self.login_page.enter_password("anything")
        self.login_page.click_login()
        time.sleep(2)
        
        # BUG #3: No sanitization, input is used as-is
        # Check console logs for unsanitized data
        logs = self.login_page.get_console_logs()
        
        # Check if SQL injection string appears in logs (vulnerability)
        log_messages = [log.get('message', '') for log in logs]
        found_in_logs = any(sql_injection in msg for msg in log_messages)
        
        if found_in_logs:
            pytest.fail(f"BUG FOUND: SQL injection string '{sql_injection}' found in console logs - No sanitization")
        
        # Also check if it's displayed unsanitized
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=3)
        if is_welcome_shown:
            welcome_text = self.login_page.get_welcome_message_email()
            if sql_injection in welcome_text:
                pytest.fail(f"BUG FOUND: SQL injection string displayed without sanitization")
    
    @pytest.mark.security
    @pytest.mark.sql_injection
    def test_sql_injection_or_statement(self):
        """ST-002: Test SQL injection with OR statement"""
        sql_payloads = [
            "' OR '1'='1",
            "' OR '1'='1'--",
            "admin' OR '1'='1'--"
        ]
        
        for payload in sql_payloads:
            self.driver.refresh()
            time.sleep(1)
            
            self.login_page.enter_email(payload)
            self.login_page.enter_password("' OR '1'='1")
            self.login_page.click_login()
            time.sleep(1)
            
            # BUG #3: Vulnerable to SQL injection
            logs = self.login_page.get_console_logs()
            log_messages = [log.get('message', '') for log in logs]
            
            # Check if payload appears unsanitized
            found = any(payload in msg for msg in log_messages)
            if found:
                print(f"VULNERABILITY: SQL payload '{payload}' found in logs")
    
    @pytest.mark.security
    @pytest.mark.sql_injection
    def test_sql_injection_union(self):
        """ST-003: Test SQL injection with UNION statement"""
        union_injection = "' UNION SELECT * FROM users--"
        
        self.login_page.enter_email(union_injection)
        self.login_page.enter_password("password")
        self.login_page.click_login()
        time.sleep(2)
        
        # Check if unsanitized
        logs = self.login_page.get_console_logs()
        log_messages = [log.get('message', '') for log in logs]
        
        found = any("UNION" in msg for msg in log_messages)
        if found:
            pytest.fail("BUG FOUND: UNION SQL injection not sanitized")
    
    @pytest.mark.security
    @pytest.mark.sql_injection
    def test_sql_injection_comment(self):
        """ST-004: Test SQL injection with comment syntax"""
        comment_injection = "admin'/*"
        
        self.login_page.enter_email(comment_injection)
        self.login_page.enter_password("*/")
        self.login_page.click_login()
        time.sleep(2)
        
        # Check console for unsanitized input
        logs = self.login_page.get_console_logs()
        print(f"Testing comment injection: {comment_injection}")
        
        # Document behavior
        is_accepted = self.login_page.is_welcome_message_displayed(timeout=2)
        if is_accepted:
            print("VULNERABILITY: SQL comment injection accepted")
    
    # =============================================
    # XSS (CROSS-SITE SCRIPTING) TESTS - BUG #7
    # =============================================
    
    @pytest.mark.security
    @pytest.mark.xss
    def test_xss_script_tag_injection(self):
        """ST-005: Test XSS with script tag in email"""
        xss_payload = "<script>alert('XSS')</script>"
        
        self.login_page.enter_email(xss_payload)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # BUG #7: May not escape HTML
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=3)
        
        if is_welcome_shown:
            welcome_text = self.login_page.get_welcome_message_email()
            
            # If script tag appears unescaped, it's a critical vulnerability
            if "<script>" in welcome_text:
                pytest.fail("CRITICAL: XSS vulnerability - Script tag not escaped")
            
            # Check if it was escaped properly
            if "&lt;script&gt;" in welcome_text or "script" not in welcome_text.lower():
                print("XSS payload was escaped - Good!")
            else:
                print(f"XSS test result: {welcome_text}")
    
    @pytest.mark.security
    @pytest.mark.xss
    def test_xss_event_handler_injection(self):
        """ST-006: Test XSS with event handler"""
        xss_payload = "<img src=x onerror=alert('XSS')>"
        
        self.login_page.enter_email(xss_payload)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Check if HTML is properly escaped
        is_welcome_shown = self.login_page.is_welcome_message_displayed(timeout=3)
        
        if is_welcome_shown:
            # Get page source to check for unescaped HTML
            page_source = self.driver.page_source
            
            if "<img" in page_source and "onerror" in page_source:
                pytest.fail("CRITICAL: XSS vulnerability - Event handlers not sanitized")
    
    @pytest.mark.security
    @pytest.mark.xss
    def test_xss_javascript_protocol(self):
        """ST-007: Test XSS with javascript: protocol"""
        xss_payload = "javascript:alert('XSS')"
        
        self.login_page.enter_email(xss_payload)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Check console logs
        logs = self.login_page.get_console_logs()
        log_messages = [log.get('message', '') for log in logs]
        
        # Check if javascript: protocol was sanitized
        found = any("javascript:" in msg for msg in log_messages)
        if found:
            print("WARNING: javascript: protocol found in logs")
    
    @pytest.mark.security
    @pytest.mark.xss
    def test_xss_html_injection(self):
        """ST-008: Test HTML injection"""
        html_injection = "<h1>Hacked</h1>"
        
        self.login_page.enter_email(html_injection)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Check if HTML is rendered
        if self.login_page.is_welcome_message_displayed(timeout=3):
            page_source = self.driver.page_source
            
            # If <h1>Hacked</h1> appears as actual HTML (not escaped), it's a vulnerability
            if "<h1>Hacked</h1>" in page_source:
                # Check if it's in the welcome message area
                try:
                    injected_element = self.driver.find_element("tag name", "h1")
                    if "Hacked" in injected_element.text:
                        pytest.fail("BUG FOUND: HTML injection successful - Tags not escaped")
                except:
                    pass
    
    # =============================================
    # AUTHENTICATION & SESSION TESTS - BUG #5
    # =============================================
    
    @pytest.mark.security
    @pytest.mark.brute_force
    def test_no_rate_limiting(self):
        """ST-009: Test for lack of rate limiting (brute force vulnerability)"""
        # BUG #5: No rate limiting implemented
        
        # Try multiple rapid login attempts
        attempt_count = 10
        successful_attempts = 0
        
        for i in range(attempt_count):
            self.driver.refresh()
            time.sleep(0.5)
            
            self.login_page.enter_email(f"test{i}@example.com")
            self.login_page.enter_password(f"wrongpassword{i}")
            self.login_page.click_login()
            time.sleep(0.5)
            
            successful_attempts += 1
        
        # All attempts should go through (no rate limiting)
        if successful_attempts == attempt_count:
            pytest.fail(f"BUG FOUND: No rate limiting - All {attempt_count} attempts processed immediately")
    
    @pytest.mark.security
    @pytest.mark.auth
    def test_password_field_visibility(self):
        """ST-010: Test password field hides input"""
        password_field = self.driver.find_element(*self.login_page.PASSWORD_INPUT)
        field_type = password_field.get_attribute("type")
        
        assert field_type == "password", \
            "Password field must use type='password' to hide input"
    
    @pytest.mark.security
    @pytest.mark.data_exposure
    def test_console_data_exposure(self):
        """ST-011: Test for sensitive data exposure in console logs"""
        # BUG #3: Console logs may expose user input
        
        test_email = "sensitive@example.com"
        test_password = "SecretPassword123!"
        
        self.login_page.enter_email(test_email)
        self.login_page.enter_password(test_password)
        self.login_page.click_login()
        time.sleep(2)
        
        # Check console logs
        logs = self.login_page.get_console_logs()
        log_messages = [log.get('message', '') for log in logs]
        
        # Check if email or password appears in logs
        email_exposed = any(test_email in msg for msg in log_messages)
        password_exposed = any(test_password in msg for msg in log_messages)
        
        if email_exposed:
            pytest.fail("BUG FOUND: Email exposed in console logs")
        
        if password_exposed:
            pytest.fail("CRITICAL BUG: Password exposed in console logs!")
    
    @pytest.mark.security
    @pytest.mark.storage
    def test_insecure_localstorage(self):
        """ST-012: Test for insecure localStorage usage"""
        # BUG #6: Stores email in plain text in localStorage
        
        test_email = "stored@example.com"
        
        # Login with Remember Me checked
        self.login_page.enter_email(test_email)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.check_remember_me()
        self.login_page.click_login()
        time.sleep(2)
        
        # Check localStorage
        stored_email = self.login_page.get_local_storage_item('userEmail')
        
        if stored_email == test_email:
            pytest.fail("BUG FOUND: Email stored in plain text in localStorage - Security risk")
        
        # If stored with encryption or hashing, it's better
        if stored_email is not None and stored_email != test_email:
            print(f"Data stored (encrypted/hashed): {stored_email}")
    
    # =============================================
    # INPUT SANITIZATION TESTS
    # =============================================
    
    @pytest.mark.security
    @pytest.mark.sanitization
    def test_special_characters_handling(self):
        """Test handling of special characters"""
        special_chars_email = "test<>\"'&@example.com"
        
        self.login_page.enter_email(special_chars_email)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Check if special characters are properly handled
        logs = self.login_page.get_console_logs()
        log_messages = [log.get('message', '') for log in logs]
        
        # Document how special characters are handled
        print(f"Testing special characters: {special_chars_email}")
    
    @pytest.mark.security
    @pytest.mark.sanitization
    def test_unicode_characters(self):
        """Test Unicode and international characters"""
        unicode_email = "测试@例え.com"
        
        self.login_page.enter_email(unicode_email)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Document behavior with Unicode
        is_accepted = self.login_page.is_welcome_message_displayed(timeout=2)
        print(f"Unicode email - Accepted: {is_accepted}")
    
    @pytest.mark.security
    @pytest.mark.sanitization
    def test_null_byte_injection(self):
        """Test null byte injection"""
        null_byte_email = "admin\x00@example.com"
        
        self.login_page.enter_email(null_byte_email)
        self.login_page.enter_password(Config.VALID_PASSWORD)
        self.login_page.click_login()
        time.sleep(2)
        
        # Check how null bytes are handled
        logs = self.login_page.get_console_logs()
        print(f"Null byte injection test completed")
    
    # =============================================
    # ADVANCED SECURITY TESTS
    # =============================================
    
    @pytest.mark.security
    @pytest.mark.advanced
    def test_ldap_injection(self):
        """Test LDAP injection attempts"""
        ldap_payload = "*)(uid=*))(|(uid=*"
        
        self.login_page.enter_email(ldap_payload)
        self.login_page.enter_password("password")
        self.login_page.click_login()
        time.sleep(2)
        
        # Document LDAP injection test
        print(f"LDAP injection test: {ldap_payload}")
    
    @pytest.mark.security
    @pytest.mark.advanced
    def test_command_injection(self):
        """Test command injection attempts"""
        command_payloads = [
            "; ls -la",
            "| cat /etc/passwd",
            "& dir",
            "`whoami`"
        ]
        
        for payload in command_payloads:
            self.driver.refresh()
            time.sleep(1)
            
            self.login_page.enter_email(f"test@example.com{payload}")
            self.login_page.enter_password("password")
            self.login_page.click_login()
            time.sleep(1)
            
            print(f"Command injection test: {payload}")
    
    @pytest.mark.security
    @pytest.mark.advanced
    def test_path_traversal(self):
        """Test path traversal attempts"""
        path_traversal = "../../../etc/passwd"
        
        self.login_page.enter_email(f"{path_traversal}@example.com")
        self.login_page.enter_password("password")
        self.login_page.click_login()
        time.sleep(2)
        
        # Document path traversal test
        print(f"Path traversal test: {path_traversal}")
