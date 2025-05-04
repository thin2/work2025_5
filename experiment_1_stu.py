# -*- coding: utf-8 -*-
"""
人工智能基础 实验报告_1 
"""
theStr = "24151A218" #串的内容是你的完整学号
theSetChars = set(theStr)
theListChars = [i for i in theSetChars] #得到theStr中各种字符（显然无重复、无序）组成的列表
theListNumberOfEachChar = [] # 定义一个空的列表theListNumberOfEachChar，存储theListChars中对应字符的出现次数。
theLength= len(theListChars)
i = 0
while i < theLength:
    theChar = theListChars[i]
    theListNumberOfEachChar[len(theListNumberOfEachChar):] = [theStr.count(theChar)]# 参照教材P45 习题2 一、填空题 (7)
    
    i += 1
print("显示串\"{}\"的统计信息：它共含{}种字符。每个字符出现的次数详情：".format(theStr, theLength))
i = 0
while i < theLength:
    print("'{}': {}".format(theListChars[i], theListNumberOfEachChar[i]))
    i += 1




