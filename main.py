import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium import webdriver
import time

path = './chromedriver'
driver = webdriver.Chrome(path)
print("Driver initiated...\n")
tests = 0

# 1. open github.com
print("Trying to navigate to GitHub")
try:
    driver.get('https://github.com/')
    driver.maximize_window()
    print("Navigated to Github\n")
    tests+=1
except WebDriverException:
    print("There is a problem with the driver\n")
WebDriverWait(driver, timeout=5)

# 2. Make sure that you are not logged in
try:
    sign_in_btn = driver.find_element(By.XPATH, value='/html/body/div[1]/header/div/div[2]/div[2]/div[2]/a').text
    if sign_in_btn != None:
        print("The user is currently not logged into GitHub, the button is present: ", sign_in_btn, "\n")
        tests+=1
    elif sign_in_btn == None:
        print("The user is currently logged in, atleast we know that the button is not present")
    else:
        print("Something went wrong")
except NoSuchElementException:
    print("The element:", sign_in_btn, " is not present")

# 3. search for the repo "typescript"
print("Searching for the term 'typescript in GitHub'\n")
try:
    driver.find_element(By.XPATH, value='/html/body/div[1]/header/div/div[2]/div[2]/div[1]/div/div/form/label/input[1]').click()
    driver.find_element(By.XPATH, value='/html/body/div[1]/header/div/div[2]/div[2]/div[1]/div/div/form/label/input[1]').send_keys('typescript',Keys.ENTER)
    tests+=1
except NoSuchElementException:
    print("No such element found")
WebDriverWait(driver, timeout=5)

# 4. Go into "TypeScript-Handbook" page
print("Navigating to the correct repository 'TypeScript-Handbook', which is located in the second page of the search")
try:
    driver.execute_script("window.scrollBy(0, 1000);")
    driver.find_element(By.XPATH, value='//*[@id="js-pjax-container"]/div/div[3]/div/div[3]/div/a[1]').click()
except ElementNotVisibleException or NoSuchElementException:
    print("The element was not found")
time.sleep(3)
print("Operation successful, navigated to the other page...\n")
try:
    driver.execute_script("window.scrollBy(0, 300);")
    driver.find_element(By.XPATH, value='//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[4]/div[2]/div[1]/div/a').click()
    tests+=1
except ElementNotVisibleException or NoSuchElementException:
    print("The element was not found\n")

# 5 Validate that the repo page shows the "is now read-only" message.
print("Validating that the repo is 'read-only'")
try:
    text = driver.find_element(By.XPATH, value="//*[contains(text(),'read-only')]").text
    if text != None:
        print("Results: ", text,"\n")
        tests+=1
    elif text == None:
        print("The element was not found")
    else:
        print("Something went wrong...")
except NoSuchElementException:
    print("Element not found...")

# 6. Validate that there are 38 branches
print("Checking that there are 38 branches in this repository...")
try:
    branches = driver.find_element(By.XPATH, value="//*[@id='repo-content-pjax-container']/div/div/div[3]/div[1]/div[1]/div[2]/a[1]/strong").text
    if branches == '38':
        print("The value of branches is correct, it is: ", branches,"\n")
        tests+=1
    elif branches != '38':
        print("The value is not 38 it is: ", branches,"\n")
    else:
        print("Something went wrong...\n")
except NoSuchElementException:
    print("Element not found...")

# 7. Validate that there are more than 180 watchers
print("Validating that there are atleast 180 watchers in the repository...")
try:
    watchers = driver.find_element(By.XPATH, value='//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[1]/div/div[7]/a').text
    if watchers[0:3] >= '180':
        print("There are over 180 watchers...the number is:\n", watchers)
        tests+=1
    elif watchers[0:3] < '180':
        print("There are less than 180 watchers", watchers)
    else:
        print("Something went wrong...")
except NoSuchElementException:
    print("Element not found...")

# 8. Validate that the build is passing
if tests == 7:
    print("The build PASSED, all tests were successful")
else:
    print("The build DIDNT PASS, some tests failed")