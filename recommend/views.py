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
        intro += '. '
    else :
        intro += '. '
    
    if isinstance(genres_list,list) and len(genres_list) > 0:
        intro += 'The movie tells about '
        for i in range(0,min(5,len(genres_list))):
            intro += genres_list[i] + ','
        intro += '. '
    
    if isinstance(keywords_list,list) and len(keywords_list) > 0:
        intro += 'Its keywords contains: '
        for i in range(0,min(5,len(keywords_list))):
            intro += keywords_list[i] + ','
        intro += '. '
    print(intro)
    return intro

    
#getm 的api相应，返回前端电影信息列表
def get_movies(request):
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
    
    def get_moviedic_list(id_list): # 根据id列表获得信息字典
        info_list = []
        for mid in id_list:
            mov = database.find_movie_id(mid)
            print(mov['id'].iloc[0])
            info_dic = {
                'id':str(mov['id'].iloc[0]),
                'title':str( mov['title'].iloc[0]),
                'introduce' : str(get_introduce(mov)),
                'urls': "http://127.0.0.1:8000/static/" + str(mov['id'].iloc[0]) + ".jpg"
            }
            info_list.append(info_dic)
        return info_list

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




#将图片以字节流发送到前端
def read_img(request):
    try:
        with open("C:/Users/sft/Desktop/数据集/电影推荐 - 副本/picture/58.jfif", 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/png")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

