from gensim.corpora import WikiCorpus
import logging


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    #載下wiki檔案後 進行解析
    wiki_corpus = WikiCorpus('zhwiki-latest-pages-meta-current.xml.bz2', dictionary={})
    texts_num = 0
    with open("./wiki_texts.txt", 'w', encoding='utf-8') as output:
        for text in wiki_corpus.get_texts():
            output.write(' '.join(text) + '\n')
            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("已處理 %d 篇文章" % texts_num)


if __name__ == "__main__":
    main()
    print('Complete!!!!!!!!!!')