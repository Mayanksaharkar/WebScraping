import pandas as pd
import requests
from bs4 import BeautifulSoup
import DbConnection as db

brands = [ 'Google', 'Apple', "Mi", 'Oneplus', 'Lava', 'Asus',
          'Iqoo', 'Sony']

for brand in brands:

    base_url = "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3D" + brand + "&param=1112&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlJlYWxtZSBzbWFydHBobmVzIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fX0%3D&wid=16.productCard.PMU_V2_15&sort=recency_desc"

    df = pd.DataFrame(columns=['title', 'rating', 'price', 'desc', 'img'])
    page_links = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('a', attrs={'class': 'cn++Ap'})
    for page in data:
        page_links.append("https://www.flipkart.com" + page.attrs['href'])

    for link in page_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('a', attrs={'class': 'CGtC98'})

        for product in products:
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

            response = db.add_to_mobiles(brand=brand, title=title, link=c_link, price=price, rating=rating,
                                         desc_short=desc_short, cover_img=cover_img, img_list=img_list,
                                         desc_long=desc_long, specification=spec_full)
            print(response)

            # df = df._append(dict1, ignore_index=True)