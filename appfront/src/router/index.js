import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import NProgress from 'nprogress' 
import 'nprogress/nprogress.css'
import movieinfo from '@/view/movieinfo'

Vue.use(Router)

export const publicRouter = [
  { path: '/home', component: () => import('@/view/home'), hidden: true},
  { path: '/register', component: () => import('@/view/register'), hidden: true},
  { path: '/search', name:'search',component: () => import('@/view/search'), hidden: true},
  { path: '/movieinfo', name:'movieinfo',component: movieinfo, hidden: true},
]

export const router = new Router({
  routes: publicRouter,
  scrollBehavior: () => ({ y: 0 })
})

router.beforeEach((to, from, next) => {
  NProgress.start()
  if(sessionStorage.getItem('user')){
    console.log('here')
    if(!store.getters.getUserInfo.length){
      let user = JSON.parse(sessionStorage.getItem('user'))
      store.dispatch('setUserInfo', user)
    }
    next()
  }
  else{
    console.log('there')
    if(to.path != '/home' && to.path != '/register'){
      next({path: '/home'})
    }
    else{
      next()
    }
  }
  NProgress.done()
})

export default router
