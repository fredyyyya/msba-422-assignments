"""
422 - Assignment 6 
Shaolong (Fred) Xue
"""
from pymongo import MongoClient

client = MongoClient("localhost", 27017)

##### Pokemon
db1 = client["samples_pokemon"]
pokemon = db1["samples_pokemon"]
projection = {"name": 1}

## Question 1
## Name and ID of all Pokemon whose 'candy_count' is >= 36 (my BD is June 30)

bd = 36
query1 = {"candy_count": {"$gte": bd}}
results1 = pokemon.find(query1, projection)
for result in results1:
    print(result)

## Question 2
## Name and ID of all Pokemon whose 'num' = '006' or '030'

query2 = {"$or": [{"num": "006"}, {"num": "030"}]}
results2 = pokemon.find(query2, projection)
for result in results2:
    print(result)

##### Crunchbase
db2 = client.crunchbase
crunchbase = db2.crunchbase_database

## Question 3
## Name and ID of all companies whose 'tag_list' includes 'text'

word = "text"
query3 = {"tag_list": {"$regex": word, "$options": "i"}} # options as i for case-insensitive
results3 = crunchbase.find(query3, projection)
for result in results3:
    print(result)

## Question 4
## Name, Twitter username, and ID of all companies founded between 2000 and 2010 or use gmail
projection2 = {"name": 1, "twitter_username" : 1}
email = "@gmail.com"
query4 = {"$or": 
        [
        {"found_year": {"$gte": 2000, "$lte": 2010}},
        {"email_address": {"$regex": email}}
        ]}
results4 = crunchbase.find(query4, projection2)
for result in results4:
    print(result)

