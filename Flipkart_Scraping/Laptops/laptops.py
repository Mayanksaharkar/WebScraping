import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import sys
import os

cwd = os.getcwd()

sys.path.append(os.path.join(cwd, '..'))

from Flipkart_Scraping.DbConnection import add_to_products
from Flipkart_Scraping.utils import get_format_link
brands = np.array(['Samsung',
                   'Apple',
                   'Infinix',
                   'Acer',
                   'MSI',
                   'Dell',
                   'Lenovo',
                   'Hp',
                   'Asus', ])


def scrap_Laptops():
    for brand in brands:

        Laptops_base_url = "https://www.flipkart.com/search?q=" + brand + "+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=hp+laptop%7CLaptops&requestId=44a9b0cc-6acb-4bc7-a211-5fffa5125ce7&as-backfill=on&sort=recency_desc"

        page_links = []
        response = requests.get(Laptops_base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('a', attrs={'class': 'cn++Ap'},limit=1)
        for page in data:
            page_links.append("https://www.flipkart.com" + page.attrs['href'])

        for link in page_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('a', attrs={'class': 'CGtC98'}, limit=3)

            for product in products:
                img_element = product.find('img', attrs={'class': 'DByuf4'})
                cover_img = img_element.get('src') if img_element else None
                cover_img = get_format_link(cover_img, "312","512")

                title_element = product.find('div', attrs={'class': 'KzDlHZ'})
                title = title_element.get_text(" ") if title_element else None

                element = product.find('div', attrs={'class': "XQDdHH"})
                rating = element.get_text(" ") if element else None

                price_element = product.find('div', attrs={'class': 'Nx9bqj _4b5DiR'})
                price = price_element.get_text(" ") if price_element else None
                price  = get_format_link(price , "₹" ,"") if price_element else None
                price  = get_format_link(price , "," ,"") if price_element else None
                price = int(price, 10) if price else None

                desc = product.find_all('li', attrs={'class': 'J+igdf'})
                desc_short = []

                for description in desc:
                    desc_ele = description.get_text(" ")
                    desc_short.append(desc_ele)

                link_element = product
                link = product.attrs['href'] if link_element else None
                c_link = "https://www.flipkart.com" + link
                # print(c_link)

                response = requests.get(c_link)
                soup = BeautifulSoup(response.text, 'html.parser')

                img_elements = soup.find_all('img', attrs={'class': '_0DkuPH'})
                img_list = []
                for img in img_elements:
                    # img_list.append(img.attrs['src'])
                    image_link = img.attrs['src'] if img else None
                    image_link = get_format_link(image_link, "128","3000")
                    img_list.append(image_link)
                desc_long = []
                desc_elements = soup.find_all('div', attrs={'class': 'pqHCzB'})

                for desc_element in desc_elements:
                    desc_head_ele = desc_element.find('div', attrs={'class': '_9GQWrZ'})
                    desc_head = desc_head_ele.get_text(" ") if desc_head_ele else None
                    desc_p_ele = desc_element.find('p')
                    desc_p = desc_p_ele.get_text(" ") if desc_p_ele else None

                    dict1 = {'title': str(desc_head), 'discription': str(desc_p)}

                    desc_long.append(dict1)
                # print(desc_full)

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

                response = add_to_products(type="All", category="laptops", brand=brand, title=title, link=c_link,
                                           price=price, rating=rating,
                                           desc_short=desc_short, cover_img=cover_img, img_list=img_list,
                                           desc_long=desc_long, specification=spec_full)
                print(response)

                # print(title, price, rating, desc_short, desc_long, spec_full , img_list, brand , c_link ,cover_img)
                # exit()
