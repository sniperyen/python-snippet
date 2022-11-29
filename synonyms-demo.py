# -*- coding: utf-8 -*-

"""
文章生成: 用一篇现有的文章进行拆分，近义词替换，然后生成一篇新的文章。
"""
import random
import time
import synonyms

import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s [line:%(lineno)d  thread:%(thread)d] %(message)s',
                    level=logging.INFO)


# 近义词替换，根据词性，替换名词，地点词
def similar(text):
    begin = time.time()
    words, tags = synonyms.seg(text)
    result = ''
    for i, word in enumerate(words):
        if len(word) > 1 and ("n" in tags[i]):
            nearby_words, nearby_words_score = synonyms.nearby(word)
            if len(nearby_words) >= 6:
                # 只在大于0.6 的近义词中寻找，如果没有大于0.6的近义词，则不替换
                if nearby_words_score[0] < 0.6:
                    result += word
                else:
                    result += random.choice(nearby_words[1:6])
            else:
                result += word
        else:
            result += word
    logging.info('文本长度: %d; 耗时: %s' % (len(text), time.time() - begin))
    return result


article = '此前，拜登也曾就弗洛伊德之死引发的抗议示威发表评论。当地时间5月31日，拜登前往特拉华州一个爆发了抗议示威活动的现场。他还在推特上发布了一张自己在现场与一名黑人谈话的照片，并写道：“我们国家现在处于痛苦之中，但我们决不能让这种痛苦摧毁我们。成为总统后，我将帮助引导这场对话。更重要的是，我会倾听。”据美国《纽约时报》报道，随着抗议活动震动全美，拜登试图和特朗普的应对方式形成鲜明对比。报道称，特朗普的做法主要是火上浇油，怒斥抗议者是“暴徒”并暗示警察会向他们开枪。与之相较，拜登及其竞选团队希望传递出他们一直希望传递的重要信息：拜登对国家的领导将是稳健的，不会给国家带来混乱。不过美联社等媒体认为，拜登应对抗议骚乱的柔和方式，可能被特朗普的“大嗓门”淹没。'

if __name__ == '__main__':
    logging.info(similar(article))
    logging.info('*' * 100)
    logging.info(similar(article))
