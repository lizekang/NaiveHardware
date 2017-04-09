import Vue from 'vue'
import Router from 'vue-router'

import Index from 'components/index/Index'
import Plan from 'components/plan/Plan'
import Create from 'components/create/Create'
import Login from 'components/login/Login'
import Register from 'components/register/Register'
import Community from 'components/community/Community'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'index', component: Index },
    { path: '/plan', name: 'plan', component: Plan },
    { path: '/create', name: 'create', component: Create },
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register },
    { path: '/community', name: 'community', component: Community }
  ]
})
