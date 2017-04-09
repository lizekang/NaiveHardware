<template lang="html">
  <div class="header">
    <div class="left" @click="">
      <router-link to="/">
        <img class="logo" src="./logo.png" />
        <img class="title" src="./naive-hardware.png" />
      </router-link>
    </div>
    <div class="right">
      <span class="item">
        <router-link to="/plan">我的家居</router-link>
      </span>
      <span class="item">
        <router-link to="/community">分享社区</router-link>
      </span>
      <span class="item">
        <router-link to="/">使用教程</router-link>
      </span>
      <span class="item">
        <router-link to="/">关于我们</router-link>
      </span>
      <div class="log">
        <img src="./person.png" class="avatar" /><span class="login"><router-link to="/login">登陆</router-link></span>/<span class="register"><router-link to="/register">注册</router-link></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'header'
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.header
  height: 78px
  background-color: #60c5ba
  overflow: hidden
  .left
    display: inline-block
    margin-left: 41px
    & > a
      display: block
      height: 100%
      padding: 12px 0 13px
      box-sizing: border-box
      .logo
        width: 61px
        height: 53px
        margin-right: 24px
        vertical-align: top
      .title
        margin-top: 21px
  .right
    float: right
    margin-right: 40px
    height: 78px
    line-height: 78px
    font-size: 0
    font-weight: 200
    .item
      display: inline-block
      height: 100%
      margin-right: 11px
      font-size: 18px
      vertical-align: top
      &:last-child // 这里为什么不能起作用？？？
        margin-right: 40px
      & > a
        display: block
        height: 100%
        color: rgb(204,236,239)
        &:hover
          color: #fff
    .log
      display: inline-block
      margin-left: 29px
      font-size: 18px
      color: rgb(204,236,239)
      .avatar
        vertical-align: middle
        margin-top: -2px
      .login
        margin-left: 5px
      .login, .register
        display: inline-block
        height: 100%
        & > a
          display: block
          height: 100%
          color: rgb(204,236,239)
          &:hover
            cursor: pointer
            color: #fff
</style>
