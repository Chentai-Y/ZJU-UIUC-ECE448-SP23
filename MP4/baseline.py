# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath
"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    
    word_set = []
    word_tag_table = []
    tag_set = []
    foo = 0
    # loop over the training set, build up the word & tag set
    for i in train:
        process = foo / len(train)*100
        print('initializing (figuring out number of words and tags):', process, '%')
        foo += 1
        for j in i:
                if j[0] not in word_set:
                        if j[0] != 'END' and j[0] != 'START':
                                word_set.append(j[0])
                                # check if the tag has been recorded
                                if j[1] not in tag_set:
                                        tag_set.append(j[1])

                else:
                        if j[1] not in tag_set:
                                tag_set.append(j[1])
                
    num_word = len(word_set)
    num_tag = len(tag_set)
    # table to record how many times a word occured in a certain tag
    word_tag_table = [0] * num_word
    for i in range(len(word_tag_table)):
        word_tag_table[i] = [0] * num_tag

    foo = 0
    tag_trained_set = [0]*num_word
    # loop over the training set, record how many times a word occured in a certain tag 
    for i in train:
           process = foo / len(train)*100
           print('training:', process, '%')
           foo += 1
           for j in i:
                  if j[0] == 'END' or j[0] == 'START':
                         continue
                  word_index = word_set.index(j[0])
                  tag_index = tag_set.index(j[1])
                  word_tag_table[word_index][tag_index] += 1
    
    # choose the most often occured tag for each word and the most often occured tag overall
    tag_occ_num = [0] * num_tag
    for i in range(len(word_tag_table)):
           max_val = max(word_tag_table[i])
           max_index = word_tag_table[i].index(max_val)
           tag_trained_set[i] = tag_set[max_index]
           for j in range(num_tag):
                  tag_occ_num[j] += word_tag_table[i][j]

    max_val = max(tag_occ_num)
    max_index = tag_occ_num.index(max_val)
    most_often_tag = tag_set[max_index]
    tagged_test_set = []
    for i in range(len(test)):
           tagged_test_set.append([])

    # tag the test set
    foo = 0
    for i in range(len(test)):
           process = foo / len(test)*100
           print('tagging:', process, '%')
           foo += 1
           for j in test[i]:
                  if j == 'START' or j == 'END':
                         tagged_test_set[i].append((j,j))
                  elif j in word_set:
                         now_index = word_set.index(j)
                         tag = tag_trained_set[now_index]
                         tagged_test_set[i].append((j,tag))
                  else:
                         tagged_test_set[i].append((j,most_often_tag))

    return tagged_test_set

                        
                         
    