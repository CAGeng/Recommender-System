from django.http import response
from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse

import json
from . import recommend,database,SendEmail
import pandas as pd
from random import shuffle
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
    
#用户未登录时的基于统计的推荐
def get_movie_no_user():
    df = recommend.get_rec_demographic()  #返回的是id的列表
    movie_id_list=[]
    for i in range(min(df.shape[0], 20)):
        mid = df.iloc[i]
        movie_id_list.append(mid)
    info_list = get_moviedic_list(movie_id_list)
    return info_list

#getm 的api响应，返回前端电影信息列表
#orzorz sft 加入了不同的排序方式的功能
def get_movies(request):
    '''
    para:
        request:包含
            uid: 用户名
            method: 排序方法
    output:信息列表
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        uid = data['uid']
        method = data['method']
    else:#debug
        uid = 'sft'
        # method = 'demographic'
        method = 'common'

    if uid == '':  #没有登录情况的推荐列表
        info_list = get_movie_no_user()
        rec_info = info_list[5:15]
        return JsonResponse(rec_info,safe=False)

    if method == 'common':
        df = recommend.get_result(uid) #默认权重
    elif method == 'demographic':
        df = recommend.get_result(uid,a=0,b=1,c=0) #纯统计数据模式
    elif method == 'content':
        df = recommend.get_result(uid,a=1,b=0,c=0) #纯内容相关度模式
    # print(df)
    movie_id_list=[]
    for i in range(df.shape[0]):
        mid = df['id'].iloc[i]
        movie_id_list.append(mid)
    

    info_list = get_moviedic_list(movie_id_list)
    
    
    # res = info_list.to_dict(orient="records")
    
    # df.append({'urls' : "http://127.0.0.1:8000/static/534.jpg"})

    
    return JsonResponse(info_list,safe=False)

#最热推荐的函数api
def get_movie_hottest(request):
    info_list = get_movie_no_user()
    rec_info = info_list[0:5]
    return JsonResponse(rec_info,safe=False)

#searchmv的函数api，用于根据用户输入的title查找电影，支持模糊查找
def search_movie(request):
    '''
    para:
        request:
            title: 用户输入的电影名（模糊的）
    output:
        电影信息的列表（字典表）
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        title = data['title']
    else:#debug
        title = 'iron man'

    df = database.find_movie_title(title)
    movie_id_list=[]
    for i in range(df.shape[0]):
        mid = df['id'].iloc[i]
        movie_id_list.append(mid)

    info_list = get_moviedic_list(movie_id_list)
    return JsonResponse(info_list,safe=False)

#orzorz
#searchmvbykind的函数api，用于搜索给定类别的电影
def search_movie_bykind(request):
    '''
    para:
        request:
            kind: 电影类别
    output:
        电影信息的列表（字典表）
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        kind = data['kind']
    else:#debug
        kind = 'Drama'

    movie_id_list = database.search_by_kind(kind)
    if len(movie_id_list) > 8:
        movie_id_list = movie_id_list[:8]
    info_list = get_moviedic_list(movie_id_list)
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
        name = 'sft'
        key = '080090'

    err = database.login(name,key)

    #获取该用户的访问权限
    isAdmin = database.find_admin(name)

    if err == 0:
        dic = {
            'status':'success',
            'info': 'admin' if isAdmin else 'normal'
        }
    elif err == 1:
        dic = {
            'status':'fail',
            'info': 'wrong key'
        }
    elif err == 2:
        dic = {
            'status':'fail',
            'info': 'wrong name'
        }
    return JsonResponse(dic,safe=False)

#根据电影id，获得该电影的一些用户评论
def get_movie_comment(mid):
    df = database.find_recommend_id(mid)
    res = []
    for i in range(df.shape[0]):
        # name = df['name'].iloc[i]
        comment = df['comment'].iloc[i]
        if comment == '':
            continue
        res.append({'comment':comment})
    return res

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
        mid = 0 #Iron Man 2

    dic = get_movdic(mid)
    dic['comment'] = get_movie_comment(mid)
    data = database.get_avg_rating(mid)
    if len(data) > 0:
        dic['rating'] = data[0]/2
    else :
        dic['rating'] = 0
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
        print(name)
    else:#debug
        name = 'sft_brother'

    if name == '':  #没有登录情况的推荐列表
        info_list = get_movie_no_user()
        rec_info = info_list[15:]
        return JsonResponse(rec_info,safe=False)

    #name 保存了前端请求的用户名
    sim_names = recommend.get_result_sim(name)
    res_list = []

    #获得用户看过的电影
    browse_list = database.get_browse_list(name)

    con = 0
    #获得“相似的用户还喜欢看”
    for sim_name in sim_names:
        movs = database.get_rec_list(sim_name)
        for mov in movs:
            if mov in browse_list:  #如果该用户看过了就不再推荐了
                continue
            if mov not in res_list :
                res_list.append(mov)
                con += 1
                if con >= 10:
                    break
        if con >= 10:
            break

    #res_list保存了推荐电影的id列表
    info_list = get_moviedic_list(res_list)

    # if len(info_list) < 5:
    #     print('sim_rec : not enough')
    #     return get_movies(request)
    
    return JsonResponse(info_list,safe=False)

#simlist的函数api，用于在电影页推荐相似电影
def get_simlist(request):
    '''
    para:
        request:包含
            m_name: 电影名
    output:
        电影信息列表
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        m_name = data['m_name']
    else:#debug
        m_name = 'Iron Man'

    m_name = [m_name]
    df = recommend.get_recommendations_mul(m_name)
    # print(df)
    movie_id_list=[]
    for i in range(df.shape[0]):
        mid = df['id'].iloc[i]
        movie_id_list.append(mid)

    info_list = get_moviedic_list(movie_id_list)
    return JsonResponse(info_list,safe=False)

#将图片以字节流发送到前端  #暂时没有用到，目前只传送url
def read_img(request):
    try:
        with open("C:/Users/sft/Desktop/数据集/电影推荐 - 副本/picture/58.jfif", 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/png")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

#regist的函数api, 用户注册
def regist(request):
    '''
    para:
        request:包含
            name: 用户名
            email: 邮箱
            key:密码
    output:
        若注册成功，返回
            status: success
            info: 空
        若用户名冲突，返回
            status: fail
            info: conflict 
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        email = data['email']
        key = data['key']
        code = data['code']

    else:#debug
        name = 'aaaaa'
        email = '1@1.com'
        key = '1'
    
    result = database.verify_Code(email, code)
    err = 0
    if result == 1:
        err = database.add_user(name,key,email)
    # print(err,result)
    if err == 0 and result == 1:
        res = {
            'status' : 'success',
            'info' : ''
        }
    elif err == 1:
        res = {
            'status' : 'fail',
            'info' : 'conflict'
        }
    elif result == 0:
        res = {
            'status' : 'fail',
            'info' : 'verifyfail'
        }

    return JsonResponse(res,safe=False)

#logout的函数api，用户注销
def logout(request):
    '''
    para:
        request:包含
            name: 用户名
    output:
        若注销成功，返回
            status: success
            info: 空
        若注销失败，返回
            status: fail
            info: 空
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']

    else:#debug
        name = 'd'

    err = database.logout(name)
    if err == 0:
        res = {
            'status' : 'success',
            'info' : ''
        }
    elif err == 1:
        res = {
            'status' : 'fail',
            'info' : ''
        }

    return JsonResponse(res,safe=False)

#addrec的函数api，用于添加一条评分记录
def add_rec(request):
    '''
    para:
        request:包含
            name: 用户名
            mid : 电影id
            rating：评分
            recommend：评论
    output:
        若添加成功，返回
            status: success
            info: 空
        若该用户已经评价过此电影，自动修改评分和评语，视作成功，返回
            status: success
            info: modify successfully
        若添加失败，返回
            status: fail
            info:失败原因 
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        mid = data['mid']
        rating = data['rating']
        recom_txt = data['recommend']

    else:#debug
        name = 'a'
        mid = 597
        rating = 3
        recom_txt = 'Good'

    err = database.add_recommend(mid, name, rating, recom_txt)
    if err == 0:
        res = {
            'status' : 'success',
            'info' : ''
        }
    elif err == 1:
        res = {
            'status' : 'fail',
            'info' : 'movie not exists'
        }
    elif err == 2:
        res = {
            'status' : 'fail',
            'info' : 'user not exists'
        }
    elif err == 3:
        res = {
            'status' : 'success',
            'info' : 'modify successfully'
        }
    return JsonResponse(res,safe=False)


#addbrowse的函数api，用于添加浏览记录
#目前的方法是无缓存的直接添加进入数据库
def add_browse(request):
    '''
    para:
        request:包含
            name: 用户名
            mid: 电影id
    output:
        若添加成功，返回
            status: success
            info: 空
        若添加失败，返回
            status: fail
            info:失败原因 
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        mid = data['mid']

    else:#debug
        name = 'a'
        mid = 597

    err = database.add_browse_record(name,[mid])
    if err == 0:
        res = {
           'status' : 'success',
            'info' : '' 
        }
    elif err == 1:
        res = {
            'status' : 'fail',
            'info' : 'user not exists'
        }

    return JsonResponse(res,safe=False)



#addmvsheet的函数api，用于添加一个用户的推荐电影单
def add_movie_sheet(request):
    '''
    para:
        request:包含
            name: 用户名
            mlist: 电影列表，形式为 '[1,2,3,4]'
    output:
        若添加成功，返回
            status: success
            info: 空
        若添加失败，返回
            status: fail
            info:失败原因 
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        mlist = data['mlist']

    else:#debug
        name = 'b'
        mlist = '[597]'
    
    from ast import literal_eval
    mlist = literal_eval(mlist)

    err = database.add_rec_list(name, mlist)
    if err == 0:
        res = {
           'status' : 'success',
            'info' : '' 
        }
    elif err == 1:
        res = {
            'status' : 'fail',
            'info' : 'user not exists'
        }
    elif err == 2:
        res = {
            'status' : 'fail',
            'info' : 'empty list'
        }
    return JsonResponse(res,safe=False)

#mvsheetlist的函数api，用于获得一个表单中的电影列表
def moviesheet_list(request):
    '''
    para:
        request:
            list_id: 列表的id
    output:
        电影信息的列表（字典表）
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        list_id = data['list_id']
    else:#debug
        list_id = '1f13dd8c36cbfe7862e95c69379b6fdb'

    movie_id_list = database.get_movie_inlist(list_id)

    info_list = get_moviedic_list(movie_id_list)
    return JsonResponse(info_list,safe=False)

#get_already_rec的函数api
def get_already_rec(request):
    '''
    para:
        request:
            name:用户名
    output:
        电影单表
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data['name']
    else:#debug
        name = 'sft'

    moviesheet_df = database.get_reclist_df(name)
    response = []
    for i in range(moviesheet_df.shape[0]):
        username = moviesheet_df['name'][i]
        sheet_id = moviesheet_df['list_id'][i]
        sheet_name = moviesheet_df['list_name'][i]
        print(sheet_name)
        response.append({"author":username,"title":sheet_name,"id":sheet_id})
    return JsonResponse(response,safe=False)

#get_collections的函数api
def get_collections(request):
    '''
    para:
        request:
            name:用户名
    output:
        电影单表
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data['name']
    else:#debug
        name = 'sft'

    sheetid_list = database.get_user_colletions(name)
    response = []
    for sheetid in sheetid_list:
        sheetdf = database.get_sheet_info(sheetid)
        if sheetdf.shape[0] == 0:
            continue
        else:
            username = sheetdf['name'][0]
            sheet_id = sheetdf['list_id'][0]
            sheet_name = sheetdf['list_name'][0]
            response.append({"author":username,"title":sheet_name,"id":sheet_id})
    return JsonResponse(response,safe=False)

def del_collection(request):
    '''
    para:
        request:包含
            name: 用户名
            listid: 列表id
    output:
        若删除成功，返回
            status: success
            info:
        否则，返回
            status: success
            info:'not exist'
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        listid = data['listid']
    else:   #debug
        name = 'sft'
        listid = '3d828cb53d4ce013832838cfa207824a'
    
    err = database.del_collection(name,listid)
    if err == 0:
        res = {
           'status' : 'success',
            'info' : '' 
        }
    elif err == 1:
        res = {
            'status' : 'success',
            'info' : 'not exist'
        }
    return JsonResponse(res,safe=False)
           

#添加收藏的函数api
def add_collection(request):
    '''
    para:
        request:包含
            name: 用户名
            listid: 列表id
    output:
        若添加成功，返回
            status: success
            info:
        否则，返回
            status: fail
            info:错误信息
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        listid = data['listid']
    else:   #debug
        name = 'a'
        listid = 'test'

    err = database.add_collection(name,listid)
    if err == 0:
        res = {
           'status' : 'success',
            'info' : '' 
        }
    elif err == 1:
        res = {
            'status' : 'success',
            'info' : 'already in'
        }

    return JsonResponse(res,safe=False)

def get_sheets(request):
    '''
    para:
        request:
    output:
        电影单表
    '''
    response = database.get_sheets(count_limit=5)
    return JsonResponse(response,safe=False)

def add_reclist_cache(request):
    '''
    para:
        request:包含
            name: 用户名
            movieid:电影id
    output:
        若重复电影，返回
            status: success
            info: already_in
        否则
            sstatus: success
            info: finish
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        movieid = data['movieid']

    else:#debug
        name = 'b'
        movieid = 2
    
    err = database.add_rec_cache(name,movieid)
    if err == 1:
        response = {
            'status': 'success',
            'info': 'already_in'
        }
    else:
        response = {
            'status': 'success',
            'info': 'finish'
        }
    return JsonResponse(response,safe=False)

def delete_reclist_cache(request):
    '''
    para:
        request:包含
            name: 用户名
            movieid:电影id
    output:
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        movieid = data['movieid']

    else:#debug
        name = 'b'
        movieid = 2
    database.del_rec_cache(name,movieid)
    response = {
        'status': 'success',
        'info': ''
    }
    return JsonResponse(response,safe=False)

def get_reclist_cache(request):
    '''
    para:
        request:包含
            name: 用户名
            movieid:电影id
    output:
        电影表
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))    
        name = data['name']

    else:#debug
        name = 'sft'

    movieidlist = database.get_rec_cache(name)
    response = get_moviedic_list(movieidlist)
    return JsonResponse(response,safe=False)

def add_from_cache(request):
    '''
    para:
        request:包含
            username: 用户名
            listname:sheet名
    output:
        
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))    
        username = data['username']
        listname = data['listname']

    else:#debug
        username = 'sft'
        listname = '好看的电影随意的名字'
    
    err = database.add_from_cache(username,listname)
    if err == 1:
        response = {
            'status': 'success',
            'info': 'Empty list'
        }
    else:
        response = {
            'status': 'success',
            'info': 'finish'
        }
    return JsonResponse(response,safe=False)


#邮箱验证相关
#generatecode的函数api，从request中获取email, 并为其生成验证码
def generatecode(request):
    '''
    para:
        request:包含
            email: 邮箱地址
    output:
        若验证码生成成功，返回
            status: success
            info: 空
        若添加失败，返回
            status: fail
            info:失败原因 
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        email = data['email']

    else:   #debug
        email = '1256736926@qq.com'
    code = database.generate_VerificationCode(email)
    err = SendEmail.sendEmail(email, code)
    if err == 0:
        res = {
           'status' : 'success',
            'info' : '' 
        }
    else:
        res = {
            'status' : 'fail',
            'info' : 'SMTPException'
        }
    return JsonResponse(res,safe=False)
    
# 现在放在regist里了，没有使用
#verifycode的函数api，从request中获取email和code,返回验证结果
def verifycode(request):
    '''
    para:
        request:包含
            email: 邮箱地址
    output:
        若验证码匹配，返回
            status: success
            info: True
        若验证码不匹配，返回
            status: success
            info:False
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        email = data['email']
        code = data['code']
    else:   #debug
        email = '1256736926@qq.com'
        code = '593523'
    result = database.verify_Code(email, code)
    if result == 1:
        res = {
           'status' : 'success',
            'info' : 'True' 
        }
    else:
        res = {
            'status' : 'success',
            'info' : 'False'
        }
    return JsonResponse(res,safe=False)

#上传电影图片
def upload_movieImg(request):
    '''
    para:
        request：包含
    output:
        若上传成功，返回
            status: success
            info: movieid
    '''
    movieid = database.getMovieid()

    try:
        files = request.FILES.getlist("file",None) # 接收前端传递过来的多个文件
        file_path = 'movies/' + str(movieid) + '.jpg'
        for file in files:
            with open(file_path, 'wb') as f:
                for content in file.chunks():
                    f.write(content)
    except Exception as result:
        print("未知错误 %s " % result)
    
    res = {
        'status' : 'success',
        'info' : str(movieid)
    }
    return JsonResponse(res, safe=False)
   
#电影上传
def upload_movie(request):
    '''
    para:
        request:包含
            title, cast, crew, keywords, genres
    output:
        若上传成功匹配，返回
            status: success
            info: 空
        若上传失败，返回
            status: fail
            info:失败原因
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        movieid = data['movieid']
        title = data['title']
        cast = data['cast']
        crew = data['crew']
        keywords = data['keywords']
        genres = data['genres']  #这个是数组，其他是字典表
    else:
        movieid = 0
        title = 'debug'
        cast = [{'value':'debug'}]
        crew = [{'value':'debug'},{'value':'debug2'}]
        keywords = [{'value':'debug'}]
        genres = ['g1','g2']

    def list2string(mylist):
        mylist = [x['value'] for x in mylist]
        mylist = "[\'" + '\',\''.join(mylist) + "\']"
        return mylist
    
    def get_director(crew):
        crewstr = ''
        for x in crew:
            crewstr += ',Director:' + x['value']
        if len(crewstr) >= 1:    
            crewstr = crewstr[1:]
        return crewstr

    cast = list2string(cast)
    crew = get_director(crew)
    genres2 = list2string(keywords)
    # 由于历史原因，genres和keywords要翻过来！
    keywords2 = "[\'" + '\',\''.join(genres) + "\']"

    print(movieid, title, cast, crew, keywords2, genres2, 0, 0)
    err = database.add_movie(movieid, title, cast, crew, keywords2, genres2, 0, 0)
    if err == 0:
        res = {
           'status' : 'success',
            'info' : '' 
        }
    else:
        res = {
            'status' : 'success',
            'info' : 'movie exits!'
        }
    return JsonResponse(res,safe=False)

#orzorz hyx
#change_password的函数api, 修改密码
def change_password(request):
    '''
    para:
        request:包含
            name: 用户名
            oldpwd: 旧密码
            newpwd: 新密码
    output:
        若修改成功，返回
            status: success
            info: 空
        若旧密码错误，返回
            status: fail
            info: wrong old password
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data['name']
        oldpwd = data['oldpwd']
        newpwd = data['newpwd']

    else:#debug
        name = 'aaaaa'
        oldpwd = '123'
        newpwd = '12345'

    err = database.change_password(name, oldpwd, newpwd)
    if err == 0:
        res = {
            'status' : 'success',
            'info' : ''
        }
    elif err == 1:
        res = {
            'status' : 'fail',
            'info' : 'wrong old password'
        }

    return JsonResponse(res,safe=False)

def add_admin(request):
    '''
    para:
        request:包含
            username: 用户名
    output:
        
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))    
        username = data['username']

    else:#debug
        username = 'sft'
    
    err = database.add_administrators(username)
    if err == 0:
        res = {
            'status' : 'success',
            'info' : ''
        }
    elif err == 1:
        res = {
            'status' : 'success',
            'info' : 'alreay exists'
        }
    return JsonResponse(res,safe=False)

def get_browse_record(request):
    '''
    param:
        request:包含 name 
    output：
        电影单
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data['name']
    else :#debug
        name = 'sft'

    movieid_list = database.get_browse_list(name)
    response = get_moviedic_list(movieid_list)
    return JsonResponse(response,safe=False)