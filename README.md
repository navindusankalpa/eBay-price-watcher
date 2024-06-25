# eBayPriceWatcher

**eBayPriceWatcher** is a Python script that monitors eBay product prices and sends notifications when prices change. Simply add product links and target prices, and the script will keep you updated on any fluctuations. Perfect for bargain hunters and collectors.

## Features

- Track Multiple Products: Store multiple eBay product links and their target prices.
- Price Monitoring: Regularly checks the current price of each stored product link.
- Notifications: Sends a notification if the price of any tracked product changes.
- Easy Setup: Simple and straightforward configuration to get started quickly.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Navindu-Karunarathne/eBay-price-watcher.git

2. Navigate to the project directory:
   ```bash
   cd eBay-price-watcher

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt   

6. Navigate to the source folder:
   ```bash
   cd src

8. Run menu.py:
   ```bash
   python3 menu.py

9. **Add products**

      ![image](https://github.com/Navindu-Karunarathne/eBay-price-watcher/assets/86160907/766a3dd6-4405-46a2-b5b3-79b306281639)
      Select 1

      ![image](https://github.com/Navindu-Karunarathne/eBay-price-watcher/assets/86160907/8d636ba0-fff8-4640-b4cb-8b19381b7740)
      Enter a product link (it must be a shortened link)

      ![image](https://github.com/Navindu-Karunarathne/eBay-price-watcher/assets/86160907/793b2997-cead-422c-b8ef-e4782a3c146f)
      Enter notification trigger price.

10. **Get cookies**
      Go to https://ebay.com and copy site cookies.
      ![Screenshot (205)](https://github.com/Navindu-Karunarathne/eBay-price-watcher/assets/86160907/db2f59c2-68d9-493c-a849-5b4a16ca2d4d)

11. **Add cookies to the app**
       Enter the name of the first cookie.
       ![image](https://github.com/Navindu-Karunarathne/eBay-price-watcher/assets/86160907/4edd7f18-0a1b-4e4b-8408-4e8813d52e5b)

    Enter the value of the given cookie. And continue adding cookies.

11. **Run app**
       Choose 3 from the menu and run the app.
       ![image](https://github.com/Navindu-Karunarathne/eBay-price-watcher/assets/86160907/724a77a4-ce52-4aa8-81fe-c61ebefcea22)

## Additionally

You can edit app looping interval and product looping interval in <i>env.json</i> file. Default time is good to protect you from **getting banned**.



   




