from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse

import json
from . import recommend,database
import pandas as pd
import cv2
# Create your views here.

#用于获取电影介绍
def get_introduce(df):
    '''
    para:
        df: 数据库中格式的一个电影条目
    output:电影介绍
    '''
    from ast import literal_eval
    import numpy as np
    #字符串->python对象
    features = ['cast', 'keywords', 'genres']
    for feature in features:
        df[feature] = df[feature].apply(literal_eval)

    #获得导演名字
    temp = df['crew'].iloc[0]
    temp = temp.split(',')
    director = None
    for x in temp:
        x = x.split(':')
        if x == None or x[0] != 'Director':
            continue
        director = x[1]

    title = df['title'].iloc[0]
    cast_list = df['cast'].iloc[0]
    keywords_list = df['keywords'].iloc[0]
    genres_list = df['genres'].iloc[0]

    intro = ''
    intro += title + ', '
    if director != None:
        intro += 'directed by ' + director + ', '
    if isinstance(cast_list,list) and len(cast_list) > 0:
        intro += 'is stared by '
        for i in range(0,min(5,len(cast_list))):
            intro += cast_list[i] + ','
        intro = intro[:-1] + '. '
    else :
        intro = intro[:-1] + '. '
    
    if isinstance(genres_list,list) and len(genres_list) > 0:
        intro += 'The movie tells about '
        for i in range(0,min(5,len(genres_list))):
            intro += genres_list[i] + ','
        intro = intro[:-1] + '. '
    
    if isinstance(keywords_list,list) and len(keywords_list) > 0:
        intro += 'Its keywords contains: '
        for i in range(0,min(5,len(keywords_list))):
            intro += keywords_list[i] + ','
        intro = intro[:-1] + '. '
    # print(intro)
    return intro

#根据id获得一个电影的信息字典
def get_movdic(mid):
    mov = database.find_movie_id(mid)
    # print(mov['id'].iloc[0])
    info_dic = {
        'id':str(mov['id'].iloc[0]),
        'title':str( mov['title'].iloc[0]),
        'introduce' : str(get_introduce(mov)),
        'urls': "http://127.0.0.1:8000/static/" + str(mov['id'].iloc[0]) + ".jpg"
    }
    return info_dic

# 根据id列表获得信息字典列表
def get_moviedic_list(id_list): 
    info_list = []
    for mid in id_list:
        info_dic = get_movdic(mid)
        info_list.append(info_dic)
    return info_list
    
#getm 的api相应，返回前端电影信息列表
def get_movies(request):
    '''
    para:
        request:包含
            uid: 用户名
    output:信息列表
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        uid = data['uid']
    else:#debug
        uid = 'a'

    df = recommend.get_result(uid)
    print(df)
    movie_id_list=[]
    for i in range(df.shape[0]):
        mid = df['id'].iloc[i]
        movie_id_list.append(mid)
    

    info_list = get_moviedic_list(movie_id_list)
    
    
    # res = info_list.to_dict(orient="records")
    
    # df.append({'urls' : "http://127.0.0.1:8000/static/534.jpg"})

    
    return JsonResponse(info_list,safe=False)


#login 的api响应，接收用户名和密码
def login(request):
    '''
    param:
        request:包含 name 和 key
    output：
        如果成功，返回status为success，info为空
        如果密码错误，返回status为fail，info为'wrong key'
        如果用户名不存在， 返回status为fail，info为'wrong name'
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data['name']
        key = data['key']
    else :#debug
        name = 'sadfd'
        key = 'asdfdas'

    if database.login(name,key) == 0:
        dic = {
            'status':'success',
            'info': ''
        }
    elif database.login(name,key) == 1:
        dic = {
            'status':'fail',
            'info': 'wrong key'
        }
    elif database.login(name,key) == 2:
        dic = {
            'status':'fail',
            'info': 'wrong name'
        }

    return JsonResponse(dic,safe=False)

#getm_info的函数api，用于展示一页具体的电影
def getm_info(request):
    '''
    para:
        request:包含
            mid: 电影id
    output:
        电影信息
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        mid = data['mid']
    else:#debug
        mid = 597 #Titanic

    dic = get_movdic(mid)
    return JsonResponse(dic,safe=False)

#getm_sim的函数api，用于过渡时期推荐
def get_movies_sim(request):
    '''
    para:
        request:包含
            uid: 用户名
    output:推荐信息列表（字典表）
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['uid']
    else:#debug
        name = 'a'

    #name 保存了前端请求的用户名
    sim_names = recommend.get_result_sim(name)
    res_list = []
    con = 0
    #获得“相似的用户还喜欢看”
    for sim_name in sim_names:
        movs = database.get_rec_list(sim_name)
        for mov in movs:
            if mov not in res_list:
                res_list.append(mov)
                con += 1
                if con >= 10:
                    break
        if con >= 10:
            break

    #res_list保存了推荐电影的id列表
    info_list = get_moviedic_list(res_list)
    
    return JsonResponse(info_list,safe=False)

#将图片以字节流发送到前端
def read_img(request):
    try:
        with open("C:/Users/sft/Desktop/数据集/电影推荐 - 副本/picture/58.jfif", 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/png")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

