<template>
    <el-container>
        <el-main>
            <v-container>
                <v-card class="card">
                    <v-toolbar dark height="50%" src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
                        <v-toolbar-title>电影上传</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-btn @click="goback()">返回</v-btn>
                    </v-toolbar>
                    <div style="margin: 20px 0;"></div>
                    <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="100px" class="demo-dynamic">
                        <!-- 输入电影名 -->
                        <el-form-item
                            prop="title"
                            label="电影名"
                            :rules="{
                                required: true, message: '电影名不能为空', trigger: 'blur'
                            }"
                        >
                        <el-col :span="20"><el-input v-model="dynamicValidateForm.title" maxlength="20" show-word-limit></el-input></el-col>
                        </el-form-item>
                        <el-divider></el-divider>
                        <!-- 输入演员名 -->
                        <el-form-item
                            v-for="(cast, index) in dynamicValidateForm.cast"
                            :label="'演员' + index"
                            :key="cast.key"
                            :prop="'cast.' + index + '.value'"
                            :rules="{
                                required: true, message: '演员名不能为空', trigger: 'blur'
                            }"
                        >
                        <el-col :span="20"><el-input v-model="cast.value" maxlength="20" show-word-limit></el-input></el-col>
                            <el-button  v-show="index != 0" @click.prevent="removeCast(cast)">删除</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="addCast">新增演员</el-button>
                        </el-form-item>
                        <el-divider></el-divider>
                        <!-- 输入摄制人员名 -->
                        <el-form-item
                            v-for="(crew, index) in dynamicValidateForm.crew"
                            :label="'摄制人员' + index"
                            :key="crew.key"
                            :prop="'crew.' + index + '.value'"
                            :rules="{
                                required: true, message: '摄制人员不能为空', trigger: 'blur'
                            }"
                        >
                            <el-col :span="20"><el-input v-model="crew.value" maxlength="20" show-word-limit></el-input></el-col>
                            <el-button  v-show="index != 0" @click.prevent="removeCrew(crew)">删除</el-button>
                        </el-form-item>
                        <el-form-item><el-button @click="addCrew">新增摄制人员</el-button></el-form-item>
                        <el-divider></el-divider>
                        <!-- 电影类型-->
                        <el-form-item 
                            label="电影类型"
                            prop="genres"
                            :rules="{
                                type: 'array', required: true, message: '请至少选择一种电影类型', trigger: 'change'  
                            }"
                        >
                            <el-checkbox-group v-model="dynamicValidateForm.genres">
                                <el-checkbox label="Adventure" name="type"></el-checkbox>
                                <el-checkbox label="Fantasy" name="type"></el-checkbox>
                                <el-checkbox label="Action" name="type"></el-checkbox>
                                <el-checkbox label="Crime" name="type"></el-checkbox>
                                <el-checkbox label="Drama" name="type"></el-checkbox>
                                <el-checkbox label="Thriller" name="type"></el-checkbox>
                                <el-checkbox label="Science Fiction" name="type"></el-checkbox>
                                <el-checkbox label="Family" name="type"></el-checkbox>
                                <el-checkbox label="Comedy" name="type"></el-checkbox>
                                <el-checkbox label="Mystery" name="type"></el-checkbox>
                                <el-checkbox label="Animation" name="type"></el-checkbox>
                                <el-checkbox label="Western" name="type"></el-checkbox>
                                <el-checkbox label="Romance" name="type"></el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                        <el-divider></el-divider>
                        <!-- 电影关键字 -->
                        <el-form-item
                            v-for="(keywords, index) in dynamicValidateForm.keywords"
                            :label="'关键字' + index"
                            :key="keywords.key"
                            :prop="'keywords.' + index + '.value'"
                            :rules="{
                                required: true, message: '关键字不能为空', trigger: 'blur'
                            }"
                        >
                        <el-col :span="20"><el-input v-model="keywords.value" maxlength="40" show-word-limit></el-input></el-col>
                        <el-button  v-show="index != 0" @click.prevent="removeKeywords(keywords)">删除</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="addKeywords">新增关键字</el-button>
                        </el-form-item>
                        <el-divider></el-divider>
                        <el-form-item 
                            label="上传图片" 
                            prop="requireImage"
                            :rules="{
                                required: true, message: '电影封面不能为空', trigger: 'change'
                            }"
                        >
                            <el-upload
                                action="http://localhost:8000/api/upload_movieImg/"
                                list-type="picture-card"
                                :limit="1"
                                :class="{hide:showUpload}"
                                :on-remove="handleRemove"
                                :on-change="handleChange"
                                :on-success="handleSuccess"
                                :on-error="handleError"
                                :auto-upload="false"
                                class="upload-demo"
                                ref="upload"
                            >
                                <i class="el-icon-plus"></i>
                                <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
                            </el-upload>
                        </el-form-item>
                        <el-divider></el-divider>
                        <el-button type="primary" round class="comfirm" @click="uploadcomfirm('dynamicValidateForm')">确认上传</el-button>
                    </el-form>
                </v-card>
            </v-container>
        </el-main>
    </el-container>
</template>

<script>
import axiosInstance from '../api/index'
export default {
    data() {
      return {
        dynamicValidateForm: {
            cast: [{
                value: ''
            }],
            crew: [{
                value: ''
            }],
            keywords: [{
                value: ''
            }],
            title: '',
            genres: [],
            requireImage: '',
        },
        showUpload: false,
        movieid: 0,
      };
    },

    beforeCreate () {
        document.body.style.background = "#000000"
    },

    methods: {
        goback(){
            this.$router.push('/home')
        },
        removeCast(item) {
            var index = this.dynamicValidateForm.cast.indexOf(item)
            if (index !== -1) {
                this.dynamicValidateForm.cast.splice(index, 1)
            }
        },
        addCast() {
            this.dynamicValidateForm.cast.push({
            value: '',
            key: Date.now()
            });
        },
        removeCrew(item) {
            var index = this.dynamicValidateForm.crew.indexOf(item)
            if (index !== -1) {
                this.dynamicValidateForm.crew.splice(index, 1)
            }
        },
        addCrew() {
            this.dynamicValidateForm.crew.push({
                value: '',
                key: Date.now()
            });
        },
        removeKeywords(item) {
            var index = this.dynamicValidateForm.keywords.indexOf(item)
            if (index !== -1) {
                this.dynamicValidateForm.keywords.splice(index, 1)
            }
        },
        addKeywords() {
            this.dynamicValidateForm.keywords.push({
                value: '',
                key: Date.now()
            });
        },
        handleRemove(file, fileList) {
            this.dynamicValidateForm.requireImage = ''
		    if(fileList.length < 1){
			    this.showUpload = false
		    }
	    },
        handleChange(file, fileList) {
            this.dynamicValidateForm.requireImage = '1'
            if(fileList.length >= 1){
                this.showUpload = true
            }
	    },
        handleSuccess(response, file, fileList) {
            this.movieid = response.info
            console.log(response)
            axiosInstance.post('http://localhost:8000/api/upload_movie/',{
                movieid: this.movieid,
                title: this.dynamicValidateForm.title,
                cast: this.dynamicValidateForm.cast,
                crew: this.dynamicValidateForm.crew,
                keywords: this.dynamicValidateForm.keywords,
                genres: this.dynamicValidateForm.genres,
                fileList: this.fileList,
            }).then((response)=>{
                var data = response.data
                if(data['status'] != "success"){
                    this.$alert('上传失败', 'FAIL', {
                        confirmButtonText:'确定'
                    })
                }
                else{
                        this.$alert('上传成功', 'SUCCESS', {
                        confirmButtonText:'确定'
                    })
                }
            }).catch((response)=>{
                console.log(response)
            })
            this.$refs.upload.clearFiles()
            this.dynamicValidateForm.requireImage = ''
            this.showUpload = false
        },
        handleError(err, file, fileList) {
            this.$alert('上传失败', 'FAIL', {
                        confirmButtonText:'确定'
            })
            this.$refs.upload.clearFiles()
            this.dynamicValidateForm.requireImage = ''
            this.showUpload = false
        },
        uploadcomfirm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.$refs.upload.submit()
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
    }
}
</script>


<style>
    .card{
        width: 100%;
    }

    .upload-demo{
        width: 82%;
        margin-left: 3%;
    }

    .comfirm{
        margin-left: 45%;
        margin-bottom: 2%;
    }

    .hide .el-upload--picture-card {
        display: none;
    }

</style>