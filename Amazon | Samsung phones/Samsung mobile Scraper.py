import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.amazon.eg'
headers =  {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US,en;q=0.9,ar;q=0.8'
}
link_list =[]
phone_data =[]

def request(page_num):
    print(f'page : {page_num}')
    url =f'https://www.amazon.eg/s?k=samsung&i=electronics&rh=n%3A21832883031&page={page_num}&language=en&qid=1658371427&ref=sr_pg_{page_num}'
    response = requests.get(url , headers)
    print('Connection Status : ' , response.status_code)
    soup = BeautifulSoup(response.content , 'html.parser')
    
    return soup.find_all('div' , {'class' : 'a-spacing-base'})

def parse (phone):
    for item in phone:
        link = item.find('a' ,{'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        link_list.append(base_url + link)

    print(len(link_list))

    for phone_link in link_list:
        session = requests.Session()
        response2 = session.get(phone_link , headers=headers)

        print('Connection Status 2 : ' , response2.status_code)

        soup2 = BeautifulSoup(response2.content , 'html.parser')
        try:
           title = soup2.find('span' ,{'id' : 'productTitle'}).text.strip()
           price = soup2.find('span' , {'class' : 'a-offscreen'}).text.strip()
           rating = soup2.find('span' , {'class' : 'a-icon-alt'}).text.strip()

           print(phone_link)
           print(title ,'| ' , price , '| ' , rating ,'\n')

        except:
            print(phone_link)
            print('NO Data \n')

        head_list =['Title' , 'Price' , 'Rating']
        data_list =[title, price, rating]
        table_ph = soup2.find('table' , {'class' : 'a-normal a-spacing-micro'})

        head_data = table_ph.find_all('td' , {'class' : 'a-span3'})
        rows_data = table_ph.find_all('td' , {'class' : 'a-span9'})


        for head in head_data:
            head_list.append(head.text.strip())

        for data in rows_data:
            data_list.append(data.text.strip())
    
        phone_details = dict( zip(head_list,data_list) )
        phone_data.append(phone_details)
 


for num in range(1,5,1):
    phone = request(num)
    parse(phone)

df = pd.DataFrame(phone_data)
print(df)

df.to_csv('Samsung_phones.csv',index = False)
df.to_excel('Samsung_phones.xlsx' , index= False)
df.to_json('Samsung_phones.json')
