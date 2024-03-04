
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import random
import re

# Set up the Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open LinkedIn login page
driver.get('https://www.linkedin.com/login')

# Login to LinkedIn
driver.find_element('id', 'username').send_keys('monalisajsr1991@gmail.com')
driver.find_element('id', 'password').send_keys('2692511@Spy')
driver.find_element(By.XPATH, "//button[normalize-space()='Sign in']").click()

# Search for 'krishna'
search_input = driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
search_input.send_keys('MEAN STACK DEVELOPER')
search_input.send_keys(Keys.RETURN)

# Click 'See all people' link
wait = WebDriverWait(driver, 30)
see_all_people_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all people')]")))
see_all_people_link.click()

data_list = []
json_file_path = 'User_Info.json'

# Loop through pages
for page_number in range(1, 2):
    # Loop through profiles on the current page
    for profile_index in range(1, 11):
        xpath = f"//div[1]//div[1]//main[1]//div[1]//div[1]//div[2]//div[1]//ul[1]//li[{profile_index}]//div[1]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//span[1]//span[1]//a[1]"

        try:
            # Wait until the element is clickable
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if element.text == "LinkedIn Member":
                continue
            else: 
                element.send_keys(Keys.CONTROL + Keys.RETURN)

            # Switch to the new window
                driver.switch_to.window(driver.window_handles[1])

            

            try:
                wait = WebDriverWait(driver, 30)
                # Click 'Contact info' to reveal details
                name = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']")))
                
                my_dict = {}

                # Loop through each element and add it to the dictionary
                my_dict['name'] = name.text

               
                # Wait until all contact details are loaded
                contact_details = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='top-card-text-details-contact-info']")))
                contact_details.click()

                wait = WebDriverWait(driver, 30)
                # Wait until all contact details are loaded
                target_a_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.link-without-visited-state.t-14')))


                # Loop through each element and add it to the dictionary
                for index, element in enumerate(target_a_elements):
                     # Check if the element is an email using regex
                    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                    if email_pattern.match(element.text):
                        my_dict['email'] = element.text
                # sleepFor = random.randint(0, 20)

                # time.sleep(sleepFor)

                if 'email' not in my_dict:
                    current_company = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Current company')]/span[1]/div[1]")))


                    my_dict['currentCompany'] = current_company.text

                data_list.append(my_dict)

            except TimeoutException as e:
                print(f"Timeout exception occurred in contact details: {e}")
                # Continue to the next iteration
                continue

            finally:
                # Close the new window
                driver.close()

                # Switch back to the original window
                driver.switch_to.window(driver.window_handles[0])

        except TimeoutException as e:
            print(f"Timeout exception occurred in profile element: {e}")
            # Continue to the next iteration
            continue

        except NoSuchElementException as e:
            print(f"Element not found exception occurred: {e}")
            # Continue to the next iteration
            continue
    # Maximum number of scroll attempts
    # max_scroll_attempts = 10

    # # Counter for scroll attempts
    # scroll_attempt = 0

    # # Flag to track whether the element is found
    # element_found = False
    # # Click 'Next' button to go to the next page
    # while scroll_attempt < max_scroll_attempts:
    #     try:
    #         # Attempt to find the element
    #         next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
    #         next_button.click()

    #         # If the element is found, break out of the loop
    #         element_found = True
    #         break
    #     except NoSuchElementException:
    #         # If the element is not found, scroll down and try again
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         scroll_attempt += 1
    # if element_found:
    #    print("Element found!")
    # # Perform actions on the element if needed
    # else:
    #    print("Element not found after scrolling to the end of the page.")
    #    driver.close()
  

    
# Save the dictionary as a JSON file
try:
    with open(json_file_path, 'r') as existing_file:
        existing_data = json.load(existing_file)
except FileNotFoundError:
    existing_data = []

existing_data.extend(data_list)

with open(json_file_path, 'w') as json_file:
    json.dump(existing_data, json_file)

# Close the browser
driver.quit()
