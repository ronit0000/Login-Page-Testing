import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'https://ronit0000.github.io/Login-Page/'

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(BASE_URL)
    time.sleep(2)
    yield driver
    driver.quit()


def test_empty_email(driver):
    """Test that empty email shows error message"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.clear()
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    # Check for email error message
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    # Enhanced validation checks
    assert email_error.text != '', "Email error message should be displayed"
    assert email_error.is_displayed(), "Email error element should be visible"
    assert 'required' in email_error.text.lower(), f"Error should mention 'required' but got: '{email_error.text}'"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert form_visible, "Form should still be visible with empty email"
    assert not welcome.is_displayed(), "Empty email should not allow login"
    
    print(f"   ✓ Email error displayed: '{email_error.text}'")


def test_invalid_email_format(driver):
    """Test that invalid email format shows error message"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@")
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    # Check for email error message
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    # Enhanced validation checks
    assert email_error.text != '', "Email error message should be displayed"
    assert email_error.is_displayed(), "Email error element should be visible"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert form_visible, "Form should still be visible with invalid email"
    assert not welcome.is_displayed(), "Invalid email should not allow login"
    
    print(f"   ✓ Email error displayed: '{email_error.text}'")


def test_empty_password(driver):
    """Test that empty password shows error message"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.clear()
    login_button.click()
    time.sleep(2)
    
    # Check for password error message
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    # Enhanced validation checks
    assert password_error.text != '', "Password error message should be displayed"
    assert password_error.is_displayed(), "Password error element should be visible"
    assert 'required' in password_error.text.lower(), f"Error should mention 'required' but got: '{password_error.text}'"
    assert email_error.text == '', f"Email error should be empty but got: '{email_error.text}'"
    assert form_visible, "Form should still be visible with empty password"
    assert not welcome.is_displayed(), "Empty password should not allow login"
    
    print(f"   ✓ Password error displayed: '{password_error.text}'")


def test_password_too_short(driver):
    """Test that password shorter than 8 characters shows error message"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    short_password = "Pass1"  # 5 characters
    email_field.send_keys("test@example.com")
    password_field.send_keys(short_password)
    login_button.click()
    time.sleep(2)
    
    # Check for password error message
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    # Enhanced validation checks
    assert password_error.text != '', "Password error message should be displayed"
    assert password_error.is_displayed(), "Password error element should be visible"
    assert '8' in password_error.text, f"Error should mention '8 characters' but got: '{password_error.text}'"
    assert email_error.text == '', f"Email error should be empty but got: '{email_error.text}'"
    assert form_visible, "Form should still be visible with short password"
    assert not welcome.is_displayed(), "Short password should not allow login"
    
    print(f"   ✓ Password error displayed: '{password_error.text}'")


def test_minimum_valid_password(driver):
    """Test that password with exactly 8 characters is accepted"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.send_keys("Pass1234")  # Exactly 8 characters
    login_button.click()
    time.sleep(3)
    
    # Check for no errors and successful login
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    form = driver.find_element(By.ID, 'loginForm')
    
    # Enhanced validation checks
    assert email_error.text == '', f"Email error should be empty but got: '{email_error.text}'"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert welcome.is_displayed(), "Valid 8-character password should allow login"
    assert not form.is_displayed(), "Form should be hidden after successful login"
    
    print("   ✓ Login successful with 8-character password (minimum valid)")


def test_valid_email_and_password(driver):
    """Test that valid email and password allow login"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("student@example.com")
    password_field.send_keys("SecurePass123")
    login_button.click()
    time.sleep(3)
    
    # Check for no errors and successful login
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    form = driver.find_element(By.ID, 'loginForm')
    
    # Enhanced validation checks
    assert email_error.text == '', f"Email error should be empty but got: '{email_error.text}'"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert welcome.is_displayed(), "Valid credentials should allow login"
    assert not form.is_displayed(), "Form should be hidden after successful login"
    
    print("   ✓ Login successful with valid email and password")


def test_email_too_short_with_valid_password(driver):
    """Test email length validation - minimum 11 characters"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    # Email with less than 11 characters: "a@test.com" = 10 chars
    short_email = "a@test.com"
    email_field.send_keys(short_email)
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    # Check if error message is displayed
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    # Enhanced validation checks
    assert email_error.text != '', "Email error message should be displayed"
    assert email_error.is_displayed(), "Email error element should be visible"
    assert '11' in email_error.text, f"Error should mention '11 characters' but got: '{email_error.text}'"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert form_visible, "Form should still be visible with short email"
    assert not welcome.is_displayed(), "Short email should not allow login"
    
    print(f"   ✓ Email error displayed: '{email_error.text}' (email: {short_email}, {len(short_email)} chars)")


def test_email_too_long_with_valid_password(driver):
    """Test email length validation - maximum 50 characters"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    # Email with more than 50 characters: 51 chars
    long_email = "verylongemailaddressfortesting123456789@example.com"
    email_field.send_keys(long_email)
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    # Check if error message is displayed
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    # Enhanced validation checks
    assert email_error.text != '', "Email error message should be displayed for long email"
    assert email_error.is_displayed(), "Email error element should be visible"
    assert '50' in email_error.text, f"Error should mention '50 characters' but got: '{email_error.text}'"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert form_visible, "Form should still be visible with long email"
    assert not welcome.is_displayed(), "Long email should not allow login"
    
    print(f"   ✓ Email error displayed: '{email_error.text}' (email: {len(long_email)} chars)")


def test_email_minimum_valid_length_with_valid_password(driver):
    """Test email at minimum valid length - 11 characters"""
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    # Email with exactly 11 characters: "a@tests.com" = 11 chars
    min_email = "a@tests.com"
    email_field.send_keys(min_email)
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(3)
    
    # Check for no errors and successful login
    email_error = driver.find_element(By.ID, 'emailError')
    password_error = driver.find_element(By.ID, 'passwordError')
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    form = driver.find_element(By.ID, 'loginForm')
    
    # Enhanced validation checks
    assert email_error.text == '', f"Email error should be empty but got: '{email_error.text}'"
    assert password_error.text == '', f"Password error should be empty but got: '{password_error.text}'"
    assert welcome.is_displayed(), "Valid 11-character email should allow login"
    assert not form.is_displayed(), "Form should be hidden after successful login"
    
    print(f"   ✓ Login successful with minimum valid email ({len(min_email)} chars)")
