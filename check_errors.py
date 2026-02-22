"""
Simple script to verify if error messages are being displayed
"""
#.\venv\Scripts\Activate.ps1; python check_errors.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = 'https://ronit0000.github.io/Login-Page/'

def check_error_implementation():
    print("\n" + "="*70)
    print("CHECKING ERROR MESSAGE")
    print("="*70 + "\n")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Check if error elements exist
    print("1. Checking if error elements exist in DOM...")
    try:
        email_error = driver.find_element(By.ID, 'emailError')
        password_error = driver.find_element(By.ID, 'passwordError')
        print("   ✓ Both emailError and passwordError elements exist\n")
    except Exception as e:
        print(f"   ✗ ERROR: {e}\n")
        driver.quit()
        return
    
    # Test 1: Empty email
    print("2. Testing EMPTY EMAIL (should show error)...")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.clear()
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    email_error_text = driver.find_element(By.ID, 'emailError').text
    if email_error_text:
        print(f"   ✓ Email error displayed: '{email_error_text}'")
    else:
        print(f"   ✗ NO EMAIL ERROR SHOWN (id=emailError is empty)")
    
    # Reload page
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Test 2: Empty password
    print("\n3. Testing EMPTY PASSWORD (should show error)...")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.clear()
    login_button.click()
    time.sleep(2)
    
    password_error_text = driver.find_element(By.ID, 'passwordError').text
    if password_error_text:
        print(f"   ✓ Password error displayed: '{password_error_text}'")
    else:
        print(f"   ✗ NO PASSWORD ERROR SHOWN (id=passwordError is empty)")
    
    # Reload page
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Test 3: Short password
    print("\n4. Testing SHORT PASSWORD - 5 chars (should show error)...")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@example.com")
    password_field.send_keys("Pass1")
    login_button.click()
    time.sleep(2)
    
    password_error_text = driver.find_element(By.ID, 'passwordError').text
    if password_error_text:
        print(f"   ✓ Password error displayed: '{password_error_text}'")
    else:
        print(f"   ✗ NO PASSWORD ERROR SHOWN (id=passwordError is empty)")
    
    # Reload page
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Test 4: Short email (< 11 chars)
    print("\n5. Testing SHORT EMAIL - 10 chars (should show error)...")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("a@test.com")
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    email_error_text = driver.find_element(By.ID, 'emailError').text
    if email_error_text:
        print(f"   ✓ Email error displayed: '{email_error_text}'")
    else:
        print(f"   ✗ NO EMAIL ERROR SHOWN (id=emailError is empty)")
    
    # Reload page
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Test 5: Long email (> 50 chars)
    long_email = "verylongemailaddressfortesting123456789@example.com"
    print(f"\n6. Testing LONG EMAIL - {len(long_email)} chars (should show error)...")
    print(f"   Email: '{long_email}'")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys(long_email)
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    email_error_text = driver.find_element(By.ID, 'emailError').text
    if email_error_text:
        print(f"   ✓ Email error displayed: '{email_error_text}'")
    else:
        print(f"   ✗ NO EMAIL ERROR SHOWN (id=emailError is empty)")
    
    # Reload page
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Test 6: Email at max boundary (= 50 chars, should be VALID)
    max_valid_email = "verylongemailaddressfortesting12345678@example.com"
    print(f"\n7. Testing MAX VALID EMAIL - {len(max_valid_email)} chars (should be ACCEPTED)...")
    print(f"   Email: '{max_valid_email}'")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys(max_valid_email)
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(3)
    
    email_error_text = driver.find_element(By.ID, 'emailError').text
    welcome_displayed = driver.find_element(By.ID, 'welcomeMessage').is_displayed()
    if not email_error_text and welcome_displayed:
        print(f"   ✓ Email accepted (no error) and login successful")
    else:
        print(f"   ✗ FAILED - Error: '{email_error_text}', Welcome: {welcome_displayed}")
    
    # Reload page
    driver.get(BASE_URL)
    time.sleep(2)
    
    # Test 7: Invalid email format
    print("\n8. Testing INVALID EMAIL FORMAT (should show error)...")
    email_field = driver.find_element(By.ID, 'email')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    email_field.send_keys("test@")
    password_field.send_keys("ValidPass123")
    login_button.click()
    time.sleep(2)
    
    email_error_text = driver.find_element(By.ID, 'emailError').text
    if email_error_text:
        print(f"   ✓ Email error displayed: '{email_error_text}'")
    else:
        print(f"   ✗ NO EMAIL ERROR SHOWN (id=emailError is empty)")
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70 + "\n")
    
    driver.quit()

if __name__ == "__main__":
    check_error_implementation()
