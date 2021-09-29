import os
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from settings import*
from twilio.rest import Client
import time

timer = 1 #Number of seconds before next command

driver = webdriver.Chrome(executable_path="Drivers/chromedriver")

driver.get("https://www.childsmath.ca/childsa/forms/main_login.php")

driver.find_element_by_id("submit").click()
time.sleep(timer)

print("Finding Username Field...")
username = driver.find_element_by_id("user_id")
print("Username Field Found. Inputting Username....")
username.send_keys(USERNAME)
time.sleep(timer)

print("Finding Password Field...")
mcmaster_password = driver.find_element_by_id("pin")
print("Password Field Found. Inputting Password....") 
mcmaster_password.send_keys(PASSWORD)
time.sleep(timer)

print("Logging In...")
driver.find_element_by_id("submit").click()
time.sleep(timer)

print("Clicking on Math 2Z03 course")
driver.find_element_by_link_text("Math 2Z03").click()

print("Checking for Open Assignments")

open_assignments = []

for i in range(1,14):
    num = str(i)
    try:
        driver.get("https://www.childsmath.ca/childsa/forms/2zStuff/onlineform_2.php?assign=" + num)
        assert_problem = driver.find_element_by_class_name("FORMfieldsText")
        title = (driver.title).split("Answer")[0]
        open_assignments.append(title)
    except NoSuchElementException:
        continue
text_to_body = "You have " + str(len(open_assignments)) + " open assignment(s): " + str(open_assignments)
print(text_to_body)

client = Client(account_sid, auth_token) 
message = client.messages.create(  
    messaging_service_sid=SID, 
    body=text_to_body,      
    to=NUMBER 
) 
 
print(message.sid)
driver.quit