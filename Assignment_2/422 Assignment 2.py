# 422 Assignment 2

## Part 1 

from bs4 import BeautifulSoup
import requests
import re

def main():
    try:
        url= "https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390"
        headers = {'User-Agent': 'Mozilla/5.0'} # faking a browser
        page = requests.get(url, headers=headers)
        # Create a beautifulsoup object 
        soup = BeautifulSoup(page.text, 'lxml')

        # find the element that contains the current price
        current = soup.select('p.list-price > span:nth-child(3)')
        
        # find the element that contains the listing price
        listing = soup.select('p.final-price > span.sale-price > span:nth-child(4)')

        # prints the HTML content to the screen, striping all characters except the numbers and the decimal point
        for i in current:
            text = (re.sub("[\$,]", "" , i.text))
            print(text)

        for j in listing:
            text = re.sub("[\D]", "", j.text)
            text = re.sub("([0-9]{4})([0-9]{2})", "\g<1>.\g<2>", text)
            print(text)

    except:
        print("Problem with the connection...")

if __name__ == '__main__':
    main()

## Part 2

def main():
    try:
        url= "https://www.usnews.com/"
        headers = {'User-Agent': 'Mozilla/5.0'} # faking a browser
        page = requests.get(url, headers=headers)
        # Create a beautifulsoup object 
        soup = BeautifulSoup(page.text, 'lxml')

        # find the url of the top story
        top_story = soup.select_one('h3 > a')
        top_url = top_story['href']
        print(top_url)

        # print the url of the second current top stroy
        sec_story = soup.select_one('div:nth-child(2) > h3 > a')
        sec_url = sec_story['href']
        print(sec_url)

        # load the second top story
        page2 = requests.get(sec_url, headers=headers)
        soup2 = BeautifulSoup(page2.text, 'lxml')

        # find and print the header of the second top story
        title = soup2.find('h1')
        print(title.string)
        
        # find and main text body the second top story
        maintext = soup2.select('div.Raw-slyvem-0 > p')

        # using regex to select the first three sentences of the main text
        alltext = ""

        for i in maintext:
            if alltext == "":
                alltext = alltext + i.text
            else:
                alltext = alltext + " " + i.text
                
        first_3 = ' '.join(re.split(r'(?<=[.?!])\s', alltext)[:3])
        print(first_3)

    except:
        print("Problem with the connection...")

if __name__ == '__main__':
    main()