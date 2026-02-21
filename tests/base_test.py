"""
🎓 BEGINNER-FRIENDLY: Base Test Setup

WHAT IS THIS FILE?
- This is the "parent" class that all tests inherit from
- It handles the boring setup stuff (opening browser, closing browser)
- Every test class inherits from BaseTest so they don't repeat code

WHAT IS pytest?
- pytest is a Python testing framework
- It automatically finds functions that start with "test_"
- It runs them and reports if they pass or fail

WHAT IS A FIXTURE?
- A fixture is setup code that runs before each test
- @pytest.fixture(autouse=True) means "run this automatically"
- Our setup() fixture opens the browser and login page
- After test finishes, teardown closes the browser
"""
import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config import Config
from pages.login_page import LoginPage


class BaseTest:
    """
    Base class for all tests
    Handles browser setup and teardown
    """
    
    # These variables will be available in all tests
    driver = None          # The browser (Chrome)
    login_page = None      # Our LoginPage object
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """
        ⚙️ SETUP: This runs BEFORE each test
        
        Steps:
        1. Create screenshots folder if it doesn't exist
        2. Open Chrome browser
        3. Maximize the window
        4. Create LoginPage object
        5. Open the login page
        
        After test finishes, the yield line passes control to teardown
        """
        print("\n🚀 Setting up test...")
        
        # Create directory for screenshots (if test fails)
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        # Open Chrome browser
        self.driver = self._open_chrome_browser()
        
        # Maximize window so we can see everything
        self.driver.maximize_window()
        
        # Create our LoginPage helper object
        self.login_page = LoginPage(self.driver)
        
        # Open the login page URL
        self.login_page.open_page(Config.BASE_URL)
        
        print(f"✅ Browser opened: {Config.BASE_URL}")
        
        # yield means "pause here, run the test, then come back"
        yield
        
        # ========================================
        # 🧹 TEARDOWN: This runs AFTER each test
        # ========================================
        
        # Take screenshot if test failed
        if request.node.rep_call.failed:
            self._save_screenshot(request.node.nodeid)
        
        # Close the browser
        if self.driver:
            self.driver.quit()
            print("🛑 Browser closed")
    
    def _open_chrome_browser(self):
        """
        Open Chrome browser with Selenium
        
        What is ChromeDriverManager?
        - It automatically downloads the correct ChromeDriver version
        - You don't need to manually download anything!
        - It's like magic 🪄
        """
        # Set Chrome options
        options = webdriver.ChromeOptions()
        
        # Uncomment next line to run tests without seeing the browser (faster!)
        # options.add_argument('--headless')
        
        # These options make Chrome more stable for testing
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Create Chrome service (this manages the ChromeDriver)
        service = ChromeService(ChromeDriverManager().install())
        
        # Return the browser driver
        return webdriver.Chrome(service=service, options=options)
    
    def _save_screenshot(self, test_name):
        """
        Take a screenshot when test fails
        
        Why is this useful?
        - You can see exactly what went wrong!
        - Screenshot shows the page state at moment of failure
        """
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = test_name.replace('::', '_').replace('/', '_')
        filepath = os.path.join("screenshots", f"{filename}_{timestamp}.png")
        
        # Save screenshot
        self.driver.save_screenshot(filepath)
        print(f"📸 Screenshot saved: {filepath}")
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """
        pytest hook to detect test failures
        (Don't worry too much about understanding this part!)
        """
        outcome = yield
        rep = outcome.get_result()
        setattr(item, f"rep_{rep.when}", rep)


# ========================================
# 🎓 LEARNING NOTES - UNDERSTANDING THE FLOW:
# ========================================
#
# When you run a test, here's what happens:
#
# 1. pytest finds all test files (test_*.py)
# 2. pytest finds all test classes (Test*)
# 3. For each test method:
#    a. Run setup() - Open browser, create LoginPage
#    b. Run test_something() - The actual test
#    c. Run teardown - Close browser, maybe take screenshot
#
# Example flow for test_page_loads_successfully():
#   - setup() opens Chrome and goes to login page
#   - test_page_loads_successfully() checks the title
#   - teardown closes Chrome
#
# Why use BaseTest?
#   - Without it, every test file would need to:
#     * Open browser
#     * Close browser
#     * Handle screenshots
#   - With BaseTest, we write that code ONCE and reuse it!
#
# This is called "Don't Repeat Yourself" (DRY) principle
#
# ========================================
# 🎯 KEY CONCEPTS YOU LEARNED:
# ========================================
# 1. What fixtures are (@pytest.fixture)
# 2. What setup/teardown means
# 3. How to open a browser with Selenium
# 4. Why we take screenshots on failure
# 5. How webdriver-manager automatically downloads ChromeDriver
#
# Next: Look at test_simple.py to see how tests use this BaseTest!
# ========================================


# pytest configuration
@pytest.fixture(scope="function", autouse=True)
def test_info(request):
    """Fixture to capture test result for screenshot"""
    yield
    # Store test result
    item = request.node
    if hasattr(item, 'rep_setup'):
        if item.rep_setup.failed:
            print(f"\nSetup failed for {item.nodeid}")
    if hasattr(item, 'rep_call'):
        if item.rep_call.failed:
            print(f"\nTest failed: {item.nodeid}")
