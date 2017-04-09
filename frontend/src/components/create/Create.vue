
<template lang="html">
  <div class="create">
    <!-- 主体部分 -->
    <div class="content-wrapper">
      <div class="left">

        <!-- 新建页左半部分 start -->
        <div class="title-wrapper">
          <span class="title">方案名称</span>
          <span class="text">{{ name ? name : '未命名' }}</span>
        </div>
        <div class="transducer-wrapper">
          <h1 class="title">
            <span class="name">传感器</span>
            <span class="tip">点击图标设置/查看参数</span>
          </h1>
          <ul>
            <li class="device-wrapper" v-for="(transducer, index) in transducers" @click="showDialog('prop', index, transducers)" @mouseover="showDelete($event)" @mouseout="hideDelete($event)">
              <v-device :device="transducer"></v-device>
              <div class="delete delete-hook" @click.stop.prevent="showDialog('delete', index, transducers)"></div>
            </li>
            <li class="device-wrapper" @click="showDialog('transducer')">
              <v-device :device="{ type: 'add' }"></v-device>
            </li>
          </ul>
        </div>
        <div class="effector-wrapper">
          <h1 class="title">
            <span class="name">效应器</span>
            <span class="tip">点击图标设置/查看参数</span>
          </h1>
          <ul>
            <li class="device-wrapper" v-for="(effector, index) in effectors" @click="showDialog('prop', index, effectors)" @mouseover="showDelete($event)" @mouseout="hideDelete($event)">
              <v-device :device="effector"></v-device>
              <div class="delete delete-hook" @click.stop.prevent="showDialog('delete', index, effectors)"></div>
            </li>
            <li class="device-wrapper" @click="showDialog('effector')">
              <v-device :device="{ type: 'add' }"></v-device>
            </li>
          </ul>
        </div>
        <!-- end -->

      </div>
      <div class="right">

          <!-- 新建页右半部分 start -->
          <div class="content">
            <div class="name">
              <h1 class="title">方案名称</h1>
              <input class="name_input" type="text" placeholder="未命名" v-model="name" />
            </div>
            <div class="type">
              <h1 class="title">类型</h1>
              <select class="type_select" v-model="type">
                <option class="option" value="public">public</option>
                <option class="option" value="private">private</option>
              </select>
            </div>
            <div class="desc">
              <h1 class="title">方案备注</h1>
              <textarea class="text" v-model="desc"></textarea>
            </div>
            <div class="save" @click="save" :class="{ hasEmpty: hasDataEmpty }">
              保存
            </div>
          </div>
          <!-- end -->
      </div>
    </div>

    <!-- 弹出层部分 -->
    <v-dialog v-show="dialogShow" :plans="plans" :transducers="transducers" :effectors="effectors" :type="dialogType" :deleteName="deleteName" :deleteFunc="deleteFunc" :setPropFunc="setPropFunc" :selectedDevice="selectedDevice" :selectedIndex="selectedIndex" @closeDialog="closeDialog"></v-dialog>
  </div>
</template>

<script>
import Device from 'components/device/Device'
import Dialog from 'components/dialog/Dialog'

import Url from 'common/js/Url'

import EventHub from '@/EventHub'

export default {
  name: 'create',
  props: {
    plans: Array,
    plan: {
      type: Object,
      default () {
        return {
          name: '',
          type: '',
          desc: '',
          transducers: [],
          effectors: []
        }
      }
    }
  },
  data () {
    return {
      dialogType: '',
      dialogShow: false,
      deleteName: '',
      deleteFunc: null,
      setPropFunc: null,
      selectedDevice: null,
      selectedIndex: -1,
      name: this.plan ? this.plan.name : '',
      type: this.plan ? this.plan.type : '',
      desc: this.plan ? this.plan.desc : '',
      transducers: this.plan ? this.plan.transducers : [],
      effectors: this.plan ? this.plan.effectors : []
    }
  },
  methods: {
    save () {
      if (!this.hasDataEmpty) {
        let auth = window.sessionStorage.getItem('auth')

        if (this.plan && this.plan.name) { // 修改 ---> 保存
          this.$http({
            method: 'PATCH',
            url: Url.editProject,
            headers: {
              Authorization: auth
            },
            body: JSON.stringify({
              project_name: this.name,
              authority: this.type === 'public',
              description: this.desc,
              uid: this.plan.uid,
              isrun: this.plan.isrun,
              sensors: this.transducers,
              effectors: this.effectors
            })
          }).then(response => {
            return response.json()
          }).then(jsonData => {
            let transducers = this.transducers
            let effectors = this.effectors

            if (jsonData.transducers) {
              transducers.uid = jsonData.transducers.uid
            }
            if (jsonData.effectors) {
              effectors.uid = jsonData.effectors.uid
            }

            jsonData.sensors.forEach((item, index) => {
              transducers[index].uid = item.uid
            })

            jsonData.effectors.forEach((item, index) => {
              effectors[index].uid = item.uid
            })

            let plan = {
              name: jsonData.project_name,
              type: jsonData.authority ? 'public' : 'private',
              desc: jsonData.description,
              createTime: jsonData.create_time,
              lastEditTime: jsonData.change_time,
              uid: jsonData.uid,
              isrun: jsonData.is_run,
              transducers: transducers,
              effectors: effectors
            }

            this.$emit('editSavePlan', plan)

            this.$router.go(-1)
          })
        } else { // 新建 ---> 保存
          this.$http({
            method: 'POST',
            url: Url.createProject,
            headers: {
              Authorization: auth
            },
            body: JSON.stringify({
              project_name: this.name,
              authority: this.type === 'public',
              description: this.desc,
              sensors: this.transducers,
              effectors: this.effectors
            })
          }).then(response => {
            return response.json()
          }).then(jsonData => {
            let transducers = this.transducers
            let effectors = this.effectors

            if (jsonData.transducers) {
              transducers.uid = jsonData.transducers.uid
            }
            if (jsonData.effectors) {
              effectors.uid = jsonData.effectors.uid
            }

            jsonData.sensors.forEach((item, index) => {
              transducers[index].uid = item.uid
            })

            jsonData.effectors.forEach((item, index) => {
              effectors[index].uid = item.uid
            })

            let plan = {
              name: jsonData.project_name,
              type: jsonData.authority ? 'public' : 'private',
              desc: jsonData.description,
              createTime: jsonData.create_time,
              lastEditTime: jsonData.change_time,
              uid: jsonData.uid,
              isrun: jsonData.is_run,
              transducers: transducers,
              effectors: effectors
            }

            this.$emit('addPlan', plan)

            this.$router.go(-1)
          })
        }
      }
    },
    showDialog (type, deviceIndex, devices) {
      this.dialogType = type
      this.dialogShow = true

      if (type === 'prop') {
        this.selectedDevice = devices[deviceIndex]
        this.selectedIndex = deviceIndex

        this.setPropFunc = ((deviceIndex, devices) => {
          return (id, functions) => {
            this.setProp(deviceIndex, devices, id, functions)
          }
        })(deviceIndex, devices)
      }

      if (type === 'delete') {
        this.deleteName = devices[deviceIndex].name

        this.deleteFunc = ((deviceIndex, devices) => {
          return () => {
            this.deleteDevice(deviceIndex, devices)
          }
        })(deviceIndex, devices)
      }
    },
    closeDialog () {
      this.dialogShow = false

      // closeDialog时清空数据
      this.dialogType = ''
      this.dialogShow = false
      this.deleteName = ''
      this.deleteFunc = null
      this.selectedDevice = null
      this.selectedIndex = -1
      this.setPropFunc = null
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
    addDevice (type, device) {
      if (type === 'transducer') {
        this.transducers.push(device)
      } else if (type === 'effector') {
        this.effectors.push(device)
      }

      this.closeDialog()
    },
    deleteDevice (index, devices) {
      devices.splice(index, 1)

      this.closeDialog()
    },
    setProp (deviceIndex, devices, id, functions) {
      devices[deviceIndex].id = id
      devices[deviceIndex].functions = functions

      this.closeDialog()
    }
  },
  computed: {
    hasDataEmpty () {
      let result = false

      if (!this.name || !this.type || !this.desc) {
        result = true
      }

      // 检测每个device的prop是否填写
      this.transducers.forEach(device => {
        if (!device.id) {
          result = true
        }

        device.functions.forEach(prop => {
          if (prop.function_name !== 'on' && prop.function_name !== 'turnOn' && !prop.args) {
            result = true
          }
        })
      })

      this.effectors.forEach(device => {
        if (!device.id) {
          result = true
        }

        device.functions.forEach(prop => {
          if (prop.function_name !== 'on' && prop.function_name !== 'turnOn' && !prop.args) {
            result = true
          }
        })
      })

      return result
    }
  },
  created () {
    EventHub.$on('add-device', this.addDevice)
    EventHub.$on('close-dialog', this.closeDialog)
  },
  beforeDestroy () {
    EventHub.$off('add-device')
    EventHub.$off('close-dialog')

    this.$emit('cleanSelected')
  },
  components: {
    'v-device': Device,
    'v-dialog': Dialog
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.create
  .content-wrapper
    display: flex
    position: fixed
    width: 100%
    min-width: 900px
    top: 78px
    bottom: 0
    overflow: hidden
    .left
      flex: auto
      background-color: #f4f4f4
      box-sizing: border-box
      padding: 49px 98px 0
      .title-wrapper
        font-size: 0
        .title
          margin-right: 66px
          font-family: 'myFont'
          font-size: 36px
          color: #436572
        .text
          font-size: 36px
          color: #73cac0
      .transducer-wrapper, .effector-wrapper
        .title
          font-size: 0
          margin-bottom: 13px
          .name
            font-size: 36px
            color: #436572
            margin-right: 28px
          .tip
            font-size: 18px
            color: #436572
        .device-wrapper
          display: inline-block
          position: relative
          margin-top: 10px
          margin-right: 14px
          vertical-align: top
          &:hover
            cursor: pointer
          .delete
            display: none
            position: absolute
            top: 0
            right: 0
            width: 25px
            height: 25px
            background-image: url('./delete.png')
            background-repeat: no-repeat
            background-size: 25px 25px
      .transducer-wrapper
        margin-top: 37px
      .effector-wrapper
        margin-top: 25px
    .right
      flex: 0 0 350px
      width: 350px
      padding-top: 53px
      background-color: #fff
      box-sizing: border-box
      box-shadow: -6px 0 18px 0 #a1a1a1
      .content
        width: 75%
        margin: 0 auto
        .name, .type, .desc
          .title
            margin-bottom: 14px
            font-size: 24px
            color: #73cac0
          .name_input, .type_select, .text
            padding: 19px 0 19px 19px
            box-sizing: border-box
            width: 100%
            border-radius: 2px
            font-size: 14px
            color: #8b8687
            background-color: #e3dede
            border: 0
            outline: none
            resize: none
            .option
              background-color: #f4f4f4
        .type
          margin-top: 25px
        .desc
          margin-top: 28px
          .text
            height: 126px
        .save
          margin: 26px auto 0
          width: 100%
          max-width: 260px
          height: 50px
          line-height: 50px
          text-align: center
          font-size: 16px
          color: #fff
          background-color: rgb(71,184,224)
          border-radius: 2px
          &:hover
            cursor: pointer
            background-color: rgb(96,197,186)
          &.hasEmpty
            background-color: gray
</style>
