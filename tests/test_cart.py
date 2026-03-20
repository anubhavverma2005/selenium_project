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

def test_add_to_cart(driver):
    """TC05 - Add a product to cart and verify badge count"""
    login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1", "Cart count should be 1"
    driver.save_screenshot("reports/TC05_add_to_cart_PASS.png")
    print("TC05 PASSED: Item added to cart successfully")

def test_remove_from_cart(driver):
    """TC06 - Remove a product from cart"""
    login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)
    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
    time.sleep(1)
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0, "Cart should be empty after removal"
    driver.save_screenshot("reports/TC06_remove_from_cart_PASS.png")
    print("TC06 PASSED: Item removed from cart successfully")

def test_sort_products_by_price(driver):
    """TC07 - Sort products low to high (State Transition test)"""
    login(driver)
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    driver.find_element(By.CSS_SELECTOR, "option[value='lohi']").click()
    time.sleep(1)
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    price_values = [float(p.text.replace("$","")) for p in prices]
    assert price_values == sorted(price_values), "Products not sorted correctly"
    driver.save_screenshot("reports/TC07_sort_products_PASS.png")
    print("TC07 PASSED: Products sorted low to high correctly")