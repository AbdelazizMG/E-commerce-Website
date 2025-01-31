from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import sys,re,time,json
import pandas as pd

class JumiaPageObjectModel(webdriver.Chrome):
     def __init__(self) -> None:
        super(JumiaPageObjectModel,self).__init__()
        self.implicitly_wait(1.5)
        self.maximize_window()

        #Create Chrome options
        self.chrome_options = Options()

        #self.chrome_options.add_argument("--headless")  
        self.data : list = []

        self.product : dict = {
            'description' : '',
            'price'       : '',
            'image'       : '',
            'category'    : ''
        }

        
        self.videos = []

     def landfirstpage(self) -> None:
        '''
        Function to land the first page of the website
        '''
        self.get("https://www.jumia.com.eg/")
        close_button = self.find_element(by= By.XPATH , value= "//button[@class='cls']")
        close_button.click()

     def search(self, target : str ) -> None:
        '''
        Function to search for a certain target
        '''
        search_bar = self.find_element(by= By.XPATH , value= "//input[@id='fi-q']")
        search_bar.send_keys(target)
        search_bar.send_keys(Keys.RETURN)

     def scrapProductsName(self) -> list:
         '''
         Function to get the product name from the information box
         '''
         products_name_obj : list = self.find_elements(by= By.XPATH , value= "//h3[@class='name']")

         products_name_text : list = []
         for product in products_name_obj:
             products_name_text.append(product.text)

         return products_name_text
    
     def scrapProductsPrice(self) -> list:
         '''
         Function to get the product price from the information box
         '''
         products_price_obj = self.find_elements(by= By.XPATH , value= "//div[@class='prc']")

         products_price_text : list = []
         for product in products_price_obj:
             products_price_text.append(product.text)

         return products_price_text
     
     def scrapProductsImage(self) -> list :
         '''
         Function to scrap the product image from the information box
         '''
         images : list = self.find_elements(by= By.XPATH , value= "//img[@class='img']")
         images_url : list = []

         for image in images:
            image_url = image.get_attribute("data-src") or image.get_attribute("src")
            images_url.append(image_url)

         return images_url

     def getNextPage(self) -> bool:
         '''
         Function to get the next page
         '''
         success : bool = True
         try:
            next_page_button = self.find_element(by= By.XPATH , value= "//a[@aria-label='Next Page']")
            ActionChains(self).move_to_element(next_page_button).click().perform()

         except Exception as e:
             success = False

         return success


if __name__ == "__main__":
    t = JumiaPageObjectModel()
    t.landfirstpage()
    t.search('Electronics')
    time.sleep(3)
    names = t.scrapProductsName()
    #print(names)
    prices = t.scrapProductsPrice()
    print('-----------------')
    #print(prices)
    images = t.scrapProductsImage()
    print('------------------')
    #print(images)

    for index in range(len(names)):
        t.product['description'] = names[index]
        t.product['price']       = prices[index]
        t.product['image']       = images[index]
        t.product['category']    = 'Electronics'

        t.data.append(t.product)
        t.product = {}

    #print(data)

    with open('data.json','w') as json_file:
        json.dump(t.data,json_file,indent=4)

    while(t.getNextPage() == True):
        names = t.scrapProductsName()
        prices = t.scrapProductsPrice()
        images = t.scrapProductsImage()
        for index in range(0,len(names)):
            t.product['description'] = names[index]
            t.product['price']       = prices[index]
            t.product['image']       = images[index]
            t.product['category']    = 'Electronics'

            t.data.append(t.product)
            t.product = {}

        with open('data.json','w') as json_file:
            json.dump(t.data,json_file,indent=4)

    time.sleep(100000)