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
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.clear()
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    assert form_visible, "Form should still be visible with empty email"
    assert not welcome.is_displayed(), "Empty email should not allow login"


def test_invalid_email_format(driver):
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@")
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    assert form_visible, "Form should still be visible with invalid email"
    assert not welcome.is_displayed(), "Invalid email should not allow login"


def test_empty_password(driver):
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.clear()
    login_button.click()
    time.sleep(2)
    
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    assert form_visible, "Form should still be visible with empty password"
    assert not welcome.is_displayed(), "Empty password should not allow login"


def test_password_too_short(driver):
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.send_keys("Pass1")
    login_button.click()
    time.sleep(2)
    
    form_visible = driver.find_element(By.ID, 'loginForm').is_displayed()
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    
    assert form_visible, "Form should still be visible with short password"
    assert not welcome.is_displayed(), "Short password should not allow login"


def test_minimum_valid_password(driver):
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.send_keys("Pass1234")
    login_button.click()
    time.sleep(3)
    
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    form = driver.find_element(By.ID, 'loginForm')
    
    assert welcome.is_displayed(), "Valid 8-character password should allow login"
    assert not form.is_displayed(), "Form should be hidden after successful login"


def test_valid_email_and_password(driver):
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("student@example.com")
    password_field.send_keys("SecurePass123")
    login_button.click()
    time.sleep(3)
    
    welcome = driver.find_element(By.ID, 'welcomeMessage')
    form = driver.find_element(By.ID, 'loginForm')
    
    assert welcome.is_displayed(), "Valid credentials should allow login"
    assert not form.is_displayed(), "Form should be hidden after successful login"
