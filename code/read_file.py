__author__ = 'FLY'
#encoding:utf-8
import numpy as np

def retrieve_info():
    """
    从文件中提取出：
    词典news_num_issue_time{新闻逻辑编号，发布时间}，
    词典news_logic_num_latest_read_time{新闻逻辑编号，最晚阅读时间}，
    词典news_num_logic_real{新闻逻辑编号，新闻实际编号}，
    词典user_num_logic_real{用户逻辑编号，用户实际编号}，
    词典user_logic_num_unrated_news_set{用户逻辑编号，用户未读新闻编号集合}，
    词典user_logic_num_latest{用户逻辑编号，（最晚的新闻逻辑编号，最晚阅读时间戳）}
    用户-新闻评分矩阵Rmn
    """
    f = open('train_data.txt')
    news_num_issue_time = dict()
    news_logic_num_latest_read_time = dict()
    news_num_logic_real = dict()
    user_num_logic_real = dict()
    user_logic_num_latest = dict()
    user_logic_num_unrated_news_set = dict()
    users = dict()
    #{用户实际编号，用户逻辑编号}
    news = dict()
    #{新闻实际编号，新闻逻辑编号}
    news_data = f.readlines()
    i = 0
    j = 0
    for new in news_data:
        new = new.strip()
        if len(new) != 0:
            new = new.split('\t')
            # if users.setdefault(new[0], i) != i:
            #     i += 1
            # if news.setdefault(new[1], j) != j:
            #     j += 1
            if not users.has_key(new[0]):
                users[new[0]] = i
                i += 1
            if not news.has_key(new[1]):
                news[new[1]] = j
                j += 1

    print len(users)
    # print users
    print i
    print j
    user_num_logic_real = dict(map(lambda t: (t[1], t[0]), users.items()))
    news_num_logic_real = dict(map(lambda t: (t[1], t[0]), news.items()))
    Rmn = np.zeros((users.__len__(), news.__len__()))
    for new in news_data:
        new = new.split('\t')
        i = users[new[0]]
        j = news[new[1]]
        Rmn[i, j] += 1
        if int(user_logic_num_latest.setdefault(users[new[0]], (news[new[1]], new[2]))[1]) < int(new[2]):
            user_logic_num_latest[users[new[0]]] = (news[new[1]], new[2])
        if int(news_logic_num_latest_read_time.setdefault(news[new[1]], new[2])) < int(new[2]):
            news_logic_num_latest_read_time[news[new[1]]] = new[2]
        if new[5] == 'NULL\n':
            if int(news_num_issue_time.setdefault(news[new[1]], new[2])) > int(new[2]):
                news_num_issue_time[news[new[1]]] = new[2]
        else:
            news_num_issue_time[news[new[1]]] = new[5]

    for i, j in zip(range(users.__len__()), range(news.__len__())):
        if Rmn[i][j] == 0:
            user_logic_num_unrated_news_set.setdefault(i, set()).add(j)

    return news_num_issue_time, news_logic_num_latest_read_time, user_num_logic_real, news_num_logic_real, \
        user_logic_num_unrated_news_set, Rmn, user_logic_num_latest








