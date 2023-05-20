"""
452 - Assignment 4 - Part 2 Code
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

path = "/Users/shaolongxue/Documents/_Misc./chromedriver"
driver = webdriver.Chrome(executable_path=path)

#driver.implicitly_wait(10)
#driver.set_script_timeout(120)
#driver.set_page_load_timeout(10)

########## Question 1 ##########
def question_1():
    driver.get("https://google.com")

    search1 = driver.find_element(By.NAME, "q")
    search1.send_keys("askew\n")

    time.sleep(5)

    driver.get("https://google.com")
    search2 = driver.find_element(By.NAME, "q")
    search2.send_keys("google in 1988\n")

    time.sleep(5)

#question_1()

########## Question 2 ##########
def question_2():
    driver.get("https://bestbuy.com")
    time.sleep(2)

    ## search for "Deal of the Day" buttom and click
    inp_dotd = driver.find_element(By.LINK_TEXT, "Deal of the Day")
    inp_dotd.click()
    time.sleep(2)

    ## search for countdown timer and print 
    inp_timer = driver.find_element(By.ID, "countdown").text
    inp_timer = ''.join(inp_timer.splitlines())
    print("Countdown")
    print(inp_timer)
    time.sleep(2)

    ## search for item url and click
    inp_item = driver.find_element(By.CLASS_NAME, "wf-offer-link")
    inp_item.click()
    time.sleep(2)

    ## search for review and click
    inp_review = driver.find_element(By.CLASS_NAME, "user-generated-content-ratings-and-reviews")
    inp_review.click()
    time.sleep(5)

    ## save the html page
    with open("/Users/shaolongxue/Documents/MSBA/2_Winter_Quarter/422_DDR/Assignment_4/bestbuy_deal_of_the_day.htm", "w") as f:
        f.write(driver.page_source)

#question_2()
