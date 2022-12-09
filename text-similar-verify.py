# -*- coding: utf-8 -*-

import numpy as np
import jieba


class CountVectorizer:
    def __init__(self):
        self.word2id = {}
        self.id2word = {}
        self.vocab_size = 0

    def fit_transform(self, texts):
        # 构建词典
        for text in texts:
            for word in text.split():
                if word not in self.word2id:
                    self.word2id[word] = self.vocab_size
                    self.id2word[self.vocab_size] = word
                    self.vocab_size += 1
        # 构建词频矩阵
        X = np.zeros((len(texts), self.vocab_size))
        for i, text in enumerate(texts):
            for word in text.split():
                X[i, self.word2id[word]] += 1
        return X

def cosine_similarity(text1, text2):
    # 将文本转换为词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([text1, text2])
    # 计算两个文本的余弦相似度
    similarity = np.dot(X[0], X[1].T) / (np.linalg.norm(X[0]) * np.linalg.norm(X[1]))
    return similarity

def cut_word(text):
    #进行中文分詞
    return " ".join(list(jieba.cut(text)))

# 定义相似度阈值
threshold = 0.8

# 输入文本
text1 = input('Please enter the first text: ')
text2 = input('Please enter the second text: ')

# 计算相似度并判断
similarity = cosine_similarity(cut_word(text1), cut_word(text2))
print(similarity)
if similarity >= threshold:
    print('The texts are similar.')
else:
    print('The texts are not similar.')
