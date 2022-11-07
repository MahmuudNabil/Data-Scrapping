#import libraries 
import requests
from bs4 import BeautifulSoup
import pandas as pd

class RightMoveScraper:
    results = []
    
    def fetch(self, url):
        print('HTTP GET REQUEST TO URL:  %s' %url)
        response =requests.get(url)
        print('Status Code : %s'%response.status_code)
        return response


    def parse(self, response):
        soup = BeautifulSoup(response.text , 'html.parser')
        
        title = [title.text.strip() for title in soup.find_all('h2', {'class':'propertyCard-title'})]
        address = [address.span.text for address in soup.find_all('address', {'class': 'propertyCard-address'})]
        description = [desc.text for desc in soup.find_all('span',{'itemprop':'description'})]
        price = [price.text.strip() for price in soup.find_all('div' , {'class' : 'propertyCard-priceValue'})]
        date =[date.text.split(' ')[-1] for date in soup.find_all('span' ,{'class' : 'propertyCard-contactsAddedOrReduced'})]
        seller = [seller.text.split('by')[-1] for seller in soup.find_all('span' , {'class': 'propertyCard-branchSummary-branchName'})]
        image = [img['src']for img in soup.find_all('img' , {'itemprop':'image'})]
        
        for index in range(0 , len(title)):
            self.results.append( {'Title' : title[index],
                                 'Address' : address[index],
                                 'Description' : description[index],
                                 'Price' : price[index],
                                 'Date' : date[index],
                                 'Seller' : seller[index],
                                 'Image': image[index]})
        
    
    def to_csv(self):
        df = pd.DataFrame(self.results)
        df.to_csv("RightMove.csv", index = False)
        
        print('Stored results to "rightmove.csv"')
    
    def run(self):
       # response = self.fetch('https://www.rightmove.co.uk/property-for-sale/London.html')
        #with open('res.html' , 'w') as html_file:
         #   html_file.write(response.text)
        '''
        html = ''
        with open('res.html' , 'r')as html_file:
            for line in html_file:  
                html += html_file.read()
        '''
        for page in range(0,20):
            page_num = page + 24
            url = f'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E93917&index={page_num}&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords='
            print(url)
            
            response = self.fetch(url)
            self.parse(response)
            self.to_csv()


if __name__ == '__main__':
    scraper = RightMoveScraper()
    scraper.run()
