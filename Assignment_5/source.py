"""
422 - Assignment 5 
Shaolong Xue
"""

import mysql.connector
import warnings
import requests
import json
import time
import re
import csv
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

### Question 2
url = "https://api.github.com/repos/apache/hadoop/contributors?&per_page=150"
username = 'fredyyyya'

# generated from my github account
token = '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'
user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Authorization': str(token)} 

# GET request to the url
page = requests.get(url, headers = user_agent, auth = (username, token))
time.sleep(2)
doc = BeautifulSoup(page.content, 'html.parser')
contributors = json.loads(str(doc))

# gather a list of urls of the 100 contributors
url_list = []

for i in range(100):
    user_url = contributors[i]['url']
    url_list.append(user_url)

### Question 3
def extract_info(i):
    # get each person's url
    contributor_url = url_list[i]

    # GET request to get info on a specific user url
    contributor_page = requests.get(contributor_url, headers = user_agent, auth = (username, token))
    contributor_doc = BeautifulSoup(contributor_page.content, 'html.parser')
    contributor_info = json.loads(str(contributor_doc))

    # store needed info into variables
    login = contributor_info['login']
    id = contributor_info['id']
    location = contributor_info['location']
    email = contributor_info['email']
    hireable = contributor_info['hireable']
    bio = contributor_info['bio']
    twitter_username = contributor_info['twitter_username']
    public_repos = contributor_info['public_repos']
    public_gists = contributor_info['public_gists']
    followers = contributor_info['followers']
    following = contributor_info['following']
    created_at = contributor_info['created_at']

    # fix the format of "created_at" for SQL later
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})Z')
    match = pattern.match(created_at)
    date, time = match.groups()
    created_at_fixed = f"{date} {time}"

    # combine info into a dictionary
    info = {
        'login': login,
        'id': id,
        'location': location,
        'email': email,
        'hireable': hireable,
        'bio': bio,
        'twitter_username': twitter_username,
        'public_repos': public_repos,
        'public_gists': public_gists,
        'followers': followers,
        'following': following,
        'created_at': created_at_fixed
    }

    return info

top_100 = []

# I've already run the for loop below and stored the result in "top_100".
# These two lines are commented out so I don't run 100 GET requests again. 

"""
for i in range(100):
    time.sleep(5)
    top_100.append(extract_info(i))
"""

# save the top_100 output to a local csv file
# running the results locally could help speed up any processing without sending many requests again.

file = open("top_100.csv", "w")
writer = csv.writer(file)
writer.writerow(['id', 'login', 'location', 'email', 'hireable', 'bio', 
            'twitter_username', 'public_repos', 'public_gists', 'followers', 'following', 'created_at'])
for dict in top_100:
    writer.writerow(dict.values())
file.close()

### Question 4 
def question_4():
    ## connect to MySQL server
    conn = mysql.connector.connect(host = 'localhost',
                                    database = 'ucdavis',
                                    user = 'root',
                                    password = 'HalaMadrid!9248')

    ## create a cursor object to execute SQL commands
    cursor = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS top_100_contributors (
            id INT PRIMARY KEY,
            login VARCHAR(255),
            location VARCHAR(255),
            email VARCHAR(255),
            hireable BOOLEAN,
            bio VARCHAR(255),
            twitter_username VARCHAR(255),
            public_repos INT,
            public_gists INT,
            followers INT,
            following INT,
            created_at DATETIME
    )
    """

    cursor.execute(query)

    ## store the data into SQL
    for user in top_100:
        insert_query = """
        INSERT INTO top_100_contributors (
            id, login, location, email, hireable, bio, 
            twitter_username, public_repos, public_gists, followers, following, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user['id'],
            user['login'],
            user['location'],
            user['email'],
            user['hireable'],
            user['bio'],
            user['twitter_username'],
            user['public_repos'],
            user['public_gists'],
            user['followers'],
            user['following'],
            user['created_at']
        )
        cursor.execute(insert_query, values)

    # commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# question_4()

"""
The reason behind the data type I chose for each variable is straightforward. 
Strings to varchar, numbers to integer, etc. 
I chose 'id' as the Primary Key because (1) it's unique for each user and (2) it can be used to easily connect
with other APIs, like the main API we started the assignment with. 
"""

### Question 5 

# to optimize search speed, I can index the three target columns so binary search can be applied on them for faster searching. 
# I can do this simply by adding an INDEX command for each column. They are the bottom three lines below. 

query = """
        CREATE TABLE IF NOT EXISTS top_100_contributors (
            id INT PRIMARY KEY,
            login VARCHAR(255),
            location VARCHAR(255),
            email VARCHAR(255),
            hireable BOOLEAN,
            bio VARCHAR(255),
            twitter_username VARCHAR(255),
            public_repos INT,
            public_gists INT,
            followers INT,
            following INT,
            created_at DATETIME,
            INDEX(login),
            INDEX(location),
            INDEX(hireable)
    )
    """