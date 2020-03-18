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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': 'mid=XfiFQwALAAGQwcyYLlxLO_xkGrFB; fbm_124024574287414=base_domain=.instagram.com; shbid=16651; shbts=1581487025.8519735; rur=FTW; fbsr_124024574287414=KwK4lUDoQxVxJt2sc439xDwCWiAcvQTcifJJzMhK3AM.eyJ1c2VyX2lkIjoiMTAwMDAwNzc2NDkwMzMwIiwiY29kZSI6IkFRQTM4bHJxWFg5Q3BtWUtwZlVTTlVZZ3czRHNoWXFtNzdoU0VWaFRTRXU2SkFET3E5NXhfSFhJb1JPeE90eURZeTJHWEkxUHV4ZnV4bjNWY2doUW9BVE03a0ViaktGVm5uQUhUMzlWMWx4WGtnZXlNNXBzS3ItT1BheWZpdmNWLUNzbEF2MnkzRFdMdGxRNktpYjFmd0diNmRNTUw1ckdteXRHTzJEWFJ6RmVQcTFEQnlPTU1iQjlVX0NPekFZWmx6UlRUX2FjaUoyZXBaN256cUxOZFJFRVpLdjlmMVcwSWo5UUxrMVpFcUxLbi1XMnp6ZDlJc1VIeDcwNDJBWmR3NGFnTEoxY0FyaXBZTWRtYTFyYktVN2lMaTg2Mk8xWW9CVWphekFDeHZrenlVTzdSaTRxZnpiZkhFamsycHltRWhMUllQbWdQYlNKZUJlUkVtajlIdlcxIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUJWa1pCbGV6bkh1ZU9UWWlHZ2lBZWJaQW9oRnlpRmxSUEhubE9PQ0dnazg1ZzE5YlFEd2hrQ0N4SGpUb0g2UXJjMkVaQnJoUU5zcXV5WkFaQlpDb0VueVRnWkJVbXlmclBpMUtkbVEyS0ppQU5vSzdrT1h4VXNzWkNLMDcyWWRrQm1aQ0hnRGd0d2FySGdvbm5kczJRcGd6RFFEc05Bc1Z1elJZejZ6V3ZJam0iLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTU4MTQ4NzIxNH0; csrftoken=osIi7PQWy7fhNmyzNZMhhdgPhfZMLPgh; ds_user_id=4515140991; sessionid=4515140991%3Aid94nJfktYQEol%3A18;'}
path_dir = ''
path_shortcode = ''
shortcode_set = set()
end_cursor = ''
has_next_page = True
each_article_url = ''



def main(): #主程式  # 爬蟲 for Instagram
    # step 1 : 設定 search_tag
    search_tag = '' #手動更改
    tag_url = 'https://www.instagram.com/explore/tags/{0}/'.format(search_tag)
    global path_dir
    path_dir = 'E:\資策會-DB106\專題\Instagram\All'
    path_dir = path_dir +'\%s' % (search_tag)
    make_dir(path_dir)

    # 開紀錄shortcode文字檔
    global path_shortcode,shortcode_set
    path_shortcode = path_dir +'\shortcode.txt'
    if  os.path.exists(path_shortcode):
        with open(path_shortcode , 'r', encoding='utf8') as f:
            for each_shortcode in f:
                shortcode_set.add(each_shortcode.replace('\n', ''))


    # step 2 : 訪問Instagram 取得 html
    html = get_html(tag_url)

    # step 3 : 取得search_tag首頁data 及 has_next_page,end_cursor
    if end_cursor == '':
        get_analysis(html,'html')

    # step  : 取得歷史 data 及 has_next_page,end_cursor
    while has_next_page :
        url = 'https://www.instagram.com/graphql/query/?query_hash=bd33792e9f52a56ae8fa0985521d141d&variables=%7B%22tag_name%22%3A%22{0}%22%2C%22first%22%3A50%2C%22after%22%3A%22{1}%22%7D'
        url = url.format(search_tag, end_cursor)
        print('next url =', url)

        json = get_html(url)
        get_analysis(json,'json')






def get_html(url): # 訪問網頁
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            #print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            raise
    except Exception as e:
        print('Exception =', e)
        time_sleep = 60 + float(random.randint(1, 4000)) / 100
        print('Crawler 休息', time_sleep, '秒')
        time.sleep(time_sleep)
        return get_html(url)

def get_analysis(data,data_format):
    if data_format == 'html':
        doc = pq(data)
        items = doc('script[type="text/javascript"]').items()
        for item in items:
            if item.text().strip().startswith('window._sharedData'):
                js_data = json.loads(item.text()[21:-1], encoding='utf-8')
                article_list = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
                global end_cursor,has_next_page
                has_next_page = bool(js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page'])
                end_cursor = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']


    elif data_format == 'json':
        try:
            js_data = json.loads(data, encoding='utf-8')
        except Exception as e:
            print('Exception =', e)
            print(data)

        article_list = js_data['data']['hashtag']['edge_hashtag_to_media']['edges']
        has_next_page = bool(js_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page'])
        end_cursor = js_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']

    print('next_has_next_page =', has_next_page)
    print('next_end_cursor =', end_cursor)

    for each_article in article_list :

        shortcode = each_article['node']['shortcode']

        if shortcode not in shortcode_set :

            global each_article_url
            each_article_url = 'https://www.instagram.com/p/'+ shortcode +'/'
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
        items = doc('script[type="text/javascript"]').items()
        for item in items:
            if item.text().strip().startswith('window.__additionalDataLoaded'):
                try:
                    js_data = json.loads(item.text()[48:-2], encoding='utf-8')
                except:
                    break
                try :
                    #標題
                    title = js_data["graphql"]["shortcode_media"]["location"]['name']
                    #print(title)
                except:
                    title = "NO_title"
                    print(title)

                try:
                    #內文
                    content = js_data["graphql"]["shortcode_media"]["edge_media_to_caption"]['edges'][0]['node']['text']
                    #print(content)
                except:
                    content = 'NO_content'
                    print(content)

                try:
                    # 留言
                    comment_times = len(js_data["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"])
                    comment_list = js_data["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]
                    comment = ''

                    for each_comment in comment_list:
                        comment += each_comment["node"]["text"]

                        comment_son_list = each_comment["node"]["edge_threaded_comments"]["edges"]
                        for each_comment_son in comment_son_list:
                            each_comment_son_clean = each_comment_son["node"]["text"].replace('\n', '')
                            comment += '\n    ' + each_comment_son_clean + '\n'
                except:
                    comment = 'NO_commentt'
                    print(comment)




                #同整存檔內容
                global each_article_url
                total = '網址 : \n' + each_article_url + '\n標題 : \n' + title + '\n內文 : \n' + content + '\n留言 : \n' + comment
                #print(total)


                #建個別資料夾
                title = replace_illegal_characters(title)
                global path_dir
                path_dir_each = path_dir + '/' + title
                if not os.path.exists(path_dir_each):
                    os.mkdir(path_dir_each)

                path_dir_each += '/' +title+ str(len(os.listdir(path_dir_each)))
                os.mkdir(path_dir_each)


                #存文字檔
                with open(path_dir_each +'/'+ title +'.txt','w',encoding='utf8' ) as f:
                    f.write(total)

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
    except :
        pass


if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')
    data_count = len(shortcode_set)
    print('已收集 : ', data_count)
