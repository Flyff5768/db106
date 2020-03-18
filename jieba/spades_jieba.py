import jieba
from jieba import analyse
import time
import os
import logging

from gensim.models import word2vec

def word_count(list):
    time_start = time.time()
    word_cunt_dict = {}

    for each_word in list:
        if len(each_word) == 1 :
            continue

        if each_word in word_cunt_dict:
            word_cunt_dict[each_word] += 1
        else:
            word_cunt_dict[each_word] = 1

    #print(word_cunt_dict)



    sort_list = []
    for each_dict_key in word_cunt_dict :
        if word_cunt_dict[each_dict_key] > 5:
            sort_list.append((each_dict_key,word_cunt_dict[each_dict_key]))


    sort_list.sort(key=lambda x:x[1],reverse=True)

    print("共",len(sort_list),'個 Tag')
    print(sort_list)
    for i in range(1,len(sort_list)):

        print('第',i ,'名 :',sort_list[i-1][0],sort_list[i-1][1])
        # print(sort_list[i - 1][0], sort_list[i - 1][1])

    cost_time = time.time() - time_start
    print('word_count 花了', cost_time / 3600, '小時')

def jieba_textrank(load_txt_path):
    time_start = time.time()
    for each in list:

        each =''.join(each)
        print(each)


        # imp = jieba.analyse.textrank(test, withWeight=True)
        # print('imp = ',imp)

        cost_time = time.time() - time_start
        print('jieba_textrank 花了', cost_time / 3600, '小時')

def jieba(load_dir_path,save_path):
    import jieba
    time_start = time.time()
    # 加入自定義 詞
    jieba.load_userdict('./mydict.txt')

    # 加入停用 詞
    # 無函式 只能變成串列 於程式中阻擋
    stopword_set = set()
    with open('./stopword.txt', encoding='utf-8') as file:
        for each_stopword in file.read().split('\n'):
            stopword_set.add(each_stopword)

    # loading will jieba txt
    dir_path = load_dir_path
    print('load_dir_path=',dir_path)
    print('全部檔案=', os.listdir(dir_path))
    txt_lines = []
    for each_txt in os.listdir(dir_path):
        if '.txt' in each_txt:
            print(each_txt)
            with open(dir_path + '\\' + each_txt, 'r', encoding='utf8') as f:
                i = 0
                for txt_line in f:

                    i += 1
                    # if '#' in txt_line:
                    #     continue

                    if i % 1000 == 0:
                        logging.info("已處理 {0} ".format(i))
                        cost_time = time.time() - time_start
                        print('jieba 花了', cost_time / 3600, '小時')

                    str_tmp = ''
                    jieba_cut_list = jieba.cut(txt_line)

                    if len(txt_line) >= 1000000:
                        print('each_line=', txt_line)
                        print('each_line_len=', len(txt_line))

                    try:
                        for each_jieba_cut in jieba_cut_list:

                            if each_jieba_cut not in stopword_set:
                                str_tmp += each_jieba_cut + " "

                        # str_tmp = str_tmp.replace('\n', '')

                    except Exception as e:
                        print(e)
                        print('jieba_cut_list',jieba_cut_list)
                        print(len(jieba_cut_list))

                    # 斷詞結果存檔
                    segSaveFile = save_path
                    with open(segSaveFile, 'ab') as saveFile:
                        saveFile.write('標題 : '.encode('utf-8')+txt_line.encode('utf-8'))
                        saveFile.write('jieba: '.encode('utf-8')+str_tmp.encode('utf-8'))
                        saveFile.write('\n'.encode())






    cost_time = time.time() - time_start
    print('jieba 花了',cost_time / 3600, '小時')
    print('save_path=',save_path)

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    jieba(load_dir_path='E:\資策會-DB106\專題\Pixnet',save_path='E:\資策會-DB106\專題\Pixnet\標題jieba_台北景點.txt')


    #
    # time_start = time.time()
    # imp_extract_tags = jieba.analyse.extract_tags(txt_notag, withWeight=True)
    # print('imp_extract_tags = ', imp_extract_tags)
    # print((time.time() - time_start) / 60)
    #
    #
    #
    # time_start = time.time()
    # imp_textrank = jieba.analyse.textrank(txt_notag, withWeight=True)
    # print('imp_textrank = ',imp_textrank)
    # print((time.time() - time_start) / 60)

if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')



