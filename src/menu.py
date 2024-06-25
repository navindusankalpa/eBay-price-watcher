import json
import os
import app
import asyncio
class Configure:
    def __init__(self):
        self.links_file = ".\\json\\links.json"
        self.cookies_file = ".\\json\\cookies.json"
        self.product_file = ".\\json\\product.json"

    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def write_json(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def append_to_json(self, file_path, new_data):
        data = self.read_json(file_path)
        if isinstance(data, list):
            data.append(new_data)
        elif isinstance(data, dict):
            data.update(new_data)
        else:
            data = [data, new_data]
        self.write_json(file_path, data)

    def save_links(self, links):
        try:
            self.append_to_json(self.links_file, links)
            print("Links appended successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def save_products(self, products):
        try:
            self.append_to_json(self.product_file, products)
            print("Products appended successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def add_products(self):
        os.system('cls')
        print("Remember to add shortned URLs of products. Otherwise the app might break.\nGo to https://www.shorturl.at/\n")
        products = {}
        while True:
            product_link = input("Enter product link (or enter 0 to exit): ")
            if product_link == "0":
                break
            product_trg_price = input("Enter trigger value for the product (enter 0 to skip): ")
            if product_trg_price == "0":
                products[product_link] = "null"
            else:         
                products[product_link] = product_trg_price
        if products:
            self.save_products(products)

    def save_cookies(self, cookies):
        try:
            self.append_to_json(self.cookies_file, cookies)
            print("Cookies appended successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def add_links(self):    
        links = []
        while True:
            input_link = input("Enter eBay product URL, enter 0 when finished: ")
            if input_link != "0":
                if input_link == "":
                    continue
                links.append(input_link.strip())
            else:
                break
        if links:
            self.save_links(links)

    def add_cookies(self):
        cookies = {}
        while True:
            cookie_name = input("Enter cookie name (or enter 0 to exit): ")
            if cookie_name == "0":
                break
            cookie_value = input(f"Enter value of cookie {cookie_name}: ")            
            cookies[cookie_name] = cookie_value
        if cookies:
            self.save_cookies(cookies)
            
    async def run_app(self):
        app_obj = app.App()
        await app_obj.start_requesting()

    async def show_menu(self):
        os.system('cls')
        while True:
            menu_message = "\n1. Add products\n2. Add cookies\n3. Run app\n4. Exit\nEnter your choice >>> "
            try:
                input_cmd = input(menu_message)
                if input_cmd == "1":
                    self.add_products()
                elif input_cmd == "2":
                    self.add_cookies()
                elif input_cmd == "3":
                    await self.run_app()
                elif input_cmd == "4":
                    exit()
                else:
                    print("Enter a valid command.")
            except ValueError:
                print("Invalid input. Please enter a number.")
async def main():
    config = Configure()
    await config.show_menu()

if __name__ == "__main__":
    asyncio.run(main())
