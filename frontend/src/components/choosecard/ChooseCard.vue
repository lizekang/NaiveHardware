<template lang="html">
  <div class="choosecard">
    <h1 class="title">选择{{ typeMap[type] }}</h1>
    <ul class="devices" ref="deviceUl">
      <li class="device-wrapper device-hook" v-for="device in devices" @click="select(device)">
        <v-device :device="device" :selected="selectDevice ? selectDevice.type === device.type : false"></v-device>
      </li>
    </ul>
    <div class="button" @click="addDevice">
      确认
    </div>
    <div class="close-wrapper">
      <v-close></v-close>
    </div>
  </div>
</template>

<script>
import Device from 'components/device/Device'
import Close from 'components/close/Close'

import EventHub from '@/EventHub'

import { default as TRANSDUCER, type as TransducerType } from 'common/js/TransducerType'
import { default as EFFECTOR, type as EffectorType } from 'common/js/EffectorType'

export default {
  name: 'choosecard',
  props: {
    type: String
  },
  data () {
    return {
      selectDevice: null
    }
  },
  mounted () {
    window.addEventListener('resize', () => {
      this.$nextTick(() => {
        this._resizeDeviceMargin()
      })
    })
  },
  methods: {
    select (device) {
      this.selectDevice = device
    },
    addDevice () {
      if (this.selectDevice) {
        EventHub.$emit('add-device', this.type, this.selectDevice)

        this.$nextTick(() => {
          this.selectDevice = null
        })
      }
    },
    _resizeDeviceMargin () {
      let deviceUl = this.$refs.deviceUl

      if (deviceUl) {
        let width = deviceUl.clientWidth
        let devices = deviceUl.getElementsByClassName('device-hook')

        // 清除所有margin
        for (let i = 0; i < devices.length; i++) {
          let item = devices[i]

          item.style.marginLeft = 0
          item.style.marginRight = 0
        }

        // 因为max-width为 900 * 30% 所以不会又每行2个
        if (width >= 260 && width < 350) { // 每行3个 80*3+10*2 ~ 80*4+10*3
          for (let i = 1; i <= devices.length; i++) {
            if (i % 3 === 2) {
              let item = devices[i - 1]
              let margin = Math.floor((width - 240 - 1) / 2) // -1 ---> 防止0.5px的width出现bug

              item.style.marginLeft = margin + 'px'
              item.style.marginRight = margin + 'px'
            }
          }
        } else {
          // 每行4个
          for (let i = 1; i <= devices.length; i++) {
            if (i % 4 === 2) {
              let margin = Math.floor((width - 320 - 1) / 3)
              // let marginHalf = Math.floor(margin / 2)
              let item = devices[i - 1]

              item.style.marginLeft = margin + 'px'
              item.style.marginRight = margin + 'px'
            } else if (i % 4 === 3) {
              let margin = Math.floor((width - 320) / 3)
              // let marginHalf = Math.floor(margin / 2)
              let item = devices[i - 1]

              item.style.marginRight = margin + 'px'
            }
          }
        }
      }
    }
  },
  created () {
    this.typeMap = {
      [TRANSDUCER]: '传感器',
      [EFFECTOR]: '效应器'
    }

    this.$nextTick(() => {
      this._resizeDeviceMargin()
    })
  },
  computed: {
    devices () {
      let result = []

      if (this.type === TRANSDUCER) {
        TransducerType.forEach(transducer => {
          let item = {
            type: transducer.type,
            name: transducer.name
          }

          if (transducer.functions) {
            item.functions = transducer.functions
          }

          result.push(item)
        })
      } else if (this.type === EFFECTOR) {
        EffectorType.forEach(effector => {
          let item = {
            type: effector.type,
            name: effector.name
          }

          if (effector.functions) {
            item.functions = effector.functions
          }

          result.push(item)
        })
      }

      return result
    }
  },
  components: {
    'v-device': Device,
    'v-close': Close
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
.choosecard
  padding: 54px 78px 99px
  border-radius: 2px
  background-color: #fff
  position: relative
  .title
    margin-bottom: 20px
    font-size: 36px
    color: #60c5ba
    text-align: center
  .devices
    .device-wrapper
      display: inline-block
      margin-top: 35px
      &:hover
        cursor: pointer
  .button
    margin: 46px auto 0
    width: 80%
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
