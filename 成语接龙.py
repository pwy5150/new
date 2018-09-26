# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:25:25 2018

@author: pwy5150
"""

from langconv import * #简繁体转换
import pandas as pd
import random
import os
os.chdir('./')
#输入:
#--------------把输入内容和语料库里最短的词做比较，如果长度小于语料库最短的词就重新输入--------------
#--------------如果有出现字母或者数20字就再来一次--------------
#--------------再增加一项输入有繁体的时候，用转换函数检查--------------


#简繁体检查，繁体转简体,检验是否出现错别字以及把输入的词转换
def translation(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    #df[col] = df[col].apply()
    sentence = Converter('zh-hans').convert(sentence)
    #print('转换成功')
    return sentence
#长度检验
def min_len(lst):
    Min = []
    for i in lst:
        Min.append(len(i))
    return min(Min)
def max_len(lst):
    Max = []
    for i in lst:
        Max.append(len(i))
    return max(Max)
#区分汉字，编码的内容
def isAllZh(s):
    for c in s:
        if not('\u4e00' <= c <= '\u9fa5'):
            return False
    return True
#区分字母和数字
def input_(lst):
    a = input('请输入成语:\n')
    while isAllZh(a) == False or a.isnumeric() == True:
        print('请再试一次')
        a = input('请重新输入成语:')
    else:
        while len(a) < min_len(lst) or len(a) > max_len(lst):
            print('请再试一次')
            a = input('请重新输入成语:')        
        else:
            print('你输入的是:%s'%(a))
            return a
#------------------读取语料库并筛选字段----------------------------
#输出字段列表
def read_col():
    data = pd.read_excel('chengyu.xlsx',encoding='gbk')
    return data.columns.tolist()
#读取文件
def read():
    data = pd.read_excel('chengyu.xlsx',encoding='gbk')
    return data
#选择字段
def choose_df():
    df = read()
    collst= read_col()
    for col in collst:
        if col == '成语':
            df[col] = df[col].apply(lambda x:translation(x))
            df[col] = df[col].str.replace('，','')
            s = df[col]
    return s
#匹配
def match():
    new = choose_df().values
    lst = new.tolist()
    word = translation(input_(lst))
    while word not in new:
        print('匹配不成功,请再输入一次:')
        word = translation(input_(lst))
    else:
        print('匹配成功')
        return word
#这是做提取最后一个字符，以及检验临时语料库长度是否为0
def loop_take():
    word = match()
    s = choose_df()
    pattern = word[-1]
    #str.match 精确匹配
    #str.contains 包含
    #str.startswith 以什么开头
    take_lst = s[s.str.startswith(pattern,na=False)].values.tolist()
    try:
        num = random.randint(1,len(take_lst))
        new = take_lst[num-1]
        return(new)
    except:
        return('找不到成语')
#循环成语接龙
def loop():
    word = match()
    s = choose_df()
    pattern = word[-1]
    take_lst = s[s.str.startswith(pattern,na=False)].values.tolist()
    while len(take_lst)!=0:
        a = loop_take()
        print(a)
        if a == '找不到成语':
            print('game over')
            print('电脑输了')
            break
    else:
        print('game over')
loop()
            
#---------------------------------这段循环----------------------------------
#问题:忘记忽略标点符号,解决办法:直接处理excel 文件里面的标点符号(已经解决)
#loop这里最好不显示，这是为了让loop里面的while判断出来的临时语库的长度不为0
#还缺了一个认输机制
#认输这里，要重新写才行