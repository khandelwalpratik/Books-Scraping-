

from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import random


column_names = ['Title', 'Link', 'Price', 'Quantity in Stock']
base_url = 'http://books.toscrape.com/catalogue/'

allBooks=[]
for i in range(1,51):
    response = requests.get(f"http://books.toscrape.com/catalogue/page-{i}.html")
    data = BeautifulSoup(response.text, 'html.parser')
    book = data.find_all(class_='product_pod')
    for i in book:
        b_url = base_url + i.h3.a['href']
        allBooks.append(b_url)

        
Book_details=[]
for i in allBooks:
    response = requests.get(i)
    data = BeautifulSoup(response.text, 'html.parser')
    title = data.h1.string
    price = data.find(class_='price_color').string
    qty = data.find(class_='instock availability')
    qty = qty.contents[-1].strip()
    qty = int(re.search('\d+',qty).group())
    price = float(re.search('[\d.]+',price).group())
    
    Book_details.append([title, i, price, qty])
    
df = pd.DataFrame(Book_details,columns=column_names)
df.to_csv("alldata3.csv",index=False)

df=pd.read_csv("alldata3.csv")
list=df.values.tolist()
sorted_data = sorted(list, key=lambda x: x[3])
random_number=random.randint(0,100)

title,link,price,qty=sorted_data[random_number]

print("recommended book to buy :",link)
print("Hurry stock available",qty)
print("price",price)

    

