#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 15:39:38 2021

@author: andrew close
"""
# Import Relevant Packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# This is the path to the Selenium web drive for Chrome located on the local machine
webdriver_path = r'/Users/andrewclose/bin/chromedriver'

# This is the URL for the list of integrations maintained on SourceForge. 

# Sometimes the SourceForge server won’t serve up the next page and quits with no indication.
# This program support a restart option to create a URL as per the following example: 
# https://sourceforge.net/software/product/Slack/integrations/?page=47
# The output file is opened in append mode to pick up where the last run stopped.
# Note: SourceForge currently lists 20 integrations per web page.

vendor = input("Enter \"S\" for Slack or \"M\" for Microsoft Teams: ").upper()
while((vendor != "S") and (vendor != "M")):
    vendor = input("Enter \"S\" for Slack or \"M\" for Microsoft Teams: ").upper()

# Build the base URL used if no restart is required.
if vendor == "S":
    url =" https://sourceforge.net/software/product/Slack/integrations/"
else:
    url ="https://sourceforge.net/software/product/Microsoft-Teams/integrations/"
    
restart = input("Do you want to restart at a specific page? (Y/N) ").upper()  

# If restarting append the page number to the base URL and open the output file in append mode.    
if (restart == "Y"):
    page = input("What page do you want to restart at? ")
    url = url + "?page=" + str(page)
    if vendor == "S":
        f = open("slack integrations.txt", "a")
    else:
        f = open("teams integrations.txt", "a")
else:
    if vendor == "S":
        f = open("slack integrations.txt", "w")
    else:
        f = open("teams integrations.txt", "w")
    
# Path to webdriver
browser = webdriver.Chrome(webdriver_path)

# URL to scrape
browser.get(url)
 
# Find all the integration names on the webpage  — they are in an h3 inside a link (HTML a)
# Advance through each page printing names of integrations

while True:
    # Find the interation names via xpath
    integs = browser.find_elements_by_xpath("//a/h3")
    
    # print the content of those h3s
    for integ in integs:
        f.write(integ.get_attribute("innerHTML"))
        f.write("\n")
    
    # Get the button by xpath
    next_buttons = browser.find_elements_by_xpath("//li[@class='pagination-next ']/a")
   
    if len(next_buttons) < 1:
        # If there are no more pages then break out of the loop
        break
    else:
        # Otherwise go to the next page by sending the button a click
        status = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Next'))).click()
        print(f"Return status from next webpage: {status}")
# That's all!
browser.quit()
f.close()