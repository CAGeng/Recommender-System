<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <img :src="Img" style="width:100px;height:130px">
    
    <button type="submit" @click="get()">submit</button>
    <button type="submit" @click="getimage()">IMAGE</button>
  </div>
</template>

<script>
import axiosInstance from '../api/index'
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      // Img: require('C:/Users/sft/Desktop/软件工程/django/movie_rec_sys/appfront/src/components/254.jpg'),
      Img: ''
    }
  },
  methods: {
    get(){
      axiosInstance.post('http://localhost:8000/api/getm/',{
        uid: 'b'
      })
      .then((response)=>{
        console.log(response)
        this.msg = response.data
        this.Img = 'http://127.0.0.1:8000/static/767.jfif'
      }).catch((response)=>{
          console.log(response)
      })
    },
    getimage(){
      axiosInstance.post('http://localhost:8000/api/images/',{

			},{
        responseType: "arraybuffer", 
      })
      .then(res => {
        return 'data:image/png;base64,' + btoa(
          new Uint8Array(res.data)  //处理图片格式
            .reduce((data, byte) => data + String.fromCharCode(byte), '')
        );
      })
      .then(data => {
        this.Img = data //图片地址 <img src='data' />
      })
    }
  },
  
}
</script>