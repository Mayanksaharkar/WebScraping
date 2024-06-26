import os, sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

cwd = os.getcwd()
sys.path.append(os.path.join(cwd, '..'))
from Flipkart_Scraping.DbConnection import add_to_products
from Flipkart_Scraping.utils import get_format_link


def scrap_HomeAppliances():
    types = ['Television', 'Refrigerator', 'washing machine', 'air conditioners']

    for type in types:

        mobiles_base_url = "https://www.flipkart.com/search?q=" + type + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=popularity"

        page_links = []
        response = requests.get(mobiles_base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('a', attrs={'class': 'cn++Ap'}, limit=4)
        for page in data:
            page_links.append("https://www.flipkart.com" + page.attrs['href'])

        for link in page_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            class_values = ['CGtC98', 'wjcEIp']
            products = soup.find_all('a', class_=lambda c: c and any(cls in c.split() for cls in class_values) , limit=5)

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

                cover_img = get_format_link(img_list[0], "1000", "512") if img_list else None

                rating = soup.find('div', attrs={'class': "XQDdHH"})
                rating = float(rating.get_text(" ")) if rating else None

                price_ele = soup.find('div', attrs={'class': 'Nx9bqj CxhGGd'})
                price = price_ele.get_text(" ") if price_ele else None
                price  = get_format_link(price , "," ,"") if price_ele else None
                price  = get_format_link(price , "₹" ,"")  if price_ele else None
                price = int(price, 10) if price else None

                desc = soup.find_all('li', attrs={'class': 'J+igdf'})
                desc_short = []
                for description in desc:
                    desc_ele = description.get_text(" ")
                    desc_short.append(desc_ele)

                desc_long = []
                desc_elements = soup.find_all('div', attrs={'class': 'pqHCzB'})

                for desc_element in desc_elements:
                    desc_head_ele = desc_element.find('div', attrs={'class': '_9GQWrZ'})
                    desc_head = desc_head_ele.get_text(" ") if desc_head_ele else None
                    desc_p_ele = desc_element.find('p')
                    desc_p = desc_p_ele.get_text(" ") if desc_p_ele else None

                    dict1 = {'title': str(desc_head), 'discription': str(desc_p)}

                    desc_long.append(dict1)

                spec_containers = soup.find_all('div', attrs={'class': 'GNDEQ-'})
                spec_full = []
                for container in spec_containers:
                    spec_head_ele = container.find('div', attrs={'class': '_4BJ2V+'})
                    spec_head = spec_head_ele.get_text(" ") if spec_head_ele else None
                    spec_rows = container.find_all('tr', attrs={'class': 'WJdYP6'})
                    spec_rows_list = []

                    for spec_row in spec_rows:
                        spec_key_ele = spec_row.find('td', attrs={'class': '+fFi1w'})
                        spec_key = spec_key_ele.get_text(" ") if spec_key_ele else None
                        spec_value_ele = spec_row.find('li', attrs={'class': 'HPETK2'})
                        spec_value = spec_value_ele.get_text(" ") if spec_value_ele else None
                        # dict1 = {str(spec_key): spec_value}
                        dict1 = {"spec_title": str(spec_key), "spec_body": str(spec_value)}
                        spec_rows_list.append(dict1)
                    spec_full.append({'title': str(spec_head), 'spec_row_list': spec_rows_list})

                # print( title, img_list, desc_short, rating, desc_long, spec_full, price , link)

                response = add_to_products(type=type, category="homeAppliances", brand=brand, title=title,
                                           rating=rating, price=price, desc_short=desc_short, desc_long=desc_long,
                                           specification=spec_full, link=link, img_list=img_list, cover_img=cover_img)
                print(response)
                # print(title, price, rating, desc_short, desc_long, spec_full , img_list, brand , link ,cover_img)
                # exit()


# print(df)
# scrap_HomeAppliances()