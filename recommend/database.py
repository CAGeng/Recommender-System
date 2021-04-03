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

    # create VerificationCode table
    cursor.execute('create table verificationcode(\
                        email varchar(100) not null,\
                        code char(6) not null,\
                        time datetime not null);')
    conn.commit()
    print('Success create verificationcode table!')
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
#sft:根据标题的查找采取模糊查找的方式
def find_movie_title(title):
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    df = pd.read_sql('select * from movie where title LIKE "%{}%"'.format(title), db)    
    return df


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
        print(str(id) + ': movie does not exist!')
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

#获得一个用户的所有推荐影单，会自动合并
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

    if data == None:
        return []

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

#邮箱认证相关
import random
import time
import datetime
from datetime import datetime

#生成验证码
def generate_VerificationCode(email):
    VerificationCode = random.random()
    VerificationCode = (int)(VerificationCode*1000000)
    VerificationCode = str.rjust(str(VerificationCode),0)

    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('select * from verificationcode where email = "{}"'.format(email))

    if len(cursor.fetchall()) == 0:
        cursor.execute('insert into  verificationcode(email,code,time) values("{}","{}",now())'.format(email,VerificationCode))
    else:
        cursor.execute('update verificationcode set code = "{}", time = now() where email = "{}"'.format(VerificationCode,email))
    conn.commit()
    cursor.close()
    conn.close()
    return VerificationCode

#根据输入的邮箱查找对应的验证码，并将其与输入的验证码进行比较
def verify_Code(email, code):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('select code, time from verificationcode where email = "{}"'.format(email))
    conn.commit()

    data = cursor.fetchone()
    if data != None:
        VerificationCode, CodeTime = data
    else:
        cursor.close()
        return 0
    if VerificationCode != code:
        cursor.close()
        return 0
    else:
        cursor.execute('delete from verificationcode where email = "{}"'.format(email))
        conn.commit()
        cursor.close()
        if (datetime.now()-CodeTime).seconds > 1800:
            return 0
        else:
            return 1

#更新验证信息，超时的删去
def update_verificationcode():
    print("in update_verificationcode")
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    cursor = conn.cursor()

    cursor.execute('delete from verificationcode where minute(timediff(time,now())) > 30')
    conn.commit()
    cursor.close()
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
    # 用户
    users = ['a','b', 'c' , 'd', 'e']
    user_con = len(users)
    for i in range(user_con):
        add_user(users[i],'1','1@1.com')

    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #随机评分

    # import random

    # movie_con = len(ids)
    # for i in range(user_con):
    #     rec = []
    #     for j in range(20):   # 每个用户添加大约50条评分
    #         m = random.randint(0,movie_con - 1)
    #         if m in rec:  #（用户，电影）键 重复的不要
    #             continue
    #         rec.append(m)
    #         s = random.uniform(0,5)
    #         # print(i,m,s)
    #         add_recommend(ids[m],users[i],s,'')
    
    

#用于检验推荐算法的构造样例
def create_check_rec_algo_data():   
    add_user('sft', '080090', 'ohouhou@qq.com')
    #sft比较喜欢科幻和动作电影，所以他给这些电影都打了满分
    add_recommend(559, 'sft', 5, "Good!It's the best movie I'd ever seen~") #Spider-Man 3
    add_recommend(1726, 'sft', 5, "The plot is full of ups and downs.Exciting!") #Iron Man
    add_recommend(10138, 'sft', 5, "Great, the ending is memorable!") #Iron Man 2
    add_recommend(19995, 'sft', 5, "Good!It's the best movie I'd ever seen~") #Avatar
    add_recommend(36668, 'sft', 5, "The plot is full of ups and downs.Exciting!") #X-Men: The Last Stand
    add_recommend(68721, 'sft', 5, "The plot is full of ups and downs.Exciting!") #Iron Man 3
    add_recommend(102382, 'sft', 5, "The plot is full of ups and downs.Exciting!") #The Amazing Spider-Man 2
    add_recommend(99861, 'sft', 5, "Good!It's the best movie I'd ever seen~") #Avengers: Age of Ultron
    add_recommend(127585, 'sft', 5, 'Perfect!') #X-Men: Days of Future Past
    add_recommend(246655, 'sft', 5, "Great, the ending is memorable!") #X-Men: Apocalypse
    add_recommend(76757, 'sft', 5, "The plot is full of ups and downs.Exciting!") #Jupiter Ascending
    #sft不喜欢幼稚电影、家庭片和剧情片，所以给他们打了0分
    add_recommend(597, 'sft', 0, '') #Titanic
    add_recommend(150540, 'sft', 0, "The plot is a bit boring, but the special effects are OK.") #Inside Out
    add_recommend(158852, 'sft', 0, "The movie is not interesting at all. I've been sleeping!") #Tomorrowland
    add_recommend(278927, 'sft', 0, "The movie is not interesting at all. I've been sleeping!") #The Jungle Book
    add_recommend(155, 'sft', 0, "The movie is not interesting at all. I've been sleeping!") #The Dark Knight
    add_recommend(2698, 'sft', 0, "The plot is a bit boring, but the special effects are OK.") #Evan Almighty
    add_recommend(10192, 'sft', 0, "The movie is not interesting at all. I've been sleeping!") #Shrek Forever After
    
    #sft的兄弟和sft志趣相投
    add_user('sft_brother', '080090', 'ohouhou@qq.com')
    add_recommend(10138, 'sft_brother', 5, "The plot is full of ups and downs.Exciting!") #Iron Man 2
    add_recommend(19995, 'sft_brother', 5, "Good!It's the best movie I'd ever seen~") #Avatar
    add_recommend(36668, 'sft_brother', 5, "Great, the ending is memorable!") #X-Men: The Last Stand
    add_recommend(68721, 'sft_brother', 5, "The plot is full of ups and downs.Exciting!") #Iron Man 3
    add_recommend(246655, 'sft_brother', 5, "Good!It's the best movie I'd ever seen~") #X-Men: Apocalypse

    add_recommend(158852, 'sft_brother', 0, "The plot is a bit boring, but the special effects are OK.") #Tomorrowland
    add_recommend(278927, 'sft_brother', 0, "The movie is not interesting at all. I've been sleeping!") #The Jungle Book
    add_recommend(155, 'sft_brother', 0, "The movie is not interesting at all. I've been sleeping!") #The Dark Knight

    #sft的姐妹和sft志趣相投
    add_user('sft_sister', '080090', 'ohouhou@qq.com')
    add_recommend(10138, 'sft_sister', 5, "The plot is full of ups and downs.Exciting!") #Iron Man 2
    add_recommend(246655, 'sft_sister', 5, "Great, the ending is memorable!") #X-Men: Apocalypse
    add_recommend(36668, 'sft_sister', 5, "The plot is full of ups and downs.Exciting!") #X-Men: The Last Stand
    add_recommend(68721, 'sft_sister', 5, "Good!It's the best movie I'd ever seen~") #Iron Man 3

    add_recommend(158852, 'sft_sister', 0, "The movie is not interesting at all. I've been sleeping!") #Tomorrowland
    
    #sft的敌人和sft兴趣截然相反
    add_user('sft_enemy', '080090', 'ohouhou@qq.com')
    add_recommend(10138, 'sft_enemy',0, "I regret spending money to see the film") #Iron Man 2
    add_recommend(19995, 'sft_enemy',0, "The plot is a bit boring, but the special effects are OK.") #Avatar
    add_recommend(36668, 'sft_enemy',0, "I regret spending money to see the film") #X-Men: The Last Stand
    add_recommend(68721, 'sft_enemy',0, "The plot is a bit boring, but the special effects are OK.") #Iron Man 3
    add_recommend(246655, 'sft_enemy',0, "I regret spending money to see the film") #X-Men: Apocalypse

    add_recommend(158852, 'sft_enemy',5, "Great, the ending is memorable!") #Tomorrowland
    add_recommend(278927, 'sft_enemy',5, "Good!It's the best movie I'd ever seen~") #The Jungle Book
    add_recommend(155, 'sft_enemy',5, "The plot is a bit boring, but the special effects are OK.") #The Dark Knight

    #sft的另一个敌人和sft兴趣也很不同
    add_user('sft_enemy2', '080090', 'ohouhou@qq.com')
    add_recommend(10138, 'sft_enemy2',0, "I regret spending money to see the film") #Iron Man 2
    add_recommend(19995, 'sft_enemy2',0, "The plot is a bit boring, but the special effects are OK.") #Avatar
    add_recommend(36668, 'sft_enemy2',0, "I regret spending money to see the film") #X-Men: The Last Stand
    add_recommend(246655, 'sft_enemy2',0, "The plot is a bit boring, but the special effects are OK.") #X-Men: Apocalypse

    add_recommend(158852, 'sft_enemy2',5, "The plot is full of ups and downs.Exciting!") #Tomorrowland
    add_recommend(278927, 'sft_enemy2',5, "Good!It's the best movie I'd ever seen~") #The Jungle Book
    add_recommend(155, 'sft_enemy2',5,"The plot is full of ups and downs.Exciting!") #The Dark Knight
    add_recommend(10192, 'sft_enemy2', 5, "The plot is full of ups and downs.Exciting!") #Shrek Forever After

    #添加sft的推荐影单
    add_rec_list('sft',[559,1726,10138,19995,36668,127585,76757,99861])
    #添加sft敌人的推荐影单
    add_rec_list('sft_enemy',[158852,278927,155,10192,2698])
    #给sft的兄弟姐妹和敌人添加浏览记录
    add_browse_record('sft',[559,1726,10138,19995,36668,127585,76757,99861,102382])
    add_browse_record('sft_brother',[10138,19995,36668,68721,246655])
    add_browse_record('sft_sister',[10138,246655,158852])
    add_browse_record('sft_enemy',[597,150540,158852,278927,155,2698,10192])

def create_check_rec_algo_data2():  
    db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

    df = pd.read_sql('select id from movie', db)

    size = df.shape[0]
    halfsiz = int(size/2)
    #dog 喜欢看前一半电影
    add_user('dog', '080090', '1@1.com')
    for i in range(halfsiz):
        mid = df.iloc[i,0]
        add_recommend(mid, 'dog', 5, '')
    #dog 不喜欢看后一半电影
    for i in range(halfsiz,size):
        mid = df.iloc[i,0]
        add_recommend(mid, 'dog', 0, '')

    #dog2 和dog类似
    add_user('dog2', '080090', '1@1.com')
    for i in range(halfsiz - 5):
        mid = df.iloc[i,0]
        add_recommend(mid, 'dog2', 5, '')
    #dog2 
    for i in range(halfsiz - 5,size):
        mid = df.iloc[i,0]
        add_recommend(mid, 'dog2', 0, '')

    #dog3 和dog相反
    add_user('dog3', '080090', '1@1.com')
    for i in range(halfsiz - 4):
        mid = df.iloc[i,0]
        add_recommend(mid, 'dog3', 0, '')
    #dog2 
    for i in range(halfsiz - 4,size):
        mid = df.iloc[i,0]
        add_recommend(mid, 'dog3', 5, '')

if __name__ == '__main__':
    init_db()
    init_tables_base()
    create_check_rec_algo_data() #添加构造数据
    # add_rec_list('a',[254,597,2268])

    # add_browse_record('sadf',[254,597,2268,8487])
    # print(get_browse_list('a'))
    # add_browse_record('a',[58,155,217])
    # print(get_browse_list('a'))

#添加评语
# def add_comment_data():
#     db = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)

#     name_df = pd.read_sql('select name from user', db)
#     name_list = name_df['name'].values.tolist()
    
#     comment_list = ["Good!It's the best movie I'd ever seen~",
#                     "Perfect!",
#                     "Great, the ending is memorable!",
#                     "The movie is not interesting at all. I've been sleeping!",
#                     "The plot is a bit boring, but the special effects are OK.",
#                     "I regret spending money to see the film",
#                     "Boring!Wasted two hours of my life",
#                     "The plot is full of ups and downs.Exciting!"]

#     con1 = len(name_list)
#     con2 = len(comment_list)