import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, SVD, model_selection
from surprise.model_selection import cross_validate
from surprise import SVDpp
import surprise
from pymysql import *
import pymysql
# from recommend import database
# from database import *

#根目录
basepath = './recommend/'
# basepath = './'  # debug

# 连接参数
host = 'localhost'
port = 3306
user = 'root'
password = 'sft080090'
database = 'movie2'
charset = 'utf8'

#这是加载一些用于预训练和测试的英文电影数据集，最终不会使用到
# def load_pretrain():
#     #data for pretraining
#     df1 = pd.read_csv('./input/tmdb_5000_credits.csv')
#     df2 = pd.read_csv('./input/tmdb_5000_movies.csv')
#     df1.columns = ['id','tittle','cast','crew']
#     df2= df2.merge(df1,on='id')
#     movie_df = df2  # movie set
#     return movie_df

#从mysql加载电影的相关数据，包括：
#  --id  编号（key）
#  --title  标题
#  --cast  主演列表
#  --crew  工作人员，按照‘职位：姓名’ 的格式，目前主要提取其中的导演数据
#  --vote_average  平均评分，满分为10
#  --vote_count  评分数，用于IMDB方法中筛选电影
#  --keywords  关键词列表
#  --genres  题材，可以多于1个
def load_movies():
    conn = connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    df = pd.read_sql('select * from movie',conn)
    conn.close()	
    return df


    

#加载ratings
def load_ratings():
    conn = connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    ratings = pd.read_sql('select * from recommend' ,conn)
    conn.close()
    ratings.columns = ['movieId','userId','rating','recommend']
    return ratings[['movieId','userId','rating']]

#这是一个基于统计的推荐，简单的按照平均评分排序，并使用了IMDB formula提高热门影片的评分
#与用户和电影相关度无关，适用于新用户
#这个函数会将按评分排出的顺序保存下来，如果没有添加新的电影，就不需要多次调用这个函数，直接使用下面的推荐
#Demographic Filtering
def demographic_filtering(movie_df):
    C = movie_df['vote_average'].mean()
    # m = movie_df['vote_count'].quantile(0.9)
    m = 1000
    #筛选movies
    q_movies = movie_df#.copy().loc[movie_df['vote_count'] >= m]
    def weighted_rating(x, m = m, C = C):
        v = x['vote_count']
        R = x['vote_average']
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)
    
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
    #Sort movies based on score calculated above
    q_movies = q_movies.sort_values('score', ascending=False)

    #save
    demographic_rec = q_movies[['id', 'score']]
    demographic_rec.to_csv(basepath + "recommend_model/demographic_rec.csv",index=False,sep=',')
    #Print the top 15 movies
    return demographic_rec

#这个函数加载统计推荐的排序列表，并作出推荐
def get_rec_demographic():
    df = pd.read_csv(basepath + "recommend_model/demographic_rec.csv")
    return df['id']

#这是基于用户之前看过的电影，依照内容相关度做出推荐（content-based,CF)
#提取出我们认为有用的特征，计算cos_similarity，然后对于输入的特定的电影列表（表示用户已将看过的），
#推荐函数会计算每一个电影对已有电影列表相关系数的和，相关度最高的若干电影将被推荐。
#Content-based filtering
# Function that takes in movies' title as input and outputs most similar movies

#这是推荐函数，会自动加载之前保存好的cos_similarity矩阵
def get_recommendations_mul(title_list, cosine_sim=None,movie_df=None):

    if movie_df is None:
        print("Err: No loaded movie")
        return

    indices = pd.Series(movie_df.index, index=movie_df['title'])


    if cosine_sim is None:
        cosine_sim = np.loadtxt(basepath + "recommend_model/cosine_sim.txt")


    def get_score(x,indices,title_list,cosine_sim):
        score = 0
        idx0 = x
        for title in title_list:
            idx = indices[title]
            score += cosine_sim[idx0][idx]
        return score

    size = len(cosine_sim[0])
    sim_scores = range(0,size)
    sim_scores = sorted(sim_scores, key=lambda x: get_score(x,indices,title_list,cosine_sim), reverse=True)

    # Get the movie indices
    movie_indices = []
    siz = 0
    for i in range(0,size):
        if movie_df['title'].iloc[sim_scores[i]] in title_list:
            continue
        movie_indices.append(sim_scores[i])
        siz += 1
        if siz >= 10:
            break
    # Return the top 10 most similar movies
    return movie_df[['id','title']].iloc[movie_indices]  


#这是计算cos_similarity的函数，需要对特征提取并清洗，最后把矩阵保存下来
#只有当必要的时候（添加了新的电影），才需要重新计算
def content_filtering(movie_df):
    def get_list(x):
        return x.split(',')

    features = ['cast', 'keywords', 'genres']
    for feature in features:
        movie_df[feature] = movie_df[feature].apply(get_list)

    def get_director(x):
        lst = x.split(',')
        for m in lst:
            temp = m.split(':')
            if len(temp) < 2:
                continue
            if temp[0] == 'Director':
                return temp[1]
        return np.nan

    movie_df['director'] = movie_df['crew'].apply(get_director)
    
    # Function to convert all strings to lower case and strip names of spaces
    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            #Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    # Apply clean_data function to your features.
    features = ['cast', 'keywords', 'director', 'genres']

    for feature in features:
        movie_df[feature] = movie_df[feature].apply(clean_data)


    def create_soup(x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
    movie_df['soup'] = movie_df.apply(create_soup, axis=1)

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(movie_df['soup'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    np.savetxt(basepath + "recommend_model/cosine_sim.txt",cosine_sim)
    
    # movie_df = movie_df.reset_index()
    return 

#这是一个基于奇异值分解（svd）的协同过滤算法，即在多用户系统中，根据相似用户的评分来预测特定用户对于特定电影的评分。
#也就是类似于：”和您类似的用户还喜欢看“，这样的推荐思路。
#这个算法的好处是尝试从评分矩阵中提取隐藏语义，从而对数据降维，避免每次预测都需要对巨大的评分矩阵进行操作。
#使用了surprise 库中实现的自动SVD++算法，比之普通的SVD，他添加了对隐式反馈的修正项。
#collaborative filtering

#下面的函数会保存训练的模型，如非必要（添加了一定数量的新的评价记录），不需要重新训练，可以直接加载模型用于预测评分。
def collaborative_filtering(ratings):
    reader = Reader()
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

    svd = SVDpp(lr_all=0.07,reg_all=0.002,n_epochs=20)
    '''
    n_factors –因素的数量。默认值为20。
    n_epochs – SGD过程的迭代次数。默认值为 20。
    init_mean –因子向量初始化的正态分布平均值。默认值为0。
    init_std_dev –因子向量初始化的正态分布的标准偏差。默认值为0.1。
    lr_all –所有参数的学习率。默认值为0.007。
    reg_all –所有参数的正则项。默认值为 0.02。
    '''
    cross_validate(svd, data, measures=['RMSE', 'MAE'],verbose=True)

    surprise.dump.dump(basepath + "recommend_model/SVD_model",algo=svd)
    

#下面的推荐模型用于对已经”稳定“在推荐系统中的用户和电影进行推荐，对于特定的用户，他会按照一定的权重考虑每个电影在
#上面三种推荐策略中的评分，最终根据总评顺序获得最终的推荐。
def get_recommendation(userid,title_list):
    movie_df = pd.read_csv(basepath + "/recommend_model/movie.csv")

    def get_score_1(x,title_list,cosine_sim,indices): #content based
        score = 0.0
        idx0 = x
        con = 0
        for title in title_list:
            con += 1
            idx = indices[title]
            score += cosine_sim[idx0][idx]
        if con == 0:
            return 0
        return score/con


    def get_score_2(mid):  #demographic
        rating = pd.read_csv(basepath + "recommend_model/demographic_rec.csv")
        temp = rating[rating['id'] == mid]['score']
        return temp.iloc[0]

    def get_score_3(mid,user):  # svd based
        (_,algo) = surprise.dump.load(basepath + "recommend_model/SVD_model")
        rating = (algo.predict(user,mid)).est
        return rating

    indices = pd.Series(movie_df.index, index=movie_df['title'])
    cosine_sim = np.loadtxt(basepath + "recommend_model/cosine_sim.txt")

    a = 20
    b = 0.33
    c = 0.33
    def get_score_final(x,userid,title_list,cosine_sim,indices,a,b,c,movie_df):
        score1 = get_score_1(x,title_list,cosine_sim,indices)
        mid = movie_df.loc[x,'id']
        # print('mid:',mid)
        score2 = get_score_2(mid)
        score3 = get_score_3(mid,userid)
        # print(x)
        # print('----')
        # print(score1 * a)
        # print(score2 * b)
        # print(score3 * c)
        score = score1 * a + score2 * b + score3 * c
        # print(score)
        return score

    size = len(cosine_sim[0])

    scores = [0 for i in range(size)]
    for i in range(size):
        scores[i] = get_score_final(i,userid,title_list,cosine_sim,indices,a,b,c,movie_df)

    sim_scores = range(0,size)
    sim_scores = sorted(sim_scores, key=lambda x: scores[x], reverse=True)

    # Get the movie indices
    movie_indices = []
    siz = 0
    for i in range(0,size):
        if movie_df['title'].iloc[sim_scores[i]] in title_list:
            continue
        movie_indices.append(sim_scores[i])
        print(scores[sim_scores[i]])
        siz += 1
        if siz >= 10:
            break
    # Return the top 10 most similar movies
    return movie_df[['id','title']].iloc[movie_indices]   


#前面的协同过滤模型有一个问题：SVD++的功能是对稀疏矩阵中未知的点进行预测，也就是说，只能预测本来就在
#矩阵中的用户，而对于新出现的用户不能预测。如果每当新的用户出现时都重新训练开销无疑是巨大的。

#我按照下面的处理过程解决这个问题：
'''
1.通过随机梯度下降的方法分解评分矩阵（含未知数的稀疏矩阵），分解结果为维度更低的两个隐因子矩阵P,Q
2.A' = PQ为评分预测矩阵，对他进行奇异值分解得到A' = USV，可推知A'V(转制)S(逆) = U
3.令W = V(转制)S(逆),则有A'W = U，其中A'为评分矩阵（m*n），W为特征提取矩阵（n*k），U为用户特征矩阵（m*k）
4.转而对于新用户，当知道了他对一系列电影的评分（1*n矩阵）后，将它乘以W可以提取其特征，并与U比较，可以获得和他相关度高的老用户
5.因此我们只需要保存W（n*k）和U（m*k），就可以完成对新用户的相关用户搜索，每次只需要进行一次矩阵乘法和cos_similarity计算就可以了
6.相比于整张评分表的（m*n）大小，此方案从时间和存储空间上都大大节省。
'''
#这种推荐将被主要用作冷启动用户到”稳定“用户的过渡阶段（在新的SVD++模型训练之前）。

#下面的两个函数采用随机梯度下降的方法完成含未知数矩阵的分解。
def subt_with_none(m,m_est):#对未统计的评分不计算平方误差的减法
    sizx = m.shape[0]
    sizy = m.shape[1]
    for i in range(0,sizx):
        for j in range(0,sizy):
            if m[i][j] == -1:
                m[i][j] = m_est[i][j]
    return m - m_est

def LFM_ed2(D, k=3, iter_times=1000, alpha=0.01, learn_rate=0.0001):
    '''
    此函数实现的是最简单的 LFM 功能
    :param D: 表示需要分解的评价矩阵, type = np.ndarray
    :param k: 分解的隐变量个数
    :param iter_times: 迭代次数
    :param alpha: 正则系数
    :param learn_rate: 学习速率
    :return:  分解完毕的矩阵 U, V, 以及误差列表err_list
    '''
    assert type(D) == np.ndarray
    m, n = D.shape  # D size = m * n
    U = np.random.rand(m, k) 
    V = np.random.randn(k, n)
    err_list = []
    for t in range(iter_times):
        D_est = np.matmul(U, V)
        ERR = subt_with_none(D,D_est)  #对未统计的评分不计算平方误差
        
        U_grad = -2 * np.matmul(ERR, V.transpose()) + 2 * alpha * U
        V_grad = -2 * np.matmul(U.transpose(), ERR) + 2 * alpha * V
        U = U - learn_rate * U_grad
        V = V - learn_rate * V_grad

        ERR2 = np.multiply(ERR, ERR)
        ERR2_sum = np.sum(np.sum(ERR2))
        err_list.append(ERR2_sum)
    return U, V, err_list

#下面的函数对A'进行奇异值分解
def do_svd(A,k=3):
    U, S, V = np.linalg.svd(A)

    S_1 = np.eye(k) * S[:k]
    U_1 = U[:, :k]
    V_1 = V[:k, :] 

    W = np.dot(V_1.T, np.linalg.inv(S_1))

    np.savetxt(basepath + "recommend_model/W.txt",W)
    np.savetxt(basepath + "recommend_model/U.txt",U_1)

#下面的函数调用前面两个函数，将上述的W和U保存起来，用于之后的推荐。
def create_svd_matrix(number_user,number_movie,movie_df, ratings,k=3):
    name2index = {}
    number_user = 0
    data = ratings[['userId', 'movieId', 'rating']]
    #构造 用户名-序号 字典
    for i in range(0,data.shape[0]):
        u = data['userId'][i]   
        if u not in name2index.keys():
            name2index[u] = number_user
            number_user += 1

    np.save(basepath + "recommend_model/u_name2index.npy", name2index)

    indices = pd.Series(movie_df.index, index=movie_df['id'])

    A = [[-1 for i in range(0,number_movie)] for j in range(0,number_user)]
    A = np.array(A)
    for i in range(0,data.shape[0]):
        u = data['userId'][i]  #这里是用户名
        uid = name2index[u]
            
        m = indices[data['movieId'][i]]
        rating = data['rating'][i]
        A[uid][m] = rating

    (P,Q,_) = LFM_ed2(A,k=k)
    A_1 = np.dot(P,Q)

    do_svd(A_1,k=k)

#”过渡“期基于相似度的推荐算法
def get_recommend_svdsim(user_name):
    conn = connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    ratings = pd.read_sql('select * from recommend \
                            where name = "{}"'.format(user_name),conn)
    conn.close()

    ratings.columns = ['movieId','userId','rating','recommend']
    data = ratings[['movieId', 'rating']]

    movie_df = pd.read_csv(basepath + "recommend_model/movie.csv")
    movie_num = movie_df.shape[0]

    R = [np.nan for i in range(0,movie_num)] #行向量
    indices = pd.Series(movie_df.index, index=movie_df['id'])

    for i in range(0,data.shape[0]):
        ind = indices[data['movieId'][i]]
        R[ind] = data['rating'][i]
    
    U = np.loadtxt(basepath + "recommend_model/U.txt")
    W = np.loadtxt(basepath + "recommend_model/W.txt")

    def dot_ignore_nan(A,B,n,k=3,m=1):
        if m !=1:
            #Not finish
            return
       
        ans = [0.0 for i in range(0,k)]
        ans = np.array(ans)
        for i in range(0,k):
            sumd = 0
            for j in range(0,n):
                if np.isnan(A[j]) == False :
                    sumd += A[j] * B[j][i]
            ans[i] = sumd
        return ans
    
    U_new = dot_ignore_nan(R,W,movie_num,k=U.shape[1])
    cos_sim = np.dot(U,U_new.T)

    index_set = range(0,U.shape[0])
    index_set = sorted(index_set, key=lambda x: cos_sim[x], reverse=True)

    name2index = np.load(basepath + "recommend_model/u_name2index.npy",allow_pickle=True).item()
    index2name = {} 
    for x in name2index.items():
        index2name[x[1]] = x[0] 
    name_list = [index2name[x] for x in index_set]
    return name_list


def train():
    #加载数据
    movie_df = load_movies()
    movie_df.to_csv(basepath + "recommend_model/movie.csv",index=False,sep=',')
    
    ratings = load_ratings()

    print('movie:', movie_df.shape)
    print('rating:', ratings.shape)

    demographic_filtering(movie_df)# 重新获得model
    content_filtering(movie_df)#重新获得model
    collaborative_filtering(ratings)#重新获得model
    create_svd_matrix(number_user=99 ,number_movie=movie_df.shape[0], movie_df=movie_df, ratings=ratings,k=3)

#用户浏览历史记录相关
#debug 暂时先粘贴过来
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

def find_movie_id(id):
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset)
    df = pd.read_sql('select * from movie where id = {}'.format(id),conn)
    return df
####

def mid_to_title(id):
    df = find_movie_id(id)
    return df['title'].iloc[0]

def get_result(user_id):
    if 1:   #用户处于稳定阶段
        #获得看过的电影列表：waiting to finish
        browse_record = get_browse_list(user_id)
        browse_record = [mid_to_title(x) for x in browse_record]
        return get_recommendation(user_id,browse_record)
    else : #过渡阶段
        return get_recommend_svdsim(user_id)

def get_result_sim(user_id):
    return get_recommend_svdsim(user_id)

# def train_pretraindata():
#     movie_df = load_pretrain()

#     demographic_filtering(movie_df)# 重新获得model
#     content_filtering(movie_df)#重新获得model

#测试程序
if __name__ == '__main__':
    # movie_df = load_pretrain()
    # movie_df = load_movies()
    # movie_df.to_csv("./recommend_model/movie.csv",index=False,sep=',')
    # demographic_filtering(movie_df)# 重新获得model
    # # print(get_rec_demographic())
    # content_filtering(movie_df)#重新获得model
    # # print(get_recommendations_mul(['Hi!Li Huanying'],movie_df=movie_df))
    # collaborative_filtering()#重新获得model
    # print(get_recommendation(1,['Hi!Li Huanying']))
    # create_svd_matrix(3,3,movie_df)


    # train()
    # print(get_recommend_svdsim(1))


    # train()
    print(get_result_sim('aaaaa'))
    print(get_result('aaaaa'))
    # print(get_result('b'))
    # print(get_result('c'))
    # print(get_result('d'))
    # print(get_result('e'))
    
