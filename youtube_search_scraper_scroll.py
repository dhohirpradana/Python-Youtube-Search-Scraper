import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.get("https://www.youtube.com/results?search_query=indonesia")
time.sleep(1)

print(browser.find_elements(By.XPATH, "//div[@id='contents']"))

# no_of_pagedowns = 20

# while no_of_pagedowns:
#     elem.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.2)
#     no_of_pagedowns-=1

# for post in post_elems:
#     print(post.text)