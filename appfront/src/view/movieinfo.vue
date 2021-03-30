<template>
	<div>我是aaa
	<button @click="back">点我返回</button>
	</div>
	
</template>
 
<script>
export default {
  name: 'movieinfo',
  /*data () {
    return {
      msg: '哈哈'
    }
  },*/
  methods:{
  	back(){
  		this.$router.push('/home')
  	}
  }
}
</script>