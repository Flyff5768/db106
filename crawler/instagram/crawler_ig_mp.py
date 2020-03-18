import os
import json
import time
import random
import requests

from pyquery import PyQuery as pq
import logging
import multiprocessing as mp




headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': 'mid=XfiFQwALAAGQwcyYLlxLO_xkGrFB; fbm_124024574287414=base_domain=.instagram.com; shbid=16651; shbts=1581487025.8519735; rur=FTW; fbsr_124024574287414=KwK4lUDoQxVxJt2sc439xDwCWiAcvQTcifJJzMhK3AM.eyJ1c2VyX2lkIjoiMTAwMDAwNzc2NDkwMzMwIiwiY29kZSI6IkFRQTM4bHJxWFg5Q3BtWUtwZlVTTlVZZ3czRHNoWXFtNzdoU0VWaFRTRXU2SkFET3E5NXhfSFhJb1JPeE90eURZeTJHWEkxUHV4ZnV4bjNWY2doUW9BVE03a0ViaktGVm5uQUhUMzlWMWx4WGtnZXlNNXBzS3ItT1BheWZpdmNWLUNzbEF2MnkzRFdMdGxRNktpYjFmd0diNmRNTUw1ckdteXRHTzJEWFJ6RmVQcTFEQnlPTU1iQjlVX0NPekFZWmx6UlRUX2FjaUoyZXBaN256cUxOZFJFRVpLdjlmMVcwSWo5UUxrMVpFcUxLbi1XMnp6ZDlJc1VIeDcwNDJBWmR3NGFnTEoxY0FyaXBZTWRtYTFyYktVN2lMaTg2Mk8xWW9CVWphekFDeHZrenlVTzdSaTRxZnpiZkhFamsycHltRWhMUllQbWdQYlNKZUJlUkVtajlIdlcxIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUJWa1pCbGV6bkh1ZU9UWWlHZ2lBZWJaQW9oRnlpRmxSUEhubE9PQ0dnazg1ZzE5YlFEd2hrQ0N4SGpUb0g2UXJjMkVaQnJoUU5zcXV5WkFaQlpDb0VueVRnWkJVbXlmclBpMUtkbVEyS0ppQU5vSzdrT1h4VXNzWkNLMDcyWWRrQm1aQ0hnRGd0d2FySGdvbm5kczJRcGd6RFFEc05Bc1Z1elJZejZ6V3ZJam0iLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTU4MTQ4NzIxNH0; csrftoken=osIi7PQWy7fhNmyzNZMhhdgPhfZMLPgh; ds_user_id=4515140991; sessionid=4515140991%3Aid94nJfktYQEol%3A18;'}
path_dir = ''
path_shortcode = ''
shortcode_set = set()
end_cursor = ''
has_next_page = True
each_article_url = ''



def main(tag): #主程式  # 爬蟲 for Instagram
    # step 1 : 設定 search_tag
    search_tag = tag

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
    print('shortcode_set :',len(shortcode_set))



    # step 2 : 訪問Instagram 取得 html
    html = get_html(tag_url)

    # multiprocessing
    # 任務佇列
    task_queue = mp.JoinableQueue()
    start_multiprocessing(task_queue, path_dir, path_shortcode)

    # step 3 : 取得search_tag首頁data 及 has_next_page,end_cursor
    if end_cursor == '':
        get_analysis(html,'html',task_queue, path_dir, path_shortcode)

    # step  : 取得歷史 data 及 has_next_page,end_cursor
    while has_next_page :
        url = 'https://www.instagram.com/graphql/query/?query_hash=bd33792e9f52a56ae8fa0985521d141d&variables=%7B%22tag_name%22%3A%22{0}%22%2C%22first%22%3A50%2C%22after%22%3A%22{1}%22%7D'
        url = url.format(search_tag, end_cursor)
        print('next url =', url)

        json = get_html(url)
        try:
            get_analysis(json,'json',task_queue, path_dir, path_shortcode)
        except Exception as e:
            print('Exception =', e)
            print(json)
            collect_Exception(e)



        time_sleep = random.randint(0, 2)
        print('chang_page 休息', time_sleep, '秒')
        time.sleep(time_sleep)

def get_html(url): # 訪問網頁
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        HTTP_Status_Code = [200, 401, 404]
        if response.status_code in HTTP_Status_Code:
            # print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            raise
    except Exception as e:
        collect_Exception(e)
        print('Exception =', e)
        time_sleep = 60 + float(random.randint(1, 4000)) / 100
        print('Crawler 休息', time_sleep, '秒','---url:',url)
        time.sleep(time_sleep)
        return get_html(url)

def get_analysis(data,data_format,task_queue, path_dir, path_shortcode):
    if data_format == 'html':
        doc = pq(data)
        article_count = doc('meta[name="description"]')
        print(article_count.attr('content'))
        items = doc('script[type="text/javascript"]').items()
        for item in items:
            if item.text().strip().startswith('window._sharedData'):
                js_data = json.loads(item.text()[21:-1], encoding='utf-8')
                article_list = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
                global end_cursor,has_next_page
                has_next_page = bool(js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page'])
                end_cursor = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']


    elif data_format == 'json':

        js_data = json.loads(data, encoding='utf-8')
        article_list = js_data['data']['hashtag']['edge_hashtag_to_media']['edges']
        has_next_page = bool(js_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page'])
        end_cursor = js_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']

    print('next_has_next_page =', has_next_page)
    print('next_end_cursor =', end_cursor)
    global shortcode_set

    for each_article in article_list:
        shortcode = each_article['node']['shortcode']
        if shortcode not in shortcode_set:
            task=[article_list.index(each_article) + 1,len(article_list),shortcode]
            task_queue.put(task)  # 放進_任務佇列
            shortcode_set.add(shortcode)

    print('start_multiprocessing')
    task_queue.join()  # 確定任務佇列 處理完主程式才離開(主程式結束 任務佇列會繼續
    print('exit_multiprocessing')

    data_count = len(shortcode_set)
    print('已收集 : ', data_count)

def start_multiprocessing(task_queue, path_dir, path_shortcode):

    for i in range(0,10):

        #工作程序1
        worker = mp.Process(target=crawler_multiprocessing, args=(i, task_queue, path_dir, path_shortcode))
        worker.daemon = True
        worker.start()

def crawler_multiprocessing(worker_id,task_queue,path_dir,path_shortcode):
    while True:

        task_list_get = task_queue.get()
        print('worker_id =', worker_id, ',stard_task')
        shortcode = task_list_get[2]

        global each_article_url
        each_article_url = 'https://www.instagram.com/p/' + shortcode + '/'



        html_article = get_html(each_article_url)
        get_data(html_article,path_dir)

        # 存文字檔
        with open(path_shortcode, 'a', encoding='utf8') as f:
            f.write(shortcode + '\n')


        time_sleep = random.randint(1, 3)
        print('worker_id =', worker_id, ',done_task---', task_list_get[0], ' / ', task_list_get[1],',Crawler 休息', time_sleep, '秒', each_article_url)
        time.sleep(time_sleep)
        task_queue.task_done()

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

def get_data(html,path_dir):
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
                    title = "NA"
                    print(title)

                try:
                    #內文
                    content = js_data["graphql"]["shortcode_media"]["edge_media_to_caption"]['edges'][0]['node']['text']
                    #print(content)
                except:
                    content = 'NA'
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
                    comment = 'NA'
                    print(comment)




                #同整存檔內容
                global each_article_url
                total = '{ "文章網址":"' + each_article_url + '","標題":"' + title +'","景點名稱":"NA"' +',"文章內容":"' + content.replace('\n','') + '","留言":"' + comment.replace('\n','') +'","地址":"NA"'+',"縣市":"台北市"' +'}'
                #print(total)

                # js_data = json.loads(total, encoding='utf-8')
                # print(js_data['文章網址'])
                # print(js_data['標題'])
                # print(js_data['景點名稱'])
                # print(js_data['文章內容'])
                # print(js_data['留言'])
                # print(js_data['地址'])
                # print(js_data['縣市'])


                #建個別資料夾
                title = replace_illegal_characters(title)
                # path_dir_each = path_dir + '/' + title
                # os.mkdir(path_dir_each)
                #存文字檔
                with open(path_dir +'/'+ title +'.txt','a',encoding='utf8' ) as f:
                    f.write(total+'\n')
                    f.write('-----\n')


                # #存照片
                # try :
                #     img_url_list = js_data["graphql"]["shortcode_media"]['edge_sidecar_to_children']['edges']
                #     for img_url_each in img_url_list :
                #         img_url = img_url_each['node']['display_url']
                #         #print(img_url_list.index(img_url_each))
                #         request.urlretrieve(img_url,path_dir_each +'/'+ title +'---%s' %img_url_list.index(img_url_each) +'.jpg')
                # except :
                #      collect_Exception(e)
                #     img_url = js_data["graphql"]["shortcode_media"]['display_url']
                #     request.urlretrieve(img_url,path_dir_each + '/' + title + '.jpg')
    except Exception as e:
        print(e)
        collect_Exception(e)


def collect_Exception(e):
    # 存文字檔
    with open('Exception.txt', 'a', encoding='utf8') as f:
        f.write(str(e) + '\n')
    pass



if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # tag_list = ['台北景點','宜蘭景點', '桃園景點', '苗栗景點', '基隆景點', '新北景點', '新竹景點']  # 手動更改
    # tag_list = ['台北美食', '宜蘭美食', '桃園美食', '苗栗美食', '基隆美食', '新北美食', '新竹美食']  # 手動更改
    tag_list = ['新北景點']#記得改縣市
    for each_tag in tag_list:
        main(each_tag)

    print('Complete!!!!!!!!!!')
    data_count = len(shortcode_set)
    print('已收集 : ', data_count)

