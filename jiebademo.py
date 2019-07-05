import jieba.posseg as psg
from collections import Counter

import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud,ImageColorGenerator


def cut_cache(text):
    words_with_attr = [(x.word,x.flag) for x in psg.cut(text) if len(x.word)>=2]
    with open('cut_cache.txt','w+',encoding='utf8') as f:
        for x in words_with_attr:
            f.write('{0}\t{1}\n'.format(x[0],x[1]))
    return words_with_attr


def clean(text):
    stop_attr = ['a','ad','b','c','d','f','df','m','mq','p','r','rr','s','t','u','v','z']
    clean = [x[0] for x in text if x[1] not in stop_attr]
    return clean

def get_top(words,topn):
    result = {}
    c = Counter(words).most_common(topn)
    with open('reslut{0}.txt'.format(topn),'w+',encoding='utf8') as f:
        for x in c:
            f.write('{0},{1}\n'.format(x[0],x[1]))
            result[x[0]] = x[1]
    return result


def generate_wordCloud(img_bg_path,top_words_with_freq,font_path,to_save_img_path,background_color = 'white'):

    img_bg = imread(img_bg_path)
    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color=background_color,  # 词云图片的背景颜色，默认为白色
                   max_words=500,  # 最大显示词数为1000
                   mask=img_bg,  # 背景图片蒙版
                   max_font_size=50,  # 字体最大字号
                   random_state=30,  # 字体的最多模式
                   width=4000,  # 词云图片宽度
                   margin=20,  # 词与词之间的间距
                   height=2800)  # 词云图片高度

    # 用top_words_with_freq生成词云内容
    wc.generate_from_frequencies(top_words_with_freq)

    # 用matplotlib绘出词云图片显示出来
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

    wc.to_file(to_save_img_path)


def main():
    santi_text = open('./santi.txt','r',encoding='utf8').read()
    word = cut_cache(santi_text)
    clean_word = clean(word)
    result = get_top(clean_word,500)
    generate_wordCloud('./bg.jpg', result, './yahei.ttc', './santi_cloud.png')
    print('end')
if __name__=='__main__':
    main()
