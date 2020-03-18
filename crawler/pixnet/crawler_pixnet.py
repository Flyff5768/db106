import os
import re
import sys
import json
import time
import random
import requests
from hashlib import md5
from pyquery import PyQuery as pq
from urllib import request


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
path_dir = ''
path_shortcode = ''
shortcode_set = set()


each_article_url = ''



def main(tag): #主程式  # 爬蟲 for Instagram

    # step 1 : 設定 search_tag
    search_tag = tag


    global path_dir
    path_dir = 'E:\資策會-DB106\專題\Pixnet\All'
    path_dir = path_dir +'\%s' % (search_tag)
    make_dir(path_dir)

    # 開紀錄shortcode文字檔
    global path_shortcode,shortcode_set
    path_shortcode = path_dir +'\shortcode.txt'
    if  os.path.exists(path_shortcode):
        with open(path_shortcode , 'r', encoding='utf8') as f:
            for each_shortcode in f:
                shortcode_set.add(each_shortcode.replace('\n', ''))




    # step2  : 取得歷史 data 及 has_next_page,end_cursor

    for page in range(1,100):

        tag_url = 'https://www.pixnet.net/mainpage/api/tags/{0}/feeds?page={1}&per_page=20&filter=articles&sort=related&refer=https%3A%2F%2Fwww.pixnet.net%2F'
        url = tag_url.format(search_tag, page)
        print('next url =', url)

        json = get_html(url)
        get_analysis(json,'json')

        time_sleep = random.randint(0, 2)
        print('chang_page 休息', time_sleep, '秒')
        time.sleep(time_sleep)






def get_html(url): # 訪問網頁
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        HTTP_Status_Code =[200,401,404]
        if response.status_code in HTTP_Status_Code:
            #print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            raise
    except Exception as e:
        print(e)
        time_sleep = 60 + float(random.randint(1, 4000)) / 100
        print('Crawler 休息', time_sleep, '秒')
        time.sleep(time_sleep)
        return get_html(url)

def get_analysis(data,data_format):


    js_data = json.loads(data, encoding='utf-8')
    article_list = js_data['data']['feeds']


    for each_article in article_list :

        shortcode = each_article['member_uniqid']

        if shortcode not in shortcode_set :

            global each_article_url
            each_article_url = each_article['link']
            print(article_list.index(each_article)+1,'/',len(article_list),each_article_url)

            html_article = get_html(each_article_url)


            get_data(html_article)

            shortcode_set.add(shortcode)

            # 存文字檔

            with open(path_shortcode, 'a', encoding='utf8') as f:
                f.write(shortcode + '\n')

            data_count = len(shortcode_set)
            time_sleep = random.randint(0, 2)
            print('已收集 : ',data_count,',Crawler 休息', time_sleep, '秒')
            time.sleep(time_sleep)




def replace_illegal_characters(string):
    list =['*','|','\\',':','\"','<','>','?','/','.',' ','-','.','[',']','。','＠','～','、','》','【','@','】','，','(',')','．','｜']
    for c in list:
        string = string.replace(c, '')

    return string


def make_dir(path_dir):
    list = path_dir.split('\\')
    path_str = list[0]

    for each in list[1:]:
        path_str += "\\" + each

        if not os.path.exists(path_str):
            os.mkdir(path_str)


def get_data(html):
    try:
        doc = pq(html)

        try:
            #標題
            items = doc('h2[itemprop="headline"]').items()
            for item in items:
                title = item.text()
                #print(title)
        except Exception as e:
            print(e)
            title = "NA"
            print(title)

        try:
            content = ''
            # 內文
            items = doc('div[id="article-content-inner"] p').items()
            for item in items:
                content += item.text() +'\n'

            # print('content =', content)

        except Exception as e:
            print(e)
            content = 'NA'
            print(content)

        comment = 'NA'
        # print(comment)


        # 同整存檔內容
        global each_article_url
        total = '{ "文章網址":"' + each_article_url + '","標題":"' + title + '","景點名稱":"NA"' + ',"文章內容":"' + content.replace(
            '\n', '') + '","留言":"' + comment.replace('\n', '') + '","地址":"NA"' + ',"縣市":"台北市"' + '}'
        # print(total)

        # 建個別資料夾
        title = replace_illegal_characters(title)
        # path_dir_each = path_dir + '/' + title
        # os.mkdir(path_dir_each)
        # 存文字檔
        with open(path_dir + '/' + title + '.txt', 'a', encoding='utf8') as f:
            f.write(total + '\n')
            f.write('-----\n')


        # #存照片
        # items = doc('link[rel="image_src"]').items()
        # img_url_list = []
        # for item in items:
        #     img_url_list.append(item.attr('href'))
        # for img_url_each in img_url_list :
        #
        #     request.urlretrieve(img_url_each,path_dir_each +'/'+ title +'---%s' %img_url_list.index(img_url_each) +'.jpg')

    except Exception as e:
        print(e)
        # 存文字檔
        with open('Exception.txt', 'a', encoding='utf8') as f:
            f.write(str(e)+'\n')
        pass


if __name__ == '__main__':
    # tag_list = ['台北景點','新北景點','基隆景點', '桃園景點','新竹景點', '苗栗景點','宜蘭景點' ]  # 手動更改
    tag_list = ['台北美食', '宜蘭美食', '桃園美食', '苗栗美食', '基隆美食', '新北美食', '新竹美食']  # 手動更改
    # tag_list = ['基隆景點']  # 記得改縣市
    for each_tag in tag_list:
        main(each_tag)


    print('Complete!!!!!!!!!!')
    data_count = len(shortcode_set)
    print('已收集 : ', data_count)
