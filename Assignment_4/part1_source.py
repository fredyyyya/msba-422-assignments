"""
452 Assignment 4 - Part 1 Code
Shaolong (Fred) Xue
"""

from bs4 import BeautifulSoup
import requests
import time

session = requests.session()

user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
username = "HalaMadrid"
password = "ynadamas!"
login_url = "https://www.planespotters.net/user/login"
profile_url = "https://www.planespotters.net/member/profile"

###### Question 1 ######
## 1. Access login page (GET)
page = session.get(login_url, headers=user_agent)
soup = BeautifulSoup(page.content, 'html.parser')

## 2. Read and store cookies
cookies = page.cookies.get_dict()
print("Old Cookies:")
print(cookies)

## 3. Parse the response and read the value of input fields
input1 = soup.select("div.planespotters-form input[name=csrf]")[0]
input2 = soup.select("div.planespotters-form input[name=rid]")[0]

csrf = input1.get('value')
rid = input2.get('value')

payload = {"username": "HalaMadrid",
            "password": "ynadamas!",
            "csrf": csrf,
            "rid": rid}

###### Question 2 ######
## 1. Login into the website (POST)
time.sleep(3)

page2 = session.post(login_url, data=payload,
                        headers=user_agent,
                        cookies=cookies)

new_cookies = session.cookies.get_dict()
print("New Cookies:")
print(new_cookies)

###### Question 3 ######
## 1. Add cookies from new response to previous cookies
all_cookies = {**cookies, **new_cookies}

###### Question 4 ######
## 1. Verify login status 
time.sleep(3)
profile_page = session.get(profile_url, cookies=new_cookies,
                            headers=user_agent)

###### Question 5 ######
## 1. Print BeautifulSoup profile page object
soup3 = BeautifulSoup(profile_page.content, 'html.parser')
print(soup3.prettify())

## 2. All cookies
print("All cookies")
print(all_cookies)

## 3. A boolean check of my username

if "HalaMadrid" in soup3.get_text():
    print("True (Login Successful)")
else:
    print("False (Login Failed)")
