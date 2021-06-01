<template>
    <el-container>
        <el-main>
            <v-container>
                <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                    <v-toolbar-title>我的已推荐</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn @click="goback()">返回</v-btn>
                </v-toolbar>
                <v-container class="scc5">
                    <v-card  v-for="item in rec_list" :key="item.id" class="scrd5" color="#000000">
                        <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                            <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                            <v-spacer></v-spacer>
                            <!--update by jbt -->
                            <v-btn @click="movielistinfo(item.id)">影单详情</v-btn>
                        </v-toolbar>
                    </v-card>
                </v-container>
                <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                    <v-toolbar-title>我的收藏</v-toolbar-title>
                    <v-spacer></v-spacer>
                </v-toolbar>
                <v-container class="scc5">
                    <v-card  v-for="item in star_list" :key="item.id" class="scrd5" color="#000000">
                        <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                            <v-toolbar-title>{{ item.title }}( Author: {{ item.author }} )</v-toolbar-title>
                            <v-spacer></v-spacer>
                            <!--update by jbt -->
                            <v-btn @click="deletemovielistinfo(item.id)" class="rec3">删除影单</v-btn>
                            <v-btn @click="movielistinfo(item.id)">影单详情</v-btn>
                        </v-toolbar>
                    </v-card>
                </v-container>
                <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                    <v-toolbar-title>我的待推荐</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn @click="upload_rlist()">上传</v-btn>
                </v-toolbar>
                <v-container class="scc5">
                    <v-card  v-for="item in wt_rec_list" :key="item.id" class="scrd1" color="#000000">
                        <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                            <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                            <v-spacer></v-spacer>
                            <!--update by jbt -->
                            <v-btn @click="remove_from_rlist(item.id)" class="rec3">取消推荐</v-btn>
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
            <!-- updated by jbt -->
            <el-dialog :title="'上传推荐影单'" :visible.sync="dialogvisible" :width="'40%'" :before-close="handleclose" center>
                <el-row>
                    <el-col :span="18" :offset="3">
                        <el-input placeholder="请输入影单名称" v-model="listname" ></el-input>
                    </el-col>
                </el-row>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="permission">确定</el-button>
                    <el-button type="primary" @click="handleclose">取消</el-button>
                </span>
            </el-dialog>
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
            dialogvisible: false,
            listname: '',
            rec_list: [
                {id:0, date:"2020/09/02", title:"科幻", author:"test"},
                {id:1, date:"2021/01/01", title:"爱情", author:"sft"},
            ],
            star_list: [
                {id:0, date:"2020/09/02", title:"科幻", author:"test"},
                {id:1, date:"2021/01/01", title:"爱情", author:"sft"},
            ],
            wt_rec_list: [
                {id:0, title: "测试样例1", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例1"},
                {id:1, title: "测试样例2", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例2"},
                {id:2, title: "测试样例3", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例3"},
                {id:3, title: "测试样例4", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例4"}
            ],
        }
    },

    methods: {
        
        deletemovielistinfo(v){
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            axiosInstance.post('http://localhost:8000/api/del_collection/',{
                name: username,
                listid:v
            })
            .then((response)=>{
                window.location.reload()
            })
            .catch((response)=>{
                console.log(response)
            })
        },

        goback(){
            this.$router.push('/home')
        },

        getData(){
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username

            //已推荐
            axiosInstance.post('http://localhost:8000/api/get_already_rec/',{
                name: username
            })
            .then((response)=>{
                var data = response.data
                this.rec_list = data
            })
            .catch((response)=>{
                console.log(response)
            })

            //收藏
            axiosInstance.post('http://localhost:8000/api/get_collections/',{
                name: username
            })
            .then((response)=>{
                var data = response.data
                this.star_list = data
            })
            .catch((response)=>{
                console.log(response)
            })

            //待上传
            axiosInstance.post('http://localhost:8000/api/get_reclist_cache/',{
                name: username
            })
            .then((response)=>{
                var data = response.data
                this.wt_rec_list = data
            })
            .catch((response)=>{
                console.log(response)
            })
        },

        detail( v ){
            // 跳转到该电影详情页
            this.$router.push({
                path: '/movieinfo',
                query:{
                    mid : this.$Base64.encode(JSON.stringify(v))
                }
            })
        },

        remove_from_rlist( v ){
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            axiosInstance.post('http://localhost:8000/api/delete_reclist_cache/',{
                name: username,
                movieid:v
            })
            .then((response)=>{
            })
            .catch((response)=>{
                console.log(response)
            })
           window.location.reload()
        },

        upload_rlist(){
            this.dialogvisible = true
        },

        handleclose(){
            this.dialogvisible = false
            this.listname = ""
        },

        permission(){
            // 上传影单
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            axiosInstance.post('http://localhost:8000/api/add_from_cache/',{
                username: username,
                listname: this.listname
            })
            .then((response)=>{
                var data = response.data
                if(data['info'] == 'Empty list'){
                    this.$message('空列表');
                }
                else {
                    this.$message('上传成功');
                    window.location.reload()
                }
            
            })
            .catch((response)=>{
                console.log(response)
            })
            
        },

        movielistinfo( v ){
            // 跳转到该电影推荐单详情页
            this.$router.push({
                path: '/listinfo',
                query:{
                    listid : this.$Base64.encode(JSON.stringify(v))
                }
            })
        }
    
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

    .scc5{
        padding-left: 0px;
        padding-right: 0px;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-between;
        display: flex;
        margin-bottom: 50px; 
    }
    
    .scc2{
        padding: 0px;
    }

    .scrd5{
        width: 100%;
        height: 50px;
        margin-top: 10px;
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
    .rec3{
        margin-right: 20px;
    }

</style>