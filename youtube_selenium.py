from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd

url = 'https://www.youtube.com/c/MaksimKorzh_aka_CodeMonkeyKing/videos'


def scrape_youtube(url, n_videos):
    ends = round(n_videos/30)+1
    PATH = 'C:\Program Files (x86)\chromedriver.exe'

    video_list = []
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    body = driver.find_element_by_tag_name('body')
    for _ in range(ends):
        body.send_keys(Keys.END)
        time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    videos = soup.findAll('div', {'id': 'dismissable'})
    for video in videos:
        video_dict = {}
        video_dict['title'] = video.find('a', {'id': 'video-title'}).text
        video_dict['video_url'] = 'https://www.youtube.com/' + video.find('a', {'id': 'video-title'})['href']
        meta = video.find('div', {'id': 'metadata-line'}).findAll('span')
        video_dict['views'] = meta[0].text
        video_dict['video_age'] = meta[1].text
        video_list.append(video_dict)
    youtube_df = pd.DataFrame(video_list)
    youtube_df.to_csv('king_videos.csv', index=False)
    print(youtube_df.head())


scrape_youtube(url, n_videos=302)
