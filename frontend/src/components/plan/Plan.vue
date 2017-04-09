<template lang="html">
  <div class="plan">
    <div class="content-wrapper">
      <div class="left" ref="left">
        <h1 class="title">方案页</h1>
        <div class="plan-wrapper">
          <ul ref="planUl">
            <li v-for="(plan, index) in plans" class="plan-item plan-hook" @click="selectPlan(plan, index)" @mouseover="showDelete($event)" @mouseout="hideDelete($event)">
              <div class="number">
                {{ index + 1 }}
              </div>
              <div class="text">
                {{ plan.name }}
              </div>
              <div class="delete delete-hook" @click.stop.prevent="showDialog('delete', index)"></div>
            </li>
            <li class="add-item plan-hook">
              <router-link to="/create"></router-link>
            </li>
          </ul>
        </div>
      </div>

      <transition name="slide" @enter="enter">
        <div class="right" v-if="selectedPlan !== null">
          <div class="content">
            <h1 class="title">方案详情</h1>
            <div class="prop name">
              <span class="key">方案名称</span>
              <span class="value">{{ selectedPlan.name }}</span>
            </div>
            <div class="prop type">
              <span class="key">方案标签</span>
              <span class="value">{{ selectedPlan.type }}</span>
            </div>
            <div class="prop createTime">
              <span class="key">创建时间</span>
              <span class="value">{{ selectedPlan.createTime }}</span>
            </div>
            <div class="prop lastEditTime">
              <span class="key">最后编辑时间</span>
              <span class="value">{{ selectedPlan.lastEditTime }}</span>
            </div>
            <div class="prop desc">
              <span class="key">方案备注</span>
              <p class="text">
                {{ selectedPlan.desc }}
              </p>
            </div>
            <div class="button-wrapper">
              <div class="edit" @click="editPlan">
                编辑
              </div>
              <div class="deploy" @click="showDialog(deployString)">
                {{ isDeploy }}
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 弹出层：这里有删除页和部署页 -->
    <v-dialog v-show="deleteShow" :type="dialogType" :deleteType="'plan'" :plan="selectedPlan" :deleteName="deleteName" :deleteFunc="deleteFunc" @closeDialog="closeDialog"></v-dialog>
  </div>
</template>

<script>
import Dialog from 'components/dialog/Dialog'

import EventHub from '@/EventHub'

export default {
  name: 'plan',
  props: {
    plans: Array
  },
  data () {
    return {
      selectedPlan: null,
      selectedIndex: -1,
      deleteShow: false,
      deleteName: '',
      deleteFunc: null,
      dialogType: ''
    }
  },
  methods: {
    editPlan () {
      this.$emit('editPlan', this.selectedPlan, this.selectedIndex)
      this.$router.push({ name: 'create' })
    },
    selectPlan (plan, index) {
      this.selectedPlan = plan
      this.selectedIndex = index
    },
    showDialog (type, planIndex) {
      console.log('ok')

      this.deleteShow = true
      this.dialogType = type

      if (type === 'delete') {
        this.selectedPlan = this.plans[planIndex]

        this.deleteName = this.plans[planIndex].name

        // 闭包立即执行，传给子组件一个方法来进行删除操作
        this.deleteFunc = ((planIndex) => {
          return () => {
            this.deletePlan(planIndex)
          }
        })(planIndex)
      }
    },
    deletePlan (index) {
      this.plans.splice(index, 1)

      this.closeDialog()
    },
    closeDialog () {
      this.deletePlanIndex = -1

      this.deleteShow = false
      this.deleteFunc = null
    },
    showDelete (event) {
      let target = event.currentTarget
      let deleteDom = target.getElementsByClassName('delete-hook')[0]

      deleteDom.style.display = 'block'
    },
    hideDelete (event) {
      let target = event.currentTarget
      let deleteDom = target.getElementsByClassName('delete-hook')[0]

      deleteDom.style.display = 'none'
    },
    enter (el, done) {
      let leftDom = this.$refs.left

      leftDom.style.paddingRight = 414 + 'px'

      this.$nextTick(() => {
        this._resizePlanMargin()
      })

      el.addEventListener('transitionend', done)
    },
    _resizePlanMargin () {
      let planUl = this.$refs.planUl

      if (planUl) {
        let width = planUl.clientWidth
        let plans = planUl.getElementsByClassName('plan-hook')

        // 清除所有margin
        for (let i = 0; i < plans.length; i++) {
          let item = plans[i]

          item.style.marginLeft = 0
          item.style.marginRight = 0
        }

        if (width >= 260 && width < 540) { // 每排一个: 260 ~ 260*2+20
          for (let i = 0; i < plans.length; i++) {
            let item = plans[i]
            let margin = Math.floor((width - 260 - 1) / 2)

            item.style.marginLeft = margin + 'px'
            item.style.marginRight = margin + 'px'
          }
        } else if (width >= 540 && width < 820) { // 如果两个一排： 260*2+20 ~ 260*3+40
          for (let i = 1; i <= plans.length; i++) {
            if (i % 2 === 1) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 520 - 1))

              item.style.marginRight = margin + 'px'
            }
          }
        } else if (width >= 820 && width < 1100) { // 如果三个一排： 260*3+40 ～ 260*4+60
          for (let i = 1; i <= plans.length; i++) {
            if (i % 3 === 2) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 780 - 1) / 2)

              item.style.marginLeft = margin + 'px'
              item.style.marginRight = margin + 'px'
            }
          }
        } else if (width >= 1100 && width < 1380) { // 四个一排 260*4+60 ~ 260*5+80
          for (let i = 1; i <= plans.length; i++) {
            if (i % 4 === 2) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 1040 - 1) / 3)

              item.style.marginLeft = margin + 'px'
              item.style.marginRight = margin + 'px'
            } else if (i % 4 === 3) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 1040 - 1) / 3)

              item.style.marginRight = margin + 'px'
            }
          }
        } else { // 5个一排
          for (let i = 1; i <= plans.length; i++) {
            if (i % 5 === 2) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 1300 - 1) / 4)

              item.style.marginLeft = margin + 'px'
            } else if (i % 5 === 3) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 1300 - 1) / 4)

              item.style.marginLeft = margin + 'px'
              item.style.marginRight = margin + 'px'
            } else if (i % 5 === 4) {
              let item = plans[i - 1]
              let margin = Math.floor((width - 1300 - 1) / 4)

              item.style.marginRight = margin + 'px'
            }
          }
        }
      }
    }
  },
  computed: {
    isDeploy () {
      if (this.selectedPlan.isrun) {
        return '停止部署'
      } else {
        return '部署'
      }
    },
    deployString () {
      console.log(this.selectedPlan)

      if (this.selectedPlan.isrun) {
        return 'undeploy'
      } else {
        return 'deploy'
      }
    }
  },
  created () {
    this.$nextTick(() => {
      this._resizePlanMargin()
    })

    EventHub.$on('close-dialog-plan', this.closeDialog)
    EventHub.$on('add-plan', this.addPlan)
  },
  beforeDestroy () {
    EventHub.$off('close-dialog-plan')
  },
  mounted () {
    // 在mounted中绑定事件
    window.addEventListener('resize', () => {
      this.$nextTick(() => {
        this._resizePlanMargin()
      })
    })
  },
  components: {
    'v-dialog': Dialog
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.plan
  .content-wrapper
    position: fixed
    width: 100%
    min-width: 900px
    top: 78px
    bottom: 0
    overflow: hidden
    background-color: #f4f4f4
    .left
      height: 100%
      box-sizing: border-box
      padding: 79px 64px 0 98px
      overflow: auto
      .title
        font-family: 'myFont'
        font-size: 60px
        color: rgb(31,78,95)
        margin-bottom: 42px
      .plan-wrapper
        font-size: 0
        .plan-item, .add-item
          display: inline-block
          width: 260px
          height: 260px
          margin-bottom: 44px
          border-radius: 2px
          box-shadow: 0 0 10px 1px #a1a1a1
          vertical-align: top
          &:hover
            cursor: pointer
        .plan-item
          position: relative
          .number
            height: 220px
            line-height: 220px
            font-family: 'myFont'
            font-size: 130px
            color: rgb(96,197,186)
            background-color: #fff
            text-align: center
            border-radius: 2px 2px 0 0
          .text
            height: 40px
            line-height: 40px
            font-family: 'myFont'
            font-size: 24px
            color: #fff
            background-color: #60c5ba
            text-align: center
            border-radius: 0 0 2px 2px
          .delete
            display: none
            position: absolute
            top: 0
            right: 0
            width: 25px
            height: 25px
            background-image: url('./delete.png')
            background-size: 25px 25px
            background-repeat: no-repeat
        .add-item
          & > a
            display: inline-block
            width: 100%
            height: 100%
            background-image: url('./add.png')
            background-size: 260px 260px
            background-repeat: no-repeat
    .right
      position: absolute
      top: 0
      right: 0
      width: 350px
      height: 100%
      box-sizing: border-box
      padding-top: 91px
      background-color: #fff
      box-shadow: -6px 0 18px 0 #a1a1a1
      &.slide-enter-active, &.slide-leave-active
        transition: all 0.3s
      &.slide-enter, &.slide-leave-active
        transform: translate3d(100%,0,0)
      .content
        box-sizing: border-box
        padding: 0 22px 0
        .title
          font-family: 'myFont'
          font-size: 24px
          color: rgb(96,197,186)
          margin-bottom: 8px
        .prop
          margin-top: 26px
          box-sizing: border-box
          padding-left: 21px
          font-size: 0
          position: relative
          .key, .value, .text
            font-size: 14px
            color: rgb(139,134,135)
          .value
            position: absolute
            left: 140px
          .text
            display: block
            line-height: 25px
            margin-top: 11px
            padding-left: 29px
        .button-wrapper
          margin-top: 55px
          display: flex
          height: 50px
          justify-content: space-between
          padding: 0 21px 0
          .edit, .deploy
            flex: 0 0 120px
            width: 120px
            font-size: 16px
            color: #fff
            line-height: 50px
            text-align: center
            border-radius: 2px
            &:hover
              cursor: pointer
          .edit
            background-color: rgb(71,184,224)
            &:hover
              background-color: rgb(96,197,186)
          .deploy
            background-color: rgb(255,188,66)
            &:hover
              background-color: rgb(230,170,60)
</style>
