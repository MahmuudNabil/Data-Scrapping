import requests 
from bs4 import BeautifulSoup
import pandas as pd 
import time

links_list = []
data_list = []
base_url = 'https://www.thewhiskyexchange.com/'
headers ={
         'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

def request(page_num):
    print (f'page {page_num}')
    url = f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={page_num}'

    response = requests.get(url)
    soup = BeautifulSoup(response.content , 'html.parser')

    return soup.find_all('li' ,{'class' : 'product-grid__item'})


def parse(whisky):
    for item in whisky:
        link = item.find('a' , {'class' : 'product-card'})['href']
        links_list.append(base_url + link)

    for link in links_list:
        response2 = requests.get(link , headers = headers)
        soup2 = BeautifulSoup(response2.content , 'html.parser')

        title = soup2.find('h1' , {'class' : 'product-main__name'}).text.strip()
        title = title.split("\n")[0]
        price = soup2.find('p' ,{'class' : 'product-action__price'}).text.strip()[1:]
        try:
            rating = soup2.find('span' , {'class' : 'star-rating'}).text.strip()
        except : 
            rating ='No Ratting'
    
        data = {
            'title' : title,
            'rating': rating,
            'price' : price
        }
        data_list.append(data)


def output():
    df = pd.DataFrame(data_list)
    df.to_csv('whisky.csv' , index = False)
    print('Saved to csv file! ')

    page_num = 1
    page_num = 1


    page_num = 1

page_num = 1

for page_num in range(1,3,1):
    whisky_list = request(page_num)
    time.sleep(2)
    parse(whisky_list)
        
print('Completed Total Whiskies is : ' , len(data_list))
output()

