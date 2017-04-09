<template lang="html">
  <div class="deploycard">
    <h1 class="title">IP设置</h1>
    <h2 class="text">本地服务器IP</h2>
    <input class="input" type="text" placeholder="例：127.0.0.1:8000" v-model="server_ip" />
    <h2 class="text">设备IP</h2>
    <input class="input" type="text" placeholder="例：192.168.1.1：6666" v-model="device_ip" />
    <div class="button" @click="deploy">
      确认
    </div>
    <div class="close-wrapper">
      <v-close></v-close>
    </div>
  </div>
</template>

<script>
import Close from 'components/close/Close'

import EventHub from '@/EventHub'
import Url from 'common/js/Url'

export default {
  name: 'deploycard',
  props: {
    plan: Object,
    type: String
  },
  data () {
    return {
      server_ip: '',
      device_ip: ''
    }
  },
  methods: {
    deploy () {
      let auth = window.sessionStorage.getItem('auth')

      if (this.type === 'deploy') {
        this.$http({
          method: 'POST',
          url: Url.deploy(this.plan.uid),
          headers: {
            Authorization: auth
          },
          body: {
            uid: this.plan.uid,
            server_ip: this.server_ip,
            device_ip: this.device_ip
          }
        }).then(response => {
          return response.json()
        }).then(jsonData => {
          if (jsonData.errno) { // 成功
            this.plan.isrun = true

            EventHub.$emit('close-dialog-plan')
          } else { // 失败
            alert('部署失败')
          }
        })
      } else if (this.type === 'undeploy') {
        this.$http({
          method: 'POST',
          url: Url.undeploy(this.plan.uid),
          headers: {
            Authorization: auth
          },
          body: {
            uid: this.plan.uid,
            server_ip: this.server_ip,
            device_ip: this.device_ip
          }
        }).then(response => {
          return response.json()
        }).then(jsonData => {
          if (jsonData.errno) { // 成功
            this.plan.isrun = false

            EventHub.$emit('close-dialog-plan')
          } else { // 失败
            alert('停止失败')
          }
        })
      }
    }
  },
  components: {
    'v-close': Close
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.deploycard
  padding: 53px 54px 75px
  box-sizing: border-box
  border-radius: 2px
  background-color: #fff
  position: relative
  .title
    margin-bottom: 23px
    font-size: 36px
    color: #60c5ba
    text-align: center
  .text
    margin: 21px 0 7px
    font-size: 18px
    color: #60c5ba
  .input
    padding: 19px 0 19px 19px
    box-sizing: border-box
    width: 100%
    border-radius: 2px
    font-size: 14px
    color: #8b8687
    background-color: #e3dede
    outline: none
  .button
    margin-top: 45px
    width: 100%
    height: 50px
    height: 50px
    line-height: 50px
    font-size: 14px
    color: #fff
    background-color: #47b8e0
    border-radius: 2px
    text-align: center
    &:hover
      cursor: pointer
  .close-wrapper
    position: absolute
    top: 12px
    right: 14px
</style>
