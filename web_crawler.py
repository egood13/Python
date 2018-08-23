


import re
import urllib
import pandas as pd
from bs4 import BeautifulSoup



url = 'https://www.ssactivewear.com/ps/closeout?Page=All' # web page

# read html
with urllib.request.urlopen(url) as response:
	html = response.read()
soup = BeautifulSoup(html, "lxml")

div_id = "M_M_zProducts" # id to search
products = soup.find(name="div", id=div_id) # extracts one tag with name and id given

product_names = list(products.find_all("div", class_="name"))
style_nums = []
for i in product_names:
	style_nums.append(i.text) # extracts text and adds to list


pd.DataFrame(style_nums, columns=["style_nums"]).to_excel("style_nums.xlsx", index=False) # save to excel file