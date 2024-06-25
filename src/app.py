import data_reader as dr
import requests
from bs4 import BeautifulSoup
import re
import time
import os
import notification
#from win11toast import toast

class App:

    def __init__(self):
        self.data_reader_obj = dr.DataReader()
        self.cookies = self.data_reader_obj.get_cookies()
        self.product = self.data_reader_obj.get_products()
        self.env_time = self.data_reader_obj.get_env()

        self.notification_obj = notification.Notifier()
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)

    def convert_price_to_float(self, price_str):
        cleaned_price_str = re.sub(r'[^\d.]', '', price_str)
        try:
            price_float = float(cleaned_price_str)
            return price_float
        except ValueError:
            print(f"Error converting price: {price_str}")
            return None

    async def start_requesting(self):
        os.system('cls')
        print("App is running press ^C to exit...")
        while(True):
            for product_link, trigger_price in self.product.items():
                try:
                    responce = requests.get(product_link)
                    if responce.status_code == 200:
                        soup = BeautifulSoup(responce.content, 'html.parser')
                        price_container = soup.find('div', class_='x-price-primary')
                        title_element = soup.find('title')
                        product_title = ""
                        if title_element:
                            product_title = title_element.text.strip()
                        if price_container:
                            price_tag = price_container.find('span', class_='ux-textspans').text.strip()
                            if price_tag:
                                price = self.convert_price_to_float(price_tag)
                                if trigger_price != "null":
                                    try:
                                        trigger_price_float = float(trigger_price)
                                        if trigger_price_float > price:
                                            await self.notification_obj.show_notification(True, product_title, price_tag, product_link)
                                            #toast('Price Dropped', 'Price of ' + product_title + ' dropped to ' + price_tag, icon=self.notification_icon_path, buttons=[{'activationType': 'protocol', 'arguments': product_link, 'content': 'View Product'},
                                            #                                            {'activationType': 'protocol', 'arguments': 'http:Dismiss', 'content': 'Dismiss'}])
                                            
                                        elif trigger_price_float < price:
                                            await self.notification_obj.show_notification(False, product_title, price_tag, product_link)
                                            #toast('Price Rose', 'Price of ' + product_title + ' rose to ' + price_tag, icon=self.notification_icon_path, buttons=[{'activationType': 'protocol', 'arguments': product_link, 'content': 'View Product'},
                                            #                                            {'activationType': 'protocol', 'arguments': 'http:Dismiss', 'content': 'Dismiss'}])
                                    except ValueError:
                                        print(f"Invalid trigger price '{trigger_price}' for product '{product_link}'")
                            else:
                                print(f"Price is unreachable for product '{product_link}'")
                        else:
                            print("Price container not found!")
                    else:
                        print(f"Outgoing request error, status '{responce.status_code}'")
                except Exception as e:
                    print(f"Error: {e}")
                time.sleep(int(self.env_time['itemLoopInterval']))
            time.sleep(int(self.env_time['appLoopInterval']))