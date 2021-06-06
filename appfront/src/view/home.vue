<template>
    <el-container>
        <el-header style="text-align: right; font-size: 100%">
            <el-row :gutter="20" style="marginTop:10px">
                <el-col :span="3" :offset="1">
                    <el-image :src="url" :fit="'cover'">
                    </el-image>
                </el-col>
                <!-- 搜索 -->
                <el-col :span="6" :offset="4">
                    <el-input placeholder="movie" v-model="input1">
                    </el-input>
                </el-col>
                <el-col :span="1">
                    <el-button type="primary" icon="el-icon-search" @click="search()">搜索</el-button> 
                </el-col>
                <!-- 查看自己的推荐列表 -->
                <el-col :span="1" :offset="1">
                    <el-button type="primary" icon="el-icon-s-home" @click="show_my_rlist()">我的推荐</el-button> 
                </el-col>
                <!-- 管理员上传电影 -->
                <el-col :span="1" :offset="4">
                    <el-button v-show="isAdmin" type="primary" icon="el-icon-plus" @click="upload_movie()"></el-button> 
                </el-col>
                <!-- 右上角菜单，登陆注册 -->
                <el-dropdown @command="handlecommand2">
                    <i class="el-icon-plus" style="margin-right: 15px"></i>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="a" :disabled="eddi1">综合</el-dropdown-item>
                        <el-dropdown-item command="b" :disabled="eddi2">最热门</el-dropdown-item>
                        <el-dropdown-item command="c" :disabled="eddi3">最相关</el-dropdown-item>
                        
                    </el-dropdown-menu>
                </el-dropdown>
                <el-dropdown @command="handlecommand">
                    <i class="el-icon-s-custom" style="margin-right: 15px"></i>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="login" :disabled="edi1">登录</el-dropdown-item>
                        <el-dropdown-item command="register" :disabled="edi2">注册</el-dropdown-item>
                        <el-dropdown-item command="change" :disabled="edi3">注销</el-dropdown-item>
                        <el-dropdown-item command="logout" :disabled="edi4">登出</el-dropdown-item>
                        <!-- orzorz hyx -->
                        <el-dropdown-item command="changepwd" :disabled="edi5">修改密码</el-dropdown-item>
                        <!-- updated by jbt -->
                        <el-dropdown-item command="beadmin" :disabled="edi6">成为管理员</el-dropdown-item>
                        <el-dropdown-item command="record" :disabled="edi7">查看浏览记录</el-dropdown-item>
                        <el-dropdown-item command="personalinfo" :disabled="edi8">查看个人信息</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <el-avatar icon="el-icon-user"></el-avatar>
            </el-row>
        </el-header>
        <el-main>
            <el-col :span="18" :offset="3">
                <el-row class="carousel" align="middle">
                    <el-carousel :height="elh + 'px'" :interval="3000" type="card" :loop="true">
                        <!-- 最热推荐 -->
                        <el-carousel-item v-for="item in datalist" :key="item.id" :span="12">
                            <el-row class="imfg">
                                <img id="test" :src="item.urls" class="img"/>
                            </el-row>
                        </el-carousel-item>
                    </el-carousel>
                </el-row>
                <v-container class="wntj">
                    <!-- 推荐列表 -->
                    <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>为您推荐</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-container class="cc">
                        <v-card  v-for="item in movielist" :key="item.id" class="crd1" color="#000000">
                            <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                                <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <!--update by jbt -->
                                <v-btn @click="add_to_rlist(item.id)" class="rec">加入推荐</v-btn>
                                <!-- 进入电影详情页 -->
                                <v-btn @click="detail(item.id)">电影详情</v-btn>

                                
                                <!-- <v-btn @click="fttest()">电影详情</v-btn> -->

                            </v-toolbar>
                            <v-container class="cc2">
                                <el-row class="crd2">
                                    <!-- 图片 -->
                                    <img :src="item.urls" class="img1"/>
                                </el-row>
                            </v-container>
                        </v-card>
                    </v-container>
                    <!-- 相似的人还喜欢看 -->
                    <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg" style="margin-top:50px">
                        <v-toolbar-title>与您类似的人还喜欢看</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-container class="cc">
                        <v-card  v-for="item in movielist2" :key="item.id" class="crd1" color="#000000">
                            <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                                <v-toolbar-title>{{ item.title }}</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <!--update by jbt -->
                                <v-btn @click="add_to_rlist(item.id)" class="rec">加入推荐</v-btn>
                                <!-- 进入电影详情页 -->
                                <v-btn @click="detail(item.id)">电影详情</v-btn>
                            </v-toolbar>
                            <v-container class="cc2">
                                <el-row class="crd2">
                                    <!-- 图片 -->
                                    <img id="test" :src="item.urls" class="img1"/>
                                </el-row>
                            </v-container>
                        </v-card>
                    </v-container>
                    <v-toolbar class="forhome" dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>其他人的推荐影单</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-container class="scc5">
                        <v-card  v-for="item in rec_list" :key="item.id" class="scrd5" color="#000000">
                            <v-toolbar dark height="50px" src="https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg">
                                <v-toolbar-title>{{ item.title }}( Author: {{ item.author }} )</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <!--update by jbt -->
                                <v-btn @click="star(item.id)" class="rec">收藏影单</v-btn>
                                <v-btn @click="movielistinfo(item.id)">影单详情</v-btn>
                            </v-toolbar>
                        </v-card>
                    </v-container>
                </v-container>
            </el-col>
            <!-- 登录弹窗 -->
            <el-dialog :title="'电影推荐系统登录'" :visible.sync="dialogvisible1" :width="'40%'" :before-close="handleclose" center>
                <el-row>
                    <el-col :span="18" :offset="3">
                        <el-input placeholder="请输入用户名或邮箱" v-model="form.username"></el-input>
                        <el-input style="marginTop:5%" placeholder="请输入密码" v-model="form.password" show-password></el-input>
                    </el-col>
                </el-row>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="register">注册</el-button>
                    <el-button type="primary" @click="login">登录</el-button>
                </span>
            </el-dialog>

            <!-- orzorz hyx -->
            <!-- 修改密码弹窗 -->
            <el-dialog :title="'修改密码'" :visible.sync="dialogvisible2" :width="'40%'" :before-close="handleclose" center>
                <el-row>
                    <el-col :span="18" :offset="3">
                        <el-input placeholder="请输入旧密码" v-model="form.oldpwd" show-password></el-input>
                        <el-input style="marginTop:5%" placeholder="请输入新密码" v-model="form.newpwd" show-password></el-input>
                        <el-input style="marginTop:5%" placeholder="请再次输入新密码" v-model="form.rnewpwd" show-password></el-input>
                    </el-col>
                </el-row>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="changepwd">确定</el-button>
                    <el-button type="primary" @click="handleclose">取消</el-button>
                </span>
            </el-dialog>

            <!-- updated by jbt -->
            <el-dialog :title="'成为管理员'" :visible.sync="dialogvisible3" :width="'40%'" :before-close="handleclose2" center>
                <el-row>
                    <el-col :span="18" :offset="3">
                        <el-input placeholder="请输入口令" v-model="adminpass" show-password></el-input>
                    </el-col>
                </el-row>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="adminpermission">确定</el-button>
                    <el-button type="primary" @click="handleclose2">取消</el-button>
                </span>
            </el-dialog>

            <el-dialog :title="'个人信息'" :visible.sync="dialogvisible4" :width="'40%'" :before-close="handleclose3" center>
                <el-row>
                    <el-col :span="18" :offset="3">
                        邮箱:{{userinfo.email}}
                        用户名：{{userinfo.username}}
                        密码:{{userinfo.password}}
                    </el-col>
                </el-row>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="handleclose3">确定</el-button>
                    <el-button type="primary" @click="handleclose3">取消</el-button>
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

    data() {
        return {
            input1: '',
            // orzorz hyx
            oldpwd: '',
            form:{
                username: '',
                password: '',
                authority: '',
                email:  '',
            },
            res_data:{
                status: '',
                info: '',
            },
            eddi1: false,
            eddi2: false,
            eddi3: false,
            edi1: false,
            edi2: false,
            edi3: true,
            edi4: true,
            edi5: true,// orzorz hyx
            edi6: true,
            edi7: true,
            edi8: true,
            elh: 2000,
            swh: 0,
            xs: 0.36,
            dialogvisible1: false,
            dialogvisible2: false,// orzorz hyx
            dialogvisible3: false,
            dialogvisible4: false,
            adminpass: '',
            userinfo:{
                username: '',
                password: '',
                authority: '',
                email:  '',
            },

            isAdmin: false,
            url: 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2874029257,2442413353&fm=26&gp=0.jpg',
            datalist: [
                {id:0, text: "测试样例1", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg'},
                {id:1, text: "测试样例2", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg'},
                {id:2, text: "测试样例3", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg'},
                {id:3, text: "测试样例4", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg'}
            ],
            movielist: [
                {id:0, title: "测试样例1", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例1"},
                {id:1, title: "测试样例2", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例2"},
                {id:2, title: "测试样例3", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例3"},
                {id:3, title: "测试样例4", urls: 'https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg', introduce:"测试样例4"}
            ],
            movielist2: [
                {id:0, title: "测试样例1", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例1"},
                {id:1, title: "测试样例2", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例2"},
                {id:2, title: "测试样例3", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例3"},
                {id:3, title: "测试样例4", urls: 'https://cdn.pixabay.com/photo/2020/07/12/07/47/bee-5396362_1280.jpg', introduce:"测试样例4"}
            ],
            rec_list: [
                {id:0, date:"2020/09/02", title:"科幻", author:"test"},
                {id:1, date:"2021/01/01", title:"爱情", author:"sft"},
            ],
        }
    },

    methods: {
        // 新后端测试
        fttest(){
            axiosInstance.post('http://localhost:9999/',{
                name: 'sf',
                key: '111'
            })
            .then((response)=>{
                console.log(response)
            })
        },

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
                this.isAdmin = false
            }
            else if(v == "change"){
                this.sendmsg()
            }
            else if(v == "changepwd"){// orzorz hyx
                this.dialogvisible2 = true
            }
            else if(v == "beadmin"){
                this.dialogvisible3 = true
            }
            else if(v == "record"){
                this.$router.push({ path: '/record' })
            }
            else if(v == "personalinfo"){
                var user = sessionStorage.getItem('user')
                user = JSON.parse(user)
                this.username = user.username
                this.dialogvisible4 = true
            }
        },

        handlecommand2( v ){
            if(v == "a"){
                var test = sessionStorage.getItem('user')
                test = JSON.parse(test)
                this.userinfo = test
                test = test.username
                console.log(test)

                axiosInstance.post('http://localhost:8000/api/getm/',{
                    uid: test,
                    method:'common'
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist = response.data
                    this.eddi1 = true
                    this.eddi3 = this.eddi2 = false
                }).catch((response)=>{
                    console.log(response)
                })

            }
            else if(v == "b"){
                var test = sessionStorage.getItem('user')
                test = JSON.parse(test)
                this.userinfo = test
                test = test.username
                console.log(test)

                axiosInstance.post('http://localhost:8000/api/getm/',{
                    uid: test,
                    method:'demographic'
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist = response.data
                    this.eddi2 = true
                    this.eddi1 = this.eddi3 = false
                }).catch((response)=>{
                    console.log(response)
                })
            }
            else if(v == "c"){
                var test = sessionStorage.getItem('user')
                test = JSON.parse(test)
                this.userinfo = test
                test = test.username
                console.log(test)

                axiosInstance.post('http://localhost:8000/api/getm/',{
                    uid: test,
                    method:'content'
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist = response.data
                    this.eddi3 = true
                    this.eddi1 = this.eddi2 = false
                }).catch((response)=>{
                    console.log(response)
                })
            }
            
        },

        // 注销函数
        sendmsg(){
            var test = sessionStorage.getItem('user')
            test = JSON.parse(test)
            test = test.username
            axiosInstance.post('http://localhost:8000/api/logout/',{
                name: test,
            })
            .then((response)=>{
                var data = response.data
                if(data['status'] == 'success'){
                    this.$alert('注销成功','Success Message',{
                        confirmButtonText:'确定'
                    })
                    sessionStorage.removeItem('user')
                    window.location.reload()
                    this.isAdmin = false
                }
                else{
                    this.$alert('我们出了点问题~','FAIL',{
                        confirmButtonText:'确定'
                    })
                    sessionStorage.removeItem('user')
                    window.location.reload()
                    this.isAdmin = false
                }
            })
            .catch((response)=>{
                console.log(response)
            })
        },

        handleclose(){
            this.dialogvisible1 = false
            this.dialogvisible2 = false// orzorz hyx
            this.form.newpwd = ""
            this.form.rnewpwd = ""
        },

        handleclose2(){
            this.dialogvisible3 = false
            this.adminpass = ""
        },

        handleclose3(){
            this.username = ""
            this.dialogvisible4 = false
        },

        adminpermission(){
            var code = "18csxypnb"
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            if(this.adminpass == code){
                axiosInstance.post('http://localhost:8000/api/add_admin/',{
                    username: username,
                })
                .then((response)=>{
                    var data = response.data
                    if(data['info'] == 'alreay exists'){
                        this.$alert('已经是管理员','Fail',{
                            confirmButtonText:'确定'
                        })
                        this.isAdmin = true
                        this.form.authority = 'admin'
                        sessionStorage.setItem('user', JSON.stringify(this.form))
                    }
                    else{
                        this.$alert('恭喜成为管理员','Success',{
                            confirmButtonText:'确定'
                        })
                        this.isAdmin = true
                        this.form.authority = 'admin'
                        sessionStorage.setItem('user', JSON.stringify(this.form))
                    }
                    window.location.reload()
                }).catch((response)=>{
                    console.log(response)
                })
            }
            else{
                this.$alert('口令错误', 'FAIL', {
                    confirmButtonText:'确定'
                })
            }
        },

        login(){
            
            // sessionStorage.setItem('user', JSON.stringify(res.data))
            axiosInstance.post('http://localhost:8000/api/login/',{
                name: this.form.username,
                key: this.form.password
            })
            .then((response)=>{
                console.log(response)
                this.res_data = response.data
                if(this.res_data['status'] == 'success'){
                    this.form.authority = this.res_data['info'] 
                    this.form.email = this.res_data['email']
                    sessionStorage.setItem('user', JSON.stringify(this.form))
                    this.userinfo = this.form
                    console.log(this.userinfo)
                    this.$alert('登录成功','Success Message',{
                        confirmButtonText:'确定'
                    })
                    window.location.reload()
                }
                else{
                    if(this.res_data['info'] == 'wrong key'){
                        this.$alert('密码错误', 'FAIL', {
                            confirmButtonText:'确定'
                        })
                    }
                    else{
                        this.$alert('用户不存在', 'FAIL', {
                            confirmButtonText:'确定'
                        })
                    }
                    this.form.username = ""
                    this.form.password = ""
                    this.form.authority = ""
                }

            }).catch((response)=>{
                console.log(response)
            })
            
        },

        register(){
            this.$router.push('/register')
        },

        // orzorz hyx
        changepwd(){
            if(this.form.oldpwd == ""){
                this.$alert('请输入旧密码！','FAIL',{
                    confirmButtonText:'确定'
                })
            }
            else if(this.form.newpwd == ""){
                this.$alert('请输入新密码！','FAIL',{
                    confirmButtonText:'确定'
                })
            }
            else if(this.form.rnewpwd == ""){
                this.$alert('请再次输入新密码！','FAIL',{
                    confirmButtonText:'确定'
                })
            }
            else if(this.form.newpwd == this.form.rnewpwd){
                var user = sessionStorage.getItem('user')
                user = JSON.parse(user)
                var username = user.username
                axiosInstance.post('http://localhost:8000/api/changepwd/',{
                    name: username,
                    oldpwd: this.form.oldpwd,
                    newpwd: this.form.newpwd
                })
                .then((response)=>{
                    console.log(response)
                    this.res_data = response.data
                    if(this.res_data['status'] == 'success'){
                        this.form.authority = this.res_data['info']
                        this.$alert('修改成功，请重新登录','Success Message',{
                            confirmButtonText:'确定'
                        })
                        sessionStorage.removeItem('user')
                        window.location.reload()
                        this.isAdmin = false
                    }
                    else{
                        console.log('fail to change password')
                        this.$alert('旧密码错误','Success Message',{
                            confirmButtonText:'确定'
                        })
                    }
                }).catch((response)=>{
                    console.log(response)
                })
            }
            else{
                this.$alert('两次输入不一致', 'FAIL', {
                    confirmButtonText:'确定'
                })
            }
        },

        upload_movie(){
            this.$router.push('/movieupload')
        },

        search(){
            if(sessionStorage.getItem('user')){
                this.$router.push({
                    path:'/search',
                    query:{
                        name: this.$Base64.encode(JSON.stringify(this.input1))
                    }
                })
            }
            else{
                this.$message('请先登录');
            }
        },

        setsize(){
            this.elh = this.swh * this.xs
        },

        setconfig(){
            if(sessionStorage.getItem('user')){
                var user = sessionStorage.getItem('user')
                user = JSON.parse(user)
                var temp = user.authority
                this.isAdmin = temp =='admin' ? true : false
                this.edi1 = true
                this.edi2 = true
                this.edi3 = false
                this.edi4 = false
                this.edi5 = false// orzorz hyx
                this.edi6 = temp =='admin' ? true : false
                this.edi7 = false
                this.edi8 = false
            }
            else{
                this.edi1 = false
                this.edi2 = false
                this.edi3 = true
                this.edi4 = true
                this.edi5 = true// orzorz hyx
                this.edi6 = true
                this.edi7 = true
                this.edi8 = true
            }
        },

        getData(){
            axiosInstance.post('http://localhost:8000/api/gethot/',{
            })
            .then((response)=>{
                console.log(response)
                this.datalist = response.data
            }).catch((response)=>{
                console.log(response)
            })
            
            if(sessionStorage.getItem('user')){
                var test = sessionStorage.getItem('user')
                test = JSON.parse(test)
                this.userinfo = test
                test = test.username
                console.log(test)

                axiosInstance.post('http://localhost:8000/api/getm/',{
                    uid: test,
                    method:'common'
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist = response.data
                }).catch((response)=>{
                    console.log(response)
                })

                axiosInstance.post('http://localhost:8000/api/getmsim/',{
                    uid: test
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist2 = response.data
                }).catch((response)=>{
                    console.log(response)
                })
            }
            else{
                axiosInstance.post('http://localhost:8000/api/getm/',{
                    uid: '',
                    method:'demographic'
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist = response.data
                }).catch((response)=>{
                    console.log(response)
                })

                axiosInstance.post('http://localhost:8000/api/getmsim/',{
                    uid: ''
                })
                .then((response)=>{
                    console.log(response)
                    this.movielist2 = response.data
                }).catch((response)=>{
                    console.log(response)
                })
            }
            //推荐影单
            axiosInstance.post('http://localhost:8000/api/get_sheets/',{
            })
            .then((response)=>{
                console.log(response)
                this.rec_list = response.data
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
                    mid : this.$Base64.encode(JSON.stringify(v))
                }
            })
        },

        add_to_rlist( v ){
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            axiosInstance.post('http://localhost:8000/api/add_reclist_cache/',{
                name: username,
                movieid: v
            })
            .then((response)=>{
                var data = response.data
                if(data['info'] == 'already_in'){
                    this.$message('已经存在');
                }
                else {
                    this.$message('加入清单成功');
                }
            }).catch((response)=>{
                console.log(response)
            })
        },

        show_my_rlist(){
            this.$router.push('/recommendlist')
        },

        star( v ){
            var user = sessionStorage.getItem('user')
            user = JSON.parse(user)
            var username = user.username
            console.log(username)
            axiosInstance.post('http://localhost:8000/api/addcol/',{
                name: username,
                listid: v
            })
            .then((response)=>{
                var data = response.data
                if(data['info'] == 'already in'){
                    this.$message("已经收藏过这个影单了~")
                }
                else {
                    // console.log("success ")
                    this.$message("收藏成功")
                }
            }).catch((response)=>{
                console.log(response)
            })
        },

        movielistinfo( v ){
            // 跳转到该电影推荐单详情页
            if(sessionStorage.getItem('user')){
                this.$router.push({
                    path: '/listinfo',
                    query:{
                        listid : this.$Base64.encode(JSON.stringify(v))
                    }
                })
            }
            else{
                this.$message('请先登录');
            }
            
        }
        
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

    .carousel{
        width: 75%;
        margin-left: 15%;
        
    }
    .img{
        width: 150%;
        height: 150%;
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
    
    /* update by jbt*/
    .rec{
        margin-right: 20px;
    }

    .forhome{
        margin-top: 30px;
    }

</style>