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
# Modified Spring 2021 by Kiran Ramnath (kiranr2@illinois.edu)

"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
import numpy as np
import math

def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    
    START_TAG = "START"
    END_TAG = "END"
    UNKNOWN = "UNKNOWN"
    
    # Part1: Count occurrences of tags, tag pairs, tag/word pairs  
    tot_sent = 0
    tag_occ = {}
    tag_pair_occ = []
    emi_occ = {}

    for sentence in train:
        process = tot_sent/len(train)*100
        print('training--part 1 in 5:',process,'%')
        tot_sent += 1
        for item in sentence:
            word = item[0]
            tag = item[1]
            if tag not in tag_occ:
                tag_occ[tag] = 1
            else:
                tag_occ[tag] += 1
    

    #del tag_occ[START_TAG]
    #del tag_occ[END_TAG]
    tag_pair_occ = {}
    emi_occ = {}
    word_bag = []
    for key in tag_occ.keys():
        tag_pair_occ.setdefault(key, {})
        emi_occ.setdefault(key, {})
    count = 0
    for sentence in train:
        count += 1
        process = count/len(train)*100
        print('training--part 2 in 5:',process,'%')
        for i in range(1, len(sentence)): # get rid off start and end
            pre_tag = sentence[i-1][1]
            word = sentence[i][0]
            tag = sentence[i][1]

            if tag not in tag_pair_occ[pre_tag]:
                tag_pair_occ[pre_tag][tag] = 1
            else:
                tag_pair_occ[pre_tag][tag] += 1

            if word not in emi_occ[tag]:
                emi_occ[tag][word] = 1
            else:
                emi_occ[tag][word] += 1

            if word not in word_bag:
                word_bag.append(word)

    
    sub_ini_occ = {}
    for key in tag_occ:
        if key not in tag_pair_occ[START_TAG]:
            num = 0
        else:
            num = tag_pair_occ[START_TAG][key]
        sub_ini_occ[key] = num

    # Part2: Compute smoothed probabilities
    sub_ini_prob = {}
    tag_pair_prob = {}
    emi_prob = {}

    lap_coef = 0.001
    
    tag_list = []
    for tag in tag_occ.keys():
        tag_list.append(tag)
    tag_num = len(tag_list)
    print(tag_list)
    for i in range(tag_num):
        tag = tag_list[i]
        if START_TAG in tag_pair_occ[tag]:
            del tag_pair_occ[tag][START_TAG]
        if END_TAG in tag_pair_occ[tag]:
            del tag_pair_occ[tag][END_TAG]

    del sub_ini_occ[START_TAG]
    del sub_ini_occ[END_TAG]
    del tag_pair_occ[START_TAG]
    del tag_pair_occ[END_TAG]
    del emi_occ[START_TAG]
    del emi_occ[END_TAG]
    del tag_occ[START_TAG]
    del tag_occ[END_TAG]


    count = 0
    for key in sub_ini_occ:
        count += 1
        process = count/len(sub_ini_occ)*100
        print('training--part 3 in 5:',process,'%')
        ini_occ = sub_ini_occ[key]
        smoothed_prob = (ini_occ + lap_coef) / (tot_sent + lap_coef * tag_num)
        log_prob = math.log(smoothed_prob)
        sub_ini_prob[key] = log_prob

    count = 0
    for key_1 in tag_pair_occ:
        count += 1
        process = count/len(tag_pair_occ)*100
        print('training--part 4 in 5:',process,'%')
        tag_pair_prob.setdefault(key_1,{})
        tot_pair = sum(tag_pair_occ[key_1].values())
        for key_2 in tag_occ:
            if key_2 not in tag_pair_occ[key_1]:
                occ = 0
            else:
                occ = tag_pair_occ[key_1][key_2]
            
            smoothed_prob = (occ + lap_coef) / (tot_pair + lap_coef * tag_num)
            log_prob = math.log(smoothed_prob)
            tag_pair_prob[key_1][key_2] = log_prob

    count = 0
    for key_1 in emi_occ:
        count += 1
        process = count/len(emi_occ)*100
        print('training--part 5 in 5:',process,'%')
        emi_prob.setdefault(key_1,{})
        tot_emi = sum(emi_occ[key_1].values())
        for word in word_bag:
            if word not in emi_occ[key_1]:
                occ = 0
            else:
                occ = emi_occ[key_1][word]
            smoothed_prob = (occ + lap_coef) / (tot_emi + lap_coef * tag_num)
            log_prob = math.log(smoothed_prob)
            emi_prob[key_1][word] = log_prob
    
    
    tag_list = []
    for tag in sub_ini_prob.keys():
        tag_list.append(tag)
    tag_num = len(tag_list)

    # Part4: Construct the trellis. Notice that for each tag/time pair, 
    # you must store not only the probability of the best path but also 
    # a pointer to the previous tag/time pair in that path.
    result = []
    count = 0
    for sentence in test:
        count += 1
        process = count/len(test)*100
        print('conducting viterbi for testing set:',process,'%')
        word_num = len(sentence)
        vtb_prob_table = np.zeros((tag_num,word_num-2))
        vtb_pointer_table = np.zeros((tag_num,word_num-2))

        for i in range(tag_num):
            tag = tag_list[i]
            p_ini = sub_ini_prob[tag]
            word = sentence[1]
            if word in word_bag:
                p_emi = emi_prob[tag][word]
            else:
                p_emi = 0
            p_tot = p_ini + p_emi
            ptr = i
            vtb_prob_table[i][0] = p_tot
            vtb_pointer_table[i][0] = ptr

        for i in range(2,word_num-1):
            word = sentence[i]
            for j in range(tag_num):
                tag = tag_list[j]
                if word in word_bag:
                    p_emi = emi_prob[tag][word]
                else:
                    p_emi = 0
                p_tot = -1000
                ptr = 0
                for k in range(tag_num):
                    pre_tag = tag_list[k]
                    p_pair = tag_pair_prob[pre_tag][tag]
                    p_prev = vtb_prob_table[k][i-2]
                    p_tot_temp = p_prev + p_pair + p_emi
                    if p_tot_temp > p_tot:
                        p_tot = p_tot_temp
                        ptr = k
                vtb_prob_table[j][i-1] = p_tot
                vtb_pointer_table[j][i-1] = ptr
        
        path_end = np.argmax(vtb_prob_table[:,-1])
        
        ptr = path_end
        result_tag_list = []
        for i in range(word_num-2, 0, -1):
            tag = tag_list[ptr]
            word = sentence[i]
            result_tag_list.append((word,tag))
            pre_ptr = ptr
            ptr = int(vtb_pointer_table[pre_ptr][i-1])
            

        result_tag_list.reverse()
        result_tag_list.insert(0,(START_TAG,START_TAG))
        result_tag_list.append((END_TAG,END_TAG))
        result.append(result_tag_list)

    
    # Part5: Return the best path through the trellis
    
    return result