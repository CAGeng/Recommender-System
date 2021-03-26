from pymysql import *
import pymysql
import pandas as pd

from functools import wraps

# 连接参数
host = 'localhost'
port = 3306
user = 'root'
password = 'sft080090'
database = 'movie2'
charset = 'utf8'

# 创建数据库
def create_database():
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute('drop database if exists {};'.format(database))
    cursor.execute('create database {};'.format(database))
    conn.commit()
    # debug
    print('Success create database!')
    cursor.close()
    conn.close()

# 创建表格
def create_tables():
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()
    # create movie table
    cursor.execute('create table movie(\
                        id int not null,\
                        title varchar(100) not null,\
                        cast varchar(1500),\
                        crew varchar(3000),\
                        genres varchar(300),\
                        keywords varchar(4000),\
                        vote_count int default 0,\
                        vote_average double default 5.0,\
                        primary key(id));')
    conn.commit()
    # debug
    print('Success create movie table!')
    # create user table
    cursor.execute('create table user(\
                        name varchar(15) not null,\
                        password varchar(15) not null,\
                        email varchar(100) not null,\
                        browse_record varchar(3000) default "[]",\
                        primary key(name));')
    conn.commit()
    # debug
    print('Success create user table!')
    # create recommend table 
    #评分表
    cursor.execute('create table recommend(\
                        id int not null,\
                        name varchar(25) not null,\
                        rating double,\
                        comment varchar(1000),\
                        primary key(id, name),\
                        foreign key(id) references movie(id),\
                        foreign key(name) references user(name));')
    conn.commit()

    # create rec_list table
    cursor.execute('create table rec_list(\
                        name varchar(25) not null,\
                        movie_list varchar(3000) not null);')
    conn.commit()
    # debug
    print('Success create rec_list table!')
    cursor.close()
    conn.close()


def init_db():
    create_database()
    create_tables()


# 查找电影（id），返回一个dataframe
def find_movie_id(id):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    df = pd.read_sql('select * from movie where id = {}'.format(id),conn)
    return df

# 查找电影（title）
def find_movie_title(title):
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    df = pd.read_sql('select * from movie where title = "{}"'.format(title), db)    
    return df

# 进度条
# count = 0
# percent = 0

# 添加电影
def add_movie(id, title, cast, crew, genres, keywords, vote_count, vote_average):
    if find_movie_id(id).shape[0] > 0:
        print('movie exists!')
        return

    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()
    
    cursor.execute('insert into movie (id, title, cast, crew, genres, keywords, vote_count, vote_average) values ({}, "{}", "{}", "{}", "{}", "{}", {}, {})'.format(id, title, cast, crew, genres, keywords, vote_count, vote_average))
    conn.commit()
    # debug
    # global count, percent
    # count += 1
    # if count == 48:
    #     count = 0
    #     percent += 1
    #     a = '*' * percent
    #     b = '.' * (100 - percent)
    #     print("\r{}%[{}->{}]".format(percent, a, b),end='')
    
    cursor.close()
    conn.close()

# 查找是否存在用户名
def find_user(name):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('select * from user where name = "{}"'.format(name))
    data = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return data

# 添加用户
def add_user(name, key, email):
    if find_user(name):
        print('user name exists!')
        return 1
    
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('insert into user (name, password, email) values ("{}", "{}", "{}")'.format(name, key, email))
    conn.commit()

    cursor.close()
    conn.close()
    return 0

# 登录（用户名，密码）
def login(name, key):
    data = find_user(name)
    
    if data:
        # data = cursor.fetchone()
        if data[1] == key:
            print('Successfully logged in!')
            return 0
        else:
            print('Wrong password!')
            return 1  
    else:
        print('Username does not exist!')
        return 2

'''
# 
'''
# 查找是否存在评分
def find_recommend(id, name):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('select * from recommend where id = {} and name = "{}"'.format(id, name))
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data

# 查找评分（id）
def find_recommend_id(id):
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

    df = pd.read_sql('select * from recommend where id = {}'.format(id), db)
    
    return df

# 查找推荐（name）
def find_recommend_name(name):
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

    df = pd.read_sql('select * from recommend where name = "{}"'.format(name), db)
    
    return df

# 添加推荐
def add_recommend(id, name, rating, comment):
    if find_recommend(id, name):
        #如果存在，则提供修改功能
        print('recommend exists!')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
        cursor = conn.cursor()

        cursor.execute('UPDATE recommend set rating={},comment="{}" where id = {} and name = "{}"'.format(rating, comment,id, name))
        conn.commit()

        cursor.close()
        conn.close()
        return 3
    
    if not find_movie_id(id).shape[0] > 0:
        print('movie does not exist!')
        return 1
    
    if not find_user(name):
        print('user does not exist!')
        return 2
    
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('insert into recommend (id, name, rating, comment) values ({}, "{}", {}, "{}")'.format(id, name, rating, comment))
    conn.commit()

    cursor.close()
    conn.close()
    return 0
    
'''
#####################################   扩展   #########################################################
'''
#用户检查的装饰器
def user_check_decorator(f):
    @wraps(f)
    def check_and_f(name,mlist):
        if not find_user(name):
            print('user does not exist!')
            return 1
        return f(name,mlist)

    return check_and_f

#推荐列表相关的
# 向推荐列表（类似歌单的形式）中添加一个条目(name,mlist)，不会合并
@user_check_decorator
def add_rec_list(name,mlist):

    rec = ""
    fl = 1
    for x in mlist:
        if fl == 1:
            rec += str(x)
            fl = 0
        else:
            rec += '//' + str(x)
    if rec == "":
        print('Empty list')
        return 2
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('insert into rec_list (name,movie_list) values ("{}", "{}")'.format(name,rec))
    conn.commit()

    cursor.close()
    conn.close()
    return 0

def get_rec_list(name):
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

    df = pd.read_sql('select movie_list from rec_list where name = "{}"'.format(name), db)

    target = []
    con = 0
    for i in range(df.shape[0]):
        mlist = df.iloc[i,0]
        mlist = mlist.split('//')
        for x in mlist:
            x = int(x)
            if x in target:
                continue
            target.append(x)
            con += 1
            if con >= 10:
                return target
    return target

#用户浏览历史记录相关
def get_browse_list(name):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('select browse_record from user where name = "{}"'.format( name))
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    from ast import literal_eval
    data = data[0]
    data = literal_eval(data)

    return data


@user_check_decorator
def add_browse_record(name, mlist):
    data = get_browse_list(name)
    #合并
    for mov in mlist:
        if mov in data:
            continue
        data.append(mov)
    
    res = '['
    for x in data:
        res += str(x) + ','
    res = res[:-1] + ']'
    
    #写回数据库
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('UPDATE user set browse_record = "{}" where name = "{}"'.format(res,name))
    conn.commit()

    cursor.close()
    conn.close()
    return 0

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
#下面的不要在后端调用，是用来初始化服务器和数据库的
def init_tables_base():
    import pandas as pd
    #data for pretraining
    input_path = "C:/Users/sft/Desktop/数据集/推荐/input/"
    df1 = pd.read_csv(input_path + 'tmdb_5000_credits.csv')
    df2 = pd.read_csv(input_path + 'tmdb_5000_movies.csv')
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

    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////

    #使用前若干条
    movie_df = df2.head(100)

    for i in range(0, movie_df.shape[0]):
        director = movie_df.loc[i,'director']
        crew = 'Director:' + director
        movie_df.loc[i,'crew'] = crew

    movie_df = movie_df[['id','title','cast' ,'crew','keywords',  'genres', 'vote_count','vote_average']]


    movie_df = movie_df.drop(30)
    ids = []

    for i in range(99):  #用前99个电影
        # print(i)
        if i == 30 :  #有问题的数据，给删掉，还剩98个电影了
            continue
        movie = movie_df.loc[i,:]
        ids.append(movie_df.loc[i,'id'])
        # print(movie['id'],movie['title'],movie['cast'],movie['crew'],movie['vote_count'],movie['vote_average'],movie['keywords'],movie['genres'])
        add_movie(movie['id'],movie['title'],movie['cast'],movie['crew'],movie['keywords'],movie['genres'],movie['vote_count'],movie['vote_average'])


    #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    users = ['a','b', 'c' , 'd', 'e']
    user_con = len(users)
    for i in range(user_con):
        add_user(users[i],'1','1@1.com')

    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    import random

    movie_con = len(ids)
    for i in range(user_con):
        rec = []
        for j in range(50):   # 每个用户添加大约50条评分
            m = random.randint(0,movie_con - 1)
            if m in rec:  #（用户，电影）键 重复的不要
                continue
            rec.append(m)
            s = random.uniform(0,5)
            # print(i,m,s)
            add_recommend(ids[m],users[i],s,'')
    



if __name__ == '__main__':
    # init_db()
    # init_tables_base()
    # add_rec_list('a',[254,597,2268])
    # add_rec_list('a',[102382,597,2268])

    # add_browse_record('sadf',[254,597,2268,8487])
    # print(get_browse_list('a'))
    add_browse_record('a',[58,155,217])
    print(get_browse_list('a'))