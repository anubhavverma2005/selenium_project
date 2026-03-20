import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

BASE_URL = "https://www.saucedemo.com"

def test_valid_login(driver):
    """TC01 - Valid login with correct credentials"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    assert "inventory" in driver.current_url, "Login failed - not redirected to inventory"
    driver.save_screenshot("reports/TC01_valid_login_PASS.png")
    print("TC01 PASSED: Valid login successful")

def test_invalid_password(driver):
    """TC02 - Invalid login with wrong password"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "Username and password do not match" in error.text
    driver.save_screenshot("reports/TC02_invalid_password_PASS.png")
    print("TC02 PASSED: Error message shown for wrong password")

def test_empty_credentials(driver):
    """TC03 - Login with empty fields"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "Username is required" in error.text
    driver.save_screenshot("reports/TC03_empty_credentials_PASS.png")
    print("TC03 PASSED: Empty credentials validation works")

def test_locked_user_login(driver):
    """TC04 - Locked out user cannot login (Boundary case)"""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "locked out" in error.text.lower()
    driver.save_screenshot("reports/TC04_locked_user_PASS.png")
    print("TC04 PASSED: Locked user correctly blocked")