"""
🎓 BEGINNER-FRIENDLY: Page Object Model for Login Page

What is Page Object Model (POM)?
- It's a design pattern that creates a Python class for each web page
- The class contains all the elements (buttons, inputs) on that page
- It makes tests easier to read and maintain

Think of it like this:
- Instead of writing driver.find_element(...) in every test
- We write login_page.enter_email() - much simpler!
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    This class represents our Login Page
    It knows how to find and interact with all elements on the page
    """
    
    # ========================================
    # STEP 1: Define where elements are located on the page
    # ========================================
    # By.ID means "find element by its ID attribute"
    # By.CSS_SELECTOR means "find element using CSS selector"
    
    EMAIL_INPUT = (By.ID, 'email')                    # The email input box
    PASSWORD_INPUT = (By.ID, 'password')              # The password input box
    REMEMBER_ME_CHECKBOX = (By.ID, 'rememberMe')      # Remember me checkbox
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')  # The login button
    
    EMAIL_ERROR = (By.ID, 'emailError')               # Error message for email
    PASSWORD_ERROR = (By.ID, 'passwordError')         # Error message for password
    
    WELCOME_MESSAGE = (By.ID, 'welcomeMessage')       # Success message after login
    
    def __init__(self, driver):
        """
        Initialize the page - this runs when we create a LoginPage object
        driver = the browser that Selenium controls
        wait = helps us wait for elements to load (instead of crashing)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements
    
    # ========================================
    # STEP 2: Define actions we can perform on the page
    # ========================================
    
    def open_page(self, url):
        """
        Open the login page in the browser
        Example: login_page.open_page("https://example.com")
        """
        self.driver.get(url)
        return self  # Return self allows method chaining (explained below)
    
    def enter_email(self, email):
        """
        Type text into the email field
        
        How it works:
        1. Wait until the email field appears on page (EC.presence_of_element_located)
        2. Clear any existing text (clear())
        3. Type the new email (send_keys())
        """
        email_field = self.wait.until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_field.clear()
        email_field.send_keys(email)
        return self  # Return self allows: login_page.enter_email().enter_password()
    
    def enter_password(self, password):
        """
        Type text into the password field
        Same process as enter_email()
        """
        password_field = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login_button(self):
        """
        Click the login button
        
        EC.element_to_be_clickable waits until:
        - Element is visible AND
        - Element is enabled (not disabled)
        Then it's safe to click!
        """
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()
        return self
    
    def get_email_error_message(self):
        """
        Get the error message shown under the email field
        Returns empty string "" if no error is shown
        """
        try:
            error_element = self.driver.find_element(*self.EMAIL_ERROR)
            return error_element.text
        except:
            return ""  # No error found
    
    def get_password_error_message(self):
        """
        Get the error message shown under the password field
        Returns empty string "" if no error is shown
        """
        try:
            error_element = self.driver.find_element(*self.PASSWORD_ERROR)
            return error_element.text
        except:
            return ""  # No error found
    
    def is_welcome_message_shown(self):
        """
        Check if the welcome message appears after successful login
        Returns True if message is visible, False otherwise
        
        This is useful to verify that login actually worked!
        """
        try:
            # Wait up to 5 seconds for welcome message
            wait = WebDriverWait(self.driver, 5)
            welcome_element = wait.until(
                EC.visibility_of_element_located(self.WELCOME_MESSAGE)
            )
            return welcome_element.is_displayed()
        except:
            return False  # Welcome message not found = login failed
    
    # ========================================
    # STEP 3: Helper methods for complete actions
    # ========================================
    
    def do_login(self, email, password):
        """
        🎯 MAIN METHOD: Perform complete login action
        
        This is a shortcut that does all steps at once:
        1. Enter email
        2. Enter password
        3. Click login button
        
        Example usage in tests:
            login_page.do_login("test@example.com", "Password123")
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_page_title(self):
        """
        Get the current page title
        Example: "Login Page" or "Welcome"
        """
        return self.driver.title


# ========================================
# 🎓 LEARNING NOTES FOR BEGINNERS:
# ========================================
# 
# 1. Why use Page Object Model?
#    - Makes tests easier to read: login_page.do_login() vs driver.find_element(By.ID, 'email').send_keys()
#    - If the page changes, you only update the Page class, not every test!
#    - Reusable: Write the method once, use it in multiple tests
#
# 2. What is "self"?
#    - self refers to the current LoginPage object
#    - self.driver = the browser instance
#    - self.wait = the WebDriverWait instance
#
# 3. What is "return self"?
#    - It lets you chain methods: login_page.enter_email("test@test.com").enter_password("pass").click_login_button()
#    - This is called "method chaining"
#
# 4. What is WebDriverWait?
#    - It waits for an element to appear before interacting with it
#    - Prevents errors like "Element not found" when page is still loading
#    - wait.until(EC.presence_of_element_located(...)) = "wait until element is present"
#
# 5. Common Selenium Methods:
#    - driver.get(url) = Open a webpage
#    - element.send_keys("text") = Type text into an input
#    - element.click() = Click on button/link
#    - element.text = Get the text content
#    - element.is_displayed() = Check if element is visible
#
# 🎯 Next step: Look at the test files to see how we USE this LoginPage class!
# ========================================
