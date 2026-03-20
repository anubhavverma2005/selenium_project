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

def login(driver):
    driver.get("https://www.saucedemo.com")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)

def test_full_checkout(driver):
    """TC08 - Complete end-to-end checkout flow"""
    login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1)
    driver.find_element(By.ID, "checkout").click()
    # Fill checkout form (BVA - valid normal values)
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("110001")
    driver.find_element(By.ID, "continue").click()
    time.sleep(1)
    driver.find_element(By.ID, "finish").click()
    time.sleep(1)
    confirmation = driver.find_element(By.CLASS_NAME, "complete-header")
    assert "Thank you" in confirmation.text
    driver.save_screenshot("reports/TC08_checkout_complete_PASS.png")
    print("TC08 PASSED: Full checkout completed successfully")

def test_checkout_empty_form(driver):
    """TC09 - Checkout with empty form fields (BVA - below minimum)"""
    login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "continue").click()  # Submit empty form
    time.sleep(1)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "First Name is required" in error.text
    driver.save_screenshot("reports/TC09_empty_checkout_PASS.png")
    print("TC09 PASSED: Empty checkout form validation works")

def test_logout(driver):
    """TC10 - Logout functionality"""
    login(driver)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(1)
    assert driver.current_url == "https://www.saucedemo.com/"
    driver.save_screenshot("reports/TC10_logout_PASS.png")
    print("TC10 PASSED: Logout successful")