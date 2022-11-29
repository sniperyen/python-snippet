# encoding: utf-8

"""
汉字转拼音的用法，参考 https://cuiqingcai.com/6519.html
"""

from pypinyin import pinyin
from pypinyin import lazy_pinyin
from pypinyin import slug
from pypinyin import Style

import logging

logging.basicConfig(format='%(asctime)s [line:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':
    s = "我们是共产主义接班人"
    logging.info(slug(s, separator=''))
    logging.info(slug(s, separator='', style=Style.FIRST_LETTER))
    logging.info(lazy_pinyin(s, errors='ignore'))
    logging.info(pinyin(s))
