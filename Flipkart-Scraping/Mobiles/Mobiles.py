import requests
from bs4 import BeautifulSoup
import pandas as pd

brands = ['Redmi', 'Samsung', 'Vivo', 'Oppo', 'Poco', 'Motorola', 'Google', 'Apple', "Mi", 'Oneplus', 'Lava', 'Asus',
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
        products = soup.find_all('div', attrs={'class': 'tUxRFH'})
        for product in products:
            img_element = product.find('img', attrs={'class': 'DByuf4'})
            img = img_element.get('src') if img_element else None

            title_element = product.find('div', attrs={'class': 'KzDlHZ'})
            title = title_element.get_text(" ") if title_element else None

            element = product.find('div', attrs={'class': "XQDdHH"})
            rating = element.get_text(" ") if element else None

            price_element = product.find('div', attrs={'class': 'Nx9bqj _4b5DiR'})
            price = price_element.get_text(" ") if price_element else None

            desc = product.find_all('li', attrs={'class': 'J+igdf'})
            desc_list = []

            for description in desc:
                desc_ele = description.get_text(" ")
                desc_list.append(desc_ele)

            dict1 = {'title': title, 'rating': rating, 'price': price, 'desc': desc_list, 'img':img}
            # print(dict1)
            df = df._append(dict1, ignore_index=True)

    print(df)
    df.to_csv(brand + ".csv")
