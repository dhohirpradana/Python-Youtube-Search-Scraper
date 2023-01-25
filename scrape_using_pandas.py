import requests
from bs4 import BeautifulSoup 

yt = "https://www.youtube.com/results?search_query=gcam"
page = requests.get(yt).content
soup = BeautifulSoup(page, 'html.parser')
# print(soup.prettify())

for link in soup.find_all('a'):
    print(link.get('href'))