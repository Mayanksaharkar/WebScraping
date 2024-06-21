from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def ConnectToDB():
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client['ProductDB']
    print(client)
    return db


def add_to_products(type,category, brand, title, link, price, rating, desc_short, cover_img, img_list, desc_long,
                    specification):
    collection = db['products']
    new_doc = {'type':type,'category': category, 'brand': brand, 'title': title, 'link': link, 'price': price, 'rating': rating,
               'desc_short': desc_short,
               'cover_img': cover_img, 'img_list': img_list, 'desc_long': desc_long, 'specification': specification}

    existing_doc = collection.find_one({'link':link})
    # print(existing_doc)
    if existing_doc:
        return 'Already Exists'
    else:
        response = collection.insert_one(new_doc).inserted_id
        return response


db = ConnectToDB()

