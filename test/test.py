import requests
import json

#推荐
def testcase1():
    print("----------------------test1-----------------------------------")
    url = "http://localhost:8000/api/getm/"
    data = {"uid":"sft","method":"common"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/getm/"
    data = {"uid":"sft","method":"demographic"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/getm/"
    data = {"uid":"sft","method":"content"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/getm/"
    data = {"uid":"","method":"common"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())

#登录
def testcase2():
    print("----------------------test2-----------------------------------")
    url = "http://localhost:8000/api/login/"
    data = {"name":"sft","key":"080090"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/login/"
    data = {"name":"sfsadfsdt","key":"080090"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/login/"
    data = {"name":"sft","key":"080sadfasfd090"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())

#添加收藏
def testcase3():
    print("----------------------test3-----------------------------------")
    url = "http://localhost:8000/api/addcol/"
    data = {"name":"sft","listid":"11s1"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/addcol/"
    data = {"name":"sft","listid":"11s1"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())

#添加推荐的电影
def testcase4():
    print("----------------------test4-----------------------------------")
    url = "http://localhost:8000/api/add_reclist_cache/"
    data = {"name":"sft","movieid":3}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/add_reclist_cache/"
    data = {"name":"sft","movieid":3}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())

#添加评论评分
def testcase5():
    print("----------------------test5-----------------------------------")
    url = "http://localhost:8000/api/addrec/"
    data = {"name":"a","mid":597,"rating":3,"recommend":"good"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/addrec/"
    data = {"name":"a","mid":597,"rating":3,"recommend":"good"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/addrec/"
    data = {"name":"a","mid":-2,"rating":3,"recommend":"good"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())
    url = "http://localhost:8000/api/addrec/"
    data = {"name":"zxvzxcv","mid":597,"rating":3,"recommend":"good"}
    res = requests.post(url=url,data=json.dumps(data))
    print(res.json())


if __name__=="__main__":
    #白盒
    testcase1()
    testcase2()
    testcase3()
    testcase4()
    testcase5()
