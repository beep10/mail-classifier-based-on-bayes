# -*- coding: UTF-8 -*-
import codecs
import json
import random
import math

###获取元信息中的特征###
def get_inf(s):
    meta = list()
    text = codecs.open(s,"r","utf-8")
    send = False
    to = False
    date = False
    pr1 = False
    pr2 = False
    for line in text.readlines():
        l = line.split()
        if len(line) == 1:
            break
        if l[0] == "Received:" and send == False:
            meta.insert(0,l[2])
            send = True
        if l[0] == "To:" and to == False:
            meta.insert(1,l[1])
            to = True
        if l[0] == "Date:" and date == False:
            meta.insert(2,l[1])
            meta.insert(3,l[2]+l[3]+l[4])
            meta.insert(4,l[5][0:2])
            date = True
        if l[0] == "X-Priority:" and pr1 == False:
            meta.insert(5,l[1])
            pr1 = True
        if l[0] == "X-MSMail-Priority:" and pr2 == False:
            meta.insert(6,l[1])
            pr2 = True
    text.close()
    if send == False:
        meta.insert(0,'u')
    if to == False:
        meta.insert(1,'u')
    if date == False:
        meta.insert(2,'u')
        meta.insert(3,'u')
        meta.insert(4,'u')
    if pr1 == False:
        meta.insert(5,'u')
    if pr2 == False:
        meta.insert(6,'u')
    return meta

###获取正文信息###
def get_msg(s):
    msg = ""
    ismsg = False
    text = codecs.open(s,"r","utf-8")
    for line in text.readlines():
        if ismsg == True:
            msg += line
        if len(line) == 1:
            ismsg = True
    text.close()
    return msg

# 参数说明：
# train_list:训练集
# valid_list:验证集
# precent_of_train:训练比例
# num_of_feature:特征词数量
# mode:判定方式：1为只是用特征词，2为只使用元数据，3为两者都使用
def work(train_list,valid_list,precent_of_train,num_of_feature,mode):
    d = dict()
    sender = dict()
    to = dict()
    week = dict()
    date = dict()
    time = dict()
    pr1 = dict()
    pr2 = dict()
    tr_list = random.sample(train_list,int(precent_of_train*len(train_list)))
    ####分词统计####
    num_ham = 1
    num_spam = 1
    for i in range(len(tr_list)):
        entry = tr_list[i].split()
        if entry[0] == "spam":
            num_spam += 1
        else:
            num_ham += 1
        if mode == 1 or mode == 3:
            msg = get_msg(entry[1])
            words = msg.split()
            if entry[0] == "spam":
                for j in words:
                    if d.has_key(j):
                        d[j][0] += 1
                    else:
                        d[j] = [2,1,1.0]
            else:
                for j in words:
                    if d.has_key(j):
                        d[j][1] += 1
                    else:
                        d[j] = [1,2,1.0]
        if mode == 2 or mode == 3:
            meta = get_inf(entry[1])
            if entry[0] == "spam":
                if sender.has_key(meta[0]):
                    sender[meta[0]][0] += 1.0
                else:
                    sender[meta[0]] = [2.0,1.0]
                if to.has_key(meta[1]):
                    to[meta[1]][0] += 1.0
                else:
                    to[meta[1]] = [2.0,1.0]
                if week.has_key(meta[2]):
                    week[meta[2]][0] += 1.0
                else:
                    week[meta[2]] = [2.0,1.0]
                if date.has_key(meta[3]):
                    date[meta[3]][0] += 1.0
                else:
                    date[meta[3]] = [2.0,1.0] 
                if time.has_key(meta[4]):
                    time[meta[4]][0] += 1.0
                else:
                    time[meta[4]] = [2.0,1.0]
                if pr1.has_key(meta[5]):
                    pr1[meta[5]][0] += 1.0
                else:
                    pr1[meta[5]] = [2.0,1.0]
                if pr2.has_key(meta[6]):
                    pr2[meta[6]][0] += 1.0
                else:
                    pr2[meta[6]] =[2.0,1.0]
            else:
                if sender.has_key(meta[0]):
                    sender[meta[0]][1] += 1.0
                else:
                    sender[meta[0]] = [1.0,2.0]
                if to.has_key(meta[1]):
                    to[meta[1]][1] += 1.0
                else:
                    to[meta[1]] = [1.0,2.0]
                if week.has_key(meta[2]):
                    week[meta[2]][1] += 1.0
                else:
                    week[meta[2]] = [1.0,2.0]    
                if date.has_key(meta[3]):
                    date[meta[3]][1] += 1.0
                else:
                    date[meta[3]] = [1.0,2.0]
                if time.has_key(meta[4]):
                    time[meta[4]][1] += 1.0
                else:
                    time[meta[4]] = [1.0,2.0]    
                if pr1.has_key(meta[5]):
                    pr1[meta[5]][1] += 1.0
                else:
                    pr1[meta[5]] = [1.0,2.0]
                if pr2.has_key(meta[6]):
                    pr2[meta[6]][1] += 1.0
                else:
                    pr2[meta[6]] = [1.0,2.0]
    if mode == 2 or mode == 3:
        for i in sender:
            sender[i][0] = sender[i][0] / (num_spam + len(sender))
            sender[i][1] = sender[i][1] / (num_ham + len(sender))
        for i in to:
            to[i][0] = to[i][0] / (num_spam + len(to))
            to[i][1] = to[i][1] / (num_ham + len(to))
        for i in week:
            week[i][0] = week[i][0] / (num_spam + len(week))
            week[i][1] = week[i][1] / (num_ham + len(week))
        for i in date:
            date[i][0] = date[i][0] / (num_spam + len(date))
            date[i][1] = date[i][1] / (num_ham + len(date))
        for i in time:
            time[i][0] = time[i][0] / (num_spam + len(time))
            time[i][1] = time[i][1] / (num_ham + len(time))
        for i in pr1:
            pr1[i][0] = pr1[i][0] / (num_spam + len(pr1))
            pr1[i][1] = pr1[i][1] / (num_ham + len(pr1))
        for i in pr2:
            pr2[i][0] = pr2[i][0] / (num_spam + len(pr2))
            pr2[i][1] = pr2[i][1] / (num_ham + len(pr2))
    if mode == 1 or mode == 3:
        for i in d:
            d[i][2] = float(d[i][0]) / float(d[i][1])
        ####特征抽取####
        def cmp(x,y):
            if d[x][2] > d[y][2]:
                return -1
            if d[x][2] < d[y][2]:
                return 1
            return 0
        ###从大到小排序###
        key = d.keys()
        key = sorted(key,cmp)
        ##特征##
        featspam = key[0:num_of_feature]
        featham = key[len(key)-num_of_feature:len(key)]
    
    ####检测####
    correct = 0
    dd = dict()
    ddd = dict()
    for i in valid_list:
        entry = i.split()  
        ans1 = 0.0
        ans2 = 0.0
        ans = 0.0    
        if mode == 1 or mode == 3:
            for i in featspam:
                dd[i] = 1.0
            for i in featham:
                ddd[i] = 1.0
            msg = get_msg(entry[1])
            words = msg.split()
            for j in words:
                if dd.has_key(j):
                    dd[j] += 1.0
                if ddd.has_key(j):
                    ddd[j] += 1.0
            for j in featspam:
                ans1 += math.log(dd[j])
            for j in featham:
                ans1 -= math.log(ddd[j])
        if mode == 2 or mode == 3:
            meta = get_inf(entry[1]) 
            if sender.has_key(meta[0]):
                ans2 += math.log(sender[meta[0]][0])
                ans2 -= math.log(sender[meta[0]][1])
            if to.has_key(meta[1]):
                ans2 += math.log(to[meta[1]][0])
                ans2 -= math.log(to[meta[1]][1])
            if week.has_key(meta[2]):
                ans2 += math.log(week[meta[2]][0])
                ans2 -= math.log(week[meta[2]][1])
            if date.has_key(meta[3]):
                ans2 += math.log(date[meta[3]][0])
                ans2 -= math.log(date[meta[3]][1])
            if time.has_key(meta[4]):
                ans2 += math.log(time[meta[4]][0])
                ans2 -= math.log(time[meta[4]][1])
            if pr1.has_key(meta[5]):
                ans2 += math.log(pr1[meta[5]][0])
                ans2 -= math.log(pr1[meta[5]][1])
            if pr2.has_key(meta[6]):
                ans2 += math.log(pr2[meta[6]][0])
                ans2 -= math.log(pr2[meta[6]][1])
        if mode == 1:
            ans = ans1
        elif mode == 2:
            ans = ans2 + 4
        else:
            ans = ans1 + ans2 + 1
        if(ans >= 0):
            if(entry[0] == "spam"):
                correct += 1
        else:
            if(entry[0] == "ham"):
                correct += 1
    return float(correct)/float(len(valid_list))

####样本随机分为5份####
f = codecs.open("index","r","utf-8")
index = f.readlines()[0:64620]
f.close()
for i in range(len(index)):
    index[i] = index[i].replace("data","data_cut")
random.shuffle(index)
le = len(index)/5
k_1 = index[0:le]
k_2 = index[le:2*le]
k_3 = index[2*le:3*le]
k_4 = index[3*le:4*le]
k_5 = index[4*le:5*le]

print work(k_1+k_2+k_3+k_4,k_5,1.0,5000,3)
print work(k_5+k_2+k_3+k_4,k_1,1.0,5000,3)
print work(k_1+k_5+k_3+k_4,k_2,1.0,5000,3)
print work(k_1+k_2+k_5+k_4,k_3,1.0,5000,3)
print work(k_1+k_2+k_3+k_5,k_4,1.0,5000,3)
