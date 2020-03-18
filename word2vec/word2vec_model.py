from gensim.models import word2vec
import matplotlib.pyplot as plt
import time

def built_model(txt_path):

    # 建模型
    time_start = time.time()
    sentences = word2vec.LineSentence(txt_path)
    model = word2vec.Word2Vec(sentences, size=300, iter=100, sg=0, workers=3)

    model.save("./word2vec_model_words{0}.model".format(model.corpus_total_words))

    print(model.corpus_total_words)
    cost_time = time.time() - time_start
    print('built_model 花了', cost_time / 3600, '小時')


def load_model(model_path,test_words_list):
    # load 模型
    model = word2vec.Word2Vec.load(model_path)

    for each_word in test_words_list:

        print('{0} :'.format(each_word))
        try:
            each_word_similar_list = model.most_similar(each_word)
            print(each_word_similar_list)
            x = [a[0] for a in each_word_similar_list]
            y = [a[1] for a in each_word_similar_list]

            # 原始圖案
            plt.plot(x,y)
            plt.title('{0}'.format(each_word), weight="bold")
            plt.show()
        except KeyError as e:
            # print(e)
            print('Sorry word {0} not in vocabulary'.format(each_word))

def main():

    # 模式切換
    # mode = 'built_model'
    mode = 'load_model'

    if mode == 'built_model':

        # 建模型
        built_model(txt_path="C:\\Users\Big data\PycharmProjects\PyETL2\Spades_Team\segDone_spades_v3.txt")




    elif mode == 'load_model':

        test_words_list = ['踏青']
        # test_words_list =['公園綠地','踏青','綠地',
        #                   '觀光夜市','夜市','小吃',
        #                   '百貨商圈','逛街']
        #load 來模型使用
        load_model(model_path="C:\\Users\Big data\PycharmProjects\PyETL2\Spades_Team\word2vec_model_words57876037.model",
                   test_words_list=test_words_list)


if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')