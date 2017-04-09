// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'

Vue.config.productionTip = false

Vue.use(VueResource)

import 'common/stylus/index.styl'

router.beforeEach((to, from, next) => {
  if (to.name === 'index' || to.name === 'login' || to.name === 'register') {
    next()
  } else {
    if (!window.sessionStorage.getItem('auth')) {
      next({ name: 'login' })
    } else {
      next()
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  router
})
