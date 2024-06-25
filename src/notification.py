#from win11toast import toast_async, clear_toast
import os
from noti import toast_async
class Notifier():
    def __init__(self):
        self.notification_icon_path = os.path.join(os.getcwd(), "logo.png")

    async def show_notification(self, is_dropped, product_title, price_tag, product_link):
        if(is_dropped):
            await toast_async('Price Dropped', 'Price of ' + product_title + ' dropped to ' + price_tag, icon=self.notification_icon_path, duration='short', buttons=[{'activationType': 'protocol', 'arguments': product_link, 'content': 'View Product'},
                                                                                        {'activationType': 'protocol', 'arguments': 'http:Dismiss', 'content': 'Dismiss'}])
        else:
            await toast_async('Price Rose', 'Price of ' + product_title + ' rose to ' + price_tag, icon=self.notification_icon_path, duration='short', buttons=[{'activationType': 'protocol', 'arguments': product_link, 'content': 'View Product'},
                                                                                        {'activationType': 'protocol', 'arguments': 'http:Dismiss', 'content': 'Dismiss'}])  