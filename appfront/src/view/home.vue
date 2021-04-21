<template>
    <el-container>
        <el-header style="text-align: right; font-size: 100%">
            <el-row :gutter="20" style="marginTop:10px">
                <el-col :span="3" :offset="1">
                    <el-image :src="url" :fit="'cover'">
                    </el-image>
                </el-col>
                <!-- 搜索 -->
                <el-col :span="6" :offset="6">
                    <el-input placeholder="movie" v-model="input1">
                    </el-input>
                </el-col>
                <el-col :span="1">
                    <el-button type="primary" icon="el-icon-search" @click="search()">搜索</el-button> 
                </el-col>
                <!-- 管理员上传电影 -->
                <el-col :span="1" :offset="4">
                    <el-button v-show="isAdmin" type="primary" icon="el-icon-plus" @click="upload_movie()"></el-button> 
                </el-col>
                <!-- 右上角菜单，登陆注册 -->
                <el-dropdown @command="handlecommand">
                    <i class="el-icon-s-custom" style="margin-right: 15px"></i>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="login" :disabled="edi1">登录</el-dropdown-item>
                        <el-dropdown-item command="register" :disabled="edi2">注册</el-dropdown-item>
                        <el-dropdown-item command="change" :disabled="edi3">注销</el-dropdown-item>
                        <el-dropdown-item command="logout" :disabled="edi4">登出</el-dropdown-item>
                        <!-- orzorz hyx -->
                        <el-dropdown-item command="changepwd" :disabled="edi5">修改密码</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <el-avatar icon="el-icon-user"></el-avatar>
            </el-row>
        </el-header>
        <el-main>
            <el-col :span="18" :offset="3">
                <el-carousel :height="elh + 'px'" :interval="3000">
                    <!-- 最热推荐 -->
                    <el-carousel-item v-for="item in datalist" :key="item.id">
                        <el-row class="imfg">
                            <img id="test" :src="item.urls" class="img"/>
                        </el-row>
                        <el-divider></el-divider>
                        <el-row class="try">
                            <span class="exp">{{ item.text }}</span>
                        </el-row>
                    </el-carousel-item>
                </el-carousel>
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
            },
            res_data:{
                status: '',
                info: '',
            },
            edi1: false,
            edi2: false,
            edi3: true,
            edi4: true,
            edi5: true,// orzorz hyx
            elh: 2000,
            swh: 0,
            xs: 0.36,
            dialogvisible1: false,
            dialogvisible2: false,// orzorz hyx
            isAdmin: false,
            url: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=4181532436,846702450&fm=11&gp=0.jpg',
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
            ]
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
                    sessionStorage.setItem('user', JSON.stringify(this.form))
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
                var temp = sessionStorage.getItem('user')
                temp = temp.slice(-7,-2)
                this.isAdmin = temp =='admin' ? true : false
                this.edi1 = true
                this.edi2 = true
                this.edi3 = false
                this.edi4 = false
                this.edi5 = false// orzorz hyx
            }
            else{
                this.edi1 = false
                this.edi2 = false
                this.edi3 = true
                this.edi4 = true
                this.edi5 = true// orzorz hyx
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