<template>

    <v-container fluid class="fill-height">
            
        <v-card elevation="24" style="marginLeft:25%;width:50%">
            <v-toolbar dark height="80%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                <v-toolbar-title>电影推荐系统注册</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn @click="goback()">返回</v-btn>
            </v-toolbar>
            <v-card-text>
                <v-form ref="form">
                    <v-text-field v-model="form.username" label="username" type="text" counter="20"></v-text-field>
                    <v-text-field v-model="form.e_mail" label="e-mail" type="text"></v-text-field>
                    <v-text-field v-model="form.vericode" label="verify" type="text"></v-text-field>
                    <v-text-field v-model="form.password" label="password" type="password" counter="16"></v-text-field>
                    <v-text-field v-model="form.rpassword" label="repeatpassword" type="password" counter="16"></v-text-field>
                    <v-btn @click="register()">注册</v-btn>
                    <v-btn absolute right @click="getvericode()">获取邮箱验证码</v-btn>
                </v-form>
            </v-card-text>
        </v-card>
    </v-container>

</template>


<script>
import axiosInstance from '../api/index'
export default {
    
    beforeCreate () {
        document.body.style.background = "linear-gradient(70deg,#0f0 0%, #00f 100%)"
    },

    data() {
        return {
            form: {
                username: '',
                e_mail: '',
                password: '',
                rpassword: '',
                vericode: ''
            },
        }
    },

    methods: {
        goback(){
            this.$router.push('/home')
        },

        register(){
            //网上的轮子 , 检查用户名规范性
            function check_user_name(str)
            {
                // 检查是否含有特殊字符
                function check_other_char(str)
                {
                    var arr = ["&", "\\", "/", "*", ">", "<", "@", "!"];
                    for (var i = 0; i < arr.length; i++)
                    {
                        for (var j = 0; j < str.length; j++)
                        {
                            if (arr[i] == str.charAt(j))
                            {
                                return true;
                            }
                        }
                    }   
                    return false;
                }

                var str2 = "该用户名合法";
                if ("" == str)
                {
                    str2 = "用户名为空";
                    return str2;
                }
                else if ((str.length < 5) || (str.length > 20))
                {
                    str2 = "用户名必须为5 ~ 20位";
                    return str2;
                }
                else if (check_other_char(str))
                {
                    str2 = "不能含有特殊字符";
                    return str2;
                }
                return str2;
            }

            var checkresult = check_user_name(this.form.username)
            if(checkresult != "该用户名合法"){
                this.$alert(checkresult, 'FAIL', {
                    confirmButtonText:'确定'
                })
            }
            else if(this.form.password == this.form.rpassword){
                axiosInstance.post('http://localhost:8000/api/regist/',{
                    name: this.form.username,
                    email: this.form.e_mail,
                    key: this.form.password,
                    code: this.form.vericode
                })
                .then((response)=>{
                    console.log(response)
                    this.res_data = response.data
                    // console.log(res_data)
                    if(this.res_data['status'] == 'success'){
                        sessionStorage.setItem('user', JSON.stringify(this.form))
                        this.$alert('注册成功','Success Message',{
                            confirmButtonText:'确定'
                        })
                        this.$router.push('/home')
                    }
                    else{
                        if(this.res_data['info'] == 'conflict'){
                            this.$alert('冲突', 'FAIL', {
                                confirmButtonText:'确定'
                            })
                        }
                        else if(this.res_data['info'] == 'verifyfail'){
                            this.$alert('验证码错误', 'FAIL', {
                                confirmButtonText:'确定'
                            })
                        }
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
        getvericode(){
            axiosInstance.post('http://localhost:8000/api/generatecode/',{
                email: this.form.e_mail,
            })
            .then((response)=>{
                var data = response.data
                if(data['status'] != "success"){
                    this.$alert('邮箱错误', 'FAIL', {
                        confirmButtonText:'确定'
                    })
                }
                else{
                    this.$alert('已发送', 'SUCCESS', {
                        confirmButtonText:'确定'
                    })
                }
            }).catch((response)=>{
                console.log(response)
            })
        },
    
    },

}

</script>

<style>

    .card{
        width: 40%;
        margin-top: 8%;
        margin-left: 30%;
    }

    .header{
        height:200px;
        width: 100%;
        text-align: center;
    }

    .inputbox{
        min-height:100%;
        width: 100%;
        margin-top: 0;
    }

    .plh{
        margin-top:5%;
    }

    .test{
        background-color: #000000;
        height: 100%;
    }

</style>