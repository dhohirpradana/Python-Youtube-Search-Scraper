from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import datetime
import os

# options = webdriver.ChromeOptions()
# # options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("--disable-features=NetworkService")
driver = webdriver.Firefox(options=options)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')


def handler(request, jsonify):
    body = request.get_json()

    if body is None:
        return jsonify({'message': 'No body provided'}), 400

    try:
        query = body['query']
        scroll = body['scroll']
    except Exception as e:
        return jsonify({'message': str(e) + " not provided"}), 400

    query_url = urllib.parse.quote(query)
    print('Query URL: ', query_url)
    now = datetime.datetime.now()

    driver.get(f"https://www.youtube.com/results?search_query={query_url}")

    scroll_height = driver.execute_script("return window.innerHeight")
    video_links = []
    video_titles = []
    video_views = []
    video_published_times = []

    max_scroll = scroll
    file_name = f"{query}_scroll-{max_scroll}_{now.strftime('%Y%m%d_%H%M%S')}"

    # while True:
    while max_scroll > 0:
        print("Scroll:", max_scroll)
        max_scroll -= 1
        video_ids = driver.find_elements(By.XPATH, "//a[@id='video-title']")
        print('video_ids: ', video_ids)

        for i, video_id in enumerate(video_ids):
            print("videoTitle", video_id.get_attribute("title"))
            print("videoID", video_id.get_attribute("href"))
            video_links.append(video_id.get_attribute("href"))
            video_titles.append(video_id.get_attribute("title"))

        video_infos = driver.find_elements(
            By.XPATH, "//span[@class='inline-metadata-item style-scope ytd-video-meta-block']")
        # print('video_infos: ', video_infos)

        for i, video_info in enumerate(video_infos):
            if "views" in video_info.text:
                view_count = video_info.text
                video_views.append(view_count)
            elif "ago" in video_info.text:
                published_time = video_info.text
                video_published_times.append(published_time)

        document_height_before = driver.execute_script(
            "return document.documentElement.scrollHeight")
        driver.execute_script(
            f"window.scrollTo(0, {document_height_before + scroll_height});")
        
        # write to file
        with open(f"{BASE_DIR}/results/{file_name}.txt", "a") as f:
            print(video_titles)
            for i, video_link in enumerate(video_links):
                print(video_link)
                # if i < len(video_links) - 1:
                #     f.write(
                #         f"{video_link} ‽ {video_titles[i]} ‽ {video_views[i]} ‽ {video_published_times[i]}\n")
                # else:
                #     f.write(
                #         f"{video_link} ‽ {video_titles[i]} ‽ {video_views[i]} ‽ {video_published_times[i]}")

        time.sleep(1.5)
        document_height_after = driver.execute_script(
            "return document.documentElement.scrollHeight")
        if document_height_after == document_height_before:
            break

    driver.quit()
    return jsonify({'message': 'success', "filename": file_name}), 200
