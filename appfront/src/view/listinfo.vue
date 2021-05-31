<template>
    <el-container>
        <el-main>
            <v-container>
                <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                    <v-toolbar-title>影单详情</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn @click="goback()">返回</v-btn>
                </v-toolbar>
                <v-container class="scc">
                    <v-card  v-for="item in movielist" :key="item.id" class="scrd1" color="#000000">
                        <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                            <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                            <v-spacer></v-spacer>
                            <!-- 进入电影详情页 -->
                            <v-btn @click="detail(item.id)">电影详情</v-btn>
                        </v-toolbar>
                        <v-container class="scc2">
                            <el-row class="scrd2">
                                <!-- 图片 -->
                                <img :src="item.urls" class="simg1"/>
                            </el-row>
                        </v-container>
                    </v-card>
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

    data(){
        return{
            movielist: [
                {id:0, title: "测试样例1", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例1"},
                {id:1, title: "测试样例2", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例2"},
                {id:2, title: "测试样例3", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例3"},
                {id:3, title: "测试样例4", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例4"}
            ],
        }
    },

    methods: {
        
        goback(){
            this.$router.push('/recommendlist')
        },

        getData(){
            var listid = JSON.parse(this.$Base64.decode(this.$route.query.listid))
            axiosInstance.post('http://localhost:8000/api/mvsheetlist/',{
                list_id: listid
            })
            .then((response)=>{
                console.log(response)
                this.movielist = response.data
            }).catch((response)=>{
                console.log(response)
            })

        },
        
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
                    mid : this.$Base64.encode(JSON.stringify(v))
                }
            })
        },
    
    },

    created(){
        this.getData()
    }
}
</script>
<style>
    .scrd2{
        width:100%;
        height:450px;
        display: flex;
    }

    .scc{
        padding-left: 0px;
        padding-right: 0px;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-between;
        display: flex;
    }
    
    .scc2{
        padding: 0px;
    }

    .scrd1{
        width: 49.5%;
        height: 500px;
        margin-top: 10px;
    }

    .simg1{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* update by jbt*/
    .rec1{
        margin-right: 20px;
    }

</style>