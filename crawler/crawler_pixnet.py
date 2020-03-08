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

# https://www.instagram.com/p/B8vDCPOHMVZ/
# https://www.instagram.com/p/B8sePznp0HV/







headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
path_dir = ''
path_shortcode = ''
shortcode_set = set()


each_article_url = ''



def main(): #主程式  # 爬蟲 for Instagram

    # step 1 : 設定 search_tag
    search_tag = '桃園景點' #手動更改


    global path_dir
    path_dir = 'E:\資策會-DB106\專題\Pixnet\All'
    path_dir = path_dir +'\%s' % (search_tag)
    make_dir(path_dir)

    # 開紀錄shortcode文字檔
    global path_shortcode,shortcode_set
    path_shortcode = path_dir +'\shortcode.txt'
    if  os.path.exists(path_shortcode):
        with open(path_shortcode , 'r', encoding='utf8') as f:
            all_shortcode = f.readlines()
            print(all_shortcode)
            all_shortcode = [shortcode.replace('\n','') for shortcode in all_shortcode]
            print(all_shortcode)
            for each_shortcode in all_shortcode:
                shortcode_set.add(each_shortcode)

            print(shortcode_set)




    # step2  : 取得歷史 data 及 has_next_page,end_cursor
    page = 1
    while True :

        tag_url = 'https://www.pixnet.net/mainpage/api/tags/{0}/feeds?page={1}&per_page=5&filter=articles&sort=related&refer=https%3A%2F%2Fwww.pixnet.net%2F'
        url = tag_url.format(search_tag, page)
        print('next url =', url)

        json = get_html(url)
        get_analysis(json,'json')
        page += 1





def get_html(url): # 訪問網頁
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            #print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
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
    list =['*','|','\\',':','\"','<','>','?','/',' .',' ']
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
            title = "NO_title"
            print(title)

        try:
            # 內文
            items = doc('h2[itemprop="headline"]').items()
            for item in items:
                content = item.text()
                print(content)
        except Exception as e:
            print(e)
            content = 'NO_content'
            print(content)

        try:
            # 留言
            items = doc('h2[itemprop="headline"]').items()
            for item in items:
                comment = item.text()
                # print(comment)
        except Exception as e:
            print(e)
            comment = 'NO_commentt'
            print(comment)








        # #同整存檔內容
        # global each_article_url
        # total = '網址 : \n' + each_article_url + '\n標題 : \n' + title + '\n內文 : \n' + content + '\n留言 : \n' + comment
        # #print(total)
        #
        #
        # #建個別資料夾
        # title = replace_illegal_characters(title)
        # global path_dir
        # path_dir_each = path_dir + '/' + title
        # if not os.path.exists(path_dir_each):
        #     os.mkdir(path_dir_each)
        #
        # path_dir_each += '/' +title+ str(len(os.listdir(path_dir_each)))
        # os.mkdir(path_dir_each)
        #
        #
        # #存文字檔
        # with open(path_dir_each +'/'+ title +'.txt','w',encoding='utf8' ) as f:
        #     f.write(total)

        # #存照片
        # try :
        #     img_url_list = js_data["graphql"]["shortcode_media"]['edge_sidecar_to_children']['edges']
        #     for img_url_each in img_url_list :
        #         img_url = img_url_each['node']['display_url']
        #         #print(img_url_list.index(img_url_each))
        #         request.urlretrieve(img_url,path_dir_each +'/'+ title +'---%s' %img_url_list.index(img_url_each) +'.jpg')
        # except :
        #     img_url = js_data["graphql"]["shortcode_media"]['display_url']
        #     request.urlretrieve(img_url,path_dir_each + '/' + title + '.jpg')


    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')
    data_count = len(shortcode_set)
    print('已收集 : ', data_count)
