from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import obsws_python as obs
import time

# Program start
meet_link = input("Enter meet link: ")

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
    time.sleep(5)  # Adjust the wait time as needed

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

def is_access_granted():
    # Define a condition that checks for access to the Google Meet meeting
    return "call_end" in driver.page_source

def check_join():
    # Check if the bot is in the meeting some seconds later
    while not (is_access_granted()):
        time.sleep(5)

    print("In the call")

def mute_mic():
    mic_button = driver.find_elements(By.XPATH, '//div[@data-is-muted="false"]')[0]
    mic_button.click()

def turn_cam():
    # cam_button = driver.find_element()
    cam_button = driver.find_elements(By.XPATH, '//div[@data-is-muted="false"]')[1]
    cam_button.click()

def record_meet():
  obs_server_ip = 'localhost'
  obs_server_port = 4455
  obs_server_password = 'YRRhHglb6RhyMT5H'

  # pass conn info if not in config.toml
  cl = obs.ReqClient(host=obs_server_ip, port=obs_server_port, password=obs_server_password, timeout=3)

  input_list = cl.get_input_list()


  primary_source = ""
  for input in input_list.inputs:
    # print(input["unversionedInputKind"])
    if (input["unversionedInputKind"] == "pipewire-desktop-capture-source") or (input["unversionedInputKind"] == "monitor_capture"):
      primary_source = input["inputName"]
  
  # Quit if no selected source
  if primary_source == "":
    print("No selected source")
    exit()

  # souce status
  source_active = cl.get_source_active(input_list.inputs[2]["inputName"])
  for keys in source_active.attrs():
    print(keys + " = " + str(getattr(source_active, keys)))

  cl.start_record()
  
  while True:
    # Check if the meeting has ended by examining the page's elements
    if 'Meeting has ended' in driver.page_source:
        break

    # Check if the meeting has ended by examining the page's elements
    if 'No one else is in this meeting' in driver.page_source:
        break

    # Check if you've been kicked out by examining the page's elements
    if "You've been removed from the meeting" in driver.page_source:
        break

    time.sleep(5)  # Check conditions every 5 seconds


  cl.stop_record()

start_session()
mute_mic()
turn_cam()
ask_to_join()
check_join()
record_meet()
driver.close()