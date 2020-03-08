import requests
from bs4 import BeautifulSoup
import os
import time
import random

# 開檔
path_dir = 'E:\專題\Yahoo'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
search_tag = '百貨商圈'  # 手動更改
url = 'https://travel.yahoo.com.tw/search/{0}'.format(search_tag)
post_url = 'https://travel.yahoo.com.tw/ajax/LoadMore.php'

post_data_str = """P: 4
T: 百貨商圈
type: search
GATitle: 關鍵字搜尋"""

post_data = {}

for i in post_data_str.split('\n'):
    post_data[i.split(': ')[0]] = i.split(': ')[1]

post_data['P'] = '0'
# print(post_data)

for p in range(1, 100):
    post_data['P'] = str(p)
    res = requests.post(post_url, headers=headers, data=post_data)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    title = soup.select('div[class="item_block"] a')[6:]
    # print(title)
    for each_title in title:
        # print(each_title)
        article_url = 'https://travel.yahoo.com.tw'+each_title["href"]
        res_article = requests.get(article_url)
        # print(res_article)
        article_soup = BeautifulSoup(res_article.text, 'html.parser')
        [s.extract() for s in article_soup('figcaption')]
        # print(article_soup)

        # 標題
        # article_title = article_soup.select('div[class="post_header"] h1')
        # print(article_title)

        # 內文
        article = article_soup.select('div[class="post_content"]')
        # print(article)
        # for i in article_title:
        #     string = i.text
        #     list = ['*', '|', '\\', ':', '\"', '<', '>', ']', '[', '? ', '/', '《', '》', '・', '/', '，', '「', '」', '！', '｜', '【', '】', '？', '、', '.', '’', '–', '～', '?']
        #     for c in list:
        #         string = string.replace(c, '')
        #     # print(string)
        #     time.sleep(1)

        for u in article:
            content = u.text
            p = content.strip()
            # print(p)
        with open(path_dir + '\Article.txt', 'a', encoding='utf8') as f:
            f.write(p)

        # 同整存檔內容
        # global each_article_url
        # total = '標題 : \n' + string + '\n內文 : \n' + p + '\n'

        # # 建個別資料夾
        # global path_each_dir
        # path_dir_each = path_dir + '/' + string
        # if not os.path.exists(path_dir_each):
        #     os.mkdir(path_dir_each)

        # # 寫入檔案
        # with open(path_dir_each + '/' + string + '.txt', 'w', encoding='utf8') as f:
        #     f.write(total)
# time.sleep(5)

print('Complete!!!!!!!!!!')