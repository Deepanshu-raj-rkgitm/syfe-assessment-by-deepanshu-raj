from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)


url = "https://www.saucedemo.com/"

# first task starts here
print("Task 1 starts here")
def login(username, password):
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def verify_login(expected_url, error_message=None):
    try:
        if error_message:
            error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))).text
            assert error == error_message
        else:
            wait.until(EC.url_contains(expected_url))
            assert driver.current_url.endswith(expected_url)
    except (AssertionError, TimeoutException):
        print("Login verification failed.")


login("standard_user", "secret_sauce")
verify_login("/inventory.html")

login("invalid_user", "wrong_password")
verify_login("/", "Epic sadface: Username and password do not match any user in this service.")
print("Task 1 ends here")

# second  task starts here
print("Task 2 starts here")
driver.get("https://www.saucedemo.com/inventory.html")
driver.find_element(By.CLASS_NAME, "product_sort_container").click()
driver.find_element(By.XPATH, "//option[@value='lohi']").click()


driver.find_element(By.XPATH, "//div[text()='Sauce Labs Backpack']/following::button[1]").click()
driver.find_element(By.XPATH, "//div[text()='Sauce Labs Bike Light']/following::button[1]").click()


assert driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "2"
print("The cart icon shows the number `2`.")
print("Task 2 ends here")
 
# third task starts here
print("Task 3 starts here") 
driver.find_element(By.LINK_TEXT, "Sauce Labs Onesie").click()
driver.find_element(By.CLASS_NAME, "btn_primary").click()


assert driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "3"
print("The cart icon shows the number `3`.")
print("Task 3 ends here")

# fourth task starts here
print("Task 4 starts here")
driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()


items = driver.find_elements(By.CLASS_NAME, "cart_item")
for item in items:
    price = float(item.find_element(By.CLASS_NAME, "inventory_item_price").text.strip('$'))
    if 8 <= price <= 10:
        item.find_element(By.CLASS_NAME, "cart_button").click()
        break


assert driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "2"
print("The cart icon shows the number `2`.")
print("Task 4 ends here")

# Tfifth task starts here
driver.find_element(By.ID, "checkout").click()
driver.find_element(By.ID, "first-name").send_keys("John")
driver.find_element(By.ID, "last-name").send_keys("Doe")
driver.find_element(By.ID, "postal-code").send_keys("12345")
driver.find_element(By.ID, "continue").click()


total = driver.find_element(By.CLASS_NAME, "summary_total_label").text
print(f"Total amount: {total}")


driver.find_element(By.ID, "finish").click()
assert "THANK YOU FOR YOUR ORDER" in driver.page_source
print("Task 5 ends here")

# task 6 starts here
print("Task 6 starts here")
driver.find_element(By.ID, "react-burger-menu-btn").click()
wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
assert driver.current_url == url
print("Verify redirection back to the login page (`/`).")
print("Task 6 ends here")

# Close browser
driver.quit()
