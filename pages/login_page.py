"""
Page Object Model for Login Page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    """Page Object for the Login Page"""
    
    # Locators
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    REMEMBER_ME_CHECKBOX = (By.ID, 'rememberMe')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    
    EMAIL_ERROR = (By.ID, 'emailError')
    PASSWORD_ERROR = (By.ID, 'passwordError')
    
    WELCOME_MESSAGE = (By.ID, 'welcomeMessage')
    USER_EMAIL_DISPLAY = (By.ID, 'userEmail')
    
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, 'a.forgot-password')
    SIGNUP_LINK = (By.CSS_SELECTOR, 'a.signup-link')
    
    LOGIN_FORM = (By.ID, 'loginForm')
    
    def __init__(self, driver, wait_time=10):
        """Initialize the page object"""
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)
    
    def load(self, url):
        """Load the login page"""
        self.driver.get(url)
        return self
    
    def enter_email(self, email):
        """Enter email into the email field"""
        email_field = self.wait.until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_field.clear()
        email_field.send_keys(email)
        return self
    
    def enter_password(self, password):
        """Enter password into the password field"""
        password_field = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def check_remember_me(self):
        """Check the Remember Me checkbox"""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self
    
    def uncheck_remember_me(self):
        """Uncheck the Remember Me checkbox"""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if checkbox.is_selected():
            checkbox.click()
        return self
    
    def click_login(self):
        """Click the login button"""
        login_btn = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_btn.click()
        return self
    
    def submit_login(self, email, password, remember_me=False):
        """Complete login flow"""
        self.enter_email(email)
        self.enter_password(password)
        if remember_me:
            self.check_remember_me()
        self.click_login()
        return self
    
    def get_email_error(self):
        """Get email error message"""
        try:
            error_element = self.driver.find_element(*self.EMAIL_ERROR)
            return error_element.text
        except:
            return ""
    
    def get_password_error(self):
        """Get password error message"""
        try:
            error_element = self.driver.find_element(*self.PASSWORD_ERROR)
            return error_element.text
        except:
            return ""
    
    def is_welcome_message_displayed(self, timeout=5):
        """Check if welcome message is displayed"""
        try:
            self.wait = WebDriverWait(self.driver, timeout)
            welcome = self.wait.until(
                EC.visibility_of_element_located(self.WELCOME_MESSAGE)
            )
            return welcome.is_displayed()
        except TimeoutException:
            return False
    
    def get_welcome_message_email(self):
        """Get the email displayed in welcome message"""
        try:
            email_display = self.driver.find_element(*self.USER_EMAIL_DISPLAY)
            return email_display.text
        except:
            return ""
    
    def is_login_form_displayed(self):
        """Check if login form is visible"""
        try:
            form = self.driver.find_element(*self.LOGIN_FORM)
            return form.is_displayed()
        except:
            return False
    
    def get_email_value(self):
        """Get current value of email field"""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        return email_field.get_attribute('value')
    
    def get_password_value(self):
        """Get current value of password field"""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        return password_field.get_attribute('value')
    
    def is_remember_me_checked(self):
        """Check if Remember Me checkbox is checked"""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        return checkbox.is_selected()
    
    def click_forgot_password(self):
        """Click Forgot Password link"""
        link = self.driver.find_element(*self.FORGOT_PASSWORD_LINK)
        link.click()
        return self
    
    def click_signup(self):
        """Click Sign Up link"""
        link = self.driver.find_element(*self.SIGNUP_LINK)
        link.click()
        return self
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
    
    def get_console_logs(self):
        """Get browser console logs"""
        try:
            logs = self.driver.get_log('browser')
            return logs
        except:
            return []
    
    def get_local_storage_item(self, key):
        """Get item from localStorage"""
        return self.driver.execute_script(f"return localStorage.getItem('{key}');")
    
    def execute_script(self, script):
        """Execute JavaScript on the page"""
        return self.driver.execute_script(script)
