<template>
  <div id="app">
    <v-header></v-header>

    <!-- 主体内容 -->
    <div class="content">
      <router-view :plans="plans" :plan="selectedPlan" @addPlan="addPlan" @editPlan="editPlan" @editSavePlan="editSavePlan" @cleanSelected="cleanSelected"></router-view>
    </div>
  </div>
</template>

<script>
import Header from 'components/header/Header'

import EventHub from '@/EventHub'

export default {
  name: 'app',
  data () {
    return {
      nickname: '',
      name: '',
      uid: '',
      plans: [],
      selectedPlan: null,
      selectedIndex: -1
    }
  },
  methods: {
    addPlan (plan) {
      this.plans.push(plan)
    },
    editPlan (selectedPlan, selectedIndex) {
      this.selectedPlan = selectedPlan
      this.selectedIndex = selectedIndex
    },
    editSavePlan (plan) {
      this.plans.splice(this.selectedIndex, 1, plan)

      this.cleanSelected()
    },
    cleanSelected () {
      this.selectedPlan = null
      this.selectedIndex = -1
    },
    setApp (app) {
      this.nickname = app.nick_name
      this.name = app.name
      this.uid = app.uid

      this.plans = app.projects.map(item => {
        let transducers = item.sensors.map(item => {
          let functions = this.functionsMap[item.type]

          functions.uid = item.functions.uid
          functions.function_name = item.functions.function_name
          functions.args = item.functions.args

          return {
            id: item.id,
            type: item.type,
            name: this.typeMap[item.type],
            functions: functions,
            uid: item.uid
          }
        })

        let effectors = item.effectors.map(item => {
          let functions = this.functionsMap[item.type]

          functions.uid = item.functions.uid
          functions.function_name = item.functions.function_name
          functions.args = item.functions.args

          return {
            id: item.id,
            type: item.type,
            name: this.typeMap[item.type],
            functions: functions,
            uid: item.uid
          }
        })

        return {
          name: item.project_name,
          type: item.authority ? 'public' : 'private',
          desc: item.description,
          createTime: item.create_time,
          lastEditTime: item.change_time,
          uid: item.uid,
          isrun: item.is_run,
          transducers,
          effectors
        }
      })
    }
  },
  created () {
    this.typeMap = {
      'buzzer-gpio': '蜂鸣器',
      'ky-016': 'LED灯',
      'ruff-v1-infrared-sender': '红外发射器',
      'lcd1602-pcf8574a-hd44780': '显示器',
      'relay-1c': '继电器',
      'button-gpio': '按钮',
      'sound-01': '声音传感器',
      'dht11': '温湿度传感器',
      'gy-30': '光照传感器',
      'time': '时间传感器'
    }

    this.functionsMap = {
      'buzzer-gpio': [
        { function_name: 'turnOn', tip: '打开', argsTip: '无', args: '' }
      ],
      'ky-016': [
        { function_name: 'turnOn', tip: '发光', argsTip: '无', args: '' }
      ],
      'ruff-v1-infrared-sender': [],
      'lcd1602-pcf8574a-hd44780': [],
      'relay-1c': [
        { function_name: 'turnOn', tip: '接通', argsTip: '无', args: '' }
      ],
      'button-gpio': [
        { function_name: 'on', tip: '按下', argsTip: '无', args: 'push' }
      ],
      'sound-01': [
        { function_name: 'on', tip: '检测声音', argsTip: '无', args: 'sound' }
      ],
      'dht11': [
        { function_name: 'getTemperature', tip: '温度', argsTip: '>30' },
        { function_name: 'getRelativeHumidity', tip: '湿度', argsTip: '>30' }
      ],
      'gy-30': [
        { function_name: 'getIlluminance', tip: '光照值', argsTip: '>30' }
      ],
      'time': [
        { function_name: 'time', tip: '设置时间', argsTip: '12:00-13:00' }
      ]
    }

    EventHub.$on('set-app', this.setApp)
  },
  beforeDestroy () {
    EventHub.$off('set-app')
  },
  components: {
    'v-header': Header
  }
}
</script>

<style lang="stylus" rel="stylesheet/stylus" scoped>
</style>
