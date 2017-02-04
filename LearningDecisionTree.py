# # -*- coding:utf8 -*-
import scipy.io as sio
import math as mt
import matplotlib.pyplot as plt
import numpy as np
import time
from graphviz import Digraph

__Author__ = 'Tree_Diagram'

# 将选中的表情设置为1，其他为0,对应binary_targets
def choose_emotion(facial_expression, emotion):
    choosen_emotion = []
    for emo in facial_expression:
        if emo == emotion:
            choosen_emotion.append(1)
        else:
            choosen_emotion.append(0)
    return choosen_emotion

# 将属性编号为0到44，对应attributes
def generate_attributes(num_attributes):
    return [range(0, 45)]

def examples_havesamevalue(binary_targets):
    flag=True
    if len(binary_targets) !=0:
        target=binary_targets[0]

    # 遍历所有的example
    for j in range(0,len(binary_targets)):
        if target!=binary_targets[j]:
            flag=False
            break
    if flag:
        return target
    else:
        return -1

def get_information_gain(p, n):
    return - p / (p + n) * mt.log10(p / (p + n)) / mt.log10(2) - n / (p + n) * mt.log10(n / (p + n)) / mt.log10(2)

#fine
def choose_best_attribute(data_set, attributes, binary_target):
    n0 = 0
    n1 = 0
    information_gain = []
    for value in binary_target:
        if value == 1:
            n1 += 1
        else:
            n0 += 1

    entropy = get_information_gain(n1, n0)

    num = len(data_set[0])

    for index in xrange(num):
        pn1 = 0
        pn0 = 0
        nn0 = 0
        nn1 = 0

        for ind, value in enumerate(data_set[:, index]):
            if value == 1:
                if binary_target[ind] == 1:
                    pn1 += 1
                else:
                    nn1 += 1
            else:
                if binary_target[ind] == 1:
                    pn0 += 1
                else:
                    nn0 += 1

        entropy0 = (pn0 + nn0) / (n1 + n0) * get_information_gain(pn0, nn0)
        entropy1 = (pn1 + nn1) / (n1 + n0) * get_information_gain(pn1, nn1)
        information_gain.append(entropy - entropy0 - entropy1)

    return list.index(max(information_gain))

def majority_value(binary_targets):
    length = 0
    for row in binary_targets:
        if row == 1:
            length = length + 1

    if length * 2 >= len(binary_targets):
        return 1
    else:
        return 0

def generate_sub(examples,binary_targets,best_attribute,attribute_state):
    myexamples=[]
    mybinary_targets=[]
    for ind in enumerate(examples):
        if examples[ind][best_attribute]==attribute_state:
            myexamples.append(examples[ind])
            mybinary_targets.append(binary_targets[ind])
    return myexamples,mybinary_targets

# 主要被调用函数
def DECISION_TREE_LEARNING(examples, attributes, binary_targets):
    target_value=examples_havesamevalue(binary_targets)

    if target_value!=-1:
        if target_value==1:
            return [time.time(),'YES',[]]
        else:
            return [time.time(), 'NO', []]
    elif len(attributes)==0:
        ma_value=majority_value(binary_targets)
        if ma_value==1:
            return [time.time(),'YES',[]]
        else:
            return [time.time(), 'NO', []]
    else:
        best_attribute=choose_best_attribute(examples,attributes,binary_targets)
        tree=[time.time(),str(best_attribute),[]]
        for attribute_state in [0,1]:
            name=time.time()
            tree[2].append(name)
            newexamples,newbinary_targets=generate_sub(examples,binary_targets,best_attribute,attribute_state)
            if len(newexamples)==0:
                return [time.time(),majority_value(binary_targets),[]]
            else:
                del attributes[best_attribute]
                del newexamples[:,best_attribute]
                DECISION_TREE_LEARNING(newexamples,attributes,newbinary_targets)[0]=name
    tree = 1
    return tree

def DrawDecisionTree(label, tree, dot):
    for node in tree:
        if node[0] == label:
            item = node
        break
    [label, name, leaves]= item
    dot.node(label, name)
    if len(leaves) == 0:
        pass
    else:
        DrawDecisionTree(leaves[0], tree, dot)
        DrawDecisionTree(leaves[1], tree, dot)
        dot.edges(label, leaves[0], label='0')
        dot.edges(label, leaves[1], label='1')
    return dot

if __name__ == "__main__":
    # 导入数据
    matfn = u'/home/roland/PycharmProjects/test1/forStudents/cleandata_students.mat'
    data = sio.loadmat(matfn)
    # 45个属性的数据,对应choose_emotion中第一个参数
    facial_expression = data['y']
    # 不同的label,对应examples
    actions = data['x']
    target= examples_havesamevalue(choose_emotion(facial_expression,4))
    print target
    print len(data['x'][0])



