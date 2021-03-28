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
                    <v-text-field v-model="form.password" label="password" type="password" counter="16"></v-text-field>
                    <v-text-field v-model="form.rpassword" label="repeatpassword" type="password" counter="16"></v-text-field>
                    <v-btn @click="register()">注册</v-btn>
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
                rpassword: ''
            },
        }
    },

    methods: {
        
        goback(){
            this.$router.push('/home')
        },

        register(){
            
            if(this.form.password == this.form.rpassword){
                axiosInstance.post('http://localhost:8000/api/regist/',{
                    name: this.form.username,
                    email: this.form.e_mail,
                    key: this.form.password
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
        }
    },
    
    mounted(){
        
    }
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