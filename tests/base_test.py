"""
Base test class with common setup and teardown
"""
import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import Config
from pages.login_page import LoginPage


class BaseTest:
    """Base test class with common functionality"""
    
    driver = None
    login_page = None
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup test - runs before each test"""
        # Create screenshot directory if it doesn't exist
        if Config.SCREENSHOT_ON_FAILURE and not os.path.exists(Config.SCREENSHOT_DIR):
            os.makedirs(Config.SCREENSHOT_DIR)
        
        # Initialize driver based on browser config
        self.driver = self._get_driver()
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.driver.maximize_window()
        
        # Initialize page object
        self.login_page = LoginPage(self.driver, Config.EXPLICIT_WAIT)
        
        # Load the page
        self.login_page.load(Config.BASE_URL)
        
        yield
        
        # Teardown - runs after each test
        if request.node.rep_call.failed and Config.SCREENSHOT_ON_FAILURE:
            self._take_screenshot(request.node.nodeid)
        
        if self.driver:
            self.driver.quit()
    
    def _get_driver(self):
        """Get WebDriver instance based on config"""
        browser = Config.BROWSER
        
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if Config.HEADLESS:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # Enable console logs
            options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
            
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if Config.HEADLESS:
                options.add_argument('--headless')
            
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        
        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            if Config.HEADLESS:
                options.add_argument('--headless')
            
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _take_screenshot(self, nodeid):
        """Take screenshot on test failure"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Clean up node ID for filename
        filename = nodeid.replace('::', '_').replace('/', '_')
        filepath = os.path.join(Config.SCREENSHOT_DIR, f"{filename}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
        print(f"\nScreenshot saved: {filepath}")
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Hook to get test result for screenshot on failure"""
        outcome = yield
        rep = outcome.get_result()
        setattr(item, f"rep_{rep.when}", rep)


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
