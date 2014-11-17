__author__ = 'LiGe'
#encoding:utf-8
#记录每个用户的最后浏览的时间，以及每个新闻的发布时间

def map_time():
    f=open('train_data.txt','r')
    datas=f.readlines()
    users=set()
    user_late_time=dict()
    #news_time=dict()
    for line in datas:
        line=line.strip()
        line=line.split('\t')
        if line[0] not in users:
            users.add(line[0])
            user_late_time[line[0]]=line[2]
    return user_late_time

def map_item_issue_time():
    f=open('train_data.txt','r')
    datas=f.readlines()
    item=set()
    item_issue_time=dict()
    for line in datas:
        line=line.strip()
        line=line.split('\t')
        if line[1] not in item:
            item.add(line[1])
            item_issue_time[line[1]]=line[5]
    return item_issue_time


