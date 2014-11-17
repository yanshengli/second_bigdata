__author__ = 'LiGe'
#encoding:utf-8
import math


#读取用户集合，用户-新闻集合
def csv_to_list():
    f=open('train_data.txt')
    item=list()
    users=dict()
    user=set()
    ignore_user=set()
    temp=list()
    user_item_time=dict()
    news_data=f.readlines()
    for new in news_data:
        new=new.strip()
        if len(new)!=0:
            new=new.split('\t')
            if new[0] not in user:
                if len(user)!=0:
                    user_item_time[previous[0]]=temp
                    temp=list()
                    users[previous[0]]=item
                    item=list()
                    temp.append((new[1],new[2]))
                    item.append(new[1])
                    user.add(new[0])
                else:
                    user.add(new[0])
                    temp=list()
                    temp.append((new[1],new[2]))
                    item=list()
                    item.append(new[1])
            else:
                item.append(new[1])
                temp.append((new[1],new[2]))
                ignore_time=abs(float(new[2])-float(previous[2]))
                if ignore_time>3600 and len(item)==2:
                        ignore_user.add(previous[0])
            previous=new
        users[previous[0]]=item
        user_item_time[previous[0]]=temp
    return users,user_item_time,ignore_user