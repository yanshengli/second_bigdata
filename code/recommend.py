__author__ = 'LiGe'
#encoding:utf-8
import csv
from numpy import *
from read_file1 import csv_to_list
from latest_new import map_time
from latest_new import map_item_issue_time
import datetime
import time


#把发布时间转换为标准unix时间后，换算成秒数
def cal_time(t1):
    #t1='2014年03月08日12:31'
    t1=t1.strip()
    if t1.find('年')<0:
        t1='2014年03月15日12:31'
    t1=t1.replace('年','-')
    t1=t1.replace('月','-')
    t1=t1.replace('日',' ')
    if t1.find(':')<0:
        t1=t1+'00:00'
    t1=t1+':00'
    s = t1
    d = datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())

#计算近邻TopN用户的子函数
def RBF(user_item,user,d,user_item_time,alpha=0.02):
    interres=list(set(user_item[user]).intersection(set(user_item[d])))
    sum=0
    t1=0
    t2=0
    simi=0.0
    for item in interres:
        for line in user_item_time[user]:
            if line[0]==item:
                t1=line[1]
                break
        for line in user_item_time[d]:
            if line[0]==item:
                t2=line[1]
                break
        sum=sum+1/(1+alpha*abs(float(t1)-float(t2)))
        simi=float(sum)/float(math.sqrt(len(user_item[user])*len(user_item[d])))
    return simi

#计算近邻用户
def pearsSim(user, user_item,user_item_time):
    score=list()
    for d in user_item:
        if d==user:continue
        sim=RBF(user_item,user,d,user_item_time,alpha=0.02)
        score.append((sim,d))
    return sorted(score, key=lambda jj:jj[0], reverse=True)[:150]


def sim(k,item,user_item,user_item_time,fre,alpha=0.02):#求物品与物品的相似度,考虑了时间维度,找出有两种物品的用户，然后计算其距离，采用的是基于项目相似性的计算
    count=0
    score=0
    t1=0.0
    t2=0.0
    for line in user_item:
        flag1=0
        flag2=0
        score=0
        if k in user_item[line]:
            if item in user_item[line]:
                for item_time in user_item_time[line]:
                    if item_time[0]==k:
                        t1=item_time[1]
                        flag1=1
                    if item_time[0]==item:
                        t2=item_time[1]
                        flag2=1
                    if flag1 and flag2:
                        break
                score=1/(1+alpha*abs(float(t1)-float(t2)))
        count=count+score
    count=count/math.sqrt(fre[k]*fre[item])
    return count


def interest_distribution(user,user_item,user_item_time,item_fre,user_latest_time,item_issue_time,h=0.2):#对用户未读项的分布的计算
    #user_item_interest_socre=dict()
    Beta=1.40479988345e-11
    item_interest_score=list()
    for item in item_fre:#记住，一定是按照顺序放入list中的，是按照同一种顺序放入的
        if item not in user_item[user]:#对未知项进行评分估计
            count=0.0
            for k in user_item[user]:
                distance=1-sim(k,item,user_item,user_item_time,item_fre)
                #print distance
                count=count+math.exp(-float(distance*distance)/float(2*h*h))
            count=0.8*count/(len(user_item[user])*math.sqrt(2*math.pi)*h)+0.2*(math.exp(-Beta*(int(user_latest_time[user])-int(cal_time(item_issue_time[item])))))#时效性与兴趣偏好融合
            item_interest_score.append((item,count))
    return item_interest_score

#给近邻用户进行编号处理，方便后面核密度估计的计算
def create_feature(user,recos,user_item):
    union_item=dict()
    local_user_item=dict()
    for line in recos:
        for data in user_item[line[1]]:
            if data not in union_item:
                union_item[data]=1
            else:
                union_item[data]=union_item[data]+1
    for line in user_item[user]:
        if line not in union_item:
            union_item[line]=1
        else:
            union_item[line]=union_item[line]+1
    for line in recos:
        local_user_item[line[1]]=user_item[line[1]]
    local_user_item[user]=user_item[user]
    return union_item,local_user_item


def recommend1():
    j=0
    csvfile = file('csv_result19.csv', 'wb')
    writer=csv.writer(csvfile)
    user_item,user_item_time,ignore_user=csv_to_list()
    user_latest_time=map_time()
    item_issue_time=map_item_issue_time()
    predict=list()
    print ignore_user
    print len(ignore_user)
    for user in user_item:
        if user not in ignore_user:
            recos=pearsSim(user,user_item,user_item_time)#求解相似用户
            item_fre,local_user_item=create_feature(user,recos,user_item)#编号处理
            item_score=interest_distribution(user,local_user_item,user_item_time,item_fre,user_latest_time,item_issue_time,h=0.4)#计算核密度
            number=len(user_item[user])
            if number>30:
                number=20
            final_result=sorted(item_score, key=lambda jj:jj[1], reverse=True)[:(number/10)+1]#结果排序
            print final_result
            for line in final_result:
                    if line[1]>0.25:
                        writer.writerow((user,line[0]))
                        j=j+1
        print j
    csvfile.close()
    return predict


if __name__=='__main__':
    predict=recommend1()




