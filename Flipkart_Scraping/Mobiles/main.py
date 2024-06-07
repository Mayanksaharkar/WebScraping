import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


def fetch_mobiles():
    brands = np.array(['Redmi', 'Samsung', 'Poco', 'Vivo', 'Google', 'Apple', "Mi", 'Oneplus', 'Lava', 'Asus',
                       'Iqoo', 'Sony'])
    brand_url = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3D{brand}&param=1112&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlJlYWxtZSBzbWFydHBobmVzIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fX0%3D&wid=16.productCard.PMU_V2_15&sort=recency_desc"
    for brand in brands:
        url = brand_url.format(brand=brand)
        pages = fetch_page_links(url)
        for page in pages:
            products = fetch_product_links(page)
            for product in products:
                product_data = fetch_product_data(product)





def fetch_page_links(brand_url ):
    response = requests.get(brand_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('a', attrs={'class': 'cn++Ap'})
    return set("https://www.flipkart.com" + page.attrs['href'] for page in data)

def fetch_product_links(page_links):
    product_links = set()
    for link in page_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('a', attrs={'class': 'CGtC98'})
        product_links.update("https://www.flipkart.com" + product.attrs['href'] for product in products)
    return product_links

def fetch_product_data(product_url):


    img_element = product.find('img', attrs={'class': 'DByuf4'})
    cover_img = img_element.get('src') if img_element else None

    title_element = product.find('div', attrs={'class': 'KzDlHZ'})
    title = title_element.get_text(" ") if title_element else None

    element = product.find('div', attrs={'class': "XQDdHH"})
    rating = element.get_text(" ") if element else None

    price_element = product.find('div', attrs={'class': 'Nx9bqj _4b5DiR'})
    price = price_element.get_text(" ") if price_element else None

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
        img_list.append(img.attrs['src'])
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

    r_val = {'title':title, 'link':c_link,'price':price,'rating':rating,'desc_short':desc_short,'cover_img':cover_img,'desc_long':desc_long , 'spec_full':spec_full, 'img_list':img_list}
    return
    response = db.add_to_products(brand=brand, title=title, link=c_link, price=price, rating=rating,
                                  desc_short=desc_short, cover_img=cover_img, img_list=img_list,
                                  desc_long=desc_long, specification=spec_full)