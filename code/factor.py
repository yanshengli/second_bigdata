__author__ = 'FLY'
#encoding:utf-8

from read_file import retrieve_info
import time
import datetime
import math
from numpy import linalg as la
import numpy
import csv
import string

#转换发布时间为秒数
def cal_time(t1):
    #t1='2014年03月08日12:31'
    t1=t1.strip()
    if t1.find('年')<0:
        return t1
    t1=t1.replace('年','-')
    t1=t1.replace('月','-')
    t1=t1.replace('日',' ')
    if t1.find(':')<0:
        t1=t1+'00:00'
    t1=t1+':00'
    s = t1
    d = datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())


def cal_ave_half_period(news_num_issue_time, news_logic_num_latest_read_time):
    """
    计算每条新闻的半衰期，并求其平均值
    """
    ave_half_period = 0.0
    for i in (range(news_num_issue_time.__len__())):
        ave_half_period += (int(news_logic_num_latest_read_time[i]) - int(cal_time(news_num_issue_time[i])))
    ave_half_period /= 2.0
    return ave_half_period

#计算老化系数
def cal_info_age_factor(ave_half_period):
    return -math.log(0.5)/ave_half_period



if __name__ == '__main__':
    csvfile = file('csv_result_age.csv', 'wb')
    writer=csv.writer(csvfile)
    news_num_issue_time, news_logic_num_latest_read_time, user_num_logic_real, news_num_logic_real, \
        user_logic_num_unrated_news_set, Rmn, user_logic_num_latest = retrieve_info()

    factor = cal_info_age_factor(cal_ave_half_period(news_num_issue_time, news_logic_num_latest_read_time))#求解老化系数
    print 'factor is: ', factor    