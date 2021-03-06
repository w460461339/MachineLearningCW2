# # -*- coding:utf8 -*-
import scipy.io as sio
import math as mt
import matplotlib.pyplot as plt
import numpy as np
import time
import TestDecisionTree
import graphviz
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
    return range(0, num_attributes)


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
    pf = float(p)
    nf = float(n)
    return - pf / (pf + nf) * mt.log(pf / (pf + nf), base=2) \
           - nf / (pf + nf) * mt.log(nf / (pf + nf), base=2)


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

        for ind, value in enumerate(data_set):
            if value[index] == 1:
                if binary_target[ind] == 1:
                    pn1 += 1
                else:
                    nn1 += 1
            else:
                if binary_target[ind] == 1:
                    pn0 += 1
                else:
                    nn0 += 1

        if pn1 == 0 or nn1 == 0:
            entropy1 = 0
        else:
            entropy1 = float(pn1 + nn1) / float(n1 + n0) * get_information_gain(pn1, nn1)

        if pn0 == 0 or nn0 == 0:
            entropy0 = 0
        else:
            entropy0 = float(pn0 + nn0) / float(n1 + n0) * get_information_gain(pn0, nn0)

        information_gain.append(entropy - entropy0 - entropy1)
        print information_gain
        print "max index " + str(information_gain.index(max(information_gain)))
        print
    return information_gain.index(max(information_gain))


def majority_value(binary_targets):
    length = 0
    for row in binary_targets:
        if row == 1:
            length += 1

    if length * 2 >= len(binary_targets):
        return 1
    else:
        return 0


def generate_sub(examples,binary_targets,best_attribute,attribute_state):
    myexamples=[]
    mybinary_targets=[]
    for ind, val in enumerate(examples):
        if examples[ind][best_attribute]==attribute_state:
            myexamples.append(examples[ind])
            mybinary_targets.append(binary_targets[ind])
    return myexamples,mybinary_targets

# 主要被调用函数
TREE_NODES = []


def DECISION_TREE_LEARNING(examples, attributes, binary_targets):
    target_value=examples_havesamevalue(binary_targets)
    if target_value!=-1:
        if target_value==1:
            node = [time.time(), 'YES', []]
            TREE_NODES.append(node)
            return node
        else:
            node = [time.time(), 'NO', []]
            TREE_NODES.append(node)
            return node
    elif len(attributes)==0:
        ma_value=majority_value(binary_targets)
        if ma_value==1:
            node = [time.time(), 'YES', []]
            TREE_NODES.append(node)
            return node
        else:
            node = [time.time(), 'NO', []]
            TREE_NODES.append(node)
            return node
    else:
        best_attribute=choose_best_attribute(examples,attributes,binary_targets)
        tree=[time.time(),str(attributes[best_attribute]),[]]
        for attribute_state in [0,1]:
            newexamples,newbinary_targets=generate_sub(examples,binary_targets,best_attribute,attribute_state)
            if len(newexamples)==0:
                ma_value2 = majority_value(binary_targets)
                if ma_value2 == 1:
                    node=[time.time(), 'YES', []]
                    TREE_NODES.append(node)
                    return node
                else:
                    node = [time.time(), 'NO', []]
                    TREE_NODES.append(node)
                    return node
            else:
                attributes = attributes[:best_attribute] + attributes[best_attribute + 1:]
                newexamples = map(lambda x:x[:best_attribute] + x[best_attribute + 1:], newexamples)
                nextTreeNode=DECISION_TREE_LEARNING(newexamples,attributes,newbinary_targets)
                tree[2].append(nextTreeNode[0])
        TREE_NODES.append(tree)
    return tree

def DrawDecisionTree(nodelabel, tree, dot):
    item = []
    for node in tree:
        if node[0] == nodelabel:
            item = node
            break
    print item
    [nodelabel, name, leaves]= item
    strnodelabel = "%.18f" % nodelabel
    dot.node(strnodelabel, str(name))
    if len(leaves) == 0:
        pass
    else:
        DrawDecisionTree(leaves[0], tree, dot)
        DrawDecisionTree(leaves[1], tree, dot)
        strleaves0 = "%.18f" % leaves[0]
        strleaves1 = "%.18f" % leaves[1]
        dot.edge(strnodelabel, strleaves0, label='0',_attributes=None)
        dot.edge(strnodelabel, strleaves1, label='1',_attributes=None)
    return dot

def topythonlist(data):
    mylist=[]
    for d in data:
        for dd in d:
            mylist.append(dd)
    return mylist


def topythonnestedlist(data):
    mynestedlist=[]
    for da in data:
        mylist=[]
        for dda in da:
            mylist.append(dda)
        mynestedlist.append(mylist)
    return mynestedlist

if __name__ == "__main__":
    # load data as numpy matrix
    matfn = u'cleandata_students.mat'
    matfn2= u'noisydata_students.mat'
    data = sio.loadmat(matfn)
    noisydata=sio.loadmat(matfn2)

    # convert label to python list
    facial_expression=topythonlist(data['y'])

    # convert label to python list
    no_facial_expression=topythonlist(noisydata['y'])

    # convert label to python list
    examples =topythonnestedlist(data['x'])

    # convert label to python list
    noisyexample=topythonnestedlist(noisydata['x'])

    # for attribute
    attributes=generate_attributes(45)

    # for clean TREE
    TREELIST = []
    for x in range(1,11):
        for j in range(1,7):
            # for binary_targets
            binary_targets = choose_emotion(facial_expression, j)
            DECISION_TREE_LEARNING(examples[x::10],attributes,binary_targets[x::10])
            TREELIST.append(TREE_NODES)
            TREE_NODES=[]

    for tree in TREELIST:
        print tree

    print 'noisy'

    # for noisy TREE
    NOISYTREELIST=[]
    for x in range(1,11):
        for j in range(1,7):
            # for binary_targets
            binary_targets = choose_emotion(no_facial_expression, j)
            DECISION_TREE_LEARNING(noisyexample[x::10],attributes,binary_targets[x::10])
            NOISYTREELIST.append(TREE_NODES)
            TREE_NODES=[]

    for tree in NOISYTREELIST:
        print tree

    test_labbel = TestDecisionTree.predictions(TREELIST, test_examples)
    print test_labbel
    print len(test_labbel)
    dot = Digraph(comment='learning_draw')
    DrawDecisionTree(tree[-1][1],tree,dot)
    dot.render('test-output\learning_draw.gv',view=True)
    # print len(data['x'][0])


