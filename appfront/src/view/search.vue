<template>
    <el-container>
        <el-header style="text-align: right; font-size: 100%">
            <el-row :gutter="20" style="marginTop:10px">
                <el-col :span="3" :offset="1">
                    <el-image :src="url" :fit="'cover'">
                    </el-image>
                </el-col>
                <el-col :span="1">
                    <el-button type="primary" icon="el-icon-search" @click="back">返回</el-button> 
                </el-col>
                <el-dropdown @command="handlecommand">
                    <i class="el-icon-s-custom" style="margin-right: 15px"></i>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="login" :disabled="edi1">登录</el-dropdown-item>
                        <el-dropdown-item command="register" :disabled="edi2">注册</el-dropdown-item>
                        <el-dropdown-item command="change" :disabled="edi3">修改</el-dropdown-item>
                        <el-dropdown-item command="logout" :disabled="edi4">登出</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <el-avatar icon="el-icon-user"></el-avatar>
            </el-row>
        </el-header>
        <el-main>
            <el-col :span="18" :offset="3">
                <v-container class="wntj">
                    <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>查询结果</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-container class="cc">
                        <v-card  v-for="item in movielist" :key="item.id" class="crd1" color="#000000">
                            <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                                <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <v-btn @click="detail(item.id)">电影详情</v-btn>
                            </v-toolbar>
                            <v-container class="cc2">
                                <el-row class="crd2">
                                    <img :src="item.urls" class="img1"/>
                                </el-row>
                            </v-container>
                        </v-card>
                    </v-container>
                </v-container>
            </el-col>
            <el-drawer
                :title="movietitle"
                :visible.sync="dialogvisible2"
                :direction="'rtl'"
                :before-close="handleclose2">
                <span>{{content}}</span>
            </el-drawer>
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
            input1: '',
            form:{
                username: '',
                password: '',
            },
            res_data:{
                status: '',
                info: '',
            },
            edi1: false,
            edi2: false,
            edi3: true,
            edi4: true,
            elh: 2000,
            swh: 0,
            xs: 0.36,
            picwidth: 5,
            picheight: 1,
            dialogvisible1: false,
            dialogvisible2: false,
            content: "",
            movietitle: "",
            url: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg',
            movielist: [
            ],
        }
    },

    methods: {
        handlecommand( v ){
            if(v == "login"){
                this.dialogvisible1 = true
            }
            else if(v == "register"){
                this.$router.push({ path: '/register' })
            }
            else if(v == "logout"){
                sessionStorage.removeItem('user')
                window.location.reload()
            }
        },

        handleclose(){
            this.dialogvisible1 = false
        },

        handleclose2(){
            this.dialogvisible2 = false
        },

        login(){     
        },

        register(){
        },

        back(){
            this.$router.push('/home')
        },

        setsize(){
            this.elh = this.swh * this.xs
        },

        setconfig(){
            if(sessionStorage.getItem('user')){
                this.edi1 = true
                this.edi2 = true
                this.edi3 = false
                this.edi4 = false
            }
            else{
                this.edi1 = false
                this.edi2 = false
                this.edi3 = true
                this.edi4 = true
            }
        },

        getData(){
            var searchname = this.$route.query.title
            console.log(searchname)
            axiosInstance.post('http://localhost:8000/api/searchmv/',{
                title: searchname
            })
            .then((response)=>{
                console.log(response)
                this.movielist = response.data
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


            this.dialogvisible2 = true
            for(var i=0; i<this.movielist.length; i++){
                if(this.movielist[i].id == v){
                    this.movietitle = this.movielist[i].title
                    this.content = this.movielist[i].introduce
                }
            }

            // 跳转到该电影详情页
            this.$router.push({
                path: '/movieinfo',
                query:{
                    mid : v
                }
            })
        },

        // detail2( v ){
        //     this.dialogvisible2 = true
        //     for(var i=0; i<this.movielist2.length; i++){
        //         if(this.movielist2[i].id == v){
        //             this.movietitle = this.movielist2[i].title
        //             this.content = this.movielist2[i].introduce
        //         }
        //     }
        // }
        
    },
    
    mounted(){
        this.swh = window.innerWidth
        this.setsize()
    },

    created(){
        this.setconfig()
        this.getData()
    }
}
</script>

<style>

    .img{
        max-height: 100%;
        max-width: 100%;
        min-height: 50%;
        object-fit: contain;
    }

    .imfg{
        width:100%;
        height:80%;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
    }

    .try{
        width:100%;
    }

    .exp{
        font-size:100%;
        color:white;
        text-align:center;
        display:block;
    }

    .wntj{
        display: flex;
        flex-direction: column;
        margin-top: 20px;
        padding-left: 0px;
        padding-right: 0px;
    }

    .crd1{
        width: 49.5%;
        height: 300px;
        margin-top: 10px;
    }

    .crd2{
        width:100%;
        height:250px;
        display: flex;
    }

    .cc{
        padding-left: 0px;
        padding-right: 0px;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-between;
        display: flex;
    }
    
    .cc2{
        padding: 0px;
    }

    .img1{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

</style>