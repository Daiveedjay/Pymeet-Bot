from selenium import webdriver
# Imports the main WebDriver class from the Selenium package, which allows for controlling and automating web browsers.

from selenium.webdriver.common.by import By
# Imports the 'By' class, which provides methods to select elements in web pages (e.g., by ID, class name, tag name, etc.).

from selenium.webdriver.chrome.options import Options
# Imports the 'Options' class specific to the Chrome WebDriver, which allows for customizing and setting preferences for the Chrome browser.

from selenium.webdriver.support.ui import WebDriverWait
# Imports the 'WebDriverWait' class, which allows for setting explicit waits, ensuring that certain conditions are met before proceeding.

from selenium.webdriver.support import expected_conditions as EC
# Imports the 'expected_conditions' module and renames it as 'EC'. This module provides a set of predefined conditions to use with WebDriverWait.

import obsws_python as obs
# Imports the 'obsws_python' module and renames it as 'obs'. This module provides functionalities to interact with the OBS Studio WebSockets plugin.

import time
# Imports the built-in 'time' module, which provides various time-related functions, like sleep.

# Program start
meet_link = input("Enter meet link: ")
meet_time = int(input("Enter meet time in minutes. E.g 20, 30: "))

# Initialize the Chrome WebDriver
opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument("--mute-audio")
# opt.add_argument("--disable-notifications")
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {
 
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(options=opt)

def start_session():
    # Navigate to a website
    driver.get(meet_link)

    # Wait for the page to load
    time.sleep(10)  # Adjust the wait time as needed

    # Find the input element for your name
    name_input = driver.find_element(By.TAG_NAME, "input")  # Assuming the input field has an ID attribute

    # Enter your name into the input field
    name_input.send_keys("PyMeet Bot")

def ask_to_join():
    # Ask to Join meet
    time.sleep(5)
    print("Asking to join")
    ask_btn = driver.find_element(By.XPATH,
        "//span[contains(text(),'Ask to join')]")
    ask_btn.click()
    print("Asked to join")

def is_access_granted(driver):
    # Define a condition that checks for access to the Google Meet meeting
    return "uqc-exyz-iic" in driver.page_source or "Asking to be let in" in driver.page_source

def check_join():
    # Check if the bot is in the meeting some seconds later
    element = WebDriverWait(driver, 10).until(
        EC.any_of(is_access_granted)
    )

    if element:
        print(element)
        print("In the call")

def mute_mic():
    mic_button = driver.find_elements(By.XPATH, '//div[@data-is-muted="false"]')[0]
    mic_button.click()

def turn_cam():
    # cam_button = driver.find_element()
    cam_button = driver.find_elements(By.XPATH, '//div[@data-is-muted="false"]')[1]
    cam_button.click()

def record_meet(record_time):
#   obs_server_ip = '192.168.12.168'
  obs_server_ip = 'localhost'
  obs_server_port = 4455
  obs_server_password = 'YRRhHglb6RhyMT5H'

  # pass conn info if not in config.toml
  cl = obs.ReqClient(host=obs_server_ip, port=obs_server_port, password=obs_server_password, timeout=3)

  input_list = cl.get_input_list()

  primary_source = ""
  for input_l in input_list.inputs:
    print(input_l)
    if input_l["unversionedInputKind"] == "monitor_capture":
      primary_source = input_l["inputName"]
  
  # Quit if no selected source
  if primary_source == "":
    print("No selected source")
    exit()

  # souce status
  source_active = cl.get_source_active(input_list.inputs[2]["inputName"])
  for keys in source_active.attrs():
    print(keys + " = " + str(getattr(source_active, keys)))

  cl.start_record()
  time.sleep(record_time)
  cl.stop_record()

start_session()
mute_mic()
turn_cam()
ask_to_join()
check_join()
record_meet(meet_time * 60)
driver.close()