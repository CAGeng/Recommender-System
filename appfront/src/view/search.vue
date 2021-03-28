<template>
    <v-container fluid class="fill-height">
        <v-card elevation="24" style="marginLeft:25%;width:50%">
            <v-toolbar dark height="80%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                <v-toolbar-title>{{test}}</v-toolbar-title>
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
export default {
    
    beforeCreate () {
        document.body.style.background = "#000000"
    },

    data(){
        return{
            test:"",
            form: {
                username: '',
                e_mail: '',
                password: '',
                rpassword: ''
            },
        }
    },

    created(){
        this.test = JSON.parse(this.$Base64.decode(this.$route.query.name))
    }
}
</script>