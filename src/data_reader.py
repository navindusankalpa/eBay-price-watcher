import json

class DataReader:
    def __init__(self):        
        self.cookies_file = ".\\json\\cookies.json"
        self.product_file = ".\\json\\product.json"
        self.env_file = ".\\json\\env.json"

    def get_products(self):
        try:
            with open(self.product_file, 'r') as file:
                products = json.load(file)
            return products
        except FileNotFoundError:
            print(f"Error: JSON file '{self.product_file}' not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{self.product_file}': {e}")
            return {}
        
    def get_env(self):
        try:
            with open (self.env_file, "r") as file:
                env = json.load(file)
                return env
        except FileNotFoundError:
            print(f"Error: JSON file '{self.env_file}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in '{self.env_file}'.")
    
    def get_cookies(self):
        try:
            with open(self.cookies_file, 'r') as file:
                cookies = json.load(file)
                return cookies
        except FileNotFoundError:
            print(f"Error: JSON file '{self.cookies_file}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in '{self.cookies_file}'.")
