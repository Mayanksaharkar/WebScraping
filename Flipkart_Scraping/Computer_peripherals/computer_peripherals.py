import os, sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

cwd = os.getcwd()
sys.path.append(os.path.join(cwd, '..'))
from Flipkart_Scraping.DbConnection import add_to_products
from Flipkart_Scraping.utils import get_format_link


def scrap_computer_peripherals_data():
    types = ['Monitors', 'Motherboard', 'Keyboard', 'Mouse', 'Graphics Card', 'Printers', 'Processors',
             'Cabinets for PC', 'SSD', 'HDD', 'Pen Drives']

    for type in types:

        mobiles_base_url = "https://www.flipkart.com/search?q=" + type + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=popularity"

        page_links = []
        response = requests.get(mobiles_base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('a', attrs={'class': 'cn++Ap'}, limit=2)
        for page in data:
            page_links.append("https://www.flipkart.com" + page.attrs['href'])

        for link in page_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            class_values = ['CGtC98', 'wjcEIp']
            products = soup.find_all('a', class_=lambda c: c and any(cls in c.split() for cls in class_values))

            prod_links = []
            for product in products:
                prod_links.append("https://www.flipkart.com" + product.attrs['href'])

            for link in prod_links:
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                title_ele = soup.find('span', attrs={'class': 'VU-ZEz'})
                title = title_ele.get_text("") if title_ele else None

                brand = title.split(" ")[0] if title else None


                img_eles = soup.find_all('li', attrs={'class': 'YGoYIP Ueh1GZ'})
                img_list = []
                for img in img_eles:
                    img_ele = img.find('img', attrs={'class': '_0DkuPH'})
                    img_link = img_ele.attrs['src'] if img else None
                    img_link = get_format_link(img_link, "128", "1000")
                    img_list.append(img_link)

                cover_img = get_format_link(img_list[0], "1000", "3000") if img_list else None

                rating = soup.find('div', attrs={'class': "XQDdHH"})
                rating = float(rating.get_text(" ")) if rating else None

                price_ele = soup.find('div', attrs={'class': 'Nx9bqj CxhGGd'})
                price = price_ele.get_text(" ") if price_ele else None

                desc_container = soup.find('div', attrs={'class': 'xFVion'})
                # print(desc_container)
                desc_short = desc_container.get_text(",") if desc_container else None

                desc_long = {}
                desc_elements = soup.find_all('div', attrs={'class': 'pqHCzB'})

                for desc_element in desc_elements:
                    desc_head_ele = desc_element.find('div', attrs={'class': '_9GQWrZ'})
                    desc_head = desc_head_ele.get_text(" ") if desc_head_ele else None
                    desc_p_ele = desc_element.find('p')
                    desc_p = desc_p_ele.get_text(" ") if desc_p_ele else None

                    dict1 = {str(desc_head): str(desc_p)}
                    desc_long.update(dict1)
                # print(desc_full)

                spec_containers = soup.find_all('div', attrs={'class': 'GNDEQ-'})
                spec_full = {}
                for container in spec_containers:
                    spec_head_ele = container.find('div', attrs={'class': '_4BJ2V+'})
                    spec_head = spec_head_ele.get_text(" ") if spec_head_ele else None
                    spec_rows = container.find_all('tr', attrs={'class': 'WJdYP6'})
                    spec_rows_dict = {}

                    for spec_row in spec_rows:
                        spec_key_ele = spec_row.find('td', attrs={'class': '+fFi1w'})
                        spec_key = spec_key_ele.get_text(" ") if spec_key_ele else None
                        spec_value_ele = spec_row.find('li', attrs={'class': 'HPETK2'})
                        spec_value = spec_value_ele.get_text(" ") if spec_value_ele else None
                        dict1 = {str(spec_key): spec_value}
                        spec_rows_dict.update(dict1)
                    spec_full.update({str(spec_head): spec_rows_dict})

                # print( title, img_list, desc_short, rating, desc_long, spec_full)

                response = add_to_products(type=type, category="Computer Peripherals", brand=brand, title=title,
                                           rating=rating, price=price, desc_short=desc_short, desc_long=desc_long,
                                           specification=spec_full, link=link, img_list=img_list, cover_img=cover_img)
                print(response)


    # print(df)
