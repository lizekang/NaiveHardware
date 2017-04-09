<template lang="html">
  <div class="deletecard">
    <h1 class="title">删除确认</h1>
    <h2 class="content">确定要删除 {{ deleteName }} 吗?</h2>
    <div class="button-wrapper">
      <div class="cancel" @click="cancel">
        取消
      </div>
      <div class="delete" @click="confirm">
        删除
      </div>
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
  name: 'deletecard',
  props: {
    deleteName: String,
    deleteFunc: Function,
    deleteType: String,
    plan: Object
  },
  methods: {
    cancel () {
      EventHub.$emit('close-dialog')
      EventHub.$emit('close-dialog-plan')
    },
    confirm () {
      if (this.deleteType === 'plan') {
        let auth = window.sessionStorage.getItem('auth')

        this.$http({
          method: 'DELETE',
          url: Url.deleteProject,
          headers: {
            Authorization: auth
          },
          body: {
            uid: this.plan.uid
          }
        }).then(response => {
          if (response.status === 204) {
            this.deleteFunc()
          }
        })
      } else {
        this.deleteFunc()
      }
    }
  },
  components: {
    'v-close': Close
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.deletecard
  padding: 35px 40px 25px
  border-radius: 2px
  background-color: #fff
  position: relative
  .title
    font-size: 36px
    color: #60c5ba
    text-align: center
  .content
    margin: 45px 0 40px
    font-size: 16px
    color: #8b8788
    text-align: center
  .button-wrapper
    display: flex
    height: 50px
    justify-content: space-between
    .cancel, .delete
      flex: 0 0 140px
      width: 140px
      color: #fff
      font-size: 14px
      line-height: 50px
      border-radius: 2px
      text-align: center
      &:hover
        cursor: pointer
    .cancel
      background-color: #47b8e0
    .delete
      background-color: #febc42
  .close-wrapper
    position: absolute
    top: 12px
    right: 14px
</style>
