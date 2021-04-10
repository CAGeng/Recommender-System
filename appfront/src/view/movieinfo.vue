<template>
    <el-container>
        <el-main>
            <v-container>
                <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                    <v-toolbar-title>电影详情</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn @click="goback()">返回</v-btn>
                </v-toolbar>
                <v-container class="mcc">
                    <v-card class="mcco">
                        <v-toolbar dark height="50px" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                            <v-toolbar-title>{{title1}}</v-toolbar-title>
                            <v-spacer></v-spacer>
                            <el-rate
                                v-model="value"
                                disabled
                                show-score
                                text-color="#ff9900"
                                score-template="{value}">
                            </el-rate>
                        </v-toolbar>
                        <v-container class="mcc2">
                            <el-row class="mcrd2">
                                <!-- 图片 -->
                                <img :src="urls1" class="mimg1"/>
                            </el-row>
                        </v-container>
                    </v-card>
                    <v-card class="mcco2">
                        <v-card-title>
                            详细介绍
                        </v-card-title>
                        <v-divider></v-divider>
                        {{introduce1}}
                    </v-card>
                </v-container>
                <v-container class="mcc1">
                    <v-toolbar dark height="50px" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>反馈</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-card>
                        <el-input
                            type="textarea"
                            :rows="5"
                            placeholder="请输入电影评论"
                            v-model="usercomment">
                        </el-input>
                        <el-rate
                            v-model="uservalue"
                            show-text>
                        </el-rate>
                        <v-divider></v-divider>
                        <el-button @click="userback()">提交反馈</el-button>
                    </v-card>
                </v-container>
                <v-container class="mcc1">
                    <v-toolbar dark height="50px" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>电影评论</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-card>
                        <el-table :data="commentlist" style="width: 100%">
                            <el-table-column prop="comment" label="评论" class="temp"></el-table-column>
                        </el-table>
                    </v-card>
                </v-container>
                <v-container class="mcc1">
                    <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>相似影片</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-container class="mccc">
                        <v-card  v-for="item in simlist" :key="item.id" class="mcrd1" color="#000000">
                            <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                                <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <!-- 进入电影详情页 -->
                                <v-btn @click="detail(item.id)">电影详情</v-btn>
                            </v-toolbar>
                            <v-container class="mcc2">
                                <el-row class="mcrd2">
                                    <!-- 图片 -->
                                    <img :src="item.urls" class="mimg1"/>
                                </el-row>
                            </v-container>
                        </v-card>
                    </v-container>
                </v-container>
            </v-container>                
        </el-main>
    </el-container>
</template>

<script>
import axiosInstance from '../api/index'
export default {

    beforeCreate () {
        document.body.style.background = "#000000"
    },


    data() {
        return {
            title1: "测试样例1",
            usercomment: "",
            value: 3.7,
            uservalue: null,
            urls1: "https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg",
            introduce1: "我就想试试他到底会不会自动换行啊啊啊啊啊啊啊啊啊啊啊啊啊啊看来成功了",
            commentlist:[
                {comment:"测试样例1如果太长了怎么办啊兄弟我下啊水电费缴纳数据库的管理asd发射点发航空安徽省看到了发as地方阿十大发射点发士大夫撒旦发射点发阿萨的发士大夫阿萨的法师阿斯蒂芬斯蒂芬"},
                {comment:"测试样例2"},
                {comment:"测试样例3"},
                {comment:"测试样例4"},
                {comment:"测试样例5"},
            ],
            simlist:[
                {id:0, title: "测试样例1", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例1"},
                {id:1, title: "测试样例2", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例2"},
                {id:2, title: "测试样例3", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例3"},
                {id:3, title: "测试样例4", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例4"}
            ],
        }
    },

    methods: {

        goback(){
            this.$router.push('/home')
        },

        userback(){
            var movieid2 = JSON.parse(this.$Base64.decode(this.$route.query.mid))
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            axiosInstance.post('http://localhost:8000/api/addrec/',{
                mid : movieid2,
                name:username,
                recommend:this.usercomment,
                rating:this.uservalue
            })
            .then((response)=>{
                var data = response.data
                // console.log(res_data)
                if(data['status'] == 'success'){
                    if(data['info'] == 'modify successfully'){
                        this.$alert("修改评分成功",'Success Message',{
                            confirmButtonText:'确定'
                        })
                    }
                    else{
                        this.$alert("评分成功",'Success Message',{
                            confirmButtonText:'确定'
                        })
                    }
                }
                else{
                    // fail
                    this.$alert("抱歉~我们出了一点错误~",'FAIL',{
                        confirmButtonText:'确定'
                    })
                    console.log(data['info'])
                }
            }).catch((response)=>{
                console.log(response)
            })
        },

        getData(){
            var movieid = JSON.parse(this.$Base64.decode(this.$route.query.mid))
            axiosInstance.post('http://localhost:8000/api/minfo/',{
                mid : movieid
            })
            .then((response)=>{
                console.log(response)
                var mdata = response.data
                // this.picturelist.push(mdata.urls)
                this.urls1 = mdata.urls
                this.title1 = mdata.title
                this.introduce1 = mdata.introduce
                this.value = mdata.rating
                // 获取评论信息
                this.commentlist = mdata.comment

                // 获取相似列表
                axiosInstance.post('http://localhost:8000/api/simlist/',{
                    m_name : this.title1
                })
                .then((response)=>{
                    this.simlist = response.data
                }).catch((response)=>{
                    console.log(response)
                })
            }).catch((response)=>{
                console.log(response)
            })


        },

        // 进入电影详情页，如果用户已经登录，要向后端添加浏览记录
        detail( v ){
            // 如果用户已经登录，要向后端添加浏览记录
            if(sessionStorage.getItem('user')){
                var user = sessionStorage.getItem('user')
                user = JSON.parse(user)
                var username = user.username
                axiosInstance.post('http://localhost:8000/api/addbrowse/',{
                    name: username,
                    mid: v
                })
                .then((response)=>{
                    var data = response.data
                    if(data['status'] != 'success'){
                        console.log('fail: ' + data['info'])
                    }
                    else {
                        console.log("success add browse")
                    }
                }).catch((response)=>{
                    console.log(response)
                })
            }

            // 跳转到该电影详情页
            this.$router.push({
                path: '/movieinfo',
                query:{
                    mid :  this.$Base64.encode(JSON.stringify(v))
                }
            })
        },

        
    },

    watch:{
        $route (to, from){
            this.$router.go(0)
        }
    },

    created(){
       
        this.getData()
    }
}
</script>

<style>

    .mcc{
        padding-left: 0px;
        padding-right: 0px;
        display: flex;
    }

    .mcc1{
        padding-left: 0px;
        padding-right: 0px;
    }

    .mcco{
        width: 70%;
    }

    .mcco2{
        width: 30%;
        height: 350px;
    }

    .mcco3{
        width: 100%;
    }

    .mcc2{
        padding: 0px;
    }

    .mcrd2{
        width: 100%;
        height: 300px;
        display: flex;
    }

    .mimg1{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .mcrd1{
        width: 49.5%;
        height: 350px;
        margin-top: 10px;
    }

    .temp{
        width: 100%;
    }

    .mccc{
        padding-left: 0px;
        padding-right: 0px;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-between;
        display: flex;
    }

</style>