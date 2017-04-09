<template lang="html">
  <div class="register">
    <div class="content">
      <h1 class="title">注册</h1>
      <input class="input" type="text" placeholder="邮箱" v-model="email" />
      <input class="input" type="password" placeholder="密码" v-model="password" />
      <input class="input" type="text" placeholder="昵称" v-model="nickname" />
      <div class="button" @click="submit">
        注册
      </div>
      <div class="tip">
          已有账号？<router-link class="login" to="/login">登陆</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Url from 'common/js/Url'

import EventHub from '@/EventHub'

export default {
  name: 'register',
  data () {
    return {
      email: '',
      password: '',
      nickname: ''
    }
  },
  methods: {
    submit () {
      this.$http.post(Url.register, JSON.stringify({ username: this.email, password: this.password, nick_name: this.nickname })).then(response => {
        return response.json()
      }).then(jsonData => {
        if (!jsonData.error) {
          window.sessionStorage.setItem('auth', jsonData.auth) // 存到sessionStorage用于跳转拦截

          this.$http({
            method: 'GET',
            url: Url.getUserProjects,
            headers: {
              Authorization: jsonData.auth
            }
          }).then(response => {
            return response.json()
          }).then(jsonData => {
            EventHub.$emit('set-app', jsonData)

            this.$nextTick(() => {
              this.$router.push({ name: 'plan' })
            })
          })
        }
      })
    }
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.register
  position: fixed
  width: 100%
  top: 78px
  bottom: 0
  background-color: #f4f4f4
  .content
    position: relative
    width: 480px
    height: 480px
    margin: 76px auto
    box-sizing: border-box
    padding: 57px 55px 81px
    border-radius: 2px
    background-color: #fff
    box-shadow: 0 0 25px 2px #a1a1a1
    .title
      margin-bottom: 30px
      font-size: 48px
      color: #60c5ba
      text-align: center
    .input
      width: 100%
      margin-bottom: 23px
      box-sizing: border-box
      padding: 17px 0 17px 31px
      font-size: 14px
      border-radius: 2px
      color: #8b8687
      background-color: #e3dede
      outline: none
    .button
      width: 100%
      height: 50px
      line-height: 50px
      font-size: 16px
      text-align: center
      color: #fff
      background-color: rgb(71,184,224)
      &:hover
        cursor: pointer
        background-color: rgb(96,197,186)
    .tip
      position: absolute
      bottom: 36px
      right: 55px
      font-size: 14px
      color: rgb(139,134,135)
      .login
        font-size: 14px
        color: rgb(96,197,186)
</style>
