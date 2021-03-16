#用于把csv格式的测试数据（英文电影数据集、随机生成的rating）,提取为需要的格式，并存入数据库
# 其中包括用于格式转换的get_director、 get_list函数
#处理数据从下面的分割线往下开始

from pymysql import *
#重置数据库
def clear_database():
    conn = connect(host='localhost', port=3306,database='movie_rec_system',user='root',password='sft080090',charset='utf8')
    cs1 = conn.cursor()
    cs1.execute('drop table movie;')
    cs1.execute('drop table rating;')
    conn.commit()
    cs1.close()
    conn.close()

#创建movie table
def create_movie_table():
    conn = connect(host='localhost', port=3306,database='movie_rec_system',user='root',password='sft080090',charset='utf8')
    cs1 = conn.cursor()
    # cs1.execute('drop table movie;')
    cs1.execute('create table movie(\
                    id int not null,\
                    title varchar(100),\
                    cast varchar(100),\
                    crew varchar(100) ,\
                    keywords varchar(100),\
                    genres varchar(100),\
                    vote_count int default 0,\
                    vote_average double default 5.0,\
                    primary key(id));')
    conn.commit()
    cs1.close()
    conn.close()

#创建rating table
def create_init_ratings():
    conn = connect(host='localhost', port=3306,database='movie_rec_system',user='root',password='sft080090',charset='utf8')
    cs1 = conn.cursor()
    # cs1.execute('drop table movie;')
    cs1.execute('create table rating(\
                    userId int not null,\
                    movieId int not null,\
                    rating double default 5.0,\
                    primary key(userId,movieId));')
    conn.commit()
    cs1.close()
    conn.close()

def init_database():
    # clear_database()
    create_movie_table()
    create_init_ratings()


#添加电影进入movie table
def add_movie(id,title,cast,crew,vote_count,vote_average,keywords=None,genres=None):
    if keywords is None:
        keywords = ''
    if genres is None:
        genres = ''
    conn = connect(host='localhost', port=3306,database='movie_rec_system',user='root',password='sft080090',charset='utf8')
    cs1 = conn.cursor()
    if isinstance(id,list):
        print("waiting to finish")
    else:
        cs1.execute('insert into movie (id,title,cast,crew,keywords,genres,vote_count,vote_average) values ({},"{}","{}","{}","{}","{}",{},{})'\
            .format(id,title,cast,crew,keywords,genres,vote_count,vote_average))

    conn.commit()
    cs1.close()
    conn.close()

#添加评分进入rating table
def add_rating(uid, mid, rating):
    conn = connect(host='localhost', port=3306,database='movie_rec_system',user='root',password='sft080090',charset='utf8')
    cs1 = conn.cursor()
    if isinstance(id,list):
        print("waiting to finish")
    else:
        cs1.execute('insert into rating (userId,movieId,rating) values ({},{},{})'.format(uid, mid, rating))

    conn.commit()
    cs1.close()
    conn.close()

###################################################################################################
clear_database()
init_database()
'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!手工分界线！！！！！！！！！！！！！！！！！！！！！！！

从这一部分开始用于将csv源数据清洗成为我们需要的格式。

！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
'''
import pandas as pd
#data for pretraining
df1 = pd.read_csv('./input/tmdb_5000_credits.csv')
df2 = pd.read_csv('./input/tmdb_5000_movies.csv')
df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')
# movie_df = df2  # movie set
# movie_df = movie_df.head(100)

# Parse the stringified features into their corresponding python objects
from ast import literal_eval
import numpy as np


features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)


# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

# Define new director, cast, genres and keywords features that are in a suitable form.
df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

#使用前若干条
movie_df = df2.head(100)

for i in range(0, movie_df.shape[0]):
    director = movie_df.loc[i,'director']
    crew = 'Director:' + director
    movie_df.loc[i,'crew'] = crew

movie_df = movie_df[['id','title','cast' ,'crew','keywords',  'genres', 'vote_count','vote_average']]
# print(movie_df.head(5))

movie_df = movie_df.drop(30)
ids = []

for i in range(99):  #用前99个电影
    if i == 30 :  #有问题的数据，给删掉，还剩98个电影了
        continue
    movie = movie_df.loc[i,:]
    ids.append(movie_df.loc[i,'id'])
    # print(movie['id'],movie['title'],movie['cast'],movie['crew'],movie['vote_count'],movie['vote_average'],movie['keywords'],movie['genres'])
    add_movie(movie['id'],movie['title'],movie['cast'],movie['crew'],movie['vote_count'],movie['vote_average'],movie['keywords'],movie['genres'])


import random
for i in range(1,100):    #100个用户
    rec = []
    for j in range(100):   # 每个用户添加大约100条评分（这里基本已经是对每个电影都评分了）
        m = random.randint(0,97)
        if m in rec:  #（用户，电影）键 重复的不要
            continue
        rec.append(m)
        s = random.randint(0,10)
        print(i,m,s)
        add_rating(i,ids[m],s)