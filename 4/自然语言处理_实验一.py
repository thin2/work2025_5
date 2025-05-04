#2212080182-韩宁
def FMM(dict, sentence):
    fmmresult = []
    # 词典中最长词长度
    max_len = max([len(item) for item in dict])
    start = 0
    # FMM为正向，start从初始位置开始，指向结尾即为结束
    while start != len(sentence):
        # index的初始值为start的索引+词典中元素的最大长度或句子末尾
        index = start + max_len
        if index > len(sentence):
            index = len(sentence)
        for i in range(max_len):
            # 当分词在字典中时或分到最后一个字时，将其加入到结果列表中
            if (sentence[start:index] in dict) or (len(sentence[start:index]) == 1):
                # print(sentence[start:index], end='/')
                fmmresult.append(sentence[start:index])
                # 分出一个词，start设置到index处
                start = index
                break
            # 正向时index每次向句尾挪一位
            index += -1
    return fmmresult
#%%
#2212080182-韩宁
def RMM(dict, sentence):
    rmmresult = []
    # 词典中最长词长度
    max_len = max([len(item) for item in dict])
    start = len(sentence)
    # RMM为逆向，start从末尾位置开始，指向开头位置即为结束
    while start != 0:
        # 逆向时index的初始值为start的索引-词典中元素的最大长度或句子开头
        index = start - max_len
        if index < 0:
            index = 0
        for i in range(max_len):
            # 当分词在字典中时或分到最后一个字时，将其加入到结果列表中
            if (sentence[index:start] in dict) or (len(sentence[index:start]) == 1):
                # print(sentence[index:start], end='/')
                rmmresult.insert(0, sentence[index:start])
                # 分出一个词，start设置到index处
                start = index
                break
            # 逆向时index每次向句头挪一位
            index += 1
    return rmmresult
#%%
#2212080182-韩宁
def BM(dict, sentence):
    # res1 与 res2 为FMM与RMM结果
    res1 = FMM(dict, sentence)
    res2 = RMM(dict, sentence)
    if len(res1) == len(res2):
        # FMM与RMM的结果相同时，取任意一个
        if res1 == res2:
            return res1
        else:
            # res1_sn 和 res2_sn 为两个分词结果的单字数量，返回单字较少的
            res1_sn = len([i for i in res1 if len(i) == 1])
            res2_sn = len([i for i in res2 if len(i) == 1])
            return res1 if res1_sn < res2_sn else res2
    else:
        # 分词数不同则取分出词较少的
        return res1 if len(res1) < len(res2) else res2
#%%
def load_dict(file_path):
    """
    加载词典文件，返回词典集合和最大单词长度
    :param file_path: 词典文件路径
    :return: word_dict（词典集合），max_word_length（最大单词长度）
    """
    word_dict = set()  # 使用集合存储词典中的词语，便于快速查找
    max_word_length = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                # 取每一行的第一个元素作为单词
                word = line.split()[0]
                word_dict.add(word)
                # 更新最大单词长度
                if len(word) > max_word_length:
                    max_word_length = len(word)
    return word_dict, max_word_length

#%%
word_list, max_length = load_dict('dict.txt')
print("2212080182-韩宁")
print(f"词典中的词语数量: {len(word_list)}")
print(f"词典中最大单词的长度: {max_length}")

#%%

#%%
dict = ['我', '在', '燕山大学', '读书', '专业', '是', '软件', '工程', '软件工程']
sentence = '我在燕山大学读书，专业是软件工程'
print("the results of FMM :\n", FMM(dict, sentence), end="\n")
print("the results of RMM :\n", RMM(dict, sentence), end="\n")
print("the results of BM :\n", BM(dict, sentence),end="\n")

#%%
text="在当下经济环境中，政府补贴是刺激消费、推动经济发展的重要手段。近年来，河南省出台多项补贴政策，涉及消费、就业、创业等多个领域。国家对地方经济发展的政策支持也为河南的补贴举措提供了有力保障，在此背景下，研究河南省居民对补贴的认知及消费意愿具有重要现实意义。"
print("the results of FMM :\n", FMM(word_list, text), end="\n")
print("the results of RMM :\n", RMM(word_list, text), end="\n")
print("the results of BM :\n", BM(word_list, text),end="\n")
#%%
text='研究生命起源'
print("the results of FMM :\n", FMM(word_list, text), end="\n")
print("the results of RMM :\n", RMM(word_list, text), end="\n")
print("the results of BM :\n", BM(word_list, text),end="\n")
#%%
print(FMM(word_list, text)==RMM(word_list, text)==BM(word_list, text))